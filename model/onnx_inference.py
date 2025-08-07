import onnxruntime
import numpy as np
from PIL import Image
import io

session = onnxruntime.InferenceSession("model/model.onnx")

def preprocess(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = np.array(image).astype(np.float32) / 255.0
    img_array = img_array.transpose(2, 0, 1)  # canal primero
    return np.expand_dims(img_array, axis=0)

def run_inference(image_bytes):
    input_data = preprocess(image_bytes)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    outputs = session.run([output_name], {input_name: input_data})[0]
    label = np.argmax(outputs)
    confidence = float(np.max(outputs))
    return {"label": f"Señal {label}", "confidence": confidence}

def infer_image(image_bytes: bytes):
    # Lógica real con tu modelo ONNX aquí
    return {"label": "Límite de velocidad", "confidence": 0.98}

