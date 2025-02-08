from logging import Logger
from typing import Type, Any, Dict, List, Optional
from urllib import parse

import requests
from pydantic import BaseModel

from src.models.integration.api import ApiError, ApiException


class ModelConverter:
    def __init__(self, base_type: Type, logger: Logger):
        self.base_type = base_type
        self.logger = logger.getChild(__name__)

    def convert(self, item: Dict):
        try:
            return self.base_type(**item)
        except Exception as e:
            self.logger.error(f"Failed to convert to `{self.base_type}`: {item}", exc_info=e)
            raise

    def convert_list(self, items: List[Dict]):
        results = []
        for item in items:
            try:
                converted = self.convert(item)
                results.append(converted)
            except Exception as e:
                self.logger.debug(f"Skipping failed item: `{self.base_type}`: {item}", exc_info=e)

        return results


class BaseApi:
    def __init__(self, logger: Logger, base_url: str):
        self.base_url = base_url
        self.logger = logger.getChild(__name__)
        self.headers = {
            "authority": "frontend-api-v3.pump.fun",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://pump.fun",
            "priority": "u=1, i",
            "referer": "https://pump.fun/",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }
        self.user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )

    @staticmethod
    def to_query_string(model: BaseModel) -> str:
        # Convert the Pydantic model to a dictionary
        model_dict = model.dict()

        # Prepare a list to hold query parameters
        query_params = []

        for key, value in model_dict.items():
            if isinstance(value, list):
                # Convert list to CSV string
                value = ",".join(map(str, value))
            # URL encode each key and value
            query_params.append(f"{parse.quote(str(key))}={parse.quote(str(value))}")

        # Join all query parameters with '&'
        return "&".join(query_params)

    async def _post_request(
            self, url: str,
            params: Optional[BaseModel] = None,
            data: Optional[BaseModel] = None
    ) -> Dict | List[Dict] | ApiError:
        # Initialize the session and set the user-agent
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})
        # Make the request
        response = session.post(url, params=params, headers=self.headers, data=data.model_dump_json() if data else None)
        # Output response status and content
        self.logger.debug("Params:", params.json())
        self.logger.debug("Status Code:", response.status_code)
        self.logger.debug("Response Content:", len(response.text))
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiException(
                response.status_code,
                message=(
                    f"Error retrieving data: {response.status_code}"
                    f"(url={url}, params={self.to_query_string(params)}"
                ),
                response_text=response.text
            )

    async def _get_request(self, url: str, params: BaseModel) -> Dict | List[Dict] | ApiError:
        # Initialize the session and set the user-agent
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})
        # Make the request
        response = session.get(url, params=params, headers=self.headers)
        # Output response status and content
        self.logger.debug("Params:", params.json())
        self.logger.debug("Status Code:", response.status_code)
        self.logger.debug("Response Content:", len(response.text))
        if response.status_code == 200:
            return response.json()
        else:
            raise ApiException(
                response.status_code,
                message=(
                    f"Error retrieving data: {response.status_code}"
                    f"(url={url}, params={self.to_query_string(params)}"
                ),
                response_text=response.text
            )

    async def _get_list(self, url: str, params: BaseModel, return_type: Type, path: str = None) -> Any | ApiError:
        try:
            converter = ModelConverter(base_type=return_type, logger=self.logger)
            result = await self._get_request(url, params=params)
            data = result[path] if path else result
            if isinstance(data, list):
                return converter.convert_list(data)
            else:
                return [converter.convert(data)]
        except ApiException as ae:
            self.logger.error(ae)
            raise
        except Exception as e:
            self.logger.error(e)
            raise ApiException(status_code=500, message="Unknown server error", cause=e)

    async def _get_single(self, url: str, params: BaseModel, return_type: Type, path: str = None) -> Any | ApiError:
        try:
            converter = ModelConverter(base_type=return_type, logger=self.logger)
            result = await self._get_request(url, params)
            data = result[path] if path else result
            if data and isinstance(data, list):
                data = data[0]
                return converter.convert(data)
            elif data:
                return converter.convert(data)
            else:
                return None
        except ApiException as ae:
            self.logger.error(ae)
            raise
        except Exception as e:
            self.logger.error(e)
            raise ApiException(status_code=500, message="Unknown server error", cause=e)

    async def _post(self, url: str, params: Optional[BaseModel], data: BaseModel, return_type: Type) -> Any | ApiError:
        try:
            converter = ModelConverter(base_type=return_type, logger=self.logger)
            result = await self._post_request(url, params, data=data)
            return converter.convert(result)
        except ApiException as ae:
            self.logger.error(ae)
            raise
        except Exception as e:
            self.logger.error(e)
            raise ApiException(status_code=500, message="Unknown server error", cause=e)
