import asyncio
import aio_pika


async def main():
    # 建立连接
    connection = await aio_pika.connect_robust(
        "amqp://oicquser:oicqpwd@localhost:56372/oicqmq"
    )

    # 创建通道
    channel = await connection.channel()

    # 声明队列，假设我们监听名为'example_queue'的队列，并且设置其为持久化
    queue = await channel.declare_queue('your_routing_key', durable=True)

    # 设置消息处理回调函数
    async def process_message(message: aio_pika.IncomingMessage):
        print(f"Received message: {message.body.decode()}")
        # 手动应答确认消息被正确处理
        await message.ack()

    # 开始消费消息
    await queue.consume(process_message)

    # 保持应用运行以持续监听消息
    print("Awaiting messages...")
    await asyncio.Future()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
