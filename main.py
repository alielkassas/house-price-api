from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

Instrumentator().instrument(app).expose(app)

model = joblib.load("model.pkl")

@app.post("/predict")
def predict(data: dict):

    df = pd.DataFrame([data])

    pred = model.predict(df)

    return {"prediction": float(pred[0])}
