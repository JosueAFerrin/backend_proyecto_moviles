# Funcionamiento de backend
🧠 1. ¿Cómo funciona el backend?
Arquitectura general:
java
Copy
Edit
Usuario (Postman / Flutter)
        |
        v
FastAPI backend  <---> Firebase Auth (verifica token)
        |
        v
  RabbitMQ (cola de tareas)
        |
        v
    Worker (ONNX + Python)
        |
        v
     Redis (almacena resultado temporal)
        ^
        |
FastAPI <-- GET resultado

# Pasos para implementación
📤 Paso 1: POST /predict
El usuario envía una imagen junto con un token de autenticación de Firebase.

FastAPI:

Verifica el token con la clave de Firebase.

Extrae la imagen y la convierte en bytes.

Crea un task_id (UUID).

Encola los datos en RabbitMQ con el task_id.

Devuelve el task_id.

🧵 Paso 2: Worker
Escucha la cola tasks en RabbitMQ.

Recibe la imagen (como bytes) y el task_id.

Carga el modelo ONNX y realiza la inferencia.

Guarda el resultado en Redis, bajo ese task_id, con TTL de 5 minutos.

📥 Paso 3: GET /result/{task_id}
El cliente consulta por ese task_id.

FastAPI busca en Redis el resultado.

Si está disponible, lo devuelve.

Si no, responde con 404 Not Found.

🔁 ¿Cómo conectarlo con tu propio modelo ONNX?
Paso 1: Entrena o convierte tu modelo a ONNX
Puedes convertir modelos de PyTorch, TensorFlow o scikit-learn a .onnx.

Ejemplo con PyTorch:

----------------------------------------------------------

import torch

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(model, dummy_input, "modelo.onnx")
Paso 2: Carga tu modelo en el worker
Tu archivo inference_worker.py contiene esta función:
----------------------------------------------------------


import onnxruntime

def infer_image(image_bytes):
    return {"label": "Límite de velocidad", "confidence": 0.98}

------------------------------------------------------------

Modifica así para usar tu modelo real:

import onnxruntime as ort
import numpy as np
from PIL import Image
import io

# Carga el modelo ONNX solo una vez
session = ort.InferenceSession("ruta/a/tu_modelo.onnx")

def preprocess(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))  # depende del modelo
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.transpose(2, 0, 1)  # (H, W, C) -> (C, H, W)
    img_array = np.expand_dims(img_array, axis=0)  # (1, C, H, W)
    return img_array

def infer_image(image_bytes):
    input_array = preprocess(image_bytes)
    outputs = session.run(None, {"input": input_array})
    prediction = outputs[0]

    # Lógica para decodificar predicción
    label = np.argmax(prediction)
    confidence = float(np.max(prediction))
    return {"label": str(label), "confidence": confidence}

🚀 ¿Cómo implementarlo con Flutter?
Autenticación con Firebase en Flutter:

Usa firebase_auth para iniciar sesión con correo y contraseña.

Obtén el token con:

final token = await FirebaseAuth.instance.currentUser?.getIdToken();
Enviar imagen al backend:
Usa http o dio para hacer el POST con encabezado Authorization: Bearer {token} y el archivo como multipart/form-data.

✅ Resumen
Componente	------- Rol

FastAPI	----------- Expone endpoints para subir imagenes y consultar resultados
Firebase ----------	Verifica que solo usuarios registrados accedan
RabbitMQ ----------	Cola donde se encolan tareas de inferencia
Worker ------------	Consume imágenes, ejecuta modelo ONNX, guarda resultados
Redis -------------	Almacena resultados temporalmente por task_id

# NOTA
En la carpeta de secrets va el archivo de configuración de Firebase (firebase-key).