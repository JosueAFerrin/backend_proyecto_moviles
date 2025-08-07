import aio_pika
import uuid
import pika

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

def publish_task(image_bytes: bytes, task_id: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="tasks")
    channel.basic_publish(
        exchange="",
        routing_key="tasks",
        body=image_bytes,
        properties=pika.BasicProperties(headers={"task_id": task_id})
    )
    connection.close()