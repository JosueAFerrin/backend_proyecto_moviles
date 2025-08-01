from pydantic import BaseModel

class PredictionResult(BaseModel):
    label: str
    confidence: float

class PredictionResponse(BaseModel):
    status: str
    prediction: PredictionResult | None = None
