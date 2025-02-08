from src.models.integration.api import ApiModel


class TransactionEntry(ApiModel):
    buys: int
    sells: int


class TransactionData(ApiModel):
    last_300_s: TransactionEntry
    last_900_s: TransactionEntry
    last_1800_s: TransactionEntry
    last_3600_s: TransactionEntry
    last_7200_s: TransactionEntry
    last_21600_s: TransactionEntry
    last_43200_s: TransactionEntry
    last_86400_s: TransactionEntry
    last_172800_s: TransactionEntry


class Attributes(ApiModel):
    base_symbol: str
    base_address: str
    base_price_in_currency: float
    base_price_in_usd_percent_change: float
    quote_symbol: str
    quote_address: str
    quote_price_in_currency: float
    quote_price_in_usd_percent_change: float
    base_price_in_quote: float
    quote_price_in_base: float
    volume_in_currency: float
    volume_in_usd: float
    transaction_data: TransactionData


class PoolTransactionData(ApiModel):
    id: str
    type: str
    attributes: Attributes
