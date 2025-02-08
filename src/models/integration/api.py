from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ApiError(BaseModel):
    error_code: str
    message: str
    url: Optional[str] = None

    def __repr__(self):
        return f"ApiError(error_code={self.error_code}, message={self.message}, url={self.url})"


class ApiModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.isoformat() if dt else None,
        },
        populate_by_name=True,
        arbitrary_types_allowed=False
    )


class ApiException(Exception):
    def __init__(self, status_code: int, message: str, response_text: Optional[str] = None, cause: Exception = None):
        super().__init__(message, cause)
        self.status_code = status_code
        self.response_text = response_text
