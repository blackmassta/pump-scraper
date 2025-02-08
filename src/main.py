# Apify SDK - A toolkit for building Apify Actors. Read more at:
# https://docs.apify.com/sdk/python
import json
from typing import List

from apify import Actor

from src.pump_scraper import PumpScraper
from src.utils.api import format_response
from src.utils.condition import Condition, OperatorEnum, ConditionConstant


def get_transforms(is_mkt_cap_usd: bool = False):
    transforms = {
        "filter": "term",
        "offset": None,
        "limit": None,
        "order_by": "sort",
        "order_by_direction": "order",
        "is_nsfw": "includeNsfw",
        "is_graduated": "complete",
        "has_king_of_the_hill": "king_of_the_hill_timestamp",
        "min_mkt_cap": "market_cap_usd" if is_mkt_cap_usd else "market_cap",
        "max_mkt_cap": "market_cap_usd" if is_mkt_cap_usd else "market_cap"
    }

    return transforms


async def build_params():
    params = {}
    transform = get_transforms()
    args = await Actor.get_input() or {}
    for k, v in args.items():
        if k in transform:
            if transform[k] is not None:
                params[transform[k]] = v
            else:
                params[k] = v

    return params


async def build_filters(exclude_fields: List[str] = None):
    args = await Actor.get_input() or {}
    is_mkt_cap_usd = args.pop('is_mkt_cap_usd')
    transform = get_transforms(is_mkt_cap_usd=is_mkt_cap_usd)

    if exclude_fields:
        reverse_transform = {v if v else k: k for k, v in transform.items()}
        for field in exclude_fields:
            field_name = reverse_transform.get(field) or field
            Actor.log.debug(f"Removing excluded fields {field_name} from {args}")
            if field_name in args:
                args.pop(field_name)

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
            value = None if value == "both" else bool(value)
        elif key.startswith("is_"):
            operator = OperatorEnum.EQ
            value = None if value == "both" else bool(value)
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
        client = PumpScraper(logger=Actor.log)
        # Retrieve the input object for the Actor. The structure of input is defined in input_schema.json.
        params = await build_params()
        conditions = await build_filters(client.pump_args)
        # Fetch the HTML content of the page, following redirects if necessary.
        Actor.log.info(f'Sending a request with params {params}')
        results = await client.get_results(**params)
        if results:
            Actor.log.debug(f"Filtering results by: {conditions.to_sql(results[0])}")
            filtered = format_response(filter(conditions.evaluate, results))
            Actor.log.debug(f"Filtered results {filtered}")
            # Save the extracted headings to the dataset, which is a table-like storage.
            await Actor.push_data(filtered)
        else:
            return Actor.push_data(format_response(results))
