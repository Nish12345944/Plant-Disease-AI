import React, { useRef } from 'react';
import { Mic, Upload, FileAudio } from 'lucide-react';

export default function AudioMenu({ 
  isOpen, 
  onClose, 
  onStartRecord, 
  onSelectAudioFile 
}) {
  const audioInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onSelectAudioFile(file);
      onClose();
      e.target.value = '';
    }
  };

  return (
    <>
      <input 
        type="file" 
        ref={audioInputRef} 
        style={{ display: 'none' }} 
        accept=".wav,.mp3,.m4a,.flac,.ogg,.opus,.wma,.aac,.webm,audio/*" 
        onChange={handleFileChange}
      />

      {isOpen && (
        <div className="composer-popover mic-popover animate-scale-up" id="mic-popover-menu">
          <button 
            className="popover-item"
            id="btn-popover-record-mic"
            type="button"
            onClick={() => {
              onClose();
              onStartRecord();
            }}
          >
            <Mic size={18} color="var(--primary-emerald)" />
            <div className="popover-item-text">
              <strong>Record Live Voice</strong>
              <span>Push to talk / speech-to-text</span>
            </div>
          </button>

          <button 
            className="popover-item"
            id="btn-popover-upload-audio"
            type="button"
            onClick={() => {
              audioInputRef.current?.click();
            }}
          >
            <Upload size={18} color="var(--primary-emerald)" />
            <div className="popover-item-text">
              <strong>Upload Audio File</strong>
              <span>WAV, MP3, M4A, OGG, FLAC</span>
            </div>
          </button>
        </div>
      )}
    </>
  );
}
