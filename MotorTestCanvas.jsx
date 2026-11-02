import React, { useRef, useEffect, useState } from 'react';

export default function MotorTestCanvas({
  points,
  onPointsUpdate,
  isAnalyzing,
  onRunAnalysis,
  activeSampleName
}) {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentCoords, setCurrentCoords] = useState(points || []);

  useEffect(() => {
    setCurrentCoords(points || []);
  }, [points]);

  // Redraw canvas on coordinates change
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    // Draw background grid lines (medical imaging / oscillogram aesthetic)
    ctx.strokeStyle = '#111827';
    ctx.lineWidth = 1;
    for (let x = 0; x < width; x += 30) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += 30) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }

    if (currentCoords.length < 2) return;

    // Draw coordinate path
    ctx.strokeStyle = '#14b8a6';
    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    ctx.beginPath();
    ctx.moveTo(currentCoords[0][0], currentCoords[0][1]);
    for (let i = 1; i < currentCoords.length; i++) {
      ctx.lineTo(currentCoords[i][0], currentCoords[i][1]);
    }
    ctx.stroke();

    // Highlight starting point
    ctx.fillStyle = '#0d9488';
    ctx.beginPath();
    ctx.arc(currentCoords[0][0], currentCoords[0][1], 5, 0, 2 * Math.PI);
    ctx.fill();

    // Highlight terminal point
    ctx.fillStyle = '#38bdf8';
    ctx.beginPath();
    ctx.arc(currentCoords[currentCoords.length - 1][0], currentCoords[currentCoords.length - 1][1], 5, 0, 2 * Math.PI);
    ctx.fill();
  }, [currentCoords]);

  // Drawing event handlers for freehand mode
  const handleMouseDown = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    setIsDrawing(true);
    const newCoords = [[x, y]];
    setCurrentCoords(newCoords);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing) return;
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const updated = [...currentCoords, [x, y]];
    setCurrentCoords(updated);
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
    onPointsUpdate(currentCoords);
  };

  const handleClear = () => {
    setCurrentCoords([]);
    onPointsUpdate([]);
  };

  return (
    <div className="clinical-card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <div>
          <h3 className="card-heading">Digitized Motor Exercise Canvas</h3>
          <p className="card-subtext" style={{ margin: 0 }}>
            {activeSampleName || 'Interactive Freehand Test (Draw or trace a spiral)'}
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button type="button" className="btn-secondary" onClick={handleClear} style={{ fontSize: '0.75rem' }}>
            Clear Canvas
          </button>
        </div>
      </div>

      {/* Canvas Frame */}
      <div className="canvas-wrapper">
        <canvas
          ref={canvasRef}
          width={500}
          height={340}
          className="drawing-canvas"
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
        />
        {currentCoords.length === 0 && (
          <div style={{ position: 'absolute', pointerEvents: 'none', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            Click & drag to draw a spiral or test stroke
          </div>
        )}
      </div>

      {/* Canvas Footer Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1rem' }}>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          Trace Coordinates: <strong>{currentCoords.length} pts</strong> (Sampled @ 60 Hz)
        </span>

        <button
          type="button"
          className="btn-teal"
          onClick={() => onRunAnalysis(currentCoords)}
          disabled={isAnalyzing || currentCoords.length < 5}
        >
          {isAnalyzing ? 'Extracting Features & Inferring...' : 'Execute CNN Motor Screening 🔬'}
        </button>
      </div>
    </div>
  );
}
