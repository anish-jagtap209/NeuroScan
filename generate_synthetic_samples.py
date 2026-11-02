"""Synthetic Data Generator for NeuroScan Motor Tests

Generates realistic mathematical representations of Archimedean spirals and sinusoidal waveforms
with controllable tremor frequency, velocity noise, and trajectory jitter.
"""

import json
import math
import os
import random
from typing import List, Dict, Any


def generate_archimedean_spiral(
    num_points: int = 120,
    turns: float = 3.5,
    tremor_freq: float = 0.0,
    tremor_amp: float = 0.0
) -> List[List[float]]:
    """Synthesizes an Archimedean spiral trajectory centered at (150, 150)."""
    points = []
    center_x, center_y = 150.0, 150.0
    max_theta = turns * 2 * math.pi
    b = 3.5  # spiral expansion coefficient

    for i in range(num_points):
        theta = (i / num_points) * max_theta
        r = b * theta

        # Base clean position
        x = center_x + r * math.cos(theta)
        y = center_y + r * math.sin(theta)

        # Ingest sinusoidal tremor jitter if enabled
        if tremor_amp > 0 and tremor_freq > 0:
            jitter = tremor_amp * math.sin(theta * tremor_freq * 2.0)
            noise_x = random.gauss(0, tremor_amp * 0.2)
            noise_y = random.gauss(0, tremor_amp * 0.2)
            x += jitter * math.cos(theta + math.pi / 2) + noise_x
            y += jitter * math.sin(theta + math.pi / 2) + noise_y

        points.append([round(x, 1), round(y, 1)])

    return points


def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, "synthetic_motor_samples.json")

    print(f"Generating synthetic motor test samples into {out_file}...")

    samples = [
        {
            "sample_id": "SYN-PT-101",
            "patient_alias": "Synthetic Case A (Baseline / Healthy Control)",
            "age": 58,
            "gender": "Female",
            "test_type": "Archimedean Spiral Test",
            "synthetic_classification": "Low Risk / Healthy Baseline",
            "ground_truth_label": 0,
            "kinematic_biomarkers": {
                "dominant_tremor_freq_hz": 0.8,
                "velocity_variance": 12.4,
                "pressure_stability_ratio": 0.94,
                "trajectory_entropy": 0.18,
                "drawing_duration_sec": 7.2
            },
            "points_preview": generate_archimedean_spiral(num_points=100, turns=3.0, tremor_freq=0.0, tremor_amp=0.0),
            "clinician_scenario_notes": "Smooth Archimedean spiral trajectory. Consistent radial progression with negligible postural tremor markers."
        },
        {
            "sample_id": "SYN-PT-102",
            "patient_alias": "Synthetic Case B (Mild Action Tremor Pattern)",
            "age": 64,
            "gender": "Male",
            "test_type": "Archimedean Spiral Test",
            "synthetic_classification": "Moderate Anomaly / Screening Recommended",
            "ground_truth_label": 1,
            "kinematic_biomarkers": {
                "dominant_tremor_freq_hz": 4.6,
                "velocity_variance": 38.6,
                "pressure_stability_ratio": 0.76,
                "trajectory_entropy": 0.54,
                "drawing_duration_sec": 11.8
            },
            "points_preview": generate_archimedean_spiral(num_points=120, turns=3.2, tremor_freq=4.6, tremor_amp=3.2),
            "clinician_scenario_notes": "Intermittent line oscillations detected in the 4–5 Hz band during fine motor movement. Velocity profile indicates micro-hesitations."
        },
        {
            "sample_id": "SYN-PT-103",
            "patient_alias": "Synthetic Case C (Pronounced Motor Anomaly Pattern)",
            "age": 71,
            "gender": "Male",
            "test_type": "Archimedean Spiral Test",
            "synthetic_classification": "Elevated Anomaly / Comprehensive Screening",
            "ground_truth_label": 1,
            "kinematic_biomarkers": {
                "dominant_tremor_freq_hz": 5.8,
                "velocity_variance": 64.2,
                "pressure_stability_ratio": 0.52,
                "trajectory_entropy": 0.82,
                "drawing_duration_sec": 16.4
            },
            "points_preview": generate_archimedean_spiral(num_points=140, turns=3.5, tremor_freq=5.8, tremor_amp=6.8),
            "clinician_scenario_notes": "Pronounced jagged waveforms accompanied by frequency concentration in the 5–6 Hz resting/postural tremor spectrum."
        }
    ]

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

    print("Synthetic sample generation successful.")


if __name__ == "__main__":
    main()
