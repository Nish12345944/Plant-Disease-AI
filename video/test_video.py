"""Command-line test runner for the video processing module.

Usage:
    python video/test_video.py <video_path> [--sample-fps 1.0] [--no-preview] [--cleanup]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from video.frame_extractor import (
    EmptyVideoError,
    InvalidVideoError,
    VideoProcessingError,
)
from video.processor import cleanup_frames, process_video

PREVIEW_DIR = PROJECT_ROOT / "reports" / "video_samples"
MAX_PREVIEW_FRAMES = 12


def create_contact_sheet(
    sample_paths: list[Path], output_path: Path, thumb_size: tuple[int, int] = (320, 180)
) -> None:
    """Create a clean 2D contact sheet montage of sampled frames."""
    if not sample_paths:
        return

    images = []
    for p in sample_paths:
        img = cv2.imread(str(p))
        if img is not None:
            thumb = cv2.resize(img, thumb_size, interpolation=cv2.INTER_AREA)
            # Add small label overlay
            cv2.putText(
                thumb,
                p.stem,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            images.append(thumb)

    if not images:
        return

    # Determine grid (e.g. up to 4 cols)
    cols = min(4, len(images))
    rows = (len(images) + cols - 1) // cols

    # Pad images to fill grid
    blank = images[0] * 0
    while len(images) < rows * cols:
        images.append(blank.copy())

    grid_rows = []
    for r in range(rows):
        row_imgs = images[r * cols : (r + 1) * cols]
        grid_rows.append(cv2.hconcat(row_imgs))

    montage = cv2.vconcat(grid_rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), montage, [cv2.IMWRITE_JPEG_QUALITY, 92])


def save_preview_samples(
    result: dict, target_dir: Path = PREVIEW_DIR, max_frames: int = MAX_PREVIEW_FRAMES
) -> list[Path]:
    """Copy up to max_frames extracted frames to reports/video_samples for visual inspection."""
    target_dir.mkdir(parents=True, exist_ok=True)

    # Filter to frames that exist on disk
    existing_frames = [
        f for f in result.get("frames", [])
        if f.get("path") and Path(f["path"]).exists()
    ]

    # Prioritize accepted frames first, but include samples across the duration
    if not existing_frames:
        return []

    step = max(1, len(existing_frames) // max_frames)
    selected = existing_frames[::step][:max_frames]

    copied_paths: list[Path] = []
    for idx, f_info in enumerate(selected, start=1):
        src_path = Path(f_info["path"])
        dest_path = target_dir / f"sample_{idx:02d}_{src_path.stem}.jpg"
        shutil.copy2(src_path, dest_path)
        copied_paths.append(dest_path)

    # Also build a contact sheet montage for quick inspection
    contact_sheet_path = target_dir / "contact_sheet.jpg"
    create_contact_sheet(copied_paths, contact_sheet_path)

    return copied_paths


def run_test(
    video_path: str,
    sample_fps: float = 1.0,
    save_preview: bool = True,
    cleanup: bool = False,
) -> int:
    """Execute video test and display formatted terminal summary."""
    try:
        result = process_video(
            video_path=video_path,
            sample_fps=sample_fps,
            quality_filter=True,
            save_frames=True,
        )
    except InvalidVideoError as exc:
        print(f"\n[ERROR] Invalid Video: {exc}", file=sys.stderr)
        return 1
    except EmptyVideoError as exc:
        print(f"\n[ERROR] Empty Video: {exc}", file=sys.stderr)
        return 1
    except VideoProcessingError as exc:
        print(f"\n[ERROR] Video Processing Failure: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"\n[ERROR] Unexpected Failure: {exc}", file=sys.stderr)
        return 1

    v = result["video"]

    print("==================================================")
    print("VIDEO TEST")
    print("==================================================")
    print()
    print("File:")
    print(v["filename"])
    print()
    print("Resolution:")
    print(f"{v['width']} x {v['height']}")
    print()
    print("FPS:")
    print(f"{v['fps']:.1f}")
    print()
    print("Frames:")
    print(v["frame_count"])
    print()
    print("Duration:")
    print(f"{v['duration_seconds']:.1f} sec")
    print()
    print("Sampling:")
    print(f"{result['sample_fps']:.1f} FPS")
    print()
    print("Sampled frames:")
    print(result["sampled_frames"])
    print()
    print("Accepted frames:")
    print(result["accepted_frames"])
    print()
    print("Rejected frames:")
    print(result["rejected_frames"])
    print()
    print("Temporary frame directory:")
    print(result.get("temp_dir") or "(none)")
    print()
    print("==================================================")
    print(f"{'Frame':<8} {'Time':<10} {'Quality':<12} {'Status':<12} {'Reason':<16}")
    print("-" * 58)

    for f in result.get("frames", []):
        status_str = "ACCEPTED" if f["accepted"] else "REJECTED"
        print(
            f"{f['frame_index']:<8} "
            f"{f['timestamp_seconds']:.2f}s{'':<5} "
            f"{f['quality_score']:.2f}{'':<8} "
            f"{status_str:<12} "
            f"{f['reason']:<16}"
        )

    print("==================================================")

    # Handle visual previews
    if save_preview:
        saved = save_preview_samples(result)
        print(f"\nVisual preview: Saved {len(saved)} sample frames to: {PREVIEW_DIR}")
        print(f"Contact sheet : {PREVIEW_DIR / 'contact_sheet.jpg'}")

    if cleanup:
        cleanup_frames(result)
        print(f"\nTemporary directory cleaned up: {result.get('temp_dir')}")

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Test video validation, metadata extraction, sampling, and quality filtering."
    )
    parser.add_argument("video_path", help="Path to target video file.")
    parser.add_argument(
        "--sample-fps",
        type=float,
        default=1.0,
        help="Frame sampling rate in FPS (default: 1.0).",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable copying preview sample frames to reports/video_samples.",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up the temporary frame session directory after test completes.",
    )
    args = parser.parse_args(argv)
    return run_test(
        video_path=args.video_path,
        sample_fps=args.sample_fps,
        save_preview=not args.no_preview,
        cleanup=args.cleanup,
    )


if __name__ == "__main__":
    raise SystemExit(main())
