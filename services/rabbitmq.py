import aio_pika
import uuid

async def enqueue_task(file):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()
    queue = await channel.declare_queue("tasks")

    task_id = str(uuid.uuid4())
    body = await file.read()

    await channel.default_exchange.publish(
        aio_pika.Message(body=body, headers={"task_id": task_id}),
        routing_key="tasks"
    )
    return task_id
