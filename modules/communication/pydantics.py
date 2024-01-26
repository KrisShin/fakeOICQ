from pydantic import BaseModel

from modules.communication.models import Communication, Message, MessageType
from tortoise.contrib.pydantic import pydantic_model_creator


class MessageParamPydantic(BaseModel):
    communication_id: str
    contact_id: str
    content: str
    message_type: MessageType


CommunicationPydantic = pydantic_model_creator(
    Communication,
    name="CommunicationPydantic",
)
MessagePydantic = pydantic_model_creator(
    Message,
    name="MessagePydantic",
)
