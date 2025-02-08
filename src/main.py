# Apify SDK - A toolkit for building Apify Actors. Read more at:
# https://docs.apify.com/sdk/python
from apify import Actor

from src.pump_scraper import PumpScraper
from src.utils.condition import Condition, OperatorEnum, ConditionConstant


async def build_params():
    params = {}
    transforms = {
        "filter": "term",
        "offset": None,
        "limit": None,
        "sort": None,
        "order_by": "order",
        "is_nsfw": "includeNsfw"
    }

    args = await Actor.get_input() or {}
    for k, v in args.items():
        if k in transforms:
            if v is not None:
                params[transforms[k]] = v
            else:
                params[k] = v

    return params


async def build_filters():
    args = await Actor.get_input() or {}
    transform = {
        "is_graduated": "complete",
        "has_king_of_the_hill": "king_of_the_hill_timestamp",
        "min_mkt_cap": "market_cap_usd" if args.get("is_mkt_cap_usd") else "market_cap",
        "max_mkt_cap": "market_cap_usd" if args.get("is_mkt_cap_usd") else "market_cap"
    }

    conditions = ConditionConstant(is_true=True)
    for key, value in args.items():
        if value is None:  # Skip None or null values
            continue

        if key in transform:
            field = transform[key]
        else:
            field = key  # Default to the key if no transformation exists

        # Infer operator for range-based filters
        if key.startswith("min_"):
            operator = OperatorEnum.GTE
        elif key.startswith("max_"):
            operator = OperatorEnum.LTE
        elif key.startswith("has_"):
            operator = OperatorEnum.NOT_NULL
        else:
            operator = OperatorEnum.EQ

        conditions = conditions & Condition(field, operator, value)

    return conditions


async def main() -> None:
    """Main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with Apify platform, and it also enhances performance in
    the field of web scraping significantly.
    """
    async with Actor:
        # Retrieve the input object for the Actor. The structure of input is defined in input_schema.json.
        params = await build_params()
        conditions = await build_filters()
        client = PumpScraper(logger=Actor.log)
        # Fetch the HTML content of the page, following redirects if necessary.
        Actor.log.info(f'Sending a request with params {params}')
        results = await client.get_results(**params)
        filtered = filter(conditions.evaluate, results)
        # Save the extracted headings to the dataset, which is a table-like storage.
        await Actor.push_data(filtered)
