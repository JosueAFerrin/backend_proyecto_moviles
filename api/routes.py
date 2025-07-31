from fastapi import APIRouter, UploadFile, File, Depends
from utils.firebase import verify_token
from services.rabbitmq import enqueue_task
from services.redis import get_result

router = APIRouter()

@router.post("/predict")
async def predict_image(token: str = Depends(verify_token), image: UploadFile = File(...)):
    task_id = await enqueue_task(image)
    return {"task_id": task_id, "message": "Tarea encolada exitosamente"}

@router.get("/result/{task_id}")
async def get_result_route(task_id: str, token: str = Depends(verify_token)):
    result = await get_result(task_id)
    return result
