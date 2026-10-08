import React, { useState, useRef, useEffect } from 'react';
import { 
  Camera, 
  Mic, 
  MicOff, 
  Send, 
  X, 
  Square, 
  Loader2, 
  Image as ImageIcon, 
  Video as VideoIcon, 
  FileAudio,
  Radio
} from 'lucide-react';
import CameraMenu from './CameraMenu';
import AudioMenu from './AudioMenu';

export default function Composer({
  inputText,
  setInputText,
  stagedMedia,
  setStagedMedia,
  onSendMessage,
  onOpenLiveCamera,
  onTranscribeAudioFile,
  isRecording,
  isTranscribing,
  recordingTime,
  onStartRecording,
  onStopRecording,
  isLoading
}) {
  const [cameraMenuOpen, setCameraMenuOpen] = useState(false);
  const [audioMenuOpen, setAudioMenuOpen] = useState(false);
  const inputRef = useRef(null);

  // Close menus when clicking outside
  useEffect(() => {
    const handleDocumentClick = (e) => {
      if (!e.target.closest('#composer-camera-btn') && !e.target.closest('#camera-popover-menu')) {
        setCameraMenuOpen(false);
      }
      if (!e.target.closest('#composer-mic-btn') && !e.target.closest('#mic-popover-menu')) {
        setAudioMenuOpen(false);
      }
    };
    document.addEventListener('click', handleDocumentClick);
    return () => document.removeEventListener('click', handleDocumentClick);
  }, []);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (isLoading || isRecording || isTranscribing) return;
    if (!inputText.trim() && !stagedMedia) return;

    onSendMessage({
      text: inputText.trim(),
      media: stagedMedia,
    });
  };

  const handleSelectImage = (file) => {
    const previewUrl = URL.createObjectURL(file);
    setStagedMedia({
      type: 'image',
      file,
      url: previewUrl,
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
    });
  };

  const handleSelectVideo = (file) => {
    const previewUrl = URL.createObjectURL(file);
    setStagedMedia({
      type: 'video',
      file,
      url: previewUrl,
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
    });
  };

  const handleSelectAudioFile = (file) => {
    // According to specs: uploaded audio triggers transcription into prompt box
    onTranscribeAudioFile(file);
  };

  const handleRemoveStagedMedia = () => {
    if (stagedMedia?.url) URL.revokeObjectURL(stagedMedia.url);
    setStagedMedia(null);
  };

  const formatSeconds = (sec) => {
    const m = Math.floor(sec / 60).toString().padStart(2, '0');
    const s = (sec % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const canSend = (inputText.trim().length > 0 || stagedMedia !== null) && !isLoading && !isRecording && !isTranscribing;

  return (
    <footer className="app-composer-wrapper">
      {/* Staged Media Bar above Composer */}
      {stagedMedia && (
        <div className="staged-media-chip animate-slide-up">
          <div className="staged-media-info">
            {stagedMedia.type === 'image' && (
              <>
                <img src={stagedMedia.url} alt="Staged thumbnail" className="staged-thumb" />
                <span className="staged-name">
                  <ImageIcon size={14} color="var(--primary-emerald)" /> {stagedMedia.name}
                </span>
              </>
            )}
            {stagedMedia.type === 'video' && (
              <>
                <span className="staged-name">
                  <VideoIcon size={14} color="var(--primary-emerald)" /> {stagedMedia.name} ({stagedMedia.size})
                </span>
              </>
            )}
            {stagedMedia.type === 'audio' && (
              <>
                <span className="staged-name">
                  <FileAudio size={14} color="var(--primary-emerald)" /> {stagedMedia.name}
                </span>
              </>
            )}
          </div>
          <button 
            className="btn-remove-staged" 
            onClick={handleRemoveStagedMedia}
            title="Remove attachment"
          >
            <X size={14} />
          </button>
        </div>
      )}

      {/* Main Composer Box */}
      <div className={`composer-box ${isRecording ? 'recording-active' : ''}`}>
        {/* Left: Camera / Media Button */}
        <div className="composer-action-container">
          <button
            id="composer-camera-btn"
            className="composer-btn camera-btn"
            onClick={(e) => {
              e.stopPropagation();
              setCameraMenuOpen(!cameraMenuOpen);
              setAudioMenuOpen(false);
            }}
            disabled={isRecording || isLoading}
            title="Attach Plant Image or Video"
          >
            <Camera size={20} strokeWidth={2.2} />
          </button>

          <CameraMenu 
            isOpen={cameraMenuOpen}
            onClose={() => setCameraMenuOpen(false)}
            onSelectImage={handleSelectImage}
            onSelectVideo={handleSelectVideo}
            onOpenLiveCamera={onOpenLiveCamera}
          />
        </div>

        {/* Center: Either Text Input OR Live Recording Bar */}
        {isRecording ? (
          <div className="recording-live-bar animate-fade-in">
            <div className="recording-indicator">
              <span className="rec-pulse-dot" />
              <span className="rec-text">Listening...</span>
              <span className="rec-timer">{formatSeconds(recordingTime)}</span>
            </div>
            <button 
              className="btn-stop-recording" 
              onClick={onStopRecording}
              title="Stop recording and transcribe"
            >
              <Square size={14} fill="currentColor" />
              <span>Done</span>
            </button>
          </div>
        ) : isTranscribing ? (
          <div className="transcribing-bar animate-fade-in">
            <Loader2 size={16} className="animate-spin text-emerald" />
            <span className="transcribing-text">Transcribing voice input with Whisper...</span>
          </div>
        ) : (
          <div className="composer-input-container">
            <textarea
              ref={inputRef}
              id="composer-text-input"
              className="composer-textarea"
              rows={1}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your farm..."
              disabled={isLoading}
            />
          </div>
        )}

        {/* Right: Microphone Button AND Send Button */}
        <div className="composer-right-actions">
          <div className="composer-action-container">
            <button
              id="composer-mic-btn"
              className={`composer-btn mic-btn ${isRecording ? 'recording' : ''}`}
              onClick={(e) => {
                e.stopPropagation();
                if (isRecording) {
                  onStopRecording();
                } else {
                  setAudioMenuOpen(!audioMenuOpen);
                  setCameraMenuOpen(false);
                }
              }}
              disabled={isLoading || isTranscribing}
              title="Microphone & Audio Upload"
            >
              <Mic size={19} strokeWidth={2.2} />
            </button>

            <AudioMenu
              isOpen={audioMenuOpen}
              onClose={() => setAudioMenuOpen(false)}
              onStartRecord={() => {
                setAudioMenuOpen(false);
                onStartRecording();
              }}
              onSelectAudioFile={handleSelectAudioFile}
            />
          </div>

          <button
            id="btn-composer-send"
            className={`composer-btn send-btn ${canSend ? 'active' : 'disabled'}`}
            onClick={handleSubmit}
            disabled={!canSend}
            title="Send Query (Enter)"
          >
            <Send size={17} strokeWidth={2.5} />
          </button>
        </div>
      </div>
    </footer>
  );
}
