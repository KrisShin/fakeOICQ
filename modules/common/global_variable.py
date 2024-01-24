from typing import Any

from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token/")


class BaseResponse:
    def __init__(
        self,
        message: str = 'success',
        data: Any = None,
    ) -> None:
        self.message = message
        self.data = data
