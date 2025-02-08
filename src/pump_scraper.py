from datetime import datetime
from logging import Logger
from typing import List, Union

from api.gecko_terminal import GeckoTerminal
from api.pump import PumpApi
from src.models.instruments.pool import Pool, TokenPool
from src.models.instruments.pump_token import PumpToken
from src.models.integration.api import ApiError
from src.utils.scripts import retry
from utils.api import format_response, exception_handler


class PumpScraperToken(PumpToken, TokenPool):
    scraped_date: datetime


class PumpScraper:
    def __init__(self, logger: Logger):
        self.logger = logger.getChild(__name__)
        self.pump_api = PumpApi(logger=logger)
        self.pool_api = GeckoTerminal()
        self.pump_args = {"offset", "limit", "sort", "order", "includeNsfw"}

    @exception_handler
    async def get_results(self, **kwargs) -> List[PumpScraperToken]:
        results: List[PumpScraperToken] = []

        coin_args = {k: v for k, v in kwargs.items() if k in self.pump_args}
        coins = await self.get_coins(**coin_args)
        for coin in coins:
            if not coin.raydium_pool:
                self.logger.debug(f"{coin.symbol} has no pool, skipping")
                results.append(PumpScraperToken(**coin.model_dump()))
                continue

            if coin.complete and coin.raydium_pool:
                self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...")
                pool = await self.get_pool(coin.raydium_pool)
                if pool:
                    pool_data = pool.get_token_pool()
                    results.append(PumpScraperToken(**coin.model_dump(), **pool_data.model_dump()))
                    self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...[done]")
                else:
                    results.append(PumpScraperToken(**coin.model_dump()))
                    self.logger.debug(f"Processing: {coin.symbol} ({coin.mint})...[skipped]")
            else:
                results.append(PumpScraperToken(**coin.model_dump()))
                self.logger.debug(f"{coin.symbol} skipped (pool={coin.raydium_pool}, grad={coin.complete})")

        return results

    @retry(BaseException, tries=3, delay=2, backoff=2)
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

    @retry(BaseException, tries=3, delay=2, backoff=2)
    def get_pool(self, pool_id: str) -> Union[List[Pool], ApiError]:
        return format_response(self.pool_api.get_pool(pool_id=pool_id))
