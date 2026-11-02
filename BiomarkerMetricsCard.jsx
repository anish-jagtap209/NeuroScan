import React from 'react';

export default function BiomarkerMetricsCard({ biomarkers, extractionTimeMs }) {
  if (!biomarkers) {
    return (
      <div className="clinical-card" style={{ marginTop: '1.5rem', textAlign: 'center', padding: '2rem' }}>
        <p style={{ color: 'var(--text-muted)' }}>Run analysis to extract kinematic motor biomarkers.</p>
      </div>
    );
  }

  const {
    dominant_tremor_freq_hz = 0,
    velocity_variance = 0,
    pressure_stability_ratio = 0,
    trajectory_entropy = 0,
    drawing_duration_sec = 0
  } = biomarkers;

  const isTremorElevated = dominant_tremor_freq_hz >= 3.8 && dominant_tremor_freq_hz <= 7.2;

  return (
    <div className="clinical-card" style={{ marginTop: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 className="card-heading">Extracted Kinematic Biomarkers</h3>
          <p className="card-subtext" style={{ margin: 0 }}>
            Algorithmic frequency decomposition and spatial entropy telemetry
          </p>
        </div>
        {extractionTimeMs !== undefined && (
          <span style={{ fontSize: '0.75rem', color: 'var(--teal-light)', background: 'rgba(20, 184, 166, 0.1)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
            ⚡ Feature Extraction: {extractionTimeMs} ms
          </span>
        )}
      </div>

      <div className="telemetry-grid">
        {/* Tremor Frequency */}
        <div className="telemetry-tile">
          <span className="telemetry-label">Dominant Tremor Frequency</span>
          <div className="telemetry-val" style={{ color: isTremorElevated ? 'var(--risk-high)' : 'var(--teal-light)' }}>
            {dominant_tremor_freq_hz} <span style={{ fontSize: '0.85rem' }}>Hz</span>
          </div>
          <span style={{ fontSize: '0.7rem', color: isTremorElevated ? 'var(--risk-high)' : 'var(--text-muted)' }}>
            {isTremorElevated ? '⚠️ Matches 4–7 Hz Parkinsonian band' : '✓ Normal physiological band (< 2 Hz)'}
          </span>
        </div>

        {/* Velocity Variance */}
        <div className="telemetry-tile">
          <span className="telemetry-label">Velocity Variance</span>
          <div className="telemetry-val">
            {velocity_variance} <span style={{ fontSize: '0.85rem' }}>px/s²</span>
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            Measures fine-motor smoothness and micro-hesitations
          </span>
        </div>

        {/* Pressure Stability */}
        <div className="telemetry-tile">
          <span className="telemetry-label">Pressure Stability Ratio</span>
          <div className="telemetry-val">
            {(pressure_stability_ratio * 100).toFixed(0)} <span style={{ fontSize: '0.85rem' }}>%</span>
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            Stylus contact pressure consistency
          </span>
        </div>

        {/* Trajectory Entropy */}
        <div className="telemetry-tile">
          <span className="telemetry-label">Trajectory Curvature Entropy</span>
          <div className="telemetry-val">
            {trajectory_entropy}
          </div>
          <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
            Geometric jitter and radial deviation (0.0 to 1.0)
          </span>
        </div>
      </div>
    </div>
  );
}
