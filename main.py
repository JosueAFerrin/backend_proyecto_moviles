from fastapi import FastAPI
from utils import firebase  # Esto inicializa Firebase al importar
from api.routes import router

app = FastAPI()
app.include_router(router)
