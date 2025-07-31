import aioredis

redis = aioredis.from_url("redis://redis")

async def get_result(task_id: str):
    result = await redis.get(task_id)
    if result:
        return {"status": "completed", "prediction": result.decode()}
    return {"status": "processing"}
