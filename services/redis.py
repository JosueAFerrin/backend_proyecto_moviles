import redis
import os
import pickle

# Configuración de Redis usando variables de entorno
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # Nombre del contenedor Redis en docker-compose
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Función para guardar el resultado en Redis
def save_task_result(task_id: str, result: dict):
    try:
        redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redis_conn.set(task_id, pickle.dumps(result))
        print(f"[REDIS] Resultado guardado para task_id {task_id}")
    except Exception as e:
        print(f"[REDIS ERROR] No se pudo guardar el resultado: {e}")

# Función para obtener el resultado de Redis
def get_task_result(task_id: str):
    try:
        redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        result = redis_conn.get(task_id)
        if result:
            return pickle.loads(result)
        return None
    except Exception as e:
        print(f"[REDIS ERROR] No se pudo obtener el resultado: {e}")
        return None
