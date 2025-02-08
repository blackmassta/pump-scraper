from functools import wraps
from typing import Iterator

from src.models.integration.api import ApiError
from src.utils.scripts import is_primitive


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Extract status_code and response_text if available
            status_code = getattr(e, "status_code", "Unknown")
            response_text = getattr(e, "response_text", str(e))
            url = kwargs.get("url", "Unknown")  # Retrieve 'url' from kwargs if available

            return ApiError(error_code=str(status_code), message=f"{e}\n{response_text}", url=url)

    return wrapper


def format_response(value):
    if is_primitive(value):
        return {
            'data': value
        }
    elif isinstance(value, list):
        return {
            'count': len(value),
            'data': value
        }
    elif isinstance(value, Iterator):
        value = list(value)
        return {
            'count': len(value),
            'data': value
        }
    elif isinstance(value, dict):
        return {
            'count': len(value),
            'data': value
        }
    else:
        return {
            'data': value
        }
