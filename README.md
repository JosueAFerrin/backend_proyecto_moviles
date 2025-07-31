# 🛑 Backend de Reconocimiento de Señales de Tránsito

Este proyecto es un backend para la clasificación de señales de tránsito a partir de imágenes enviadas por los usuarios autenticados. Utiliza **FastAPI**, **Firebase Authentication**, **RabbitMQ**, **Redis** y un **modelo ONNX** para realizar la inferencia de manera asíncrona.
---

## 🚀 Tecnologías Utilizadas

- **FastAPI**
- **Firebase Authentication**
- **RabbitMQ**
- **Redis**
- **ONNX Runtime**
- **Docker** + **Docker Compose**

---

## 🛠️ Requisitos Previos

- Docker y Docker Compose instalados.
- Proyecto creado en Firebase con autenticación habilitada.
- Un modelo entrenado exportado en formato `.onnx`.

---

## ⚙️ Configuración y Ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/backend-transito.git
cd backend-transito
```

### 2. Agrega tu clave privada de Firebase

```
mkdir secrets
# Copia tu clave a secrets/firebase-key.json
```

### 3. Agrega tu modelo ONNX

Coloca tu archivo `model.onnx` en la raíz del proyecto.

### 4. Levanta los servicios

```bash
docker-compose up --build
```

---

## 🔐 Autenticación con Firebase

### Obtener Token con Python

```python
import requests

email = "correo@ejemplo.com"
password = "tu_contraseña"
api_key = "TU_API_KEY_FIREBASE"

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
data = {"email": email, "password": password, "returnSecureToken": True}
res = requests.post(url, json=data)
print(res.json()["idToken"])
```

---

## 📤 Enviar Imagen a `/predict`

- Endpoint: `POST /predict`
- Header: `Authorization: Bearer <token>`
- Body: Imagen como `multipart/form-data`

Respuesta:

```json
{
  "task_id": "f5a4b3d7-2c4e-4b2f-9339-87654321abcd",
  "message": "Tarea encolada exitosamente"
}
```

---

## 📥 Consultar Resultado

- Endpoint: `GET /result/{task_id}`

Respuesta cuando hay resultado:

```json
{
  "result": "Señal: STOP"
}
```

---

## 🧠 Cómo Funciona

1. Se recibe imagen con token Firebase.
2. Se encola tarea en RabbitMQ.
3. Worker procesa imagen con modelo ONNX.
4. Resultado se guarda en Redis por 5 minutos.
5. Se consulta por `task_id`.

---

## 🧾 .gitignore sugerido

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Entornos
env/
venv/
.env
.env.*

# Secretos
secrets/
firebase-key.json

# Modelos
*.onnx
*.h5

# Logs
*.log

# Docker
*.pid

# IDEs
.vscode/
.idea/
```

---

## 🗺️ Futuras Mejoras

- Autenticación OAuth2
- Estadísticas de inferencia
- Interfaz web
- Reintentos por error

---

## 📄 Licencia

MIT License © 2025 Josué Ferrin