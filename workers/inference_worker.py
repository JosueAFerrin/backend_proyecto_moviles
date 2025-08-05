import time
import onnxruntime
import redis
import pika

def infer_image(image_bytes):
    # Código real para procesar imagen con ONNX
    # Ejemplo ficticio:
    return {"label": "Límite de velocidad", "confidence": 0.98}

def connect_redis():
    while True:
        try:
            r = redis.Redis(host="redis", port=6379)
            r.ping()
            print("[✓] Conectado a Redis")
            return r
        except redis.exceptions.ConnectionError:
            print("[!] Esperando Redis...")
            time.sleep(3)

def connect_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            channel = connection.channel()
            print("[✓] Conectado a RabbitMQ")
            return channel
        except pika.exceptions.AMQPConnectionError:
            print("[!] Esperando RabbitMQ...")
            time.sleep(3)

def callback(ch, method, properties, body):
    task_id = properties.headers.get("task_id") if properties and properties.headers else "unknown"
    print(f"[→] Tarea recibida: {task_id}")

    try:
        prediction = infer_image(body)
        r = connect_redis()
        r.setex(task_id, 300, str(prediction))  # TTL de 5 min
        print(f"[✓] Resultado almacenado en Redis con task_id={task_id}")
    except Exception as e:
        print(f"[x] Error procesando la tarea: {e}")

def consume():
    channel = connect_rabbitmq()
    channel.queue_declare(queue="tasks")
    channel.basic_consume(queue="tasks", on_message_callback=callback, auto_ack=True)
    print("[✓] Esperando tareas... Ctrl+C para detener.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupción manual. Cerrando consumer.")
    except Exception as e:
        print(f"[x] Error en el consumidor: {e}")

if __name__ == "__main__":
    consume()
