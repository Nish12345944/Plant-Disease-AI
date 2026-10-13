# Usage:
#   python audio/test_audio.py <path_to_audio_file>
# Examples:
#   python audio/test_audio.py sample.mp3
#   python audio/test_audio.py C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\audio\sample.wav
#
# Notes:
#   - Uses faster-whisper ("small" model) for local speech-to-text.
#   - Language is auto-detected; no query understanding / LLM here.
#   - Designed to be importable later: `from audio.test_audio import transcribe_audio`
"""Standalone audio transcription module (faster-whisper).

Standalone entry point for testing local speech-to-text. Kept isolated so
Model 1 / Model 2, datasets, and training code are untouched.
"""

from __future__ import annotations

import argparse
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = {
    ".wav", ".mp3", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".aac", ".webm",
    ".mp4", ".mov", ".avi", ".mkv", ".m4v",
}

DEFAULT_MODEL_SIZE = "small"

_WHISPER_MODELS: dict[tuple[str, str, str], Any] = {}
_WHISPER_LOCK = threading.Lock()


@dataclass
class TranscriptionSegment:
    """One transcribed segment with timestamps."""

    start: float
    end: float
    text: str


@dataclass
class TranscriptionResult:
    """Full transcription result for one audio file."""

    language: str
    language_probability: float
    text: str
    segments: list = field(default_factory=list)


def has_audio_stream(file_path: str | Path) -> bool:
    """Check if media file has at least one decodable audio stream using PyAV."""
    try:
        import av
        with av.open(str(file_path)) as container:
            return len(container.streams.audio) > 0
    except Exception:
        return False


def validate_audio_path(audio_path_str: str) -> Path:
    """Validate the supplied audio path, raising a clean error if unusable."""
    audio_path = Path(audio_path_str).expanduser()

    if not str(audio_path).strip():
        raise FileNotFoundError("No audio file path was supplied.")
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not audio_path.is_file():
        raise ValueError(f"Not a file: {audio_path}")
    if audio_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(
            f"Unsupported audio format '{audio_path.suffix}'. "
            f"Supported: {supported}"
        )
    return audio_path


def transcribe_audio(
    audio_path_str: str,
    model_size: str = DEFAULT_MODEL_SIZE,
    device: str = "auto",
    compute_type: str = "auto",
) -> TranscriptionResult:
    """Transcribe an audio file with faster-whisper.

    Args:
        audio_path_str: Path to the audio file.
        model_size: faster-whisper model size (default "small").
        device: "auto" (cuda if available else cpu), "cuda", or "cpu".
        compute_type: "auto" picks float16 on CUDA, int8 on CPU.

    Returns:
        TranscriptionResult with language, probability, full text, segments.
    """
    from faster_whisper import WhisperModel

    audio_path = validate_audio_path(audio_path_str)

    # If media container has no audio stream (e.g. silent video), return empty transcription gracefully
    if not has_audio_stream(audio_path):
        return TranscriptionResult(
            language="en",
            language_probability=0.0,
            text="",
            segments=[],
        )

    if device == "auto":
        try:
            import torch

            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"

    if compute_type == "auto":
        compute_type = "float16" if device == "cuda" else "int8"

    cache_key = (model_size, device, compute_type)
    with _WHISPER_LOCK:
        if cache_key not in _WHISPER_MODELS:
            _WHISPER_MODELS[cache_key] = WhisperModel(model_size, device=device, compute_type=compute_type)
        model = _WHISPER_MODELS[cache_key]

        segments_iter, info = model.transcribe(str(audio_path), beam_size=5)

        segments: list = []
        text_parts: list = []
        for seg in segments_iter:
            text = seg.text.strip()
            segments.append(
                TranscriptionSegment(start=seg.start, end=seg.end, text=text)
            )
            text_parts.append(text)

        return TranscriptionResult(
            language=info.language,
            language_probability=info.language_probability,
            text=" ".join(text_parts).strip(),
            segments=segments,
        )


def print_result(result: TranscriptionResult) -> None:
    """Print language, probability, full transcription, and segments."""
    print(f"Detected language      : {result.language}")
    print(f"Language probability   : {result.language_probability:.4f}")
    print()
    print("Complete transcription :")
    print(result.text if result.text else "(empty transcription)")
    print()
    print("Segments [start -> end] :")
    if not result.segments:
        print("  (no segments)")
        return
    for i, seg in enumerate(result.segments, start=1):
        print(f"  [{i}] {seg.start:.2f}s -> {seg.end:.2f}s : {seg.text}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file locally with faster-whisper."
    )
    parser.add_argument(
        "audio_file",
        help="Path to the audio file (wav/mp3/m4a/flac/ogg/opus/wma/aac).",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_SIZE,
        help=f'faster-whisper model size (default: "{DEFAULT_MODEL_SIZE}").',
    )
    return parser


def main(argv: list | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = transcribe_audio(args.audio_file, model_size=args.model)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # e.g. corrupt audio / model load failure
        print(f"Transcription failed: {exc}", file=sys.stderr)
        return 1

    print_result(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
