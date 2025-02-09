from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic.dataclasses import dataclass

from src.models.integration.api import ApiModel
from src.models.instruments.transaction import PoolTransactionData
from src.utils.scripts import convert_percentage


class TokenReserves(ApiModel):
    reserves: Optional[float] = None
    reserves_in_usd: Optional[float] = None


class TokenValueData(ApiModel):
    fdv_in_usd: Optional[float] = None
    market_cap_in_usd: Optional[float] = None
    market_cap_to_holders_ratio: Optional[float] = None


class HistoricalDataEntry(ApiModel):
    swaps_count: Optional[int] = None
    buyers_count: Optional[int] = None
    price_in_usd: Optional[float] = None
    sellers_count: Optional[int] = None
    volume_in_usd: Optional[float] = None
    buy_swaps_count: Optional[int] = None
    sell_swaps_count: Optional[int] = None


class SentimentVotes(ApiModel):
    total: Optional[int] = None
    up_percentage: Optional[float] = None
    down_percentage: Optional[float] = None


class GTScoreDetails(ApiModel):
    info: Optional[float] = None
    pool: Optional[float] = None
    transactions: Optional[float] = None
    holders: Optional[float] = None
    creation: Optional[float] = None


class HighLowPriceData(ApiModel):
    high_price_in_usd_24h: Optional[float] = None
    high_price_timestamp_24h: Optional[datetime] = None
    low_price_in_usd_24h: Optional[float] = None
    low_price_timestamp_24h: Optional[datetime] = None


class Attributes(ApiModel):
    address: Optional[str] = None
    name: Optional[str] = None
    fully_diluted_valuation: Optional[float] = None
    base_token_id: Optional[str] = None
    price_in_usd: Optional[float] = None
    price_in_target_token: Optional[float] = None
    reserve_in_usd: Optional[float] = None
    reserve_threshold_met: Optional[bool] = None
    from_volume_in_usd: Optional[float] = None
    to_volume_in_usd: Optional[float] = None
    api_address: Optional[str] = None
    pool_fee: Optional[float] = None
    token_weightages: Optional[dict] = None
    token_reserves: Dict[str, TokenReserves]
    token_value_data: Dict[str, TokenValueData]
    balancer_pool_id: Optional[str] = None
    swap_count_24h: Optional[int] = None
    swap_url: Optional[str] = None
    sentiment_votes: Optional[SentimentVotes] = None
    price_percent_change: Optional[str] = None
    price_percent_changes: Dict[str, str] = None
    historical_data: Dict[str, HistoricalDataEntry]
    locked_liquidity: Optional[float] = None
    security_indicators: List = []
    gt_score: Optional[float] = None
    gt_score_details: Optional[GTScoreDetails] = None
    pool_reports_count: Optional[int] = None
    pool_created_at: Optional[datetime] = None
    latest_swap_timestamp: Optional[datetime] = None
    high_low_price_data_by_token_id: Dict[str, HighLowPriceData]
    is_nsfw: Optional[bool] = None
    is_stale_pool: Optional[bool] = None
    is_pool_address_explorable: Optional[bool] = None

    @property
    def price_percent_change_value(self):
        return convert_percentage(self.price_percent_change)

    def price_percent_change_from(self, field: str):
        return convert_percentage(self.price_percent_changes.get(field))


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
    price_change_5m: float
    price_change_15m: float
    price_change_30m: float
    price_change_1h: float
    price_change_6h: float
    price_change_24h: float


class Pool(ApiModel):
    data: PoolData
    included: Optional[List[Union[PoolTransactionData]]] = None

    def get_token_pool(self) -> TokenPool:
        attr = self.data.attributes
        return TokenPool(
            pool_name=attr.name,
            price=attr.price_in_usd,
            price_change_5m=attr.price_percent_change_from(field='last_5m'),
            price_change_15m=attr.price_percent_change_from(field='last_15m'),
            price_change_30m=attr.price_percent_change_from(field='last_30m'),
            price_change_1h=attr.price_percent_change_from(field='last_1h'),
            price_change_6h=attr.price_percent_change_from(field='last_6h'),
            price_change_24h=attr.price_percent_change_value
        )
