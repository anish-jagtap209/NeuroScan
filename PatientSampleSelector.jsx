import React from 'react';

export default function PatientSampleSelector({
  samples,
  selectedSampleId,
  onSelectSample,
  onSwitchToFreehand
}) {
  return (
    <div style={{ marginBottom: '1.25rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem' }}>
        <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
          Select Patient Motor Test Case (Synthetic Cohort)
        </span>
        <button
          type="button"
          className="btn-secondary"
          style={{ fontSize: '0.75rem', padding: '0.25rem 0.6rem' }}
          onClick={onSwitchToFreehand}
        >
          ✏️ Draw Freehand Spiral / Wave
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.75rem' }}>
        {samples.map((s) => {
          const isSelected = selectedSampleId === s.sample_id;
          const isControl = s.ground_truth_label === 0;

          return (
            <div
              key={s.sample_id}
              onClick={() => onSelectSample(s)}
              style={{
                background: isSelected ? '#162238' : '#0a0e17',
                border: `1px solid ${isSelected ? 'var(--teal-light)' : 'var(--border-clinical)'}`,
                borderRadius: 'var(--radius-sm)',
                padding: '0.75rem',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ fontSize: '0.85rem', color: isSelected ? '#fff' : 'var(--text-primary)' }}>
                  {s.sample_id}
                </strong>
                <span
                  style={{
                    fontSize: '0.65rem',
                    padding: '0.15rem 0.4rem',
                    borderRadius: '4px',
                    background: isControl ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
                    color: isControl ? 'var(--risk-low)' : 'var(--risk-high)'
                  }}
                >
                  {isControl ? 'Control' : 'Anomaly'}
                </span>
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                {s.patient_alias} ({s.age}y / {s.gender})
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
