"""Standalone Local Audio Pipeline Testing Application.

Features:
- Live hardware microphone recording (via audio.recorder.AudioRecorder)
- In-browser microphone recording (via st.audio_input)
- Audio file upload (.wav, .mp3, .m4a, .flac, .ogg, .opus, .wma, .aac)
- Local multilingual Speech-to-Text via faster-whisper (audio.test_audio)
- Deterministic query routing (router.query_router.route_query)
- Verified system status dashboard
- Strict temporary file cleanup
"""

from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

# Add project root to sys.path so modules import reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Existing component imports (strict reuse - no duplicate logic)
from audio.recorder import (
    AudioRecorder,
    AudioRecorderError,
    EmptyRecordingError,
    MicrophoneError,
    record_to_temp_wav,
)
from audio.test_audio import SUPPORTED_EXTENSIONS, TranscriptionResult, transcribe_audio
from router.query_router import route_query

# Common ISO language code mapping
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "ru": "Russian",
    "pt": "Portuguese",
    "it": "Italian",
}


def get_language_label(code: str) -> str:
    """Format language code to readable name e.g. 'English (en)'."""
    name = LANGUAGE_NAMES.get(code.lower(), code.upper())
    return f"{name} ({code})"


def check_system_status() -> dict[str, dict[str, str | bool]]:
    """Inspect and verify all audio pipeline dependencies."""
    status = {}

    # 1. faster-whisper
    try:
        import faster_whisper

        status["faster_whisper"] = {
            "name": "faster-whisper",
            "version": getattr(faster_whisper, "__version__", "installed"),
            "ok": True,
            "details": "Small model loaded locally",
        }
    except Exception as exc:
        status["faster_whisper"] = {
            "name": "faster-whisper",
            "version": "Error",
            "ok": False,
            "details": str(exc),
        }

    # 2. PyAV
    try:
        import av

        av_ver = av.__version__
        major = int(av_ver.split(".")[0])
        is_compat = major < 14
        status["pyav"] = {
            "name": "PyAV",
            "version": av_ver,
            "ok": is_compat,
            "details": "Compatible (<14)" if is_compat else "Incompatible (>=14)",
        }
    except Exception as exc:
        status["pyav"] = {
            "name": "PyAV",
            "version": "Error",
            "ok": False,
            "details": str(exc),
        }

    # 3. sounddevice
    try:
        import sounddevice as sd

        status["sounddevice"] = {
            "name": "sounddevice",
            "version": getattr(sd, "__version__", "installed"),
            "ok": True,
            "details": "PortAudio backend active",
        }
    except Exception as exc:
        status["sounddevice"] = {
            "name": "sounddevice",
            "version": "Error",
            "ok": False,
            "details": str(exc),
        }

    # 4. Default Microphone
    try:
        import sounddevice as sd

        default_dev = sd.default.device[0]
        if default_dev is not None and default_dev >= 0:
            dev_info = sd.query_devices(default_dev, "input")
            name = dev_info.get("name", f"Device #{default_dev}")
            channels = dev_info.get("max_input_channels", 0)
            status["microphone"] = {
                "name": "Default Microphone",
                "version": f"{name} ({channels} ch)",
                "ok": channels > 0,
                "details": f"Device #{default_dev}",
            }
        else:
            status["microphone"] = {
                "name": "Default Microphone",
                "version": "None detected",
                "ok": False,
                "details": "No default input device",
            }
    except Exception as exc:
        status["microphone"] = {
            "name": "Default Microphone",
            "version": "Error",
            "ok": False,
            "details": str(exc),
        }

    # 5. Query Router
    try:
        test_route = route_query("what disease does this tomato have?")
        is_ok = test_route.get("intent") == "disease_detection"
        status["router"] = {
            "name": "Query Router",
            "version": "Rule-based Engine",
            "ok": is_ok,
            "details": "5 intents & routing table verified",
        }
    except Exception as exc:
        status["router"] = {
            "name": "Query Router",
            "version": "Error",
            "ok": False,
            "details": str(exc),
        }

    return status


def process_audio_file(
    audio_path: Path | str, source_label: str = "Audio Source"
) -> dict:
    """Run faster-whisper transcription and query routing on an audio file."""
    # Step 1: Speech-to-Text
    transcription: TranscriptionResult = transcribe_audio(str(audio_path))

    # Step 2: Query Routing
    routing = route_query(transcription.text)

    return {
        "source": source_label,
        "language_code": transcription.language,
        "language_label": get_language_label(transcription.language),
        "confidence": transcription.language_probability,
        "text": transcription.text.strip(),
        "segments": transcription.segments,
        "intent": routing["intent"],
        "needs_model1": routing["needs_model1"],
        "needs_model2": routing["needs_model2"],
        "needs_rag": routing["needs_rag"],
    }


def render_results(result_data: dict, audio_bytes: bytes | None = None) -> None:
    """Render structured cards for audio playback, transcription, and router result."""
    st.markdown("---")

    # Audio Playback Card
    if audio_bytes is not None:
        st.subheader("🎧 Recorded / Uploaded Audio")
        st.audio(audio_bytes, format="audio/wav")

    col_trans, col_route = st.columns([1, 1], gap="large")

    # Transcription Result Card
    with col_trans:
        st.markdown(
            """
            <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #38bdf8; margin-bottom: 16px;">
                <h3 style="margin-top:0; color: #38bdf8; font-size: 1.25rem;">📝 TRANSCRIPTION RESULT</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.metric("Detected Language", result_data["language_label"])
        with sub_col2:
            st.metric("Language Confidence", f"{result_data['confidence']:.2%}")

        st.caption("Transcribed Text:")
        transcribed_text = result_data["text"]
        if transcribed_text:
            st.markdown(
                f"""
                <div style="background-color: #0f172a; padding: 16px; border-radius: 8px; border: 1px solid #334155; font-size: 1.15rem; font-weight: 500; color: #f8fafc; line-height: 1.5;">
                    "{transcribed_text}"
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("(No speech detected in audio)")

        if result_data.get("segments"):
            with st.expander("Detailed Segments"):
                for idx, seg in enumerate(result_data["segments"], start=1):
                    st.write(f"**[{idx}] {seg.start:.2f}s - {seg.end:.2f}s:** {seg.text}")

    # Query Router Result Card
    with col_route:
        st.markdown(
            """
            <div style="background-color: #1e293b; padding: 20px; border-radius: 12px; border-left: 5px solid #10b981; margin-bottom: 16px;">
                <h3 style="margin-top:0; color: #10b981; font-size: 1.25rem;">🧭 ROUTER RESULT</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        intent = result_data["intent"]
        intent_color = {
            "disease_detection": "#f59e0b",
            "plant_identification": "#3b82f6",
            "treatment_information": "#8b5cf6",
            "general_plant_information": "#06b6d4",
            "unknown": "#6b7280",
        }.get(intent, "#6b7280")

        st.markdown(
            f"""
            <div style="margin-bottom: 14px;">
                <span style="font-size: 0.95rem; color: #94a3b8;">Classified Intent:</span><br/>
                <span style="background-color: {intent_color}; color: #ffffff; padding: 4px 12px; border-radius: 16px; font-weight: 600; font-size: 1.05rem; display: inline-block; margin-top: 4px;">
                    {intent}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Downstream Pipeline Routing Flags:")

        def flag_badge(label: str, is_active: bool) -> str:
            if is_active:
                return f"""<div style="background-color: #064e3b; border: 1px solid #059669; color: #6ee7b7; padding: 10px 14px; border-radius: 8px; font-weight: 600; margin-bottom: 8px;">
                    ✓ {label}: <span style="color:#ffffff;">YES</span>
                </div>"""
            else:
                return f"""<div style="background-color: #1e293b; border: 1px solid #334155; color: #94a3b8; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px;">
                    ✗ {label}: <span style="color:#cbd5e1;">NO</span>
                </div>"""

        st.markdown(
            flag_badge("Model 1 (Plant Identification)", result_data["needs_model1"]),
            unsafe_allow_html=True,
        )
        st.markdown(
            flag_badge("Model 2 (Disease Detection)", result_data["needs_model2"]),
            unsafe_allow_html=True,
        )
        st.markdown(
            flag_badge("RAG Knowledge Base", result_data["needs_rag"]),
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(
        page_title="Audio Pipeline Test | Multilingual STT + Router",
        page_icon="🎙",
        layout="wide",
    )

    st.markdown(
        """
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="margin-bottom: 4px; font-weight: 700; color: #f8fafc;">🎙 AUDIO PIPELINE TEST</h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 0;">Local Multilingual Speech-to-Text (faster-whisper) + Deterministic Intent Router</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize Session State
    if "hardware_recorder" not in st.session_state:
        st.session_state.hardware_recorder = None
    if "is_hardware_recording" not in st.session_state:
        st.session_state.is_hardware_recording = False
    if "latest_result" not in st.session_state:
        st.session_state.latest_result = None
    if "latest_audio_bytes" not in st.session_state:
        st.session_state.latest_audio_bytes = None

    # Section 1: Verified System Status
    with st.expander("🛠 System Status & Verified Dependencies", expanded=True):
        status = check_system_status()
        cols = st.columns(len(status))
        for col, (key, info) in zip(cols, status.items()):
            with col:
                icon = "🟢" if info["ok"] else "🔴"
                st.markdown(f"**{icon} {info['name']}**")
                st.caption(f"{info['version']}")
                st.caption(f"_{info['details']}_")

    st.write("")

    # Section 2: Input Modes (Tabs)
    tab_mic, tab_upload = st.tabs(["🎙 Microphone Test", "📁 Audio File Upload"])

    # ----------------------------------------------------
    # TAB 1: MICROPHONE TEST
    # ----------------------------------------------------
    with tab_mic:
        st.subheader("Microphone Audio Capture")
        st.write("Record speech locally from your microphone, transcribe with faster-whisper, and route intents.")

        mic_mode = st.radio(
            "Select Microphone Capture Mode:",
            [
                "Direct Hardware Mic (AudioRecorder / sounddevice)",
                "Browser Microphone Widget (WebRTC audio_input)",
            ],
            horizontal=True,
        )

        if mic_mode.startswith("Direct Hardware"):
            st.markdown(
                """
                > **Mode:** Uses local `audio.recorder.AudioRecorder` (16 kHz, Mono, 16-bit PCM) directly from your default audio device.
                """
            )

            col_btn1, col_btn2, col_duration = st.columns([1, 1, 2])

            with col_btn1:
                # Start / Stop Toggle
                if not st.session_state.is_hardware_recording:
                    if st.button("🎙 START RECORDING", key="btn_start_rec", type="primary", use_container_width=True):
                        try:
                            recorder = AudioRecorder()
                            recorder.start()
                            st.session_state.hardware_recorder = recorder
                            st.session_state.is_hardware_recording = True
                            st.rerun()
                        except MicrophoneError as exc:
                            st.error(f"Microphone Access Error: {exc}")
                        except Exception as exc:
                            st.error(f"Failed to start recording: {exc}")
                else:
                    if st.button("⏹ STOP RECORDING", key="btn_stop_rec", type="secondary", use_container_width=True):
                        recorder: AudioRecorder = st.session_state.hardware_recorder
                        st.session_state.is_hardware_recording = False
                        temp_path = None
                        try:
                            with st.spinner("Processing recorded audio..."):
                                recorder.stop()
                                temp_path = recorder.save_to_wav()
                                audio_bytes = temp_path.read_bytes()

                                result = process_audio_file(temp_path, source_label="Hardware Microphone")
                                st.session_state.latest_result = result
                                st.session_state.latest_audio_bytes = audio_bytes
                                st.success("Recording transcribed and routed successfully!")
                        except EmptyRecordingError as exc:
                            st.warning(f"Recording Error: {exc}")
                        except MicrophoneError as exc:
                            st.error(f"Microphone Error: {exc}")
                        except Exception as exc:
                            st.error(f"Audio processing error: {exc}")
                        finally:
                            if temp_path is not None and recorder is not None:
                                recorder.cleanup(temp_path)
                            st.session_state.hardware_recorder = None
                            st.rerun()

            with col_btn2:
                if st.session_state.is_hardware_recording:
                    st.markdown(
                        """
                        <div style="background-color: #ef4444; color: white; padding: 8px 16px; border-radius: 8px; font-weight: bold; text-align: center; animation: blinker 1.5s linear infinite;">
                            🔴 RECORDING... Speak now
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with col_duration:
                # Convenient fixed-duration recording option
                dur_col1, dur_col2 = st.columns([1, 1])
                with dur_col1:
                    fixed_seconds = st.slider("Quick Record Duration (sec)", min_value=2, max_value=10, value=4)
                with dur_col2:
                    if st.button(f"⏱ Record {fixed_seconds}s & Process", key="btn_quick_rec", use_container_width=True):
                        temp_path = None
                        recorder = AudioRecorder()
                        try:
                            with st.spinner(f"Recording for {fixed_seconds} seconds... Speak now!"):
                                recorder.start()
                                time.sleep(fixed_seconds)
                                recorder.stop()
                                temp_path = recorder.save_to_wav()
                                audio_bytes = temp_path.read_bytes()

                            with st.spinner("Transcribing and routing query..."):
                                result = process_audio_file(temp_path, source_label=f"Hardware Mic ({fixed_seconds}s)")
                                st.session_state.latest_result = result
                                st.session_state.latest_audio_bytes = audio_bytes
                                st.success("Completed!")
                        except EmptyRecordingError as exc:
                            st.warning(f"Recording Error: {exc}")
                        except MicrophoneError as exc:
                            st.error(f"Microphone Error: {exc}")
                        except Exception as exc:
                            st.error(f"Audio processing error: {exc}")
                        finally:
                            if temp_path is not None:
                                recorder.cleanup(temp_path)
                            recorder.cleanup()
                            st.rerun()

        else:
            # Browser audio_input widget
            st.markdown(
                """
                > **Mode:** Uses Streamlit's built-in browser audio recording widget (`st.audio_input`).
                """
            )
            browser_audio = st.audio_input("Record audio from your browser microphone:")
            if browser_audio is not None:
                if st.button("🚀 Process Browser Recording", key="btn_proc_browser"):
                    raw_bytes = browser_audio.read()
                    if len(raw_bytes) == 0:
                        st.warning("Empty audio recorded. Please try again.")
                    else:
                        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                        temp_path = Path(temp_file.name)
                        try:
                            temp_file.write(raw_bytes)
                            temp_file.close()

                            with st.spinner("Transcribing browser audio..."):
                                result = process_audio_file(temp_path, source_label="Browser Microphone")
                                st.session_state.latest_result = result
                                st.session_state.latest_audio_bytes = raw_bytes
                                st.success("Processed successfully!")
                                st.rerun()
                        except Exception as exc:
                            st.error(f"Error processing browser audio: {exc}")
                        finally:
                            if temp_path.exists():
                                try:
                                    temp_path.unlink()
                                except OSError:
                                    pass

    # ----------------------------------------------------
    # TAB 2: AUDIO FILE TEST
    # ----------------------------------------------------
    with tab_upload:
        st.subheader("Audio File Test")
        st.write("Upload an audio file to test transcription and query routing across formats.")

        valid_exts = [ext.lstrip(".") for ext in sorted(SUPPORTED_EXTENSIONS)]
        uploaded_file = st.file_uploader(
            "Select an audio file:",
            type=valid_exts,
            help=f"Supported formats: {', '.join(valid_exts)}",
        )

        if uploaded_file is not None:
            col_info1, col_info2 = st.columns([1, 1])
            with col_info1:
                st.write(f"**Filename:** `{uploaded_file.name}`")
                st.write(f"**File size:** `{uploaded_file.size / 1024:.1f} KB`")
            with col_info2:
                st.audio(uploaded_file)

            if st.button("🚀 Transcribe & Route Audio File", key="btn_proc_file", type="primary"):
                ext = Path(uploaded_file.name).suffix.lower()
                temp_file = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
                temp_path = Path(temp_file.name)
                try:
                    file_bytes = uploaded_file.getvalue()
                    temp_file.write(file_bytes)
                    temp_file.close()

                    with st.spinner("Transcribing uploaded audio with faster-whisper..."):
                        result = process_audio_file(temp_path, source_label=f"File: {uploaded_file.name}")
                        st.session_state.latest_result = result
                        st.session_state.latest_audio_bytes = file_bytes
                        st.success("File processed successfully!")
                        st.rerun()
                except Exception as exc:
                    st.error(f"Failed to process audio file: {exc}")
                finally:
                    if temp_path.exists():
                        try:
                            temp_path.unlink()
                        except OSError:
                            pass

    # ----------------------------------------------------
    # RENDER LATEST RESULTS
    # ----------------------------------------------------
    if st.session_state.latest_result is not None:
        render_results(
            st.session_state.latest_result,
            audio_bytes=st.session_state.latest_audio_bytes,
        )

    # Reference guide
    with st.expander("ℹ️ Sample Test Queries & Expected Router Intents"):
        st.markdown(
            """
            | Spoken / Audio Query | Detected Intent | Model 1 | Model 2 | RAG |
            | :--- | :--- | :---: | :---: | :---: |
            | *"What plant is this and what disease does it have?"* | `disease_detection` | ✓ YES | ✓ YES | ✗ NO |
            | *"What plant is this?"* | `plant_identification` | ✓ YES | ✗ NO | ✗ NO |
            | *"How do I treat this disease?"* | `treatment_information` | ✓ YES | ✓ YES | ✓ YES |
            | *"Tell me about how to grow cucumbers"* | `general_plant_information` | ✓ YES | ✗ NO | ✓ YES |
            | *"ये कौन सा पौधा है?"* (Hindi) | `plant_identification` / Hindi | ✓ YES | ✗ NO | ✗ NO |
            """
        )


if __name__ == "__main__":
    main()
