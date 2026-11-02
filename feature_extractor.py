"""Kinematic Feature Extraction Pipeline for Digitized Motor Tests

DISCLAIMER & EDUCATIONAL PROTOTYPE LABEL:
This module extracts physiological motor biomarkers from 2D coordinate streams (e.g. Archimedean
spiral tracing and sinusoidal waves). It calculates:
- Dominant tremor frequency using Fast Fourier Transform (FFT) on trajectory residual velocity.
- Velocity variance and drawing movement fluidity.
- Trajectory curvature entropy and dispersion.
- 64x64 spatial binary raster generation for CNN convolution.

Intended solely for research experimentation, engineering demonstration, and educational study.
"""

import math
import time
from typing import List, Tuple, Dict, Any
import numpy as np
import schemas


def rasterize_coordinates_to_matrix(
    coords: List[List[float]],
    grid_size: int = 64
) -> np.ndarray:
    """Rasters a list of 2D [x, y] coordinates into a normalized 2D matrix (grid_size x grid_size)."""
    matrix = np.zeros((grid_size, grid_size), dtype=np.float32)
    if not coords or len(coords) < 2:
        return matrix

    # Extract x and y
    xs = np.array([pt[0] for pt in coords])
    ys = np.array([pt[1] for pt in coords])

    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()

    range_x = max(max_x - min_x, 1e-5)
    range_y = max(max_y - min_y, 1e-5)

    # Normalize to [2, grid_size - 3] with padding
    pad = 4
    usable_dim = grid_size - 2 * pad
    norm_x = (((xs - min_x) / range_x) * usable_dim + pad).astype(int)
    norm_y = (((ys - min_y) / range_y) * usable_dim + pad).astype(int)

    for i in range(len(norm_x) - 1):
        x0, y0 = norm_x[i], norm_y[i]
        x1, y1 = norm_x[i + 1], norm_y[i + 1]

        # Simple Bresenham-like line stamping
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            cx = int(x0 + (x1 - x0) * (s / steps))
            cy = int(y0 + (y1 - y0) * (s / steps))
            if 0 <= cx < grid_size and 0 <= cy < grid_size:
                matrix[cy, cx] = 1.0

    return matrix


def extract_kinematic_biomarkers(
    coords: List[List[float]],
    sampling_rate_hz: float = 60.0
) -> Tuple[schemas.KinematicBiomarkers, float]:
    """Calculates kinematic biomarkers and measures extraction execution latency in milliseconds."""
    t_start = time.perf_counter()

    if len(coords) < 4:
        # Fallback values for minimal input
        biomarkers = schemas.KinematicBiomarkers(
            dominant_tremor_freq_hz=0.0,
            velocity_variance=0.0,
            pressure_stability_ratio=1.0,
            trajectory_entropy=0.0,
            drawing_duration_sec=1.0
        )
        t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        return biomarkers, round(t_elapsed_ms, 2)

    pts = np.array(coords)
    diffs = np.diff(pts[:, :2], axis=0)
    distances = np.linalg.norm(diffs, axis=1)

    # Calculate velocities (dt assumed 1 / sampling_rate_hz if timestamps omitted)
    dt = 1.0 / sampling_rate_hz
    velocities = distances / dt
    vel_variance = float(np.var(velocities))

    # FFT on velocity sequence to detect tremor frequencies (Parkinsonian resting/action tremor: 4-7 Hz)
    n = len(velocities)
    if n > 8:
        fft_vals = np.abs(np.fft.rfft(velocities - np.mean(velocities)))
        freqs = np.fft.rfftfreq(n, d=dt)

        # Focus on the physiologically relevant tremor frequency window (2.5 Hz to 9.0 Hz)
        tremor_mask = (freqs >= 2.5) & (freqs <= 9.0)
        if np.any(tremor_mask) and np.max(fft_vals[tremor_mask]) > 0:
            dominant_freq = float(freqs[tremor_mask][np.argmax(fft_vals[tremor_mask])])
        else:
            dominant_freq = float(freqs[np.argmax(fft_vals[1:]) + 1]) if len(freqs) > 1 else 0.8
    else:
        dominant_freq = 0.8

    # Trajectory entropy / direction jitter
    angles = np.arctan2(diffs[:, 1], diffs[:, 0])
    angle_changes = np.abs(np.diff(angles))
    # Normalize entropy approximation
    entropy_val = float(min(1.0, np.mean(angle_changes) / np.pi))

    # Estimated pressure / contact stability
    pressure_stability = float(max(0.2, min(1.0, 1.0 - (vel_variance / 120.0))))

    duration = float(len(coords) * dt)

    biomarkers = schemas.KinematicBiomarkers(
        dominant_tremor_freq_hz=round(dominant_freq, 2),
        velocity_variance=round(vel_variance, 2),
        pressure_stability_ratio=round(pressure_stability, 2),
        trajectory_entropy=round(entropy_val, 2),
        drawing_duration_sec=round(duration, 2)
    )

    t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return biomarkers, round(t_elapsed_ms, 2)
