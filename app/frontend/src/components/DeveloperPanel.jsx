import React, { useState } from 'react';
import { X, Check, Code, Cpu, Compass, BookOpen, Layers } from 'lucide-react';

export default function DeveloperPanel({ isOpen, onClose, telemetryData }) {
  const [activeTab, setActiveTab] = useState('summary'); // 'summary' | 'json'

  if (!isOpen) return null;

  const data = telemetryData || {
    input_types: { text: false, audio: false, image: false, video: false },
    language: 'None detected',
    original_text: 'None',
    normalized_text: 'None',
    intent: 'None',
    routing_metadata: {
      needs_model1: false,
      needs_model2: false,
      needs_rag: false,
    }
  };

  const inputs = data.input_types || {};
  const meta = data.routing_metadata || {};

  return (
    <div className="debug-drawer animate-fade-in" id="developer-debug-panel">
      <div className="debug-drawer-header">
        <div className="debug-header-title">
          <Code size={18} color="var(--primary-emerald)" />
          <h3>Developer / Input Debug Telemetry</h3>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button 
            className="btn-link"
            style={{ fontSize: '0.8rem', color: activeTab === 'summary' ? 'var(--primary-emerald)' : 'var(--text-muted)' }}
            onClick={() => setActiveTab('summary')}
          >
            Summary
          </button>
          <span style={{ color: 'var(--border-subtle)' }}>|</span>
          <button 
            className="btn-link"
            style={{ fontSize: '0.8rem', color: activeTab === 'json' ? 'var(--primary-emerald)' : 'var(--text-muted)' }}
            onClick={() => setActiveTab('json')}
          >
            Raw JSON
          </button>
          <button 
            className="btn-icon" 
            onClick={onClose} 
            title="Close Panel"
            style={{ width: '28px', height: '28px', marginLeft: '8px' }}
          >
            <X size={16} />
          </button>
        </div>
      </div>

      <div className="debug-drawer-body">
        {activeTab === 'summary' ? (
          <>
            {/* Input Types Row */}
            <div className="debug-section">
              <h4>Active Input Modalities</h4>
              <div className="debug-badges-row">
                <span className={`debug-check-item ${inputs.text ? 'active' : ''}`}>
                  {inputs.text ? <Check size={14} /> : <X size={14} />} Text
                </span>
                <span className={`debug-check-item ${inputs.audio ? 'active' : ''}`}>
                  {inputs.audio ? <Check size={14} /> : <X size={14} />} Audio
                </span>
                <span className={`debug-check-item ${inputs.image ? 'active' : ''}`}>
                  {inputs.image ? <Check size={14} /> : <X size={14} />} Image
                </span>
                <span className={`debug-check-item ${inputs.video ? 'active' : ''}`}>
                  {inputs.video ? <Check size={14} /> : <X size={14} />} Video
                </span>
              </div>
            </div>

            {/* Language & Transcriptions */}
            <div className="debug-section">
              <h4>Language & Text Normalization</h4>
              <div className="debug-grid-2">
                <div className="debug-item">
                  <span className="debug-label">Detected Language</span>
                  <span className="debug-value text-emerald">
                    {data.language ? data.language.toUpperCase() : 'N/A'}
                  </span>
                </div>
                <div className="debug-item">
                  <span className="debug-label">Router Intent</span>
                  <span className="debug-value text-accent">
                    {data.intent || 'pending'}
                  </span>
                </div>
              </div>
              <div className="debug-item mt-2">
                <span className="debug-label">Original Transcription / Input</span>
                <p className="debug-text-box">
                  {data.original_text || '—'}
                </p>
              </div>
              <div className="debug-item mt-2">
                <span className="debug-label">Normalized Query</span>
                <p className="debug-text-box">
                  {data.normalized_text || '—'}
                </p>
              </div>
            </div>

            {/* Pipeline Flags */}
            <div className="debug-section">
              <h4>Pipeline Routing Requirements</h4>
              <div className="debug-flags-list">
                <div className="debug-flag-row">
                  <div className="flag-info">
                    <Cpu size={15} />
                    <span>Needs Model 1 (Plant Identification)</span>
                  </div>
                  <span className={`flag-status ${meta.needs_model1 ? 'yes' : 'no'}`}>
                    {meta.needs_model1 ? 'YES' : 'NO'}
                  </span>
                </div>

                <div className="debug-flag-row">
                  <div className="flag-info">
                    <Layers size={15} />
                    <span>Needs Model 2 (Disease Detection)</span>
                  </div>
                  <span className={`flag-status ${meta.needs_model2 ? 'yes' : 'no'}`}>
                    {meta.needs_model2 ? 'YES' : 'NO'}
                  </span>
                </div>

                <div className="debug-flag-row">
                  <div className="flag-info">
                    <BookOpen size={15} />
                    <span>Needs RAG (Treatment / Info)</span>
                  </div>
                  <span className={`flag-status ${meta.needs_rag ? 'yes' : 'no'}`}>
                    {meta.needs_rag ? 'YES' : 'NO'}
                  </span>
                </div>
              </div>
            </div>

            {/* Model 1 & 2 Raw Diagnostics */}
            {(data.model1 || data.model2 || data.video_inference) && (
              <div className="debug-section">
                <h4>Model Raw Diagnostics</h4>
                {data.model1 && (
                  <div className="debug-item mt-2">
                    <span className="debug-label">Model 1 Plant Identification</span>
                    <span className="debug-value text-emerald">
                      {data.model1.predicted_crop || data.model1.predicted_label || 'Unknown'} ({(data.model1.confidence * 100).toFixed(1)}%)
                    </span>
                  </div>
                )}
                {data.model2 && (
                  <div className="debug-item mt-2">
                    <span className="debug-label">Model 2 Disease Localization</span>
                    <span className="debug-value text-rose">
                      {data.model2.primary_disease || 'None'} ({data.model2.percentage || 'N/A'}, {data.model2.detections_count || data.model2.detections?.length || 0} lesions)
                    </span>

                    {/* Annotated preview in debug panel */}
                    {(data.annotated_preview_url || data.model2.annotated_preview_url) && (
                      <div style={{ marginTop: '10px', borderRadius: '6px', overflow: 'hidden', border: '1px solid var(--border-subtle)' }}>
                        <div style={{ padding: '4px 8px', fontSize: '0.72rem', background: 'rgba(244, 63, 94, 0.15)', color: '#fda4af', fontWeight: 600 }}>
                          Annotated Disease Localization Bounding Boxes
                        </div>
                        <img 
                          src={data.annotated_preview_url || data.model2.annotated_preview_url} 
                          alt="Annotated preview" 
                          style={{ width: '100%', maxHeight: '200px', objectFit: 'contain', background: '#000', display: 'block' }} 
                        />
                      </div>
                    )}

                    {/* Detections list in debug panel */}
                    {data.model2.detections && data.model2.detections.length > 0 && (
                      <div style={{ marginTop: '8px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                        <strong>Detections ({data.model2.detections.length}):</strong>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '3px', marginTop: '4px' }}>
                          {data.model2.detections.slice(0, 10).map((det, i) => (
                            <div key={i} style={{ background: '#0b1220', padding: '3px 6px', borderRadius: '3px' }}>
                              #{i+1} {det.disease_label || det.disease} ({det.percentage || `${(det.confidence*100).toFixed(1)}%`}) {det.bbox && `[${det.bbox.map(v => typeof v === 'number' ? v.toFixed(0) : v).join(', ')}]`}
                            </div>
                          ))}
                          {data.model2.detections.length > 10 && (
                            <div style={{ fontStyle: 'italic' }}>+ {data.model2.detections.length - 10} more detections</div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="debug-json-container">
            <pre>{JSON.stringify(data, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
