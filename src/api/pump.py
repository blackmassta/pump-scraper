from datetime import datetime
from enum import Enum
from logging import Logger
from typing import List, Optional

from pydantic import Field

from src.api.api_base import BaseApi
from src.models.integration.api import ApiError, ApiModel
from src.models.instruments.pump_token import PumpToken
from src.models.portfolio.trade import Trade
from src.utils.scripts import stagger, days_ago


class OrderByDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


class BasePaginationFilter(ApiModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 1000
    order: Optional[str] = OrderByDirection.DESC.value


class PumpApiCoinsFilter(BasePaginationFilter):
    sort: Optional[str] = 'created_timestamp'
    includeNsfw: Optional[str] = "false"


class GetCoinsFilter(PumpApiCoinsFilter):
    is_graduated: Optional[bool] = None
    max_created_date: Optional[datetime] = None
    min_created_date: Optional[datetime] = Field(default_factory=days_ago)


class SearchCoinFilter(GetCoinsFilter):
    searchTerm: str
    type: str = 'exact'


class GetTradesFilter(BasePaginationFilter):
    minimumSize: Optional[int] = 50000000


class PumpApi(BaseApi):
    def __init__(self, logger: Logger, base_url: str = "https://frontend-api-v3.pump.fun"):
        super().__init__(base_url=base_url, logger=logger)
        self.headers = {
            "authority": "frontend-api-v3.pump.fun",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://pump.fun",
            "priority": "u=1, i",
            "referer": "https://pump.fun/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }

    async def get_tokens(self, **kwargs) -> List[PumpToken] | ApiError:
        # https://frontend-api-v3.pump.fun/coins?offset=0&limit=100&sort=created_timestamp&includeNsfw=false&order=DESC
        coins: List[PumpToken] = []
        url = f"{self.base_url}/coins"
        params = GetCoinsFilter(**kwargs)

        counter = 0
        limit = min(params.limit, 50)
        while len(coins) < params.limit:
            filters = PumpApiCoinsFilter(**{**kwargs, 'limit': limit, 'offset': counter * limit})
            result: List[PumpToken] = await self._get_list(url, params=filters, return_type=PumpToken)

            # exit if there is no data
            if not result:
                break

            # apply date range filter
            if params.max_created_date or params.min_created_date:
                filtered = list(result)
                if params.max_created_date:
                    filtered = [c for c in filtered if c.created_timestamp <= params.max_created_date]
                if params.min_created_date:
                    filtered = [c for c in filtered if c.created_timestamp >= params.min_created_date]
            else:
                filtered = result

            # apply graduated filter
            if params.is_graduated is not None:
                filtered = [c for c in result if c.complete]

            counter += 1

            # save results and stagger
            coins.extend(filtered)
            self.logger.debug(f"{len(coins)} total, last={len(filtered)}, unfiltered={len(result)}, last={result[-1].created_timestamp if result else None}")

        return coins

    async def search_token(self, term: str) -> PumpToken | ApiError:
        # https://frontend-api-v3.pump.fun/coins/search?offset=0&limit=50&sort=market_cap&includeNsfw=false&order=DESC&searchTerm=FAFO&type=exact
        if not term:
            return ApiError(error_code="INVALID", message="No symbol passed")

        url = f"{self.base_url}/coins/search"
        params = SearchCoinFilter(searchTerm=term)
        return await self._get_single(url, params=params, return_type=PumpToken)

    async def search_tokens(self, term: str, **kwargs) -> List[PumpToken] | ApiError:
        # https://frontend-api-v3.pump.fun/coins/search?offset=0&limit=50&sort=market_cap&includeNsfw=false&order=DESC&searchTerm=FAFO&type=exact
        if not term:
            return ApiError(error_code="INVALID", message="No symbol passed")

        url = f"{self.base_url}/coins/search"
        params = SearchCoinFilter(searchTerm=term, **kwargs)
        return await self._get_list(url, params=params, return_type=PumpToken)

    async def get_trades(self, coin: str, **kwargs):
        url = f"{self.base_url}/trades/all/{coin}"
        params = GetTradesFilter(**kwargs)

        return await self._get_list(url, params=params, return_type=Trade)
