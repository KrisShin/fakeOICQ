from datetime import timedelta
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from modules.common.redis_client import cache_client

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            user_id = await websocket.receive_text()
            if user_id.startswith('ping.'):
                user_id = user_id[5:]
                await cache_client.set_cache(
                    f'{user_id}.alive', 1, ex=timedelta(minutes=5)
                )

                # 向前端发送消息
                await websocket.send_text('pong')
            raise WebSocketDisconnect
        except WebSocketDisconnect:
            await cache_client.del_cache(f'{user_id}.alive')
            break
