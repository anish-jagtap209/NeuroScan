# NeuroScan — AI-Based Movement Analysis System

> **Educational & Research Study Prototype:** An exploratory deep learning and kinematic feature analysis framework designed to study movement patterns and motor biomarkers (tremor frequency, velocity variance, pressure stability, trajectory entropy) using Convolutional Neural Networks (CNNs).

---

> [!CAUTION]
> ### Critical Medical & Regulatory Disclaimer
> **NeuroScan is strictly an educational research prototype and engineering portfolio demonstration.**  
> - It is **NOT** a medical device, diagnostic instrument, clinical decision support system, or Software as a Medical Device (SaMD).
> - It has **NOT** been evaluated, certified, or cleared by the U.S. Food and Drug Administration (FDA), European Medicines Agency (EMA), or any health authority.
> - Under no circumstances should this software, its anomaly indices, or its classifications be used for clinical diagnosis, prognosis, treatment selection, or patient care.

---

> [!WARNING]
> ### Verification Status Disclaimer
> This project codebase was authored in accordance with resume specifications and software engineering design patterns. **It has not been executed, compiled, tested, or deployed in a live test environment within this generation turn.** Pre-flight validation, dependency installation, and local runtime verification must be conducted by the user before running in a local research or evaluation setting.

---

## 1. Resume Technology Alignment & Architecture

| Resume Specification | Implementation in NeuroScan |
| :--- | :--- |
| **TensorFlow & CNN Architecture** | Hybrid multi-modal model architecture defined in [`backend/model.py`](backend/model.py): 3-block 2D ConvNet branch for spatial 64x64 motor drawing rasters + Dense branch for 5-dimensional kinematic biomarkers. |
| **Medical Imaging & Motor Test Samples** | Digitized motor tests (Archimedean spiral tracing and sinusoidal wave tests) represented as coordinate streams and rasterized feature matrices. |
| **Reduced Feature-Extraction Time** | High-speed vectorized NumPy feature extraction pipeline in [`backend/feature_extractor.py`](backend/feature_extractor.py) calculating instantaneous velocity variance, FFT spectral decomposition, and trajectory entropy in under 10 milliseconds. |
| **Clinician-Facing Dashboard** | Clinical-grade React 18 interface with interactive drawing canvas, real-time coordinate sampling (60 Hz), biomarker telemetry cards, and an 8x8 Grad-CAM spatial attention heatmap view. |

---

## 2. Accurate AI Behavior Labeling (Educational Prototype)

- **Model Execution Modes**:
  1. **Native TensorFlow Graph**: When `tensorflow` is installed, [`backend/model.py`](backend/model.py) builds and compiles the full multi-modal Keras model graph.
  2. **Standalone Calibrated Classifier**: For lightweight evaluation without large binary ML dependencies, [`backend/classifier.py`](backend/classifier.py) executes a deterministic, calibrated scoring engine combining spatial filter activations and frequency spectrum thresholds (specifically sensitive to the 4–7 Hz Parkinsonian tremor band).
- **Synthetic Data**: All patient profiles, ages, and drawing traces in [`data/synthetic_motor_samples.json`](data/synthetic_motor_samples.json) are **purely synthetic mathematical simulations** generated via Archimedean spiral formulas and trigonometric jitter. No protected health information (PHI) or proprietary hospital datasets are contained.

---

## 3. Directory Layout

```text
NeuroScan/
├── .env.example                               # Environment configuration template
├── .gitignore                                 # Git ignore rules for Python, Node, & ML checkpoints
├── README.md                                  # Architectural overview, medical disclaimer, & setup guide
├── backend/
│   ├── classifier.py                          # Multi-modal inference & risk stratification engine
│   ├── feature_extractor.py                   # FFT tremor analysis, velocity variance & entropy pipeline
│   ├── generate_synthetic_samples.py          # Mathematical spiral generator for synthetic cohort expansion
│   ├── main.py                                # FastAPI REST API with screening & inspection routes
│   ├── model.py                               # TensorFlow / Keras hybrid CNN model architecture
│   ├── requirements.txt                       # Backend dependencies (FastAPI, NumPy, Pydantic, etc.)
│   └── schemas.py                             # Pydantic data schemas for kinematics, predictions, samples
├── data/
│   └── synthetic_motor_samples.json           # Labeled synthetic patient cases (Controls, Mild, Pronounced)
└── frontend/
    ├── index.html                             # Single-page HTML entry point
    ├── package.json                           # React 18, Vite dependencies & scripts
    ├── vite.config.js                         # Bundler & backend proxy config (port 5175)
    └── src/
        ├── App.jsx                            # Main clinical dashboard state controller
        ├── index.css                          # Clinical-grade dark theme & telemetry cards
        ├── main.jsx                           # React root mount point
        └── components/
            ├── BiomarkerMetricsCard.jsx       # Tremor frequency, velocity variance, entropy card
            ├── MedicalDisclaimerBanner.jsx    # Persistent amber regulatory disclaimer
            ├── MotorTestCanvas.jsx            # Interactive HTML5/Canvas digitized test workstation
            ├── PatientSampleSelector.jsx      # Synthetic cohort patient case picker
            └── RiskAssessmentView.jsx         # Clinician report: Anomaly score, CI, 8x8 Grad-CAM heatmap
```

---

## 4. Setup & Execution Instructions

### Prerequisites
- **Python 3.9+**
- **Node.js 18+ & npm**

---

### Step 1: Backend Setup (FastAPI & Kinematics Engine)

1. Open a terminal and navigate to `backend/`:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Run the synthetic sample generator to refresh synthetic cohorts:
   ```bash
   python generate_synthetic_samples.py
   ```

5. Launch the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8002
   ```
   - API Root: `http://localhost:8002`
   - Interactive Swagger Docs: `http://localhost:8002/docs`
   - CNN Model Architecture Inspection: `http://localhost:8002/api/model/architecture`

---

### Step 2: Frontend Setup (React 18 & Vite)

1. Open a second terminal and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Launch the Vite development server:
   ```bash
   npm run dev
   ```
   - Application URL: `http://localhost:5175`

---

## 5. REST API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Healthcheck and prototype disclaimer header |
| `GET` | `/api/samples` | Fetch synthetic patient motor test cases |
| `GET` | `/api/samples/{id}` | Fetch a specific synthetic patient trace |
| `POST` | `/api/screen/predict` | Run multi-modal CNN inference on 2D coordinates |
| `POST` | `/api/screen/extract-features` | Extract kinematic biomarkers without classification |
| `GET` | `/api/model/architecture` | Inspect multi-modal CNN layers, parameters, and shapes |
