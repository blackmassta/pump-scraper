import hashlib
import json
import random
import time
from functools import lru_cache
from logging import Logger
from typing import Any, Dict, List, Optional

from playwright.async_api import async_playwright
from pydantic import BaseModel

from src.api.api_base import BaseApi
from src.models.integration.api import ApiError, ApiException

PROXIES = [
    "https://150.136.247.129:1080",
    "http://3.90.100.12:80",
    "http://13.247.119.111:11",
    "http://47.251.122.81:8888",
]


def get_random_proxy():
    return random.choice(PROXIES)


@lru_cache(maxsize=100)
def cache_response(url: str, params: str):
    return None  # Placeholder for caching logic


def cache_result(url: str, params: str, data: Any, expiry: int = 300):
    cache_key = hashlib.md5(f"{url}{params}".encode()).hexdigest()
    cache_response.cache_clear()
    cache_response.cache_response[cache_key] = (time.time(), data, expiry)


class BaseWebApi(BaseApi):
    def __init__(self, logger: Logger, base_url: str):
        super().__init__(logger=logger, base_url=base_url)
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }

    async def _post_request(
            self, url: str,
            params: Optional[BaseModel] = None,
            method: str = "POST",
            data: Optional[Dict] = None
    ) -> Dict | List[Dict] | ApiError:
        proxy = get_random_proxy()
        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=True, proxy={"server": proxy})
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=self.user_agent)
            page = await context.new_page()

            query_params = self.to_query_string(params)
            full_url = f"{url}?{query_params}"

            self.logger.debug(f"{method} {full_url} via {proxy}")
            await page.evaluate(
                "(url, headers, body) => fetch(url, { method: 'POST', headers, body: JSON.stringify(body) }).then(res => res.text())",
                full_url, self.headers, data
            )

            response = await page.evaluate("() => document.body.innerText")
            await browser.close()

            try:
                parsed_response = json.loads(response)
                # cache_result(url, json.dumps(params.dict() if params else {}), parsed_response)
                return parsed_response
            except json.JSONDecodeError:
                raise ApiException(500, f"Invalid JSON from {url}", response)

    async def _get_request(
            self,
            url: str,
            params: Optional[BaseModel] = None,
            data: Optional[Dict] = None
    ) -> Dict | List[Dict] | ApiError:
        # cached = cache_response(url, json.dumps(params.dict() if params else {}))
        # if cached:
        #     return cached

        proxy = get_random_proxy()
        async with async_playwright() as p:
            # browser = await p.chromium.launch(headless=True, proxy={"server": proxy})
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=self.user_agent)
            page = await context.new_page()

            query_params = self.to_query_string(params)
            full_url = f"{url}?{query_params}"

            self.logger.debug(f"GET {full_url} via {proxy}")
            await page.goto(full_url, wait_until="networkidle")

            response = await page.evaluate("() => document.body.innerText")
            await browser.close()

            try:
                parsed_response = json.loads(response)
                # cache_result(url, json.dumps(params.dict() if params else {}), parsed_response)
                return parsed_response
            except json.JSONDecodeError:
                raise ApiException(500, f"Invalid JSON from {url}", response)
