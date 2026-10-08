const API_BASE = '/api';

/**
 * Check backend health & model status
 */
export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('fetchHealth error:', err);
    return { status: 'error', error: err.message };
  }
}

/**
 * Transcribe an audio file or recorded Blob
 * @param {Blob|File} audioBlob - Audio recording or file
 * @param {string} [language] - Optional language code hint
 */
export async function transcribeAudio(audioBlob, language = null) {
  const formData = new FormData();
  const filename = audioBlob.name || 'recording.wav';
  formData.append('file', audioBlob, filename);
  if (language) {
    formData.append('language', language);
  }

  const res = await fetch(`${API_BASE}/audio/transcribe`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Transcription failed with HTTP ${res.status}`);
  }

  return await res.json();
}

/**
 * Server-side microphone controls (fallback)
 */
export async function startServerMic() {
  const res = await fetch(`${API_BASE}/audio/mic/start`, { method: 'POST' });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to start microphone');
  }
  return await res.json();
}

export async function stopServerMic() {
  const res = await fetch(`${API_BASE}/audio/mic/stop`, { method: 'POST' });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to stop microphone');
  }
  return await res.json();
}

/**
 * Test route query intent
 * @param {string} text
 */
export async function routeQuery(text) {
  const res = await fetch(`${API_BASE}/query/route`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: text }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to route query');
  }
  return await res.json();
}

/**
 * Unified multimodal chat endpoint
 * @param {Object} params
 * @param {string} params.text
 * @param {File} [params.file]
 * @param {string} [params.inputType] - 'text' | 'image' | 'video' | 'audio'
 * @param {string} [params.language]
 * @param {string} [params.sessionId]
 */
export async function sendChatMessage({ text = '', file = null, inputType = 'text', language = null, sessionId = null }) {
  const formData = new FormData();
  formData.append('text', text);
  formData.append('input_type', inputType);
  if (language) formData.append('language', language);
  if (sessionId) formData.append('session_id', sessionId);
  if (file) {
    const defaultName = inputType === 'video' ? 'video.mp4' : inputType === 'audio' ? 'audio.wav' : 'image.jpg';
    formData.append('file', file, file.name || defaultName);
  }

  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Chat request failed with HTTP ${res.status}`);
  }

  return await res.json();
}
