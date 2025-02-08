from enum import Enum
from logging import Logger
from typing import List

from pydantic import Field

from src.api.web_api_base import BaseWebApi
from src.models.integration.api import ApiModel, ApiError
from src.models.instruments.pool import Pool


def get_dex_pools_includes() -> List[str]:
    return [
        # "dex",
        # "dex.network.explorers",
        # "dex_link_services",
        # "network_link_services",
        "pairs",
        # "token_link_services",
        # "tokens.token_security_metric",
        # "tokens.tags",
        # "pool_locked_liquidities"
    ]


class OrderByDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


class GetPoolFilters(ApiModel):
    include: List[str] = Field(default_factory=get_dex_pools_includes)
    base_token: int = 0


class GeckoTerminal(BaseWebApi):
    # https://app.geckoterminal.com/api/p1/solana/pools/ADpoE7CoikKvvNwG3TFtkXHX3NvwiWtGZ7Zz8rMm2cvd?include=dex%2Cdex.network.explorers%2Cdex_link_services%2Cnetwork_link_services%2Cpairs%2Ctoken_link_services%2Ctokens.token_security_metric%2Ctokens.tags%2Cpool_locked_liquidities&base_token=0
    def __init__(self, logger: Logger, base_url: str = "https://app.geckoterminal.com/api/p1"):
        super().__init__(logger=logger, base_url=base_url)
        self.headers = {
            "authority": "app.geckoterminal.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0",
            "if-none-match": 'W/"01541c4e2711b22ecdb85568358050ff"',
            "priority": "u=0, i",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }
        self.cookies = {
            "cf_clearance": "3Zb_0e_qHB6IBH3CFPqNKFMIg7hN2ov9OU9UoNH0X9s-1738169499-1.2.1.1-KnYVa6HIMu2ZxsnzX9uNhI_7eqGFNmBPACzEp3E5ujKvC2VxEevDYu5et2lhmC2QJv2fKGIIfoFFOWzr3c_FGUm2x8KHvMQ2wxS2cCZQ7RZb2DIkWMXgAIOosjEqAgXD.Mhxe4m8m0GPLbFKfZ01CZzT1.9Kr6NMxjWkpkF24dzqcA_SQ9TFfrS1YAQtJHyomskJn9dg1znE6ZHFVwIN2mbsbfmdCoeBrY13gZnhkPs45C5.9S38bMFLtd7DtFMq5lbY1lMFzV4nGZFpajXbtblk5yIZwrRktcilhGFdERuDQekZJyXpMz93BJGDEgQPiWDtB5cafQBdEdeUJgyR8w",
            "mp_eae71b34ac47c7d3e252b88f9f41577b_mixpanel": "%7B%22distinct_id%22%3A%20%22%24device%3A194b2fa467d52fb-0795bfcccbe88b-26011851-1fa400-194b2fa468052fe%22%2C%22%24device_id%22%3A%20%22194b2fa467d52fb-0795bfcccbe88b-26011851-1fa400-194b2fa468052fe%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.geckoterminal.com%2Fsolana%2Fpools%2FHga48QXtpCgLSTsfysDirPJzq8aoBPjvePUgmXhFGDro%3F__cf_chl_tk%3DisfC3aZrHY8W1IPlN5wxpIF51cRwLrJEozIo.rZkeKU-1738169499-1.0.1.1-1q7FUJ_x9PB0Ld2tMq2KA69.4ZTUQkckdKYwEJ9mUuA%22%2C%22%24initial_referring_domain%22%3A%20%22www.geckoterminal.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.geckoterminal.com%2Fsolana%2Fpools%2FHga48QXtpCgLSTsfysDirPJzq8aoBPjvePUgmXhFGDro%3F__cf_chl_tk%3DisfC3aZrHY8W1IPlN5wxpIF51cRwLrJEozIo.rZkeKU-1738169499-1.0.1.1-1q7FUJ_x9PB0Ld2tMq2KA69.4ZTUQkckdKYwEJ9mUuA%22%2C%22%24initial_referring_domain%22%3A%20%22www.geckoterminal.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D",
            "_ga_X7G8VKSH3M": "GS1.1.1738169537.1.0.1738169537.0.0.0",
            "_ga": "GA1.1.377756733.1738169538",
            "__gads": "ID=e4ef1238dbcbb62d:T=1738169551:RT=1738169551:S=ALNI_MYU0x68ZlMI3eGGYG5nDGV0VzKFgQ",
            "__gpi": "UID=0000103701d28658:T=1738169551:RT=1738169551:S=ALNI_MbS3v2WIliwPK1J83u5ZMS2hqmB-A",
            "__eoi": "ID=03054b14315d744c:T=1738169551:RT=1738169551:S=AA-AfjaKtKH5ruY0zB3cdk0nUB42",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Jan+29+2025+11%3A53%3A17+GMT-0500+(Eastern+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=63201b11-f0f7-4c1f-92bd-bd0c80e8ee2c&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Fwww.geckoterminal.com%2Fsolana%2Fpools%2FHga48QXtpCgLSTsfysDirPJzq8aoBPjvePUgmXhFGDro&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1",
            "__cf_bm": "JUaZdJbLpzzNQrfABeSfKvVD1GKsdNMzc.NJrMd4A8o-1738526775-1.0.1.1-Br8XVBKEU.9us1B01I4Tr2ukU27DMZ8z5BF56Ii149k1A8xhVr0ieZhFXS7fwRsbu7zIcdQLYdGPf_1ToJ.DUQ",
        }

    async def get_pool(self, pool_id: str, **kwargs) -> Pool | ApiError | None:
        if pool_id:
            url = f"{self.base_url}/solana/pools/{pool_id}"
            params = GetPoolFilters(**kwargs)

            return await self._get_single(url, params=params, return_type=Pool)
        else:
            return None
