"""Video processing and frame extraction module for plant disease prediction.

Provides robust, memory-efficient sequential video decoding, metadata inspection,
FPS-aware frame sampling, lightweight OpenCV-based quality filtering, and
temporary frame lifecycle management.
"""

from video.frame_extractor import (
    EmptyVideoError,
    InvalidVideoError,
    VideoProcessingError,
    get_video_metadata,
    validate_video,
)
from video.processor import (
    FrameQualityFilter,
    cleanup_frames,
    process_video,
)

__all__ = [
    "VideoProcessingError",
    "InvalidVideoError",
    "EmptyVideoError",
    "validate_video",
    "get_video_metadata",
    "FrameQualityFilter",
    "process_video",
    "cleanup_frames",
]
