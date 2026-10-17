import React, { useState } from 'react';
import { X, Film, CheckCircle2, AlertCircle, ShieldAlert, Scan, Eye, Crosshair, AlertOctagon } from 'lucide-react';

function formatCropDisplay(raw) {
  if (!raw) return 'Unknown';
  const str = typeof raw === 'string' ? raw : (raw?.name || raw?.label || raw?.crop || String(raw));
  const clean = str.trim().toLowerCase();
  if (clean === 'capsicum' || clean === 'bellpepper' || clean === 'bell_pepper') {
    return 'Bell Pepper';
  }
  if (clean === 'french_bean' || clean === 'bean') {
    return 'French Bean';
  }
  if (clean === 'cherry_tomato') {
    return 'Cherry Tomato';
  }
  return clean.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function ExtractedFramesModal({ isOpen, onClose, videoData }) {
  const [viewMode, setViewMode] = useState('roi'); // 'roi', 'annotated', or 'full'

  if (!isOpen || !videoData) return null;

  const frames = videoData.frame_results || videoData.frame_records || [];
  const validFrames = frames.filter(f => f.quality_status === 'valid' || f.status === 'valid' || f.quality_status === 'valid_plant_roi' || f.status === 'valid_plant_roi').length;
  const diseaseFrames = frames.filter(f => (f.disease_detections && f.disease_detections.length > 0) || f.disease_status === 'diseased').length;
  const m2Summary = videoData.model2 || {};

  const totalDecoded = videoData.total_decoded_frames || videoData.video_metadata?.frame_count || frames.length;
  const sampledCount = videoData.sampled_frames_count || frames.length;
  const rejectedCount = videoData.rejected_frames_count ?? (frames.length - validFrames);
  const m1Count = videoData.model1_inference_count ?? frames.length;
  const m2Count = videoData.model2_inference_count ?? (m2Summary.status && m2Summary.status !== 'not_applicable' && m2Summary.status !== 'not_run' ? validFrames : 0);
  const durationSec = videoData.video_duration_sec || videoData.video_metadata?.duration_seconds || 0;
  const fps = videoData.fps || videoData.video_metadata?.fps || 30.0;

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
                Decoded: {totalDecoded} • Sampled: {sampledCount} • Valid Plant: {validFrames} • Rejected: {rejectedCount} • Diseased: {diseaseFrames}
              </p>
              <p className="modal-subtitle" style={{ fontSize: '0.75rem', marginTop: '2px', color: 'var(--text-dim)' }}>
                Duration: {durationSec.toFixed(1)}s ({fps.toFixed(1)} fps) • M1 Runs: {m1Count} • M2 Runs: {m2Count} • Video: {videoData.video_name || 'Uploaded Video'}
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
              const isValid = frame.quality_status === 'valid' || frame.status === 'valid' || frame.quality_status === 'valid_plant_roi' || frame.status === 'valid_plant_roi';
              const isBlurry = frame.quality_status === 'blurry' || frame.status === 'blurry' || frame.quality_status === 'low_quality' || frame.status === 'low_quality';
              const isCropUncertain = frame.quality_status === 'crop_uncertain' || frame.status === 'crop_uncertain';
              const isNoPlant = !isCropUncertain && (frame.quality_status === 'unknown' || frame.status === 'unknown' || frame.quality_status === 'no_plant' || frame.quality_status === 'no_plant_evidence' || frame.status === 'no_plant_evidence');
              const hasDiseaseDets = (frame.disease_detections && frame.disease_detections.length > 0) || frame.disease_status === 'diseased';

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
                        {formatCropDisplay(frame.predicted_crop || frame.predicted_label)}
                      </span>
                      <span className={`frame-conf-pill ${isValid ? 'high' : 'low'}`}>
                        {((frame.confidence || 0) * 100).toFixed(1)}%
                      </span>
                    </div>

                    {/* Frame-level Model 2 Disease tag */}
                    {hasDiseaseDets && (
                      <div className="frame-disease-tag-row">
                        <span className="frame-disease-chip">
                          <AlertOctagon size={11} /> {typeof (frame.disease_label || frame.disease) === 'string' ? (frame.disease_label || frame.disease) : (frame.disease_detections?.[0]?.disease_label || 'Disease')} ({frame.disease_detections?.[0]?.percentage || `${((frame.disease_confidence || 0) * 100).toFixed(0)}%`})
                        </span>
                      </div>
                    )}

                    <div className="frame-status-tag">
                      {isValid && (
                        <span className="tag-status valid">
                          <CheckCircle2 size={12} /> Valid Plant
                        </span>
                      )}
                      {isCropUncertain && (
                        <span className="tag-status uncertain" style={{ color: '#f59e0b', background: 'rgba(245, 158, 11, 0.1)' }}>
                          <AlertCircle size={12} /> Crop Uncertain
                        </span>
                      )}
                      {isBlurry && (
                        <span className="tag-status blurry">
                          <AlertCircle size={12} /> Low Quality
                        </span>
                      )}
                      {isNoPlant && (
                        <span className="tag-status no-plant">
                          <ShieldAlert size={12} /> Low Conf / No Plant
                        </span>
                      )}
                      {isValid && frame.disease_status === 'healthy' && (
                        <span className="tag-status healthy" style={{ color: 'var(--primary-emerald)', background: 'rgba(16, 185, 129, 0.1)', marginLeft: '4px' }}>
                          <CheckCircle2 size={11} /> Healthy
                        </span>
                      )}
                      {isValid && (frame.disease_status === 'not_run' || frame.disease_status === 'not_applicable') && (
                        <span className="tag-status not-run" style={{ color: 'var(--text-dim)', background: 'rgba(255, 255, 255, 0.05)', marginLeft: '4px' }}>
                          M2 Skipped
                        </span>
                      )}
                      {isValid && frame.disease_status === 'uncertain' && !hasDiseaseDets && (
                        <span className="tag-status uncertain" style={{ color: '#f59e0b', background: 'rgba(245, 158, 11, 0.1)', marginLeft: '4px' }}>
                          <AlertCircle size={11} /> Inconclusive
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
                        {typeof (frame.filter_reason || frame.reason) === 'string' ? (frame.filter_reason || frame.reason) : ''}
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
            Plant: <strong className="text-emerald">{typeof (videoData.predicted_crop || videoData.predicted_label) === 'string' ? (videoData.predicted_crop || videoData.predicted_label) : 'Unknown'}</strong> ({((videoData.confidence || 0) * 100).toFixed(1)}%) •{' '}
            Disease:{' '}
            {(() => {
              if (m2Summary.status === 'not_applicable' || m2Summary.status === 'not_run') {
                return <strong style={{ color: '#f59e0b' }}>Disease analysis withheld / skipped ({m2Summary.message ? 'crop unverified' : 'not run'})</strong>;
              }
              if (m2Summary.status === 'uncertain') {
                return <strong style={{ color: '#f59e0b' }}>Inconclusive / Uncertain condition</strong>;
              }
              if (m2Summary.has_disease) {
                return <strong className="text-rose">{typeof m2Summary.primary_disease === 'string' ? m2Summary.primary_disease : 'Disease Detected'} ({typeof m2Summary.percentage === 'string' ? m2Summary.percentage : `${((m2Summary.confidence || 0) * 100).toFixed(1)}%`})</strong>;
              }
              if (m2Summary.status === 'healthy') {
                return <strong className="text-emerald">{typeof m2Summary.primary_disease === 'string' ? m2Summary.primary_disease : 'Healthy Foliage'} ({typeof m2Summary.percentage === 'string' ? m2Summary.percentage : '100%'})</strong>;
              }
              return <strong style={{ color: 'var(--text-muted)' }}>Not analyzed</strong>;
            })()} across {frames.length} sampled frames.
          </div>
          <button className="btn-secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
