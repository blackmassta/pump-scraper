import sys
import time
from functools import wraps

import pytz
import random
from datetime import datetime, timedelta
from typing import Optional

primitives = (bool, str, int, float, type(None))


def is_primitive(obj):
    return isinstance(obj, primitives)


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def hours_ago(hours: int = 0) -> datetime:
    """Returns the datetime for one hour ago, including timezone info."""
    tz = pytz.timezone('UTC')  # You can replace 'UTC' with your desired timezone
    now = datetime.now(tz)
    return now - timedelta(hours=hours)


def start_of_day(days_ago_val: int = 0, timezone: str = "UTC") -> datetime:
    """
    Returns the start of the day (00:00:00) for `days_ago` days ago in the given timezone.

    Args:
        days_ago_val (int): Number of days ago (e.g., 1 for yesterday, 0 for today).
        timezone (str): Timezone string (e.g., "America/New_York", "UTC").

    Returns:
        datetime: Start of the requested day in the specified timezone.
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    target_day = now - timedelta(days=days_ago_val)
    start_of_day_value = target_day.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_of_day_value


def days_ago(days: int = 1) -> datetime:
    """Returns the datetime for one hour ago, including timezone info."""
    tz = pytz.timezone('UTC')  # You can replace 'UTC' with your desired timezone
    now = datetime.now(tz)
    return now - timedelta(days=days)


def timestamp_to_date(timestamp: Optional[int]) -> Optional[datetime]:
    """
    Convert a Unix timestamp (in milliseconds) to a datetime object.
    Return None if the timestamp is None.
    """
    if timestamp is not None:
        tz = pytz.timezone('UTC')  # You can replace 'UTC' with your desired timezone
        return datetime.fromtimestamp(timestamp / 1000, tz=tz)
    return None


def convert_percentage(percentage: str) -> float:
    if not percentage:  # Check for empty or None
        return 0.0

    try:
        # Remove the '%' sign and convert to float
        return float(percentage.strip('%'))
    except ValueError:
        # If conversion fails, return 0
        return 0.0


def random_between(a: int, b: int) -> int:
    """Returns a random integer between a and b (inclusive)."""
    return random.randint(a, b)


def stagger(a: int, b: int):
    wait = random_between(a, b)
    time.sleep(wait)


def exception_swallow(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Failed call to {func}", e, file=sys.stderr)
        return None

    return wrapper


def retry(exception_to_check, tries=3, delay=2, backoff=2):
    """
    Retry calling the decorated function using an exponential backoff.

    :param exception_to_check: The exception to check. Maybe a tuple of exceptions to check.
    :param tries: Number of times to try (not retry) before giving up.
    :param delay: Initial delay between retries in seconds.
    :param backoff: Backoff multiplier (e.g. value of 2 will double the delay each retry).
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    print(f"{e}, Retrying in {_delay} seconds...", file=sys.stderr)
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)

        return wrapper

    return decorator


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise Exception(f"Boolean value expected, got {value}")
