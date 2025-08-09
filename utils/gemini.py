# utils/gemini.py

import google.generativeai as genai
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")  # modelo correcto

def interpret_prediction(prediction: dict) -> str:
    prompt = f"""
    Tengo el siguiente resultado de una predicción de una señal de tránsito: {prediction}.
    Por favor, proporciona una breve explicación comprensible de esta señal, incluyendo su significado y contexto de uso.
    """
    response = model.generate_content(prompt)
    return response.text
