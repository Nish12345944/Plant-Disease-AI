import React, { useRef, useState, useEffect } from 'react';
import { Camera, X, RefreshCw, Check } from 'lucide-react';

export default function WebcamModal({ isOpen, onClose, onCapture }) {
  const videoRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [error, setError] = useState(null);
  const [capturedBlob, setCapturedBlob] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    if (isOpen) {
      setError(null);
      setCapturedBlob(null);
      setPreviewUrl(null);
      navigator.mediaDevices?.getUserMedia({ video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } } })
        .then((s) => {
          setStream(s);
          if (videoRef.current) {
            videoRef.current.srcObject = s;
          }
        })
        .catch((err) => {
          console.error('Camera access error:', err);
          setError('Unable to access webcam or permission denied. Please select image upload instead.');
        });
    } else {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        setStream(null);
      }
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [isOpen]);

  const handleTakePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `capture_${Date.now()}.jpg`, { type: 'image/jpeg' });
        setCapturedBlob(file);
        setPreviewUrl(URL.createObjectURL(blob));
      }
    }, 'image/jpeg', 0.95);
  };

  const handleRetake = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setCapturedBlob(null);
    setPreviewUrl(null);
  };

  const handleConfirm = () => {
    if (capturedBlob) {
      onCapture(capturedBlob);
      handleClose();
    }
  };

  const handleClose = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay animate-fade-in" onClick={handleClose}>
      <div className="modal-content webcam-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">
            <Camera size={18} color="var(--primary-emerald)" />
            <h3>Take Live Plant Photo</h3>
          </div>
          <button className="btn-icon" onClick={handleClose}>
            <X size={16} />
          </button>
        </div>

        <div className="webcam-viewport">
          {error ? (
            <div className="webcam-error-box">
              <p>{error}</p>
            </div>
          ) : previewUrl ? (
            <img src={previewUrl} alt="Captured plant" className="webcam-preview-img" />
          ) : (
            <video ref={videoRef} autoPlay playsInline muted className="webcam-video-feed" />
          )}
        </div>

        <div className="modal-footer" style={{ justifyContent: 'center', gap: '16px' }}>
          {!error && !previewUrl && (
            <button className="btn-primary" onClick={handleTakePhoto} id="btn-snap-photo">
              <Camera size={18} />
              <span>Capture Photo</span>
            </button>
          )}

          {previewUrl && (
            <>
              <button className="btn-secondary" onClick={handleRetake}>
                <RefreshCw size={16} />
                <span>Retake</span>
              </button>
              <button className="btn-primary" onClick={handleConfirm} id="btn-use-photo">
                <Check size={16} />
                <span>Use This Photo</span>
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
