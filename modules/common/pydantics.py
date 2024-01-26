from datetime import timedelta
from enum import Enum, IntEnum
from typing import Tuple

from tortoise.contrib.pydantic import pydantic_model_creator

from modules.common.models import Tag

TagPydantic = pydantic_model_creator(
    Tag, name='TagPydantic', include=['key', 'description']
)


class _OptionType:
    code: int
    limit: int  # limit times
    expire: timedelta  # seconds

    def __init__(self, code, limit, expire) -> None:
        super().__init__()
        self.code = code
        self.limit = limit
        self.expire = timedelta(seconds=expire)


class UserOpration(Enum):
    LOGIN_FAILED: _OptionType = _OptionType(1, 3, 10 * 60)
    EDIT_INFO: _OptionType = _OptionType(2, 1, 30 * 60)
    EDIT_PASSWORD: _OptionType = _OptionType(3, 3, 60 * 60 * 24)
    EDIT_AVATAR: _OptionType = _OptionType(4, 1, 30 * 60)
    ADD_CONTACT: _OptionType = _OptionType(5, 50, 60 * 60 * 24)
    SEND_MESSAGE: _OptionType = _OptionType(6, 100, 5 * 60)
