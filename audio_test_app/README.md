# Audio Pipeline Testing Application

A local, standalone browser-based interface for testing the Speech-to-Text (STT) and Intent Routing pipeline. Built with Streamlit, running completely locally on Windows with zero cloud or paid API dependencies.

---

## 1. What the Application Does

- **Microphone Capture**: Records speech locally using `sounddevice` / `AudioRecorder` at 16 kHz mono 16-bit PCM, or via in-browser recording widget (`st.audio_input`).
- **Local Speech-to-Text**: Decodes audio locally using `faster-whisper-small` via PyAV 13.1.0 with auto language detection.
- **Multilingual Recognition**: Supports English, Hindi, and Indian regional languages without English-only assumptions.
- **Intent Routing**: Feeds the transcription into the project's deterministic rule-based query router (`router.query_router.route_query`).
- **Pipeline Decision Display**: Visualizes the classified intent along with downstream execution flags (`needs_model1`, `needs_model2`, `needs_rag`).
- **Temporary WAV Management**: Automatically and safely cleans up temporary WAV files after processing.

---

## 2. Architecture

```text
                  ┌──────────────────────────────────────────────┐
                  │            AUDIO INPUT OPTIONS               │
                  │  (Hardware Mic / Browser Mic / Audio File)   │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                             [ Temporary WAV File ]
                           (16 kHz Mono, 16-bit PCM)
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │     audio.test_audio.transcribe_audio  │
                     │         (faster-whisper-small)         │
                     └───────────────────┬────────────────────┘
                                         │
                      ┌──────────────────┴──────────────────┐
                      ▼                                     ▼
             [ Detected Language ]                 [ Transcribed Text ]
                      │                                     │
                      │                                     ▼
                      │                         ┌───────────────────────┐
                      │                         │   router.query_router │
                      │                         │     route_query()     │
                      │                         └───────────┬───────────┘
                      │                                     │
                      ▼                                     ▼
              Language Label & Confidence            Intent & Flags
                      │                                     │
                      └──────────────────┬──────────────────┘
                                         ▼
                           [ Streamlit Testing UI ]
                                         │
                                         ▼
                        [ Cleanup Temporary WAV File ]
```

---

## 3. Required Dependencies

The application relies strictly on existing project packages in `.\venv\`:

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `faster-whisper` | 1.2.1 | Fast local CTranslate2-based Whisper inference |
| `av` (PyAV) | 13.1.0 | Audio file decoding (required `< 14` for faster-whisper compatibility) |
| `sounddevice` | 0.5.6 | Direct hardware microphone recording |
| `streamlit` | 1.65.0 | Web application interface |
| `numpy` | 1.26.4 | Audio buffer manipulation |
| `scipy` | 1.13.0 | Audio format parsing |

---

## 4. How to Run

From the project root:

```powershell
.\venv\Scripts\python.exe -m streamlit run audio_test_app/app.py
```

The application will launch and be accessible at:
- **Local URL:** `http://localhost:8501`

---

## 5. How to Test Microphone

1. Open `http://localhost:8501` in your browser.
2. Under the **🎙 Microphone Test** tab:
   - **Interactive Mode**: Click **"🎙 START RECORDING"**, speak into your microphone, then click **"⏹ STOP RECORDING"**.
   - **Quick Record Mode**: Select a duration (e.g., 4 seconds) using the slider and click **"⏱ Record 4s & Process"**.
   - **Browser Widget**: Use the built-in `st.audio_input` recorder to record directly through your web browser.
3. Review the audio playback, detected language, transcription, and router classification.

---

## 6. How to Test an Audio File

1. Navigate to the **📁 Audio File Upload** tab.
2. Drag and drop or browse to select an audio file (`.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.opus`, `.wma`, `.aac`).
3. Click **"🚀 Transcribe & Route Audio File"**.
4. The system will save a temporary copy, transcribe it, classify the intent, and immediately clean up the temporary file.

---

## 7. Expected Output

For the test sentence:
> **"What plant is this and what disease does it have?"**

Expected Results:
- **Language**: English (`en`)
- **Confidence**: `> 0.90`
- **Transcription**: `"What plant is this and what disease does it have?"`
- **Intent**: `disease_detection`
- **Model 1 (Plant Identification)**: `✓ YES`
- **Model 2 (Disease Detection)**: `✓ YES`
- **RAG Knowledge Base**: `✗ NO`

---

## 8. Known Limitations & Future Scope

- **Non-Streaming STT**: Audio is transcribed as complete chunks after recording finishes. Real-time streaming transcription will be added in a future update.
- **Multilingual Translation**: Whisper detects and transcribes non-English languages (e.g. Hindi: *"ये कौन सा पौधा है?"*), but machine translation (IndicTrans2) is not yet attached to the router.
- **Hardware Exclusivity**: If another application has exclusive control of the default input microphone, `sounddevice` will raise a `MicrophoneError`; in that scenario, the browser microphone widget (`st.audio_input`) serves as a fallback.
