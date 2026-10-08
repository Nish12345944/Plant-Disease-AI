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
  Activity
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
          {message.text && <p className="user-text-content">{message.text}</p>}

          <div className="message-timestamp">
            {message.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
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
  const cropName = videoInference?.predicted_crop || model1?.predicted_crop || model1?.predicted_label;
  const cropConfidence = videoInference ? videoInference.confidence : model1?.confidence;
  const cropConfidencePct = typeof cropConfidence === 'number' ? (cropConfidence * 100).toFixed(1) : null;

  const hasDiseaseModel = Boolean(model2 && model2.status && model2.status !== 'not_applicable' && model2.status !== 'not_connected');
  const hasDisease = model2?.has_disease || (model2?.detections && model2.detections.length > 0);
  const diseaseName = model2?.primary_disease || (hasDisease ? 'Disease Detected' : 'No disease detected');
  const diseaseConfidence = model2?.confidence;
  const diseaseConfidencePct = typeof diseaseConfidence === 'number' ? (diseaseConfidence * 100).toFixed(1) : (model2?.percentage || '—');
  const lesionsCount = model2?.detections_count || model2?.detections?.length || 0;

  // Group detections by disease if multiple
  const diseaseGroups = useMemo(() => {
    if (!model2?.detections || model2.detections.length === 0) return [];
    const groups = {};
    model2.detections.forEach((det) => {
      const label = det.disease_label || det.disease || 'Unknown Disease';
      if (!groups[label]) {
        groups[label] = {
          name: label,
          count: 0,
          maxConfidence: 0,
        };
      }
      groups[label].count += 1;
      if (det.confidence > groups[label].maxConfidence) {
        groups[label].maxConfidence = det.confidence;
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
          {routerData && (
            <span className="intent-badge" title="Query Router Intent">
              Intent: {routerData.intent}
            </span>
          )}
        </div>

        {/* General conversational text if no model inference */}
        {!hasPlantResult && message.text && (
          <p className="assistant-summary-text">{message.text}</p>
        )}

        {/* ========================================================
            SECTION 1: 🌱 PLANT IDENTIFICATION (Model 1)
            ======================================================== */}
        {hasPlantResult && (
          <div className="model-card model1-card">
            <div className="model-card-header">
              <div className="model-badge-row">
                <Sprout size={16} color="var(--primary-emerald)" />
                <span className="model-title">PLANT IDENTIFICATION</span>
              </div>
            </div>

            <div className="model-card-body">
              <div className="result-field-group">
                <div className="result-field-row">
                  <span className="result-field-label">Crop:</span>
                  <span className="result-field-value plant-highlight">{cropName || 'Unknown'}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ========================================================
            SECTION 2: 🦠 DISEASE DETECTION (Model 2)
            ======================================================== */}
        {hasDiseaseModel && (
          <div className={`model-card model2-card ${hasDisease ? 'disease-detected' : 'healthy'}`}>
            <div className="model-card-header">
              <div className="model-badge-row">
                <Layers size={16} color={hasDisease ? '#f43f5e' : 'var(--primary-emerald)'} />
                <span className="model-title">DISEASE DETECTION</span>
              </div>
            </div>

            <div className="model-card-body">
              {hasDisease ? (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Disease:</span>
                    <span className="result-field-value disease-highlight">{diseaseName}</span>
                  </div>
                </div>
              ) : (
                <div className="result-field-group">
                  <div className="result-field-row">
                    <span className="result-field-label">Disease:</span>
                    <span className="result-field-value text-emerald">No disease detected</span>
                  </div>
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
        {videoInference && (
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
            {message.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
      </div>
    </div>
  );
}

