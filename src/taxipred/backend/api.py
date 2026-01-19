from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Load model

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.joblib"

model = joblib.load(MODEL_PATH)

# Pydantic model for input


class TripFeatures(BaseModel):
    Trip_Distance_km: float
    Trip_Duration_Minutes: float
    Passenger_Count: int
    Base_Fare: float
    Per_Km_Rate: float
    Per_Minute_Rate: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "Trip_Distance_km": 5.0,
                "Trip_Duration_Minutes": 12.0,
                "Passenger_Count": 1,
                "Base_Fare": 40.0,
                "Per_Km_Rate": 10.0,
                "Per_Minute_Rate": 2.0,
            }
        }
    }


# Create FastAPI app

app = FastAPI(
    title="Taxi Price Prediction API",
    description="API som predikterar taxipriser baserat på resinformation.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Taxi Price Prediction API",
        "docs_url": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: TripFeatures):
    """
    Ta emot feature-data och returnera ett predikterat pris.
    """
    # Arrange the values ​​in the same order as in training
    data = np.array(
        [
            [
                features.Trip_Distance_km,
                features.Trip_Duration_Minutes,
                features.Passenger_Count,
                features.Base_Fare,
                features.Per_Km_Rate,
                features.Per_Minute_Rate,
            ]
        ]
    )

    pred_price = model.predict(data)[0]
    return {
        "predicted_price": round(float(pred_price), 2),
        "currency": "SEK",
    }
