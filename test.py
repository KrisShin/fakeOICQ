import asyncio
import aiohttp
import aio_pika

async def connect_to_rabbitmq():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    return channel, connection

async def handle_websocket_messages(websocket_url, rabbit_channel):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(websocket_url) as ws:
            while True:
                msg = await ws.receive()
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.data
                    routing_key = "your_routing_key"
                    message = aio_pika.Message(body=data.encode())

                    await rabbit_channel.default_exchange.publish(
                        message,
                        routing_key=routing_key,
                    )
                    print(f"Sent to RabbitMQ: {data}")

async def main():
    rabbit_channel, rabbit_connection = await connect_to_rabbitmq()
    try:
        websocket_url = "ws://your-websocket-server-url"
        await handle_websocket_messages(websocket_url, rabbit_channel)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        await rabbit_connection.close()

if __name__ == "__main__":
    asyncio.run(main())