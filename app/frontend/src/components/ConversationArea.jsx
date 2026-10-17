import React, { useEffect, useRef, useState } from 'react';
import MessageItem from './MessageItem';
import { Sprout, MessageSquare, UploadCloud, Image as ImageIcon, Video as VideoIcon } from 'lucide-react';

export default function ConversationArea({ 
  messages, 
  onSelectPrompt, 
  onOpenFramesModal, 
  onInspectTelemetry,
  onFileDrop,
  isLoading 
}) {
  const containerRef = useRef(null);
  const bottomRef = useRef(null);
  const latestAssistantMessageRef = useRef(null);
  const fileInputRef = useRef(null);
  const [isCardDragOver, setIsCardDragOver] = useState(false);
  const lastScrolledMessageIdRef = useRef(null);
  const wasLoadingRef = useRef(false);

  useEffect(() => {
    // When a request is actively processing, scroll down to show the user's upload & loading indicator
    if (isLoading) {
      wasLoadingRef.current = true;
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      return;
    }

    if (messages.length === 0) return;

    const latestMessage = messages[messages.length - 1];
    if (!latestMessage) return;

    // Avoid repeatedly resetting the scroll position if this message was already scrolled to
    if (latestMessage.id === lastScrolledMessageIdRef.current) {
      return;
    }
    lastScrolledMessageIdRef.current = latestMessage.id;

    if (latestMessage.role === 'assistant') {
      const isMediaAnalysis = Boolean(
        latestMessage.data?.model1 ||
        latestMessage.data?.video_inference ||
        latestMessage.data?.original_image_url ||
        latestMessage.data?.media_type === 'image' ||
        latestMessage.data?.media_type === 'video'
      );

      if (isMediaAnalysis) {
        // Position chat viewport at the top of the newly rendered assistant response
        const scrollTimer = setTimeout(() => {
          if (latestAssistantMessageRef.current && containerRef.current) {
            const container = containerRef.current;
            const element = latestAssistantMessageRef.current;
            const containerRect = container.getBoundingClientRect();
            const elementRect = element.getBoundingClientRect();
            const targetScrollTop = container.scrollTop + (elementRect.top - containerRect.top) - 16;
            container.scrollTo({
              top: Math.max(0, targetScrollTop),
              behavior: 'smooth'
            });
          } else if (latestAssistantMessageRef.current) {
            latestAssistantMessageRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 50);
        return () => clearTimeout(scrollTimer);
      } else {
        // For text-only messages, preserve standard scroll-to-view
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      // User message
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
    wasLoadingRef.current = false;
  }, [messages, isLoading]);

  const samplePrompts = [
    "What plant is this?",
    "What disease does this plant have?",
    "How do I treat early blight?",
    "इस पौधे में कौन सी बीमारी है?",
  ];

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsCardDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsCardDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsCardDragOver(false);
    const files = e.dataTransfer?.files;
    if (files && files.length > 0 && onFileDrop) {
      onFileDrop(files[0]);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file && onFileDrop) {
      onFileDrop(file);
      e.target.value = '';
    }
  };

  return (
    <div className="conversation-container" ref={containerRef} id="conversation-area">
      {messages.length === 0 ? (
        <div className="empty-chat-welcome animate-fade-in">
          <div className="empty-chat-avatar">
            <Sprout size={36} color="var(--primary-emerald)" />
          </div>

          <h2 className="empty-chat-title">How can I help with your crops today?</h2>
          <p className="empty-chat-subtitle">
            Identify plant species, diagnose diseases with Model 1 + Model 2 V4, or record voice queries in Hindi & English.
          </p>

          {/* Interactive Drag & Drop Uploader Card */}
          <div 
            className={`uploader-drop-card ${isCardDragOver ? 'drag-active' : ''}`}
            onDragOver={handleDragOver}
            onDragEnter={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            title="Click or drop an image/video to analyze"
          >
            <input 
              type="file"
              ref={fileInputRef}
              style={{ display: 'none' }}
              accept=".jpg,.jpeg,.png,.webp,.bmp,.mp4,.avi,.mov,.mkv,.webm,.m4v,image/*,video/*"
              onChange={handleFileChange}
            />
            <div className="uploader-icon-wrap">
              <UploadCloud size={30} className="uploader-cloud-icon" />
            </div>
            <div className="uploader-text-wrap">
              <span className="uploader-main-text">Drag &amp; drop an image or video here</span>
              <span className="uploader-sub-text">or click to browse</span>
            </div>
            <div className="uploader-badges">
              <span className="uploader-badge"><ImageIcon size={12} /> Images (JPG, PNG, WebP)</span>
              <span className="uploader-badge"><VideoIcon size={12} /> Videos (MP4, MOV, WebM)</span>
            </div>
          </div>

          {/* Quick Prompt Chips */}
          <div className="quick-prompts-container">
            <div className="quick-prompts-grid">
              {samplePrompts.map((prompt, idx) => (
                <button
                  key={idx}
                  className="quick-prompt-btn"
                  onClick={() => onSelectPrompt(prompt)}
                >
                  <MessageSquare size={13} color="var(--primary-emerald)" />
                  <span>{prompt}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="messages-list">
          {messages.map((msg, index) => {
            const isLatestAssistant = index === messages.length - 1 && msg.role === 'assistant';
            return (
              <MessageItem 
                key={msg.id || index}
                ref={isLatestAssistant ? latestAssistantMessageRef : null}
                message={msg} 
                onOpenFramesModal={onOpenFramesModal}
                onInspectTelemetry={onInspectTelemetry}
              />
            );
          })}

          {isLoading && (
            <div className="message-wrapper assistant animate-pulse-fade">
              <div className="message-avatar assistant-avatar">
                <Sprout size={20} color="var(--primary-emerald)" />
              </div>
              <div className="message-bubble assistant-bubble loading-bubble">
                <div className="typing-indicator">
                  <span />
                  <span />
                  <span />
                </div>
                <span className="loading-label">Processing multimodal inputs...</span>
              </div>
            </div>
          )}

          <div ref={bottomRef} style={{ height: '1px' }} />
        </div>
      )}
    </div>
  );
}
