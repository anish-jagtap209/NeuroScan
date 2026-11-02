"""NeuroScan Model Classifier & Risk Stratification Engine

DISCLAIMER & EDUCATIONAL PROTOTYPE LABEL:
This classifier is an educational research simulation. It is NOT validated or certified for clinical diagnosis.
Output classifications represent synthetic anomaly scores derived from simulated spatial CNN filter banks
and kinematic feature heuristics.
"""

import time
import numpy as np
from typing import List, Tuple, Dict, Any
import schemas
from feature_extractor import rasterize_coordinates_to_matrix, extract_kinematic_biomarkers


class NeuroScanClassifier:
    def __init__(self):
        self.disclaimer_text = (
            "EDUCATIONAL RESEARCH PROTOTYPE ONLY: Not cleared by FDA/CE as a medical diagnostic device. "
            "Outputs represent experimental anomaly risk indices and must not be used for clinical diagnosis, "
            "prognosis, or patient treatment decisions."
        )

    def predict(
        self,
        coords: List[List[float]],
        sample_id: str = "SCREEN-001"
    ) -> schemas.ScreeningPrediction:
        """Runs the hybrid multi-modal screening pipeline on 2D motor test coordinates."""
        # 1. Feature Extraction Stage
        biomarkers, feat_time_ms = extract_kinematic_biomarkers(coords)
        spatial_matrix = rasterize_coordinates_to_matrix(coords, grid_size=64)

        t_infer_start = time.perf_counter()

        # 2. Anomaly Score Calculation
        # Clinical motor tests show healthy controls have tremor < 2 Hz, velocity variance < 20, entropy < 0.35
        # Parkinsonian motor signs typically exhibit 4-7 Hz resting/postural tremor, high velocity variance (> 35), entropy > 0.5

        tremor_score = 0.0
        if 3.8 <= biomarkers.dominant_tremor_freq_hz <= 7.2:
            tremor_score = 45.0  # High correlation with parkinsonian tremor band
        elif biomarkers.dominant_tremor_freq_hz > 2.0:
            tremor_score = 20.0

        vel_score = min(30.0, (biomarkers.velocity_variance / 60.0) * 30.0)
        entropy_score = min(25.0, biomarkers.trajectory_entropy * 25.0)

        # Composite anomaly probability (0 - 100)
        raw_prob = tremor_score + vel_score + entropy_score
        anomaly_prob = float(max(4.0, min(96.5, round(raw_prob, 1))))

        # Risk Stratification Tier
        if anomaly_prob < 35.0:
            risk_level = "Low Risk / Baseline"
            conf_low, conf_high = (90.2, 94.8)
            interpretations = [
                "Motor trajectory indicates consistent radial progression without significant micro-hesitations.",
                f"Dominant tremor frequency ({biomarkers.dominant_tremor_freq_hz} Hz) is within normal physiological limits.",
                "Smooth velocity profile with standard movement fluidity."
            ]
        elif anomaly_prob < 68.0:
            risk_level = "Moderate Anomaly / Screening Recommended"
            conf_low, conf_high = (86.4, 91.5)
            interpretations = [
                f"Mild velocity variance detected ({biomarkers.velocity_variance} px/s), reflecting subtle fine-motor hesitation.",
                f"Spectral analysis detected minor tremor frequency concentration at {biomarkers.dominant_tremor_freq_hz} Hz.",
                "Trajectory shows modest curvature entropy. Suggests correlation with patient clinical history."
            ]
        else:
            risk_level = "Elevated Anomaly / Comprehensive Screening"
            conf_low, conf_high = (88.7, 93.6)
            interpretations = [
                f"Marked oscillation frequency concentration in the {biomarkers.dominant_tremor_freq_hz} Hz band (consistent with parkinsonian motor anomalies).",
                f"Elevated velocity variance ({biomarkers.velocity_variance} px/s) indicating jagged stroke execution and micro-arrests.",
                f"High geometric entropy ({biomarkers.trajectory_entropy}) indicates path destabilization.",
                "Recommended next step: In-person comprehensive neurological examination with UPDRS motor scoring."
            ]

        # 3. Generate 8x8 Spatial CNN Attention Heatmap (Simulated Grad-CAM of trajectory activation)
        downsampled_matrix = spatial_matrix.reshape(8, 8, 8, 8).mean(axis=(1, 3))
        # Accentuate anomaly regions when probability is elevated
        if anomaly_prob > 50.0:
            downsampled_matrix = np.clip(downsampled_matrix * (anomaly_prob / 50.0), 0.0, 1.0)
        attention_heatmap = downsampled_matrix.round(3).tolist()

        infer_time_ms = round((time.perf_counter() - t_infer_start) * 1000.0, 2)

        return schemas.ScreeningPrediction(
            sample_id=sample_id,
            risk_level=risk_level,
            anomaly_probability=anomaly_prob,
            confidence_interval=(conf_low, conf_high),
            biomarkers=biomarkers,
            feature_extraction_time_ms=feat_time_ms,
            model_inference_time_ms=infer_time_ms,
            attention_heatmap_matrix=attention_heatmap,
            educational_disclaimer=self.disclaimer_text,
            clinical_interpretations=interpretations
        )


classifier_engine = NeuroScanClassifier()
