from datetime import datetime
from typing import Optional

from pydantic import Field

from src.models.integration.api import ApiModel
from src.models.instruments.pool import Pool, TokenPool
from src.utils.scripts import timestamp_to_date, hours_ago


class Token(ApiModel):
    mint: str
    name: str
    symbol: str
    description: Optional[str]
    creator: str
    market_cap: float
    usd_market_cap: float
    created_timestamp: Optional[datetime] = Field(alias="created_timestamp", default_factory=lambda: timestamp_to_date)


class TokenData(ApiModel):
    token: Token
    pool: Pool
    price: Optional[TokenPool] = None
