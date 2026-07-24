from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import FastAPI
import joblib
import pandas as pd
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends
import secrets

app = FastAPI(title="House Price Prediction API", version="1.0.0")

Instrumentator().instrument(app).expose(app)

model = joblib.load("model.pkl")

@app.get("/", tags=["System"])
def root():
    return {
        "service": app.title,
        "version": app.version,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

security = HTTPBasic()


def verify_metrics(credentials: HTTPBasicCredentials = Depends(security)):

    correct_username = secrets.compare_digest(
        credentials.username,
        "gr"
    )

    correct_password = secrets.compare_digest(
        credentials.password,
        "123"
    )

    if not (correct_username and correct_password):
        raise Exception("Invalid credentials")


@app.get("/metrics")
def metrics(credentials: HTTPBasicCredentials = Depends(verify_metrics)):

    return Response(
        generate_latest(),
        media_type="text/plain"
    )
    
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
