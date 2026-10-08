import React from 'react';
import { Sprout, Terminal, RotateCcw, Cpu, Sparkles } from 'lucide-react';

export default function Header({ 
  onToggleDebug, 
  isDebugOpen, 
  onResetChat, 
  backendStatus 
}) {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="brand-logo">
          <Sprout size={22} color="var(--primary-emerald)" strokeWidth={2.5} />
        </div>
        <div className="brand-titles">
          <h1>ALEXA FARMS</h1>
          <div className="brand-subtitle">
            <span className="live-dot" />
            AI Plant Assistant
          </div>
        </div>
      </div>

      <div className="header-actions">
        {/* Device & Model Status Pill */}
        <div className="status-pill" title="Model 1 Status">
          <Cpu size={14} color="var(--primary-emerald)" />
          <span>Model 1: {backendStatus?.model1_loaded ? 'Ready (RTX 3050)' : 'Loading...'}</span>
        </div>

        {/* Developer Debug Toggle Button */}
        <button 
          id="btn-toggle-debug"
          className={`btn-icon ${isDebugOpen ? 'active' : ''}`}
          onClick={onToggleDebug}
          title="Toggle Developer & Input Debug Panel"
        >
          <Terminal size={17} />
          <span className="btn-icon-label">Debug Panel</span>
        </button>

        {/* Reset Conversation */}
        <button 
          id="btn-reset-chat"
          className="btn-icon"
          onClick={onResetChat}
          title="Clear Conversation"
        >
          <RotateCcw size={16} />
        </button>
      </div>
    </header>
  );
}
