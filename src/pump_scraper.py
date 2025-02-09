from datetime import datetime
from logging import Logger
from typing import List, Union, Optional

from pydantic import Field

from src.api.gecko_terminal import GeckoTerminal
from src.api.pump import PumpApi
from src.models.instruments.pool import Pool, TokenPool
from src.models.instruments.pump_token import PumpToken
from src.models.integration.api import ApiError
from src.utils.scripts import retry, hours_ago, str_to_bool, exception_swallow
from src.utils.api import exception_handler


class PumpScraperToken(PumpToken):
    pool: Optional[TokenPool] = None
    scraped_date: datetime = Field(alias="scraped_date", default_factory=lambda: hours_ago(0))


class PumpScraper:
    def __init__(self, logger: Logger):
        self.logger = logger.getChild(__name__)
        self.pump_api = PumpApi(logger=logger)
        self.pool_api = GeckoTerminal(logger=logger)
        self.price_args = {"include_pricing"}
        self.pump_args = {"term", "offset", "limit", "sort", "order", "includeNsfw"}

    @exception_handler
    async def get_results(self, **kwargs) -> List[PumpScraperToken]:
        results: List[PumpScraperToken] = []

        coin_args = {k: v for k, v in kwargs.items() if k in self.pump_args}
        include_pricing = str_to_bool(kwargs.get("include_pricing", "false"))
        coins = await self.get_coins(**coin_args)
        for coin in coins:
            if not coin.raydium_pool or not include_pricing:
                self.logger.debug(f"{coin.symbol} has no pool, skipping")
                results.append(PumpScraperToken(**coin.model_dump()))
                continue

            if coin.complete and coin.raydium_pool:
                self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...")
                pool = await self.get_pool(coin.raydium_pool)
                if pool:
                    pool_data = pool.get_token_pool()
                    results.append(PumpScraperToken(**coin.model_dump(), pool=pool_data))
                    self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...[done]")
                else:
                    results.append(PumpScraperToken(**coin.model_dump()))
                    self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...[skipped]")
            else:
                results.append(PumpScraperToken(**coin.model_dump()))
                self.logger.debug(f"{coin.symbol} skipped (pool={coin.raydium_pool}, grad={coin.complete})")

        return results

    @retry(Exception, tries=3, delay=1, backoff=2)
    async def get_coins(
            self,
            term: str = None,
            offset: int = 0,
            limit: int = 50,
            **kwargs
    ) -> Union[List[PumpToken], ApiError]:
        if term:
            return await self.pump_api.search_tokens(term=term, offset=offset, limit=limit, **kwargs)
        else:
            return await self.pump_api.get_tokens(offset=offset, limit=limit, **kwargs)

    @exception_swallow
    @retry(Exception, tries=2, delay=3, backoff=2)
    async def get_pool(self, pool_id: str) -> Union[List[Pool], ApiError]:
        return await self.pool_api.get_pool(pool_id=pool_id)
