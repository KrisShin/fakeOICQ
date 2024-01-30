from datetime import timedelta
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from modules.common.exceptions import BadRequest, NotFound
from modules.common.global_variable import BaseResponse
from modules.common.utils import queryset_to_pydantic_model
from modules.communication.models import Communication, Message
from modules.communication.pydantics import MessageParamPydantic, MessagePydantic
from modules.user.models import ContactUser, User

from modules.user.utils import get_current_user_model
from modules.common.redis_client import cache_client


router = APIRouter()


@router.post("/message/")
async def post_message(
    params: MessageParamPydantic, me: User = Depends(get_current_user_model)
):
    """
    Send message to user.
    """
    relation = await ContactUser.get_or_none(id=params.contact_id, is_block=False)
    communication = await Communication.get_or_none(id=params.communication_id)
    if not all((relation, communication)):
        raise BadRequest('This user is not your contact')
    message = await Message.create(**params.model_dump())
    communication.latest_message = message
    await communication.save()
    # TODO: judge user online or offline to send notification
    return BaseResponse()


@router.get("/{communication_id}/{last_message_time}")
async def get_messages(
    communication_id: str,
    last_message_time: str = None,
    me: User = Depends(get_current_user_model),
):
    """
    Get messages from communication.
    """
    commuincation = await Communication.get_or_none(
        id=communication_id
    ).prefetch_related('contact_users')
    if not commuincation:
        raise NotFound('Communication not found')
    contact_user = await commuincation.contact_users[0]

    await contact_user.fetch_related('me', 'contact')

    if me not in (contact_user.me, contact_user.contact):
        raise BadRequest('You are not in this communication.')
    message_queryset = Message.filter(communication_id=communication_id)
    if last_message_time:
        message_queryset = message_queryset.filter(create_time__lt=last_message_time)
    message_queryset = await message_queryset.limit(10)
    data = queryset_to_pydantic_model(message_queryset, MessagePydantic)
    return BaseResponse(data)
