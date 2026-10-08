"""Microphone audio capture module using sounddevice.

Captures mono audio at 16 kHz from the system default microphone,
saves it to a temporary WAV file, and provides cleanup utilities.
"""

from __future__ import annotations

import logging
import queue
import tempfile
import wave
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1
DEFAULT_DTYPE = "int16"


class AudioRecorderError(Exception):
    """Base exception for audio recording errors."""


class MicrophoneError(AudioRecorderError):
    """Raised when the microphone is unavailable, unreadable, or denied."""


class EmptyRecordingError(AudioRecorderError):
    """Raised when no audio data or negligible audio was recorded."""


class AudioRecorder:
    """Manages audio recording from the default microphone into temporary WAV files."""

    def __init__(
        self,
        sample_rate: int = DEFAULT_SAMPLE_RATE,
        channels: int = DEFAULT_CHANNELS,
        dtype: str = DEFAULT_DTYPE,
        device: Optional[int | str] = None,
    ) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.device = device

        self._audio_queue: queue.Queue = queue.Queue()
        self._stream: Optional[sd.InputStream] = None
        self._is_recording: bool = False
        self._recorded_chunks: list[np.ndarray] = []
        self._active_audio_data: Optional[np.ndarray] = None
        self._created_temp_files: list[Path] = []

    @property
    def is_recording(self) -> bool:
        """Return True if recording is in progress."""
        return self._is_recording

    def _audio_callback(self, indata, frames, time_info, status) -> None:
        """Callback executed by sounddevice in a separate audio thread."""
        if status:
            logger.warning(f"Audio stream status: {status}")
        if self._is_recording:
            self._audio_queue.put(indata.copy())

    def start(self) -> None:
        """Start capturing audio from the default microphone."""
        if self._is_recording:
            logger.warning("Recording is already in progress.")
            return

        # Verify device availability
        try:
            default_dev = sd.default.device[0] if self.device is None else self.device
            if default_dev is None or default_dev < 0:
                raise MicrophoneError("No default input microphone found.")
            device_info = sd.query_devices(default_dev, "input")
            if device_info["max_input_channels"] < self.channels:
                raise MicrophoneError(
                    f"Microphone {device_info['name']} does not support {self.channels} input channel(s)."
                )
        except Exception as exc:
            raise MicrophoneError(f"Failed to access microphone device: {exc}") from exc

        self._recorded_chunks.clear()
        self._active_audio_data = None
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break

        try:
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                device=self.device,
                callback=self._audio_callback,
            )
            self._is_recording = True
            self._stream.start()
        except sd.PortAudioError as exc:
            self._is_recording = False
            raise MicrophoneError(f"PortAudio error starting microphone: {exc}") from exc
        except Exception as exc:
            self._is_recording = False
            raise AudioRecorderError(f"Unexpected error starting stream: {exc}") from exc

    def stop(self) -> np.ndarray:
        """Stop capturing audio and return the recorded numpy array."""
        if not self._is_recording and self._stream is None:
            if self._active_audio_data is not None:
                return self._active_audio_data
            raise AudioRecorderError("Recorder is not running and has no data.")

        self._is_recording = False

        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception as exc:
                logger.warning(f"Error while closing audio stream: {exc}")
            finally:
                self._stream = None

        # Drain queue
        while not self._audio_queue.empty():
            try:
                chunk = self._audio_queue.get_nowait()
                self._recorded_chunks.append(chunk)
            except queue.Empty:
                break

        if not self._recorded_chunks:
            raise EmptyRecordingError("No audio frames were captured.")

        data = np.concatenate(self._recorded_chunks, axis=0)
        # Check duration (at least 0.2s)
        total_samples = len(data)
        duration_sec = total_samples / self.sample_rate
        if duration_sec < 0.2 or total_samples == 0:
            raise EmptyRecordingError(
                f"Recording too short ({duration_sec:.2f}s). Please speak clearly into the microphone."
            )

        self._active_audio_data = data
        return data

    def save_to_wav(self, destination: Optional[str | Path] = None) -> Path:
        """Save the recorded audio data to a WAV file.

        If destination is None, creates a temporary WAV file.
        Returns the Path to the WAV file.
        """
        if self._active_audio_data is None:
            if self._is_recording:
                self.stop()
            else:
                raise AudioRecorderError("No recorded audio data available to save.")

        if destination is None:
            temp_file = tempfile.NamedTemporaryFile(
                prefix="mic_recording_", suffix=".wav", delete=False
            )
            wav_path = Path(temp_file.name).resolve()
            temp_file.close()
            self._created_temp_files.append(wav_path)
        else:
            wav_path = Path(destination).resolve()
            wav_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with wave.open(str(wav_path), "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit PCM = 2 bytes
                wf.setframerate(self.sample_rate)
                wf.writeframes(self._active_audio_data.tobytes())
        except Exception as exc:
            raise AudioRecorderError(f"Failed to write WAV file to {wav_path}: {exc}") from exc

        return wav_path

    def cleanup(self, path: Optional[str | Path] = None) -> None:
        """Delete temporary WAV file(s)."""
        if path is not None:
            target = Path(path).resolve()
            if target.exists():
                try:
                    target.unlink()
                except OSError as exc:
                    logger.warning(f"Could not delete temp file {target}: {exc}")
            if target in self._created_temp_files:
                self._created_temp_files.remove(target)
        else:
            for p in list(self._created_temp_files):
                if p.exists():
                    try:
                        p.unlink()
                    except OSError as exc:
                        logger.warning(f"Could not delete temp file {p}: {exc}")
            self._created_temp_files.clear()

    def __enter__(self) -> AudioRecorder:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._is_recording:
            try:
                self.stop()
            except Exception:
                pass
        self.cleanup()


def record_to_temp_wav(duration: Optional[float] = None) -> Path:
    """Convenience function to record audio to a temporary WAV file.

    If duration is specified, records for that fixed duration in seconds.
    Otherwise, starts recording and caller must manage start/stop using AudioRecorder.
    """
    recorder = AudioRecorder()
    if duration is not None:
        if duration <= 0:
            raise ValueError("Duration must be positive.")
        recorder.start()
        sd.sleep(int(duration * 1000))
        recorder.stop()
        return recorder.save_to_wav()
    else:
        recorder.start()
        return recorder.save_to_wav()
