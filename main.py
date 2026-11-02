import os
import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

import schemas
from classifier import classifier_engine
from feature_extractor import extract_kinematic_biomarkers
from model import build_neuroscan_cnn_model

app = FastAPI(
    title="NeuroScan — AI-Based Movement Analysis System",
    description="Educational prototype and research exploration tool for evaluating motor biomarkers and CNN feature activations in movement disorders.",
    version="1.0.0"
)

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5175,http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "NeuroScan Movement Analysis Platform",
        "system_type": "Educational Prototype & Research Framework",
        "diagnostic_disclaimer": "NOT a medical device. Not intended for clinical diagnosis."
    }


@app.get("/api/samples", response_model=List[schemas.MotorSample], tags=["Synthetic Motor Data"])
def list_synthetic_patient_samples():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_motor_samples.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


@app.get("/api/samples/{sample_id}", response_model=schemas.MotorSample, tags=["Synthetic Motor Data"])
def get_patient_sample(sample_id: str):
    samples = list_synthetic_patient_samples()
    for s in samples:
        if s.get("sample_id") == sample_id:
            return s
    raise HTTPException(status_code=404, detail="Synthetic patient sample not found.")


@app.post("/api/screen/predict", response_model=schemas.ScreeningPrediction, tags=["Screening & Inference"])
def screen_motor_test(submission: schemas.MotorTestSubmission):
    if not submission.coordinates or len(submission.coordinates) < 4:
        raise HTTPException(status_code=400, detail="Coordinate sequence too short for reliable motor analysis.")
    return classifier_engine.predict(submission.coordinates, sample_id=submission.patient_alias or "SCREEN-001")


@app.post("/api/screen/extract-features", response_model=schemas.KinematicBiomarkers, tags=["Screening & Inference"])
def extract_features_only(coordinates: List[List[float]] = Body(..., embed=True)):
    if len(coordinates) < 4:
        raise HTTPException(status_code=400, detail="Insufficient coordinates provided.")
    biomarkers, _ = extract_kinematic_biomarkers(coordinates)
    return biomarkers


@app.get("/api/model/architecture", tags=["Model Inspection"])
def get_cnn_architecture():
    arch = build_neuroscan_cnn_model()
    if isinstance(arch, dict):
        return arch
    return {
        "model_name": arch.name,
        "total_parameters": arch.count_params(),
        "layers_count": len(arch.layers),
        "status": "TensorFlow CNN Model Graph compiled successfully"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)
