import React, { useRef } from 'react';
import { Camera, Image, Video } from 'lucide-react';

export default function CameraMenu({ 
  isOpen, 
  onClose, 
  onSelectImage, 
  onSelectVideo, 
  onOpenLiveCamera 
}) {
  const imageInputRef = useRef(null);
  const videoInputRef = useRef(null);

  const handleImageFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onSelectImage(file);
      onClose();
      e.target.value = '';
    }
  };

  const handleVideoFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onSelectVideo(file);
      onClose();
      e.target.value = '';
    }
  };

  return (
    <>
      <input 
        type="file" 
        ref={imageInputRef} 
        style={{ display: 'none' }} 
        accept=".jpg,.jpeg,.png,.webp,.bmp,image/*" 
        onChange={handleImageFileChange}
      />
      <input 
        type="file" 
        ref={videoInputRef} 
        style={{ display: 'none' }} 
        accept=".mp4,.avi,.mov,.mkv,.webm,.m4v,video/*" 
        onChange={handleVideoFileChange}
      />

      {isOpen && (
        <div className="composer-popover camera-popover animate-scale-up" id="camera-popover-menu">
          <button 
            className="popover-item"
            id="btn-popover-live-camera"
            type="button"
            onClick={() => {
              onClose();
              onOpenLiveCamera();
            }}
          >
            <Camera size={18} color="var(--primary-emerald)" />
            <div className="popover-item-text">
              <strong>Take Plant Photo</strong>
              <span>Use browser camera</span>
            </div>
          </button>

          <button 
            className="popover-item"
            id="btn-popover-upload-image"
            type="button"
            onClick={() => {
              imageInputRef.current?.click();
            }}
          >
            <Image size={18} color="var(--primary-emerald)" />
            <div className="popover-item-text">
              <strong>Upload Image</strong>
              <span>JPG, PNG, WebP</span>
            </div>
          </button>

          <button 
            className="popover-item"
            id="btn-popover-upload-video"
            type="button"
            onClick={() => {
              videoInputRef.current?.click();
            }}
          >
            <Video size={18} color="var(--primary-emerald)" />
            <div className="popover-item-text">
              <strong>Upload Video</strong>
              <span>MP4, AVI, MOV, WebM</span>
            </div>
          </button>
        </div>
      )}
    </>
  );
}
