import React, { useState, useEffect } from 'react';
import MedicalDisclaimerBanner from './components/MedicalDisclaimerBanner';
import PatientSampleSelector from './components/PatientSampleSelector';
import MotorTestCanvas from './components/MotorTestCanvas';
import BiomarkerMetricsCard from './components/BiomarkerMetricsCard';
import RiskAssessmentView from './components/RiskAssessmentView';

export default function App() {
  const [samples, setSamples] = useState([]);
  const [selectedSample, setSelectedSample] = useState(null);
  const [activePoints, setActivePoints] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Load synthetic patient cohort on mount
  useEffect(() => {
    fetch('/api/samples')
      .then((res) => res.json())
      .then((data) => {
        setSamples(data);
        if (data && data.length > 0) {
          setSelectedSample(data[0]);
          setActivePoints(data[0].points_preview);
        }
      })
      .catch((err) => console.error('Failed to load synthetic samples', err));
  }, []);

  const handleSelectSample = (sample) => {
    setSelectedSample(sample);
    setActivePoints(sample.points_preview);
    setPrediction(null);
  };

  const handleSwitchToFreehand = () => {
    setSelectedSample(null);
    setActivePoints([]);
    setPrediction(null);
  };

  const handleRunAnalysis = async (coords) => {
    if (!coords || coords.length < 5) return;
    setIsAnalyzing(true);
    try {
      const response = await fetch('/api/screen/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_alias: selectedSample ? selectedSample.patient_alias : 'Freehand Interactive Patient',
          test_type: selectedSample ? selectedSample.test_type : 'Freehand Motor Tracing',
          coordinates: coords
        })
      });
      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error('Error during CNN screening inference', err);
      alert('Inference call failed. Verify backend service is running on port 8002.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div>
      {/* Top Clinical Header */}
      <header className="clinical-header">
        <div className="clinical-brand">
          <div className="brand-symbol">NS</div>
          <div>
            <h1 className="brand-text-title">NeuroScan</h1>
            <p className="brand-text-sub">AI-Based Movement Analysis & Motor Biomarker Prototype</p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>CNN Pipeline:</span>
          <span className="risk-tag tag-low" style={{ fontSize: '0.75rem', padding: '0.2rem 0.6rem' }}>
            ● Model Ready (Hybrid Multi-Modal)
          </span>
        </div>
      </header>

      {/* Persistent Regulatory & Medical Disclaimer */}
      <MedicalDisclaimerBanner />

      {/* Main Dashboard Grid */}
      <main className="dashboard-grid-container">
        {/* Synthetic Cohort Picker */}
        <PatientSampleSelector
          samples={samples}
          selectedSampleId={selectedSample?.sample_id}
          onSelectSample={handleSelectSample}
          onSwitchToFreehand={handleSwitchToFreehand}
        />

        <div className="grid-two-col">
          {/* Left Column: Canvas & Extracted Biomarkers */}
          <div>
            <MotorTestCanvas
              points={activePoints}
              onPointsUpdate={setActivePoints}
              isAnalyzing={isAnalyzing}
              onRunAnalysis={handleRunAnalysis}
              activeSampleName={selectedSample ? `${selectedSample.patient_alias} (${selectedSample.test_type})` : null}
            />

            <BiomarkerMetricsCard
              biomarkers={prediction?.biomarkers || selectedSample?.kinematic_biomarkers}
              extractionTimeMs={prediction?.feature_extraction_time_ms}
            />
          </div>

          {/* Right Column: Clinician Risk Stratification Report */}
          <div>
            <RiskAssessmentView
              prediction={prediction}
              isAnalyzing={isAnalyzing}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
