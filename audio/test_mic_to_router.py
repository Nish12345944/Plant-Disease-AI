"""Test live microphone recording piped through faster-whisper and query router.

Complete chain:
Microphone -> Temporary WAV -> transcribe_audio() -> Transcribed text -> route_query()
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path so modules import reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from audio.recorder import (
    AudioRecorder,
    AudioRecorderError,
    EmptyRecordingError,
    MicrophoneError,
)
from audio.test_audio import transcribe_audio
from router.query_router import route_query


def run_mic_test(
    duration: float | None = None,
    audio_file: str | None = None,
) -> int:
    """Run the live microphone to router test or file/duration test."""
    recorder = AudioRecorder()
    temp_wav_path: Path | None = None

    try:
        if audio_file is not None:
            # File bypass mode for verification
            print(f"Using provided audio file: {audio_file}")
            print()
            print("Processing audio...")
            print()
            transcription_result = transcribe_audio(str(audio_file))
        else:
            if duration is not None:
                # Automated duration mode
                print(f"Automated recording for {duration:.1f} seconds...")
                recorder.start()
                print("Recording...")
                print()
                time.sleep(duration)
                recorder.stop()
            else:
                # Standard interactive mode
                input("Press ENTER to start recording...")
                recorder.start()
                print("Recording...")
                print()
                input("Press ENTER to stop recording...")
                recorder.stop()

            print()
            print("Processing audio...")
            print()

            temp_wav_path = recorder.save_to_wav()
            transcription_result = transcribe_audio(str(temp_wav_path))

        language = transcription_result.language
        text = transcription_result.text.strip()

        print(f"Language: {language}")
        print(f"Transcription: {text}")
        print()

        routed = route_query(text)

        print(f"Intent: {routed['intent']}")
        print(f"needs_model1: {routed['needs_model1']}")
        print(f"needs_model2: {routed['needs_model2']}")
        print(f"needs_rag: {routed['needs_rag']}")

        return 0

    except MicrophoneError as exc:
        print(f"\nMicrophone Error: {exc}", file=sys.stderr)
        return 1
    except EmptyRecordingError as exc:
        print(f"\nRecording Error: {exc}", file=sys.stderr)
        return 1
    except AudioRecorderError as exc:
        print(f"\nAudio Recorder Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nRecording cancelled by user.")
        return 130
    except Exception as exc:
        print(f"\nUnexpected error during processing: {exc}", file=sys.stderr)
        return 1
    finally:
        if temp_wav_path is not None:
            recorder.cleanup(temp_wav_path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Record audio from microphone, transcribe with faster-whisper, and route query."
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Optional fixed duration in seconds to record (non-interactive mode).",
    )
    parser.add_argument(
        "--audio-file",
        type=str,
        default=None,
        help="Optional existing audio file path to verify the transcription -> router pipeline.",
    )
    args = parser.parse_args(argv)
    return run_mic_test(duration=args.duration, audio_file=args.audio_file)


if __name__ == "__main__":
    raise SystemExit(main())
