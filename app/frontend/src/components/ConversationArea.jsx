import React, { useEffect, useRef } from 'react';
import MessageItem from './MessageItem';
import { Sprout, MessageSquare, Mic, Image, Video, Sparkles } from 'lucide-react';

export default function ConversationArea({ 
  messages, 
  onSelectPrompt, 
  onOpenFramesModal, 
  onInspectTelemetry,
  isLoading 
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const samplePrompts = [
    "What plant is this?",
    "What disease does this plant have?",
    "How do I treat early blight?",
    "इस पौधे में कौन सी बीमारी है?",
  ];

  return (
    <div className="conversation-container" id="conversation-area">
      {messages.length === 0 ? (
        <div className="empty-chat-welcome animate-fade-in">
          <div className="empty-chat-avatar">
            <Sprout size={36} color="var(--primary-emerald)" />
          </div>

          <h2 className="empty-chat-title">How can I help with your crops today?</h2>
          <p className="empty-chat-subtitle">
            Identify plant species, diagnose diseases with localized bounding boxes, or record voice queries in Hindi & English.
          </p>

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
          {messages.map((msg, index) => (
            <MessageItem 
              key={msg.id || index} 
              message={msg} 
              onOpenFramesModal={onOpenFramesModal}
              onInspectTelemetry={onInspectTelemetry}
            />
          ))}

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
