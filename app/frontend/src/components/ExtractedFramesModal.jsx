import React, { useState } from 'react';
import { X, Film, CheckCircle2, AlertCircle, ShieldAlert, Scan, Eye, Crosshair, AlertOctagon } from 'lucide-react';

export default function ExtractedFramesModal({ isOpen, onClose, videoData }) {
  const [viewMode, setViewMode] = useState('roi'); // 'roi', 'annotated', or 'full'

  if (!isOpen || !videoData) return null;

  const frames = videoData.frame_results || videoData.frame_records || [];
  const validFrames = frames.filter(f => f.quality_status === 'valid' || f.status === 'valid').length;
  const diseaseFrames = frames.filter(f => f.disease_detections && f.disease_detections.length > 0).length;
  const m2Summary = videoData.model2 || {};

  return (
    <div className="modal-overlay animate-fade-in" onClick={onClose}>
      <div 
        className="modal-content frames-modal" 
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <div className="modal-title">
            <Film size={20} color="var(--primary-emerald)" />
            <div>
              <h3>Extracted Video Inference Frames</h3>
              <p className="modal-subtitle">
                Total Frames: {frames.length} • Valid Plant Frames: {validFrames} • Diseased Frames: {diseaseFrames} • Video: {videoData.video_name || 'Uploaded Video'}
              </p>
            </div>
          </div>
          
          <div className="modal-header-actions">
            <div className="view-toggle-pills">
              <button 
                className={`view-pill ${viewMode === 'roi' ? 'active' : ''}`}
                onClick={() => setViewMode('roi')}
                title="Show Plant ROI used for Model 1 & 2 Inference"
              >
                <Scan size={14} /> Plant ROI
              </button>
              <button 
                className={`view-pill ${viewMode === 'annotated' ? 'active' : ''}`}
                onClick={() => setViewMode('annotated')}
                title="Show Model 2 Disease Bounding Boxes on ROI"
              >
                <Crosshair size={14} /> Disease BBoxes
              </button>
              <button 
                className={`view-pill ${viewMode === 'full' ? 'active' : ''}`}
                onClick={() => setViewMode('full')}
                title="Show Full Video Frame"
              >
                <Eye size={14} /> Full Frame
              </button>
            </div>

            <button className="btn-icon" onClick={onClose} title="Close Frames View">
              <X size={18} />
            </button>
          </div>
        </div>

        <div className="frames-grid-scroll">
          <div className="frames-grid">
            {frames.map((frame, idx) => {
              const isValid = frame.quality_status === 'valid' || frame.status === 'valid';
              const isBlurry = frame.quality_status === 'blurry' || frame.status === 'blurry';
              const isNoPlant = frame.quality_status === 'unknown' || frame.status === 'unknown' || frame.quality_status === 'no_plant';
              const hasDiseaseDets = frame.disease_detections && frame.disease_detections.length > 0;
              
              let displayImg = frame.thumbnail || frame.thumbnail_url;
              if (viewMode === 'roi') {
                displayImg = frame.roi_thumbnail || frame.roi_thumbnail_url || displayImg;
              } else if (viewMode === 'annotated') {
                displayImg = frame.roi_annotated_thumbnail_url || frame.roi_thumbnail_url || displayImg;
              }

              const hasRoi = Boolean(frame.roi_thumbnail || frame.roi_thumbnail_url);

              return (
                <div key={idx} className={`frame-card ${isValid ? 'valid' : 'invalid'} ${hasDiseaseDets ? 'has-lesions' : ''}`}>
                  <div className="frame-img-container">
                    {displayImg ? (
                      <img src={displayImg} alt={`Frame ${frame.frame_idx}`} loading="lazy" />
                    ) : (
                      <div className="frame-placeholder">No Preview</div>
                    )}

                    <div className="frame-idx-badge">
                      #{frame.frame_idx ?? frame.frame_number ?? idx + 1} • {(frame.timestamp_sec ?? frame.timestamp_seconds ?? 0).toFixed(2)}s
                    </div>

                    {hasRoi && (
                      <div className="frame-roi-badge" title="Plant candidate region localized">
                        {viewMode === 'annotated' ? 'Model 2 BBox' : viewMode === 'roi' ? 'Model 1 ROI' : 'Foliage Localized'}
                      </div>
                    )}
                  </div>

                  <div className="frame-info">
                    <div className="frame-prediction-row">
                      <span className="frame-plant-name">
                        {frame.predicted_crop || frame.predicted_label || 'Unknown'}
                      </span>
                      <span className={`frame-conf-pill ${isValid ? 'high' : 'low'}`}>
                        {((frame.confidence || 0) * 100).toFixed(1)}%
                      </span>
                    </div>

                    {/* Frame-level Model 2 Disease tag if detected in annotated debug view mode */}
                    {hasDiseaseDets && viewMode === 'annotated' && (
                      <div className="frame-disease-tag-row">
                        <span className="frame-disease-chip">
                          <AlertOctagon size={11} /> {frame.disease_detections[0]?.disease_label || frame.disease_detections[0]?.disease} ({frame.disease_detections[0]?.percentage || `${(frame.disease_detections[0]?.confidence * 100).toFixed(0)}%`})
                        </span>
                      </div>
                    )}

                    <div className="frame-status-tag">
                      {isValid && (
                        <span className="tag-status valid">
                          <CheckCircle2 size={12} /> Valid Plant
                        </span>
                      )}
                      {isBlurry && (
                        <span className="tag-status blurry">
                          <AlertCircle size={12} /> Blurry
                        </span>
                      )}
                      {isNoPlant && (
                        <span className="tag-status no-plant">
                          <ShieldAlert size={12} /> Low Conf / No Plant
                        </span>
                      )}
                    </div>

                    {frame.roi_box && (
                      <div className="frame-roi-coords">
                        Box: [{frame.roi_box.join(', ')}]
                      </div>
                    )}

                    {(frame.filter_reason || frame.reason) && (
                      <span className="frame-filter-reason">
                        {frame.filter_reason || frame.reason}
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="modal-footer">
          <div className="modal-summary-text">
            Plant: <strong className="text-emerald">{videoData.predicted_crop || videoData.predicted_label || 'Unknown'}</strong> ({((videoData.confidence || 0) * 100).toFixed(1)}%) • 
            Disease: <strong className={m2Summary.has_disease ? 'text-rose' : 'text-emerald'}>{m2Summary.primary_disease || 'Healthy Specimen'}</strong> ({m2Summary.percentage || '100%'}) across {frames.length} frames.
          </div>
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
