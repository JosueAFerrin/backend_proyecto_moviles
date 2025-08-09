from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import requests
from uuid import uuid4
from services.rabbitmq import publish_task
from services.redis import get_task_result
from api.auth import verify_token
from api.schema import RegisterRequest
from utils.firebase import FIREBASE_API_KEY
from utils.gemini import interpret_prediction

router = APIRouter()

@router.post("/auth/register")
def register_user(data: RegisterRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    try:
        response = requests.post(url, json={
            "email": data.email,
            "password": data.password,
            "returnSecureToken": True
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {e}")

@router.post("/auth/login")
def login_user(data: RegisterRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    try:
        response = requests.post(url, json={
            "email": data.email,
            "password": data.password,
            "returnSecureToken": True
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=401, detail=f"Credenciales inválidas: {e}")

@router.post("/predict")
def predict(image: UploadFile = File(...), token=Depends(verify_token)):
    image_bytes = image.file.read()
    task_id = str(uuid4())
    publish_task(image_bytes, task_id)
    return {"task_id": task_id, "message": "Tarea encolada exitosamente"}

@router.get("/result/{task_id}")
def get_result(task_id: str, token=Depends(verify_token)):
    result = get_task_result(task_id)
    if not result:
        return {"status": "Pendiente o inexistente"}
    return {"status": "Listo", "resultado": result}

@router.post("/interpret")
def interpret(prediction: dict, token=Depends(verify_token)):
    try:
        interpretation = interpret_prediction(prediction)
        return {"interpretacion": interpretation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al interpretar con Gemini: {str(e)}")
