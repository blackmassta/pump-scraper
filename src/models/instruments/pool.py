from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic.dataclasses import dataclass

from src.models.integration.api import ApiModel
from src.models.instruments.transaction import PoolTransactionData
from src.utils.scripts import convert_percentage


class TokenReserves(ApiModel):
    reserves: Optional[float]
    reserves_in_usd: Optional[float]


class TokenValueData(ApiModel):
    fdv_in_usd: Optional[float]
    market_cap_in_usd: Optional[float]
    market_cap_to_holders_ratio: Optional[float]


class HistoricalDataEntry(ApiModel):
    swaps_count: Optional[int]
    buyers_count: Optional[int]
    price_in_usd: Optional[float]
    sellers_count: Optional[int]
    volume_in_usd: Optional[float]
    buy_swaps_count: Optional[int]
    sell_swaps_count: Optional[int]


class SentimentVotes(ApiModel):
    total: Optional[int]
    up_percentage: Optional[float]
    down_percentage: Optional[float]


class GTScoreDetails(ApiModel):
    info: Optional[float]
    pool: Optional[float]
    transactions: Optional[float]
    holders: Optional[float]
    creation: Optional[float]


class HighLowPriceData(ApiModel):
    high_price_in_usd_24h: Optional[float]
    high_price_timestamp_24h: Optional[datetime]
    low_price_in_usd_24h: Optional[float]
    low_price_timestamp_24h: Optional[datetime]


class Attributes(ApiModel):
    address: str
    name: str
    fully_diluted_valuation: float
    base_token_id: str
    price_in_usd: float
    price_in_target_token: float
    reserve_in_usd: float
    reserve_threshold_met: bool
    from_volume_in_usd: float
    to_volume_in_usd: float
    api_address: str
    pool_fee: Optional[float] = None
    token_weightages: Optional[dict] = None
    token_reserves: Dict[str, TokenReserves]
    token_value_data: Dict[str, TokenValueData]
    balancer_pool_id: Optional[str] = None
    swap_count_24h: int
    swap_url: str
    sentiment_votes: SentimentVotes
    price_percent_change: str
    price_percent_changes: Dict[str, str]
    historical_data: Dict[str, HistoricalDataEntry]
    locked_liquidity: Optional[float] = None
    security_indicators: List = []
    gt_score: Optional[float] = None
    gt_score_details: Optional[GTScoreDetails] = None
    pool_reports_count: Optional[int]
    pool_created_at: datetime
    latest_swap_timestamp: datetime
    high_low_price_data_by_token_id: Dict[str, HighLowPriceData]
    is_nsfw: Optional[bool] = None
    is_stale_pool: Optional[bool] = None
    is_pool_address_explorable: Optional[bool] = None

    def price_percent_change_value(self):
        return convert_percentage(self.price_percent_change)


class RelationshipItem(ApiModel):
    id: Optional[str]
    type: Optional[str]


class Relationships(ApiModel):
    dex: Dict[str, RelationshipItem]
    tokens: Dict[str, List[RelationshipItem]]
    pool_metric: Dict[str, RelationshipItem]
    pairs: Dict[str, List[RelationshipItem]]


class PoolData(ApiModel):
    id: str
    type: str
    attributes: Attributes
    relationships: Relationships


@dataclass
class TokenPool:
    pool_name: str
    price: float
    price_change_24h: float


class Pool(ApiModel):
    data: PoolData
    included: Optional[List[Union[PoolTransactionData]]] = None

    def get_token_pool(self) -> TokenPool:
        attr = self.data.attributes
        return TokenPool(
            pool_name=attr.name,
            price=attr.price_in_usd,
            price_change_24h=attr.price_percent_change_value()
        )
