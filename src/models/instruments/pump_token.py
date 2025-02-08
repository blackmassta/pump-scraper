from datetime import datetime
from typing import Optional

from pydantic import Field

from src.models.instruments.token import Token
from src.utils.scripts import timestamp_to_date


class PumpToken(Token):
    image_uri: Optional[str]
    metadata_uri: Optional[str]
    twitter: Optional[str] = None
    telegram: Optional[str] = None
    bonding_curve: Optional[str]
    associated_bonding_curve: Optional[str]
    raydium_pool: Optional[str] = None
    complete: bool
    virtual_sol_reserves: int
    virtual_token_reserves: int
    hidden: Optional[bool] = None
    total_supply: int
    website: Optional[str] = None
    show_name: bool
    last_trade_timestamp: Optional[datetime] = Field(alias="last_trade_timestamp", default_factory=lambda: timestamp_to_date)
    king_of_the_hill_timestamp: Optional[datetime] = Field(alias="king_of_the_hill_timestamp", default_factory=lambda: timestamp_to_date)
    reply_count: int
    last_reply: Optional[datetime] = Field(alias="last_reply", default_factory=lambda: timestamp_to_date)
    nsfw: bool
    market_id: Optional[str] = None
    inverted: Optional[bool] = None
    is_currently_live: bool
    username: Optional[str] = None
    profile_image: Optional[str] = None
