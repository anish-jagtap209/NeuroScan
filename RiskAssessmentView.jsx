import React from 'react';

export default function RiskAssessmentView({ prediction, isAnalyzing }) {
  if (isAnalyzing) {
    return (
      <div className="clinical-card" style={{ textAlign: 'center', padding: '3.5rem' }}>
        <div style={{ fontSize: '1.25rem', color: 'var(--teal-light)', marginBottom: '0.5rem' }}>
          Running Convolutional Neural Network...
        </div>
        <p style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
          Processing 64x64 spatial raster & fusing with kinematic dense embeddings
        </p>
      </div>
    );
  }

  if (!prediction) {
    return (
      <div className="clinical-card" style={{ textAlign: 'center', padding: '3.5rem' }}>
        <h3 className="card-heading" style={{ color: 'var(--text-muted)' }}>No Active Screening Results</h3>
        <p className="card-subtext" style={{ marginTop: '0.5rem' }}>
          Select a patient sample or draw a trajectory on the left, then click <strong>"Execute CNN Motor Screening"</strong>.
        </p>
      </div>
    );
  }

  const {
    risk_level = 'Low Risk',
    anomaly_probability = 0,
    confidence_interval = [0, 0],
    attention_heatmap_matrix = [],
    model_inference_time_ms = 0,
    clinical_interpretations = [],
    educational_disclaimer = ''
  } = prediction;

  const getRiskClass = (level) => {
    if (level.includes('Low')) return 'tag-low';
    if (level.includes('Moderate')) return 'tag-med';
    return 'tag-high';
  };

  const getRiskColor = (prob) => {
    if (prob < 35) return 'var(--risk-low)';
    if (prob < 68) return 'var(--risk-med)';
    return 'var(--risk-high)';
  };

  return (
    <div className="clinical-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div>
          <h3 className="card-heading">Clinician Screening Assessment</h3>
          <p className="card-subtext" style={{ margin: 0 }}>
            CNN Multi-modal Anomaly Probability Index
          </p>
        </div>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Inference: {model_inference_time_ms} ms
        </span>
      </div>

      {/* Main Risk Stratification Banner */}
      <div
        style={{
          background: '#0a0e17',
          border: '1px solid var(--border-clinical)',
          borderRadius: 'var(--radius-md)',
          padding: '1.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem'
        }}
      >
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Risk Stratification Tier
          </span>
          <div style={{ marginTop: '0.35rem' }}>
            <span className={`risk-tag ${getRiskClass(risk_level)}`}>
              ● {risk_level}
            </span>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
            Model Confidence Interval: <strong>{confidence_interval[0]}% – {confidence_interval[1]}%</strong>
          </p>
        </div>

        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Anomaly Probability</span>
          <div style={{ fontSize: '2.5rem', fontWeight: 800, color: getRiskColor(anomaly_probability), lineHeight: 1.1 }}>
            {anomaly_probability}%
          </div>
        </div>
      </div>

      {/* Spatial CNN Attention Heatmap (Grad-CAM Visualization) */}
      <div style={{ marginTop: '1.5rem', background: '#0a0e17', border: '1px solid var(--border-clinical)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
          <div>
            <h4 style={{ fontSize: '0.875rem', fontWeight: 700 }}>
              Spatial CNN Attention Heatmap (8x8)
            </h4>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Localizes spatial regions where convolutional kernels detected trajectory anomalies
            </p>
          </div>

          {attention_heatmap_matrix && attention_heatmap_matrix.length > 0 && (
            <div className="heatmap-grid">
              {attention_heatmap_matrix.flatMap((row, rIdx) =>
                row.map((val, cIdx) => {
                  const intensity = Math.min(1.0, val * 1.5);
                  const color =
                    intensity > 0.6
                      ? `rgba(239, 68, 68, ${intensity})`
                      : intensity > 0.2
                      ? `rgba(20, 184, 166, ${intensity})`
                      : 'rgba(30, 41, 59, 0.4)';
                  return <div key={`${rIdx}-${cIdx}`} className="heatmap-cell" style={{ backgroundColor: color }} />;
                })
              )}
            </div>
          )}
        </div>
      </div>

      {/* Clinical Interpretation Notes */}
      <div style={{ marginTop: '1.25rem', background: '#0a0e17', border: '1px solid var(--border-clinical)', borderRadius: 'var(--radius-md)', padding: '1.25rem' }}>
        <h4 style={{ fontSize: '0.875rem', fontWeight: 700, marginBottom: '0.75rem' }}>
          Clinical Pattern Interpretations
        </h4>
        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
          {clinical_interpretations.map((note, idx) => (
            <li key={idx} style={{ fontSize: '0.8125rem', color: '#cbd5e1', display: 'flex', gap: '0.5rem' }}>
              <span style={{ color: 'var(--teal-light)' }}>›</span>
              <span>{note}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Persistent Medical Disclaimer Box */}
      <div
        style={{
          marginTop: '1.25rem',
          padding: '0.75rem',
          borderRadius: 'var(--radius-sm)',
          background: 'rgba(245, 158, 11, 0.08)',
          border: '1px solid rgba(245, 158, 11, 0.25)',
          fontSize: '0.7rem',
          color: '#fbbf24',
          lineHeight: 1.4
        }}
      >
        <strong>NOTICE:</strong> {educational_disclaimer}
      </div>
    </div>
  );
}
