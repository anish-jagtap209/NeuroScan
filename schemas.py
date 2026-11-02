from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field


class KinematicBiomarkers(BaseModel):
    dominant_tremor_freq_hz: float = Field(..., description="Dominant tremor frequency component in Hertz")
    velocity_variance: float = Field(..., description="Variance in drawing stroke speed (pixels/sec)")
    pressure_stability_ratio: float = Field(..., ge=0.0, le=1.0, description="Stability of pen/stylus pressure")
    trajectory_entropy: float = Field(..., ge=0.0, le=1.0, description="Geometric jitter / Shannon entropy of path")
    drawing_duration_sec: float = Field(..., gt=0.0, description="Total duration of motor exercise in seconds")


class MotorSample(BaseModel):
    sample_id: str
    patient_alias: str
    age: int = Field(..., ge=18, le=105)
    gender: str
    test_type: str  # "Archimedean Spiral Test", "Sinusoidal Waveform Test"
    synthetic_classification: str
    ground_truth_label: int  # 0 = Control / Low Anomaly, 1 = Detected Anomaly
    kinematic_biomarkers: KinematicBiomarkers
    points_preview: List[List[float]]
    clinician_scenario_notes: Optional[str] = ""


class MotorTestSubmission(BaseModel):
    patient_alias: Optional[str] = "Anonymous Screening Patient"
    test_type: str = "Archimedean Spiral Test"
    # List of [x, y, timestamp_ms] or [x, y] coordinates
    coordinates: List[List[float]] = Field(..., min_length=10)


class ScreeningPrediction(BaseModel):
    sample_id: str
    risk_level: str  # "Low Risk / Baseline", "Moderate Anomaly", "Elevated Anomaly"
    anomaly_probability: float = Field(..., ge=0.0, le=100.0)
    confidence_interval: Tuple[float, float]
    biomarkers: KinematicBiomarkers
    feature_extraction_time_ms: float
    model_inference_time_ms: float
    attention_heatmap_matrix: Optional[List[List[float]]] = None
    educational_disclaimer: str
    clinical_interpretations: List[str]
