import React from 'react';

export default function MedicalDisclaimerBanner() {
  return (
    <div className="disclaimer-banner">
      <span style={{ fontSize: '1.1rem' }}>⚠️</span>
      <div>
        <strong>EDUCATIONAL & RESEARCH PROTOTYPE ONLY:</strong> NeuroScan is designed for educational exploration
        of convolutional neural networks and kinematic feature extraction in movement anomalies.
        It is <strong>not</strong> cleared by the FDA or CE as a medical device and is <strong>not</strong> intended
        for clinical diagnosis, prognosis, or medical treatment decisions.
      </div>
    </div>
  );
}
