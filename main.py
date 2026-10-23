"""Serve the student impact website and its prediction API."""
from pathlib import Path

import joblib
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from social_media_model import predict_new_student

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "social_media_impact_model.pkl"
model_bundle = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Social Media Impact Explorer",
    description="Student wellbeing model demo and prediction API.",
    version="1.0.0",
)


class StudentInput(BaseModel):
    """One student record using the model's expected input fields."""

    model_config = ConfigDict(extra="forbid")

    Age: int = Field(ge=10, le=100)
    Gender: str = Field(min_length=1)
    Academic_Level: str = Field(min_length=1)
    Primary_Platform: str = Field(min_length=1)
    Daily_Usage_Hours: float = Field(ge=0, le=24)
    Weekend_Extra_Hours: float = Field(ge=0, le=24)
    Device_Type: str = Field(min_length=1)
    Sleep_Duration_Hours: float = Field(ge=0, le=24)
    Sleep_Quality_Score: int = Field(ge=1, le=5)
    Late_Night_Usage: bool
    Social_Comparison_Frequency: str = Field(min_length=1)


@app.get("/", include_in_schema=False)
def website():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/style.css", include_in_schema=False)
def stylesheet():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")


@app.get("/app.js", include_in_schema=False)
def javascript():
    return FileResponse(BASE_DIR / "app.js", media_type="text/javascript")


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": MODEL_PATH.exists()}


@app.post("/predict")
def predict(student: StudentInput):
    """Return predictions for one student."""
    return predict_new_student(model_bundle, student.model_dump())
