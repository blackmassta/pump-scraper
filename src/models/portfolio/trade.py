from pydantic import Field
from datetime import datetime
from typing import Optional

from src.models.integration.api import ApiModel
from src.utils.scripts import timestamp_to_date


class Trade(ApiModel):
    signature: str
    mint: str
    sol_amount: int
    token_amount: int
    is_buy: bool
    user: str
    timestamp: Optional[datetime] = Field(alias="timestamp", default_factory=lambda: timestamp_to_date)
    tx_index: int
    username: Optional[str] = None
    profile_image: Optional[str] = None
    slot: int
