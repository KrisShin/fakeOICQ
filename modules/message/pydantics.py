from enum import IntEnum
from pydantic import BaseModel


class MessageType(BaseModel, IntEnum):
    """
    message type
    """

    TEXT: int = 1
    IMAGE: int = 2
    VEDIO: int = 3
    LINK: int = 4
    AUDIO: int = 5
    FILE: int = 6
