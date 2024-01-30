from typing import Dict
import aio_pika
from fastapi import WebSocket

from config.settings import MQ_BROKER


class WebSocketManager:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def close(self):
        await self.websocket.close()

    async def send(self, message: str, routing_key: str):
        if not self.websocket:
            raise Exception(f"WebSocket connection of {routing_key} is not established")
        # await self.websocket.send_text(message)
        await self.websocket.send_text('pong')

    # async def broadcast(self, message: str, routing_key: str = ""):
    #     for connection in self.connections:
    #         await self.send(routing_key, message, connection)

    async def receive_message(self):
        if not self.websocket:
            await self.connect(self.websocket)
        message = await self.websocket.recv()
        return message


class MQClient(object):
    client = None
    channel = None

    def __init__(self):
        self.client = None
        self.channel = None

    async def connect(self):
        if not self.client:
            self.client = await aio_pika.connect_robust(MQ_BROKER)
            self.channel = await self.client.channel()
        return self.client, self.channel

    async def close(self):
        if self.client:
            await self.client.close()

    async def send(self, message: str, routing_key: str):
        _, channel = await self.connect()
        message = aio_pika.Message(body=message.encode())
        await channel.default_exchange.publish(message, routing_key=routing_key)


class MessagePush(object):
    connection_map = Dict
    mq_client: MQClient = None

    def __init__(self) -> None:
        self.connection_map = {}
        self.mq_client = MQClient()

    async def connect(self, websocket: WebSocket, routing_key: str):
        ws = self.connection_map.get(routing_key)
        if not ws:
            ws = WebSocketManager(websocket)
            self.connection_map[routing_key] = ws
        await self.mq_client.connect()

    async def close(self, routing_key: str):
        ws = self.connection_map.get(routing_key)
        if not ws:
            ws = WebSocketManager()
            self.connection_map[routing_key] = ws
        await self.connection_map[routing_key].close()
        await self.mq_client.close()

    async def send(self, message: str, routing_key: str):
        await self.connection_map[routing_key].send(message, routing_key)
        await self.mq_client.send(message, routing_key)

    async def broadcast(self, message: str, routing_key: str = ""):
        for connection in self.connections:
            await self.send(routing_key, message, connection)


msg_client = MessagePush()
