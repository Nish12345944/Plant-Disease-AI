import React, { useState, useEffect, useRef } from 'react';
import Header from './components/Header';
import ConversationArea from './components/ConversationArea';
import Composer from './components/Composer';
import DeveloperPanel from './components/DeveloperPanel';
import ExtractedFramesModal from './components/ExtractedFramesModal';
import WebcamModal from './components/WebcamModal';
import {
  fetchHealth,
  transcribeAudio,
  sendChatMessage,
  routeQuery
} from './services/api';
import { validateMediaFile } from './services/fileValidation';
import { UploadCloud } from 'lucide-react';

export default function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(() => 'sess_' + Math.random().toString(36).substring(2, 10));
  const [inputText, setInputText] = useState('');
  const [stagedMedia, setStagedMedia] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState(null);
  const [isWindowDragActive, setIsWindowDragActive] = useState(false);

  // Modals & Panels
  const [isDebugOpen, setIsDebugOpen] = useState(false);
  const [telemetryData, setTelemetryData] = useState(null);
  const [selectedVideoData, setSelectedVideoData] = useState(null);
  const [isWebcamOpen, setIsWebcamOpen] = useState(false);

  // Audio Recording State
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isTranscribing, setIsTranscribing] = useState(false);

  // Web Audio / MediaRecorder refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerIntervalRef = useRef(null);
  const dragCounterRef = useRef(0);

  // Check backend health on mount
  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkStatus = async () => {
    const health = await fetchHealth();
    setBackendStatus(health);
  };

  // Timer effect for recording
  useEffect(() => {
    if (isRecording) {
      setRecordingTime(0);
      timerIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
      setRecordingTime(0);
    }
    return () => {
      if (timerIntervalRef.current) clearInterval(timerIntervalRef.current);
    };
  }, [isRecording]);

  /**
   * Unified file validator and stager for both drag-and-drop and click-browse
   */
  const handleStageFile = (file) => {
    if (!file) return;

    const validation = validateMediaFile(file);
    if (!validation.valid) {
      alert(`Upload Error: ${validation.error}`);
      return;
    }

    if (validation.type === 'audio') {
      handleProcessAudioBlob(file, file.name);
      return;
    }

    // Revoke previous object URL if any
    if (stagedMedia?.url) {
      URL.revokeObjectURL(stagedMedia.url);
    }

    const previewUrl = URL.createObjectURL(file);
    setStagedMedia({
      type: validation.type,
      file,
      url: previewUrl,
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(2) + ' MB',
    });
  };

  // Global window drag and drop listener
  useEffect(() => {
    const handleDragEnter = (e) => {
      e.preventDefault();
      dragCounterRef.current += 1;
      if (e.dataTransfer?.types?.includes('Files')) {
        setIsWindowDragActive(true);
      }
    };

    const handleDragLeave = (e) => {
      e.preventDefault();
      dragCounterRef.current -= 1;
      if (dragCounterRef.current <= 0) {
        dragCounterRef.current = 0;
        setIsWindowDragActive(false);
      }
    };

    const handleDragOver = (e) => {
      e.preventDefault();
      if (e.dataTransfer) {
        e.dataTransfer.dropEffect = 'copy';
      }
    };

    const handleDrop = (e) => {
      e.preventDefault();
      dragCounterRef.current = 0;
      setIsWindowDragActive(false);

      const files = e.dataTransfer?.files;
      if (files && files.length > 0) {
        handleStageFile(files[0]);
      }
    };

    window.addEventListener('dragenter', handleDragEnter);
    window.addEventListener('dragleave', handleDragLeave);
    window.addEventListener('dragover', handleDragOver);
    window.addEventListener('drop', handleDrop);

    return () => {
      window.removeEventListener('dragenter', handleDragEnter);
      window.removeEventListener('dragleave', handleDragLeave);
      window.removeEventListener('dragover', handleDragOver);
      window.removeEventListener('drop', handleDrop);
    };
  }, [stagedMedia]);

  /**
   * Start microphone recording via HTML5 MediaRecorder
   */
  const handleStartRecording = async () => {
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        alert('Microphone access is not supported by your browser environment.');
        return;
      }

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];

      let mimeType = 'audio/webm';
      if (!MediaRecorder.isTypeSupported('audio/webm')) {
        mimeType = ''; // Let browser choose default
      }

      const mediaRecorder = mimeType ? new MediaRecorder(stream, { mimeType }) : new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        const audioBlob = new Blob(audioChunksRef.current, { type: mediaRecorder.mimeType || 'audio/webm' });
        await handleProcessAudioBlob(audioBlob, 'mic_recording.webm');
      };

      mediaRecorder.start(250); // collect 250ms chunks
      setIsRecording(true);
    } catch (err) {
      console.error('Error starting microphone:', err);
      alert(`Microphone permission error: ${err.message || 'Access denied'}`);
      setIsRecording(false);
    }
  };

  /**
   * Stop microphone recording and trigger faster-whisper STT
   */
  const handleStopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  /**
   * Process recorded audio blob or uploaded audio file
   */
  const handleProcessAudioBlob = async (blobOrFile, filename = 'audio.wav') => {
    setIsTranscribing(true);
    try {
      const fileToUpload = blobOrFile instanceof File ? blobOrFile : new File([blobOrFile], filename, { type: blobOrFile.type });
      const result = await transcribeAudio(fileToUpload);

      if (result.text) {
        // Place transcribed text directly into the composer prompt box
        setInputText((prev) => {
          const trimmed = prev.trim();
          return trimmed ? `${trimmed} ${result.text.trim()}` : result.text.trim();
        });

        // Update developer telemetry
        setTelemetryData({
          input_types: { text: true, audio: true, image: false, video: false },
          language: result.language || 'en',
          original_text: result.text,
          normalized_text: result.text,
          intent: 'transcription_preview',
          routing_metadata: {
            needs_model1: false,
            needs_model2: false,
            needs_rag: false,
          }
        });
      } else {
        alert('No speech detected or audio was silent. Please try speaking again.');
      }
    } catch (err) {
      console.error('Audio transcription error:', err);
      alert(`Transcription error: ${err.message}`);
    } finally {
      setIsTranscribing(false);
    }
  };

  /**
   * Handle user prompt submission
   */
  const handleSendMessage = async ({ text, media }) => {
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      text: text,
      media: media ? { ...media } : null,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setStagedMedia(null);
    setIsLoading(true);

    try {
      const inputType = media ? media.type : 'text';
      const file = media?.file || null;

      const response = await sendChatMessage({
        text,
        file,
        inputType,
        sessionId,
      });

      // Update telemetry data for the Developer Debug Panel
      const debugState = response.unified_state || {
        input_types: {
          text: Boolean(text),
          audio: false,
          image: inputType === 'image',
          video: inputType === 'video',
        },
        language: response.language || 'en',
        original_text: response.original_query || text,
        normalized_text: text,
        intent: response.router?.intent || 'unknown',
        routing_metadata: response.router?.routing_metadata || {},
        model1: response.model1,
        model2: response.model2 || response.video_inference?.model2 || response.model1?.model2,
        video_inference: response.video_inference,
      };
      setTelemetryData(debugState);

      // Construct AI Assistant message
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: response.message,
        data: {
          model1: response.model1,
          video_inference: response.video_inference,
          model2: response.model2 || response.video_inference?.model2 || response.model1?.model2,
          knowledge: response.knowledge,
          knowledge_sources: response.knowledge_sources,
          annotated_preview_url: response.annotated_preview_url || response.model2?.annotated_preview_url || response.model1?.annotated_preview_url,
          original_image_url: (media && media.type === 'image' ? media.url : null) || response.image_url || response.model1?.image_preview_url || null,
          media_type: media?.type || null,
          router: response.router,
          telemetry: debugState,
        },
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        text: `Error processing request: ${err.message}`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectPrompt = (prompt) => {
    setInputText(prompt);
  };

  const handleResetChat = () => {
    if (window.confirm('Clear current conversation history?')) {
      setMessages([]);
      setInputText('');
      setStagedMedia(null);
      setSessionId('sess_' + Math.random().toString(36).substring(2, 10));
    }
  };

  const handleInspectTelemetry = (data) => {
    if (data?.telemetry) {
      setTelemetryData({
        ...data.telemetry,
        model1: data.model1,
        model2: data.model2,
        video_inference: data.video_inference,
      });
    }
    setIsDebugOpen(true);
  };

  return (
    <div className="app-container">
      {/* Global Drag-and-Drop Active Overlay */}
      {isWindowDragActive && (
        <div className="global-drag-overlay animate-fade-in">
          <div className="global-drag-card animate-scale-up">
            <UploadCloud size={56} className="global-drag-icon text-emerald" />
            <h3 className="global-drag-title">Drag &amp; drop an image or video here</h3>
            <p className="global-drag-subtitle">or release to analyze with Model 1 + Model 2 V4</p>
          </div>
        </div>
      )}

      {/* Top Header */}
      <Header
        onToggleDebug={() => setIsDebugOpen(!isDebugOpen)}
        isDebugOpen={isDebugOpen}
        onResetChat={handleResetChat}
        backendStatus={backendStatus}
      />

      {/* Main Conversational Layout */}
      <main className="app-main-content">
        <ConversationArea
          messages={messages}
          onSelectPrompt={handleSelectPrompt}
          onOpenFramesModal={(videoData) => setSelectedVideoData(videoData)}
          onInspectTelemetry={handleInspectTelemetry}
          onFileDrop={handleStageFile}
          isLoading={isLoading}
        />

        {/* Collapsible Developer Debug Panel */}
        <DeveloperPanel
          isOpen={isDebugOpen}
          onClose={() => setIsDebugOpen(false)}
          telemetryData={telemetryData}
        />
      </main>

      {/* Sticky Bottom Composer */}
      <Composer
        inputText={inputText}
        setInputText={setInputText}
        stagedMedia={stagedMedia}
        setStagedMedia={setStagedMedia}
        onSendMessage={handleSendMessage}
        onOpenLiveCamera={() => setIsWebcamOpen(true)}
        onTranscribeAudioFile={(file) => handleProcessAudioBlob(file, file.name)}
        onFileDrop={handleStageFile}
        isRecording={isRecording}
        isTranscribing={isTranscribing}
        recordingTime={recordingTime}
        onStartRecording={handleStartRecording}
        onStopRecording={handleStopRecording}
        isLoading={isLoading}
      />

      {/* Extracted Frames Modal (Shows all 16-24 video frames with individual predictions) */}
      <ExtractedFramesModal
        isOpen={Boolean(selectedVideoData)}
        onClose={() => setSelectedVideoData(null)}
        videoData={selectedVideoData}
      />

      {/* Live Webcam Modal */}
      <WebcamModal
        isOpen={isWebcamOpen}
        onClose={() => setIsWebcamOpen(false)}
        onCapture={(file) => handleStageFile(file)}
      />
    </div>
  );
}
