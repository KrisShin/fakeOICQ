from datetime import timedelta
import json
import aio_pika
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from config.settings import MQ_BROKER
from modules.common.exceptions import AuthorizationFailed, BadRequest

from modules.common.redis_client import cache_client
from modules.common.message_client import msg_client
from modules.communication.models import Message
from modules.user.models import ContactUser
from modules.user.utils import validate_token

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    text = await websocket.receive_text()
    if text.startswith('ping.*.'):
        _, token, communication_id = text.split('.*.')
        if not token:
            await websocket.close(1000, 'Authorization failed')
            raise BadRequest('Web socket auth failed')
        user_id = await validate_token(token)
        if user_id is False:
            await websocket.close(1000, 'Authorization failed')
            raise AuthorizationFailed()
        await msg_client.connect(websocket, communication_id)
        await websocket.send_text('pong')
        # no matter User online or not, message should send to message query.
        # await cache_client.set_cache(f'{user_id}.alive', 1, ex=timedelta(minutes=5))
    while True:
        try:
            msg = await websocket.receive_text()
            if msg.startswith('msg.'):
                msg = msg[4:]
                msg_dict = json.loads(msg)
                await Message.create(**msg_dict)
                # await cache_client.expire_cache(f'{user_id}.alive', ex=timedelta(minutes=5))
                await msg_client.send(msg, routing_key=communication_id)
                # await websocket.send_text('send success')
            else:
                raise WebSocketDisconnect
        except WebSocketDisconnect:
            print('websocket close')
            # await cache_client.del_cache(f'{user_id}.alive')
            break
