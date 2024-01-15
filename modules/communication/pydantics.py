from enum import IntEnum


class MessageType(IntEnum):
    """
    message type
    """

    TEXT = 1
    IMAGE = 2
    VEDIO = 3
    LINK = 4
    AUDIO = 5
    FILE = 6
