from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

Instrumentator().instrument(app).expose(app)

model = joblib.load("model.pkl")

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/ready")
def ready():

    if model is None:
        return {"ready": False}

    return {"ready": True}

@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    pred = model.predict(df)

    return {"prediction": float(pred[0])}
