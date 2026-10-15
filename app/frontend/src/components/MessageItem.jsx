import React, { useState, useMemo } from 'react';
import {
  Bot,
  User,
  Sprout,
  Layers,
  Film,
  CheckCircle,
  AlertTriangle,
  Volume2,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  Info,
  Crosshair,
  ShieldCheck,
  AlertOctagon,
  Image as ImageIcon,
  Activity,
  ExternalLink
} from 'lucide-react';

export default function MessageItem({ message, onOpenFramesModal, onInspectTelemetry }) {
  const [showDetectionsList, setShowDetectionsList] = useState(true);
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="message-wrapper user animate-slide-up">
        <div className="message-bubble user-bubble">
          {/* Attached Media Previews */}
          {message.media && (
            <div className="user-media-preview">
              {message.media.type === 'image' && (
                <div className="media-image-frame">
                  <img src={message.media.url} alt="Uploaded crop" className="chat-img-thumb" />
                </div>
              )}
              {message.media.type === 'video' && (
                <div className="media-video-frame">
                  <video src={message.media.url} controls className="chat-video-player" />
                </div>
              )}
              {message.media.type === 'audio' && (
                <div className="media-audio-chip">
                  <Volume2 size={16} color="var(--primary-emerald)" />
                  <audio src={message.media.url} controls className="chat-audio-player" />
                </div>
              )}
            </div>
          )}

          {/* User query text */}
          {message.text && (
            <p className="user-text-content">
              {typeof message.text === 'string' ? message.text : (message.text?.text || message.text?.message || '')}
            </p>
          )}

          <div className="message-timestamp">
            {typeof message.timestamp === 'string' ? message.timestamp : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
        <div className="message-avatar user-avatar">
          <User size={18} />
        </div>
      </div>
    );
  }

  // AI Assistant Message
  const data = message.data || {};
  const model1 = data.model1;
  const videoInference = data.video_inference;
  const model2 = data.model2 || videoInference?.model2 || model1?.model2;
  const routerData = data.router;
  const annotatedPreviewUrl = data.annotated_preview_url || model2?.annotated_preview_url;

  const hasPlantResult = Boolean(model1 || videoInference);
  const rawCrop = videoInference?.predicted_crop || model1?.predicted_crop || model1?.predicted_label;
  const formatCropDisplay = (raw) => {
    if (!raw) return '';
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
  };
  const cropName = formatCropDisplay(rawCrop);
  const cropConfidence = videoInference ? videoInference.confidence : model1?.confidence;
  const cropConfidencePct = typeof cropConfidence === 'number' ? (cropConfidence * 100).toFixed(1) : (typeof cropConfidence === 'string' ? cropConfidence : null);

  const reasonCode = model1?.reason_code || videoInference?.reason_code;
  const cropStatus = model1?.crop_status || videoInference?.crop_status;
  const isValidationRejected = (model1?.validation && model1.validation.valid === false) || model1?.status === 'rejected';
  const isUnsupportedCrop = cropStatus === 'unsupported_crop' || reasonCode === 'unsupported_crop';
  const isUncertainCrop = cropStatus === 'uncertain_crop' || reasonCode === 'uncertain_crop';
  const isSafeguardTriggered = isValidationRejected || isUnsupportedCrop || isUncertainCrop;

  const hasDiseaseModel = Boolean(model2 && model2.status && model2.status !== 'not_applicable' && model2.status !== 'not_connected' && !isSafeguardTriggered);
  const isUncertain = model2?.status === 'uncertain';
  const hasDisease = !isUncertain && Boolean(model2?.has_disease || (model2?.detections && model2.detections.length > 0));
  const rawDiseaseName = model2?.primary_disease || (hasDisease ? 'Disease Detected' : isUncertain ? 'Inconclusive — verify image' : 'No disease detected');
  const diseaseName = typeof rawDiseaseName === 'string'
    ? rawDiseaseName
    : (rawDiseaseName?.name || rawDiseaseName?.label || rawDiseaseName?.disease || (hasDisease ? 'Disease Detected' : isUncertain ? 'Inconclusive — verify image' : 'No disease detected'));
  const diseaseConfidence = model2?.confidence;
  const diseaseConfidencePct = typeof diseaseConfidence === 'number'
    ? (diseaseConfidence * 100).toFixed(1)
    : (typeof model2?.percentage === 'string' || typeof model2?.percentage === 'number' ? String(model2.percentage) : '—');
  const lesionsCount = typeof model2?.detections_count === 'number'
    ? model2.detections_count
    : (Array.isArray(model2?.detections) ? model2.detections.length : 0);

  // Group detections by disease if multiple
  const diseaseGroups = useMemo(() => {
    if (!model2?.detections || !Array.isArray(model2.detections) || model2.detections.length === 0) return [];
    const groups = {};
    model2.detections.forEach((det) => {
      const rawLabel = det.disease_label || det.disease || 'Unknown Disease';
      const label = typeof rawLabel === 'string' ? rawLabel : (rawLabel?.name || rawLabel?.label || 'Unknown Disease');
      if (!groups[label]) {
        groups[label] = {
          name: label,
          count: 0,
          maxConfidence: 0,
        };
      }
      groups[label].count += 1;
      const detConf = typeof det.confidence === 'number' ? det.confidence : 0;
      if (detConf > groups[label].maxConfidence) {
        groups[label].maxConfidence = detConf;
      }
    });
    return Object.values(groups);
  }, [model2]);

  return (
    <div className="message-wrapper assistant animate-slide-up">
      <div className="message-avatar assistant-avatar">
        <Bot size={20} color="var(--primary-emerald)" />
      </div>

      <div className="message-bubble assistant-bubble">
        {/* Header / Router Intent Pill */}
        <div className="assistant-header-row">
          <span className="brand-name-tag">ALEXA FARMS AI</span>
          {routerData && routerData.intent && (
            <span className="intent-badge" title="Query Router Intent">
              Intent: {typeof routerData.intent === 'string' ? routerData.intent : (routerData.intent?.name || 'unknown')}
            </span>
          )}
        </div>

        {/* ========================================================
            SAFEGUARD ALERT / REJECTION CARD or SECTION 1 PLANT ID
            ======================================================== */}
        {isSafeguardTriggered ? (
          <div className={`safeguard-rejection-card ${isUnsupportedCrop ? 'unsupported' : isUncertainCrop ? 'uncertain' : 'rejected'}`}>
            <div className="model-card-header">
              <div className="model-badge-row">
                {isUnsupportedCrop || isUncertainCrop ? (
                  <AlertTriangle size={18} color="#f59e0b" />
                ) : (
                  <AlertOctagon size={18} color="#f43f5e" />
                )}
                <span className="model-title" style={{ color: isUnsupportedCrop || isUncertainCrop ? '#fbbf24' : '#fb7185' }}>
                  {isUnsupportedCrop
                    ? 'UNSUPPORTED CROP'
                    : isUncertainCrop
                    ? 'UNCERTAIN CROP'
                    : reasonCode === 'blurry_image'
                    ? 'BLURRY PHOTO DETECTED'
                    : reasonCode === 'low_visibility'
                    ? 'LOW VISIBILITY / POOR LIGHTING'
                    : reasonCode === 'non_plant_image'
                    ? 'NON-PLANT IMAGE'
                    : reasonCode === 'invalid_file'
                    ? 'INVALID FILE FORMAT'
                    : 'IMAGE VALIDATION REJECTED'}
                </span>
              </div>
              <span className={`safeguard-badge ${isUnsupportedCrop ? 'badge-unsupported' : isUncertainCrop ? 'badge-uncertain' : 'badge-rejected'}`}>
                {isUnsupportedCrop
                  ? 'Unsupported Crop'
                  : isUncertainCrop
                  ? 'Uncertain Crop'
                  : reasonCode === 'non_plant_image'
                  ? 'Non-Plant Image'
                  : reasonCode || cropStatus || 'Rejected'}
              </span>
            </div>

            <div className="safeguard-message-box">
              <p>{model1?.message || model1?.reason || 'Image could not be verified for disease diagnosis.'}</p>
            </div>

            <div className="safeguard-action-row">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                Disease diagnosis is withheld to protect crops from incorrect treatments.
              </span>
              <button
                className="btn-replace-image"
                onClick={() => {
                  const cameraBtn = document.getElementById('composer-camera-btn');
                  if (cameraBtn) cameraBtn.click();
                }}
                title="Upload or capture a new photo"
              >
                <ImageIcon size={14} />
                <span>Replace Image</span>
              </button>
            </div>
          </div>
        ) : hasPlantResult && (
          <div className="model-card model1-card">
            <div className="model-card-header">
              <div className="model-badge-row">
                <Sprout size={16} color="var(--primary-emerald)" />
                <span className="model-title">PLANT IDENTIFICATION</span>
              </div>
              {(model1?.status === 'unavailable' || videoInference?.status === 'unavailable' || model1?.status === 'error' || videoInference?.status === 'error') && (
                <span style={{
                  fontSize: '0.72rem',
                  color: (model1?.status === 'error' || videoInference?.status === 'error') ? '#f43f5e' : '#f59e0b',
                  padding: '2px 6px',
                  background: (model1?.status === 'error' || videoInference?.status === 'error') ? 'rgba(244, 63, 94, 0.1)' : 'rgba(245, 158, 11, 0.1)',
                  borderRadius: '4px'
                }}>
                  {(model1?.status === 'error' || videoInference?.status === 'error') ? 'Inference Error' : 'Checkpoint Missing'}
                </span>
              )}
            </div>

            <div className="model-card-body">
              {(model1?.status === 'unavailable' || videoInference?.status === 'unavailable' || model1?.status === 'error' || videoInference?.status === 'error') ? (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-value" style={{ color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                      {(() => {
                        const plantMsg = videoInference?.message || model1?.message;
                        if (typeof plantMsg === 'string' && plantMsg.trim()) return plantMsg;
                        if (plantMsg && typeof plantMsg === 'object') {
                          return plantMsg.detail || plantMsg.message || plantMsg.reason || 'Vision model checkpoint not mounted on this server instance.';
                        }
                        return 'Vision model checkpoint not mounted on this server instance.';
                      })()}
                    </span>
                  </div>
                </div>
              ) : (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Crop:</span>
                    <span className="result-field-value plant-highlight">{cropName || 'Unknown'}</span>
                  </div>
                  {cropConfidencePct && (
                    <div className="result-field-row">
                      <span className="result-field-label">Confidence:</span>
                      <span className="result-field-value">{cropConfidencePct}%</span>
                    </div>
                  )}
                  {model1?.warning && (
                    <div className="safeguard-warning-callout">
                      <Info size={15} color="#fbbf24" style={{ flexShrink: 0, marginTop: '2px' }} />
                      <span>{model1.warning}</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================
            SECTION 2: 🦠 DISEASE DETECTION (Model 2)
            ======================================================== */}
        {hasDiseaseModel && (
          <div className={`model-card model2-card ${hasDisease ? 'disease-detected' : isUncertain ? 'uncertain' : 'healthy'}`}>
            <div className="model-card-header">
              <div className="model-badge-row">
                <Layers size={16} color={hasDisease ? '#f43f5e' : isUncertain ? '#f59e0b' : 'var(--primary-emerald)'} />
                <span className="model-title">DISEASE DETECTION</span>
              </div>
              {isUncertain && (
                <span style={{
                  fontSize: '0.72rem',
                  color: '#f59e0b',
                  padding: '2px 6px',
                  background: 'rgba(245, 158, 11, 0.1)',
                  borderRadius: '4px',
                  fontWeight: 600
                }}>
                  Inconclusive
                </span>
              )}
            </div>

            <div className="model-card-body">
              {hasDisease ? (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Disease:</span>
                    <span className="result-field-value disease-highlight">{diseaseName}</span>
                  </div>
                  {diseaseConfidencePct && (
                    <div className="result-field-row">
                      <span className="result-field-label">Confidence:</span>
                      <span className="result-field-value">{diseaseConfidencePct}%</span>
                    </div>
                  )}
                </div>
              ) : isUncertain ? (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Disease:</span>
                    <span className="result-field-value" style={{ color: '#f59e0b' }}>Inconclusive — verify image</span>
                  </div>
                  {diseaseConfidencePct && diseaseConfidencePct !== 'N/A' && (
                    <div className="result-field-row">
                      <span className="result-field-label">Confidence:</span>
                      <span className="result-field-value">{diseaseConfidencePct}%</span>
                    </div>
                  )}
                  {model2?.message && (
                    <div className="result-field-row" style={{ marginTop: '4px' }}>
                      <span className="result-field-value" style={{ color: 'var(--text-muted)', fontSize: '0.82rem', fontWeight: 400 }}>
                        {typeof model2.message === 'string' ? model2.message : (model2.message?.message || model2.message?.detail || '')}
                      </span>
                    </div>
                  )}
                </div>
              ) : (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Disease:</span>
                    <span className="result-field-value text-emerald">No disease detected</span>
                  </div>
                  {diseaseConfidencePct && (
                    <div className="result-field-row">
                      <span className="result-field-label">Confidence:</span>
                      <span className="result-field-value">{diseaseConfidencePct}%</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ========================================================
            SECTION 3: 🌿 ANALYZED IMAGE (Clean Original Image)
            ======================================================== */}
        {data.original_image_url && (
          <div className="model-card analyzed-image-card">
            <div className="model-card-header">
              <div className="model-badge-row">
                <ImageIcon size={16} color="var(--primary-emerald)" />
                <span className="model-title">ANALYZED IMAGE</span>
              </div>
            </div>

            <div className="model-card-body">
              <div className="clean-analyzed-image-frame">
                <img
                  src={data.original_image_url}
                  alt="Analyzed Plant Specimen"
                  className="clean-analyzed-img"
                />
              </div>
            </div>
          </div>
        )}

        {/* ========================================================
            SECTION 4: VIDEO FRAMES MODAL TRIGGER (If Video)
            ======================================================== */}
        {videoInference && !['unavailable', 'error'].includes(videoInference.status) && (videoInference.frames_processed > 0) && (
          <div className="video-actions-container">
            <button
              className="btn-extracted-frames"
              onClick={() => onOpenFramesModal(videoInference)}
              id="btn-show-extracted-frames"
            >
              <Film size={15} />
              <span>Show All Extracted Frames ({videoInference.frames_processed})</span>
              <ChevronRight size={15} />
            </button>
          </div>
        )}

        {/* Grounded Agricultural Assistant Guidance & Explanation */}
        {message.text && (
          <div className="assistant-guidance-container">
            <div className="assistant-text-body">
              {String(typeof message.text === 'string' ? message.text : (message.text?.text || message.text?.message || message.text?.detail || ''))
                .split('\n\n')
                .map((paragraph, idx) => (
                  <p key={idx} className="assistant-paragraph">{paragraph}</p>
                ))}
            </div>
            {Array.isArray(data.knowledge_sources) && data.knowledge_sources.length > 0 && (
              <div className="knowledge-sources-row">
                <span className="sources-label">Sources:</span>
                {data.knowledge_sources.map((src, idx) => {
                  if (!src) return null;
                  if (typeof src === 'string') {
                    return (
                      <span key={idx} className="source-citation-badge">{src}</span>
                    );
                  }
                  if (typeof src === 'object') {
                    const titleText = src.title || src.name || src.organization || src.source_id || 'Reference Source';
                    const orgText = src.organization && !src.title?.includes(src.organization) ? ` (${src.organization})` : '';
                    const isGeneral = Boolean(src.is_general);
                    const label = isGeneral ? `[General] ${titleText}${orgText}` : `${titleText}${orgText}`;
                    const targetUrl = src.url || src.url_or_doi;
                    if (targetUrl) {
                      return (
                        <a
                          key={idx}
                          href={targetUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="source-citation-badge source-citation-link"
                          title={`Open verified article: ${label}`}
                        >
                          <span>{label}</span>
                          <ExternalLink size={10} style={{ opacity: 0.85, flexShrink: 0 }} />
                        </a>
                      );
                    }
                    return (
                      <span key={idx} className="source-citation-badge" title={label}>
                        {label}
                      </span>
                    );
                  }
                  return (
                    <span key={idx} className="source-citation-badge">
                      {String(src)}
                    </span>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Footer info & Telemetry Inspector trigger */}
        <div className="assistant-card-footer">
          <button
            className="btn-inspect-telemetry"
            onClick={() => onInspectTelemetry(data)}
            title="Inspect unified debug telemetry"
          >
            <Info size={13} />
            <span>Inspect Debug State</span>
          </button>
          <span className="response-time-tag">
            {typeof message.timestamp === 'string' ? message.timestamp : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
    </div>
  );
}
