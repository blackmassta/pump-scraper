from typing import Optional

from src.models.integration.api import ApiModel


class TransactionEntry(ApiModel):
    buys: Optional[int] = None
    sells: Optional[int] = None


class TransactionData(ApiModel):
    last_300_s: Optional[TransactionEntry] = None
    last_900_s: Optional[TransactionEntry] = None
    last_1800_s: Optional[TransactionEntry] = None
    last_3600_s: Optional[TransactionEntry] = None
    last_7200_s: Optional[TransactionEntry] = None
    last_21600_s: Optional[TransactionEntry] = None
    last_43200_s: Optional[TransactionEntry] = None
    last_86400_s: Optional[TransactionEntry] = None
    last_172800_s: Optional[TransactionEntry] = None


class Attributes(ApiModel):
    base_symbol: Optional[str] = None
    base_address: Optional[str] = None
    base_price_in_currency: Optional[float] = None
    base_price_in_usd_percent_change: Optional[float] = None
    quote_symbol: Optional[str] = None
    quote_address: Optional[str] = None
    quote_price_in_currency: Optional[float] = None
    quote_price_in_usd_percent_change: Optional[float] = None
    base_price_in_quote: Optional[float] = None
    quote_price_in_base: Optional[float] = None
    volume_in_currency: Optional[float] = None
    volume_in_usd: Optional[float] = None
    transaction_data: Optional[TransactionData] = None


class PoolTransactionData(ApiModel):
    id: str
    type: str
    attributes: Optional[Attributes] = None
