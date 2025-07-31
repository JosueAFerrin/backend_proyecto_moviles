import onnxruntime
import redis
import pika

def infer_image(image_bytes):
    # Código real para procesar imagen con ONNX
    # Ejemplo ficticio:
    return {"label": "Límite de velocidad", "confidence": 0.98}

def callback(ch, method, properties, body):
    task_id = properties.headers.get("task_id")
    prediction = infer_image(body)

    r = redis.Redis(host="redis", port=6379)
    r.setex(task_id, 300, str(prediction))  # TTL de 5 min

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="tasks")
    channel.basic_consume(queue="tasks", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    consume()

