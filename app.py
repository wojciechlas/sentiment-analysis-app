from fastapi import FastAPI
from pydantic import BaseModel
import cloudpickle


app = FastAPI()
with open("artifacts/inference_class.pkl", "rb") as file:
    Inference = cloudpickle.load(file)
inference = Inference("artifacts/")


class PredtictionRequest(BaseModel):
    text: str


class PredictionResponse(BaseModel):
    prediction: str


@app.get("/")
async def root():
    return {"message": "Hello in Text Analysis API. Go to /docs for more information."}


@app.get("/health")
async def health():
    return 200


@app.post("/predict/", response_model=PredictionResponse)
async def predict(text: PredtictionRequest):
    """
    Predict the sentiment of the given text.
    """
    return {"prediction": inference.predict(text.text)}
