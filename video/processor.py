"""Video processing, sequential frame sampling, and quality filtering engine."""

from __future__ import annotations

import logging
import math
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import cv2
import numpy as np

from video.frame_extractor import (
    EmptyVideoError,
    InvalidVideoError,
    get_video_metadata,
    validate_video,
)

logger = logging.getLogger(__name__)

DEFAULT_SAMPLE_FPS = 1.0
DEFAULT_JPEG_QUALITY = 95
DEFAULT_MIN_BRIGHTNESS = 25.0
DEFAULT_MAX_BRIGHTNESS = 235.0
DEFAULT_MIN_BLUR_SCORE = 50.0  # Laplacian variance threshold


@dataclass
class QualityFilterConfig:
    """Configurable thresholds for frame quality assessment."""

    min_brightness: float = DEFAULT_MIN_BRIGHTNESS
    max_brightness: float = DEFAULT_MAX_BRIGHTNESS
    min_blur_score: float = DEFAULT_MIN_BLUR_SCORE


class FrameQualityFilter:
    """Lightweight OpenCV-based frame quality filter.

    Detects and filters out empty, severely underexposed, overexposed,
    or blurry frames using computationally lightweight statistical metrics.
    """

    def __init__(self, config: Optional[QualityFilterConfig] = None) -> None:
        self.config = config or QualityFilterConfig()

    def evaluate(self, frame: Optional[np.ndarray]) -> dict[str, Any]:
        """Assess the visual quality of a single frame.

        Args:
            frame: BGR numpy image array.

        Returns:
            Dictionary with:
            - accepted: bool
            - quality_score: float (0.0 to 1.0)
            - reason: str ('accepted', 'empty_frame', 'too_dark', 'too_bright', 'blurry')
            - brightness: float (mean grayscale intensity 0-255)
            - blur_score: float (Laplacian variance)
        """
        if frame is None or frame.size == 0 or frame.ndim < 2:
            return {
                "accepted": False,
                "quality_score": 0.0,
                "reason": "empty_frame",
                "brightness": 0.0,
                "blur_score": 0.0,
            }

        if frame.ndim == 3 and frame.shape[2] == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif frame.ndim == 3 and frame.shape[2] == 4:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        else:
            gray = frame

        mean_brightness = float(np.mean(gray))
        blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

        # Quality scoring components (0.0 to 1.0)
        # 1. Brightness score: symmetric falloff from optimal midpoint 128
        b_score = max(0.0, 1.0 - (abs(mean_brightness - 128.0) / 128.0))

        # 2. Sharpness score: smooth saturation above blur threshold
        # Variance >= 300 gets ~0.95+, variance around 50 gets ~0.45
        s_score = min(1.0, (blur_score / (blur_score + 100.0)) * 1.35)

        # Composite score
        raw_quality = 0.35 * b_score + 0.65 * s_score

        # Rule-based thresholding
        if mean_brightness < self.config.min_brightness:
            return {
                "accepted": False,
                "quality_score": round(min(0.25, raw_quality), 3),
                "reason": "too_dark",
                "brightness": round(mean_brightness, 2),
                "blur_score": round(blur_score, 2),
            }

        if mean_brightness > self.config.max_brightness:
            return {
                "accepted": False,
                "quality_score": round(min(0.25, raw_quality), 3),
                "reason": "too_bright",
                "brightness": round(mean_brightness, 2),
                "blur_score": round(blur_score, 2),
            }

        if blur_score < self.config.min_blur_score:
            return {
                "accepted": False,
                "quality_score": round(min(0.35, raw_quality), 3),
                "reason": "blurry",
                "brightness": round(mean_brightness, 2),
                "blur_score": round(blur_score, 2),
            }

        return {
            "accepted": True,
            "quality_score": round(max(0.40, min(1.0, raw_quality)), 3),
            "reason": "accepted",
            "brightness": round(mean_brightness, 2),
            "blur_score": round(blur_score, 2),
        }


def compute_sample_indices(
    total_frames: int,
    fps: float,
    sample_fps: float = DEFAULT_SAMPLE_FPS,
) -> list[int]:
    """Calculate unique, sorted frame indices to extract based on target sampling rate.

    Args:
        total_frames: Total number of frames in video.
        fps: Native video FPS.
        sample_fps: Desired sampling rate (frames per second).

    Returns:
        Sorted list of integer frame indices.
    """
    if total_frames <= 0:
        return []

    if sample_fps <= 0.0 or fps <= 0.0:
        sample_fps = DEFAULT_SAMPLE_FPS
        fps = 30.0

    step = fps / sample_fps
    if step < 1.0:
        step = 1.0

    indices = []
    current_step = 0.0
    while True:
        idx = int(round(current_step))
        if idx >= total_frames:
            break
        if not indices or idx > indices[-1]:
            indices.append(idx)
        current_step += step

    # Ensure at least the very first frame is sampled if indices is empty
    if not indices and total_frames > 0:
        indices.append(0)

    return indices


def process_video(
    video_path: str | Path,
    sample_fps: float = DEFAULT_SAMPLE_FPS,
    quality_filter: bool = True,
    save_frames: bool = True,
    output_dir: Optional[str | Path] = None,
    jpeg_quality: int = DEFAULT_JPEG_QUALITY,
    filter_config: Optional[QualityFilterConfig] = None,
) -> dict[str, Any]:
    """Process a video file with sequential sampling, quality checks, and frame storage.

    Memory Efficiency:
        Does NOT load the entire video into RAM. Uses sequential OpenCV grab()
        for skipped frames and only decodes frames targeted for sampling.

    Args:
        video_path: Path to the target video.
        sample_fps: Sampling frequency (frames per second, e.g. 1.0 or 2.0).
        quality_filter: Whether to apply the lightweight quality filter.
        save_frames: Whether to write accepted/sampled frames to disk.
        output_dir: Custom directory for temporary frames (default: temp_video_frames/session_<id>).
        jpeg_quality: Compression quality for saved frames (1-100).
        filter_config: Custom quality filter thresholds.

    Returns:
        Structured result dictionary.
    """
    path = validate_video(video_path)
    metadata = get_video_metadata(path)

    total_frames = metadata["frame_count"]
    fps = metadata["fps"]

    sample_indices = compute_sample_indices(total_frames, fps, sample_fps)
    target_indices_set = set(sample_indices)

    # Prepare temporary output directory
    temp_dir_path: Optional[Path] = None
    if save_frames:
        if output_dir is not None:
            temp_dir_path = Path(output_dir).resolve()
        else:
            session_id = uuid.uuid4().hex[:8]
            temp_dir_path = Path("temp_video_frames").resolve() / f"session_{session_id}"
        temp_dir_path.mkdir(parents=True, exist_ok=True)

    q_filter = FrameQualityFilter(filter_config) if quality_filter else None

    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise InvalidVideoError(f"Failed to open video file: {path}")

    frames_result: list[dict[str, Any]] = []
    accepted_count = 0
    rejected_count = 0

    try:
        current_frame_idx = 0
        while current_frame_idx < total_frames:
            if current_frame_idx in target_indices_set:
                ret, frame = cap.read()
                if not ret:
                    logger.warning(
                        f"Premature end of stream reading frame {current_frame_idx} in '{path.name}'"
                    )
                    break

                timestamp = round(current_frame_idx / fps, 3)

                # Quality evaluation
                if q_filter is not None:
                    eval_res = q_filter.evaluate(frame)
                    accepted = eval_res["accepted"]
                    quality_score = eval_res["quality_score"]
                    reason = eval_res["reason"]
                    brightness = eval_res["brightness"]
                    blur_score = eval_res["blur_score"]
                else:
                    accepted = True
                    quality_score = 1.0
                    reason = "accepted (filter_disabled)"
                    brightness = float(np.mean(frame)) if frame is not None else 0.0
                    blur_score = 0.0

                frame_path_str: Optional[str] = None
                if save_frames and temp_dir_path is not None:
                    file_name = f"frame_{current_frame_idx:06d}.jpg"
                    target_file = temp_dir_path / file_name
                    cv2.imwrite(
                        str(target_file),
                        frame,
                        [cv2.IMWRITE_JPEG_QUALITY, int(jpeg_quality)],
                    )
                    frame_path_str = str(target_file)

                if accepted:
                    accepted_count += 1
                else:
                    rejected_count += 1

                frames_result.append(
                    {
                        "frame_index": current_frame_idx,
                        "timestamp_seconds": timestamp,
                        "path": frame_path_str,
                        "quality_score": quality_score,
                        "accepted": accepted,
                        "reason": reason,
                        "brightness": brightness,
                        "blur_score": blur_score,
                    }
                )
            else:
                # Fast skip frame decoding
                ret = cap.grab()
                if not ret:
                    break

            current_frame_idx += 1

    finally:
        cap.release()

    return {
        "video": metadata,
        "sample_fps": sample_fps,
        "sampled_frames": len(frames_result),
        "accepted_frames": accepted_count,
        "rejected_frames": rejected_count,
        "temp_dir": str(temp_dir_path) if temp_dir_path is not None else None,
        "frames": frames_result,
    }


def cleanup_frames(target: Optional[str | Path | dict[str, Any]]) -> None:
    """Safely remove extracted temporary frames and their parent session directory.

    Args:
        target: May be a Path/string to a session directory, or the dictionary returned by process_video.
    """
    if target is None:
        return

    dir_to_remove: Optional[Path] = None

    if isinstance(target, dict):
        temp_dir = target.get("temp_dir")
        if temp_dir:
            dir_to_remove = Path(temp_dir).resolve()
    else:
        p = Path(target).resolve()
        if p.is_dir():
            dir_to_remove = p
        elif p.is_file():
            try:
                p.unlink()
            except OSError as exc:
                logger.warning(f"Failed to delete frame file {p}: {exc}")

    if dir_to_remove is not None and dir_to_remove.exists() and dir_to_remove.is_dir():
        try:
            shutil.rmtree(dir_to_remove)
            logger.info(f"Cleaned up temporary video frames directory: {dir_to_remove}")
        except Exception as exc:
            logger.warning(f"Could not remove temporary directory {dir_to_remove}: {exc}")
