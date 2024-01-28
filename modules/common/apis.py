from datetime import timedelta
import aio_pika
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from config.settings import MQ_BROKER

from modules.common.redis_client import cache_client

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = await aio_pika.connect_robust(MQ_BROKER)
    channel = await connection.channel()

    await websocket.accept()

    while True:
        try:
            user_id = await websocket.receive_text()
            print('websocket get', user_id)
            if user_id.startswith('ping.'):
                user_id = user_id[5:]
                await cache_client.set_cache(
                    f'{user_id}.alive', 1, ex=timedelta(minutes=5)
                )
                # 接收到WebSocket消息后，发布到RabbitMQ
                routing_key = "your_routing_key"
                message = aio_pika.Message(body=user_id.encode())
                await channel.default_exchange.publish(message, routing_key=routing_key)
                # 向前端发送消息
                await websocket.send_text('pong')
            else:
                raise WebSocketDisconnect
        except WebSocketDisconnect:
            print('websocket close')
            await cache_client.del_cache(f'{user_id}.alive')
            break
