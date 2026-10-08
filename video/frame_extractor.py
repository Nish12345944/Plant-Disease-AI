"""Video validation and metadata extraction utilities."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import cv2

logger = logging.getLogger(__name__)

SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".m4v",
}


class VideoProcessingError(Exception):
    """Base exception for all video processing errors."""


class InvalidVideoError(VideoProcessingError):
    """Raised when the video file cannot be opened, has unsupported format, or is corrupted."""


class EmptyVideoError(VideoProcessingError):
    """Raised when the video contains zero readable or decodable frames."""


def validate_video(video_path: str | Path) -> Path:
    """Validate that a video file exists, has a supported format, and can be decoded.

    Args:
        video_path: Path to the target video file.

    Returns:
        Resolved Path object if valid.

    Raises:
        InvalidVideoError: If file is missing, unreadable, format unsupported, or unopenable.
        EmptyVideoError: If file has no decodable frames.
    """
    if not video_path or not str(video_path).strip():
        raise InvalidVideoError("No video path provided.")

    path = Path(video_path).resolve()

    if not path.exists():
        raise InvalidVideoError(f"Video file does not exist: {path}")

    if not path.is_file():
        raise InvalidVideoError(f"Video path is not a file: {path}")

    if not os.access(path, os.R_OK):
        raise InvalidVideoError(f"Video file is not readable (permission denied): {path}")

    if path.stat().st_size == 0:
        raise EmptyVideoError(f"Video file is empty (0 bytes): {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_VIDEO_EXTENSIONS:
        supported_str = ", ".join(sorted(SUPPORTED_VIDEO_EXTENSIONS))
        raise InvalidVideoError(
            f"Unsupported video extension '{suffix}'. Supported extensions: {supported_str}"
        )

    # Test opening with OpenCV
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise InvalidVideoError(
            f"OpenCV could not open video file '{path.name}'. File may be corrupt or missing a compatible codec."
        )

    try:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            raise EmptyVideoError(
                f"Video '{path.name}' contains zero decodable frames."
            )
    finally:
        cap.release()

    return path


def decode_fourcc(fourcc_val: float | int) -> str:
    """Convert an OpenCV FourCC integer code into a 4-character string."""
    try:
        int_code = int(fourcc_val)
        if int_code <= 0:
            return "unknown"
        chars = [
            chr((int_code >> (8 * i)) & 0xFF)
            for i in range(4)
        ]
        decoded = "".join(chars).strip()
        # Ensure printable ascii
        if all(32 <= ord(c) <= 126 for c in decoded):
            return decoded
        return f"0x{int_code:08X}"
    except Exception:
        return "unknown"


def get_video_metadata(video_path: str | Path) -> dict[str, Any]:
    """Extract metadata from a video file with robust fallback handling.

    Args:
        video_path: Path to the target video file.

    Returns:
        Dictionary containing:
        - filename: str
        - width: int
        - height: int
        - fps: float
        - frame_count: int
        - duration_seconds: float
        - codec: str
        - is_estimated: bool

    Raises:
        InvalidVideoError: If video cannot be opened.
        EmptyVideoError: If video contains no frames.
    """
    path = validate_video(video_path)

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise InvalidVideoError(f"Failed to open video for metadata inspection: {path}")

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        raw_fps = cap.get(cv2.CAP_PROP_FPS)
        raw_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc_val = cap.get(cv2.CAP_PROP_FOURCC)
        codec = decode_fourcc(fourcc_val)

        is_estimated = False

        # Fallback handling for FPS
        if raw_fps is None or raw_fps <= 0.0 or raw_fps != raw_fps:  # nan check
            fps = 30.0  # sensible standard default
            is_estimated = True
            logger.warning(f"FPS could not be detected for '{path.name}'; defaulting to 30.0.")
        else:
            fps = round(float(raw_fps), 3)

        # Fallback handling for frame count
        frame_count = raw_count if raw_count > 0 else 0
        if frame_count <= 0:
            # Try manual probe if frame count property is unavailable
            logger.info(f"Frame count property unavailable for '{path.name}', probing frames...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            count = 0
            while cap.grab():
                count += 1
            frame_count = count
            is_estimated = True

        duration_seconds = round(frame_count / fps, 3) if (fps > 0 and frame_count > 0) else 0.0

        return {
            "filename": path.name,
            "path": str(path),
            "width": width,
            "height": height,
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration_seconds,
            "codec": codec,
            "is_estimated": is_estimated,
        }
    finally:
        cap.release()
