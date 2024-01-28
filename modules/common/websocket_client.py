import aio_pika

from config.settings import MQ_BROKER


async def connect_to_rabbitmq():
    connection = await aio_pika.connect_robust(MQ_BROKER)
    channel = await connection.channel()
    return channel, connection