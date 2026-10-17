"""Video Inference Pipeline for Model 1 Plant/Crop Identification.

Performs uniform temporal frame sampling (targeting 16-24 frames across video duration),
applies tight candidate plant-region (ROI) localization before Model 1 inference to isolate foliage
from people, clothing, and greenhouse structures, runs Model 1 inference on plant-focused regions,
and aggregates predictions via mean softmax probabilities across all reliable plant frames.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Optional, Union

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

from model1_test_app.inference import (
    format_class_name,
    get_eval_transform,
    normalize_crop_id,
)
from model1_test_app.plant_detector import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_MIN_BLUR_SCORE,
    assess_plant_presence_and_quality,
    extract_tight_plant_rois,
)
from video.frame_extractor import get_video_metadata, validate_video
from video.processor import FrameQualityFilter, QualityFilterConfig

logger = logging.getLogger(__name__)

# Video sampling frame targets
DEFAULT_SAMPLE_FPS = 2.0
TARGET_FRAMES_DEFAULT = None  # None indicates dynamic computation based on sample_fps & video duration
FALLBACK_TARGET_FRAMES = 8
MIN_TARGET_FRAMES = 4
MAX_TARGET_FRAMES = 60
MAX_FRAME_DIMENSION = 512
MAX_VIDEO_DURATION_SECONDS = 30.0
MAX_VIDEO_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB
DUPLICATE_DIFF_THRESHOLD = 2.0  # Mean pixel diff threshold for duplicate frames
SCENE_CHANGE_DIFF_THRESHOLD = 15.0  # Pixel diff threshold for scene transition

__all__ = [
    "DEFAULT_SAMPLE_FPS",
    "TARGET_FRAMES_DEFAULT",
    "FALLBACK_TARGET_FRAMES",
    "MIN_TARGET_FRAMES",
    "MAX_TARGET_FRAMES",
    "MAX_FRAME_DIMENSION",
    "MAX_VIDEO_DURATION_SECONDS",
    "MAX_VIDEO_SIZE_BYTES",
    "DUPLICATE_DIFF_THRESHOLD",
    "SCENE_CHANGE_DIFF_THRESHOLD",
    "compute_frame_difference",
    "predict_video",
    "extract_adaptive_video_frames",
    "compute_uniform_indices",
]

# Non-destructive quality filter defaults to preserve macro close-ups and low-depth-of-field shots
DEFAULT_VIDEO_FILTER_CONFIG = QualityFilterConfig(
    min_brightness=15.0,
    max_brightness=248.0,
    min_blur_score=10.0,
)


def compute_frame_difference(img1_bgr: Optional[np.ndarray], img2_bgr: Optional[np.ndarray]) -> float:
    """Calculate mean absolute pixel difference on tiny 32x32 grayscale thumbnails for fast deduplication."""
    if img1_bgr is None or img2_bgr is None:
        return 999.0
    try:
        g1 = cv2.resize(cv2.cvtColor(img1_bgr, cv2.COLOR_BGR2GRAY), (32, 32))
        g2 = cv2.resize(cv2.cvtColor(img2_bgr, cv2.COLOR_BGR2GRAY), (32, 32))
        return float(np.mean(np.abs(g1.astype(np.float32) - g2.astype(np.float32))))
    except Exception:
        return 999.0


def compute_uniform_indices(total_frames: int, num_samples: int) -> list[int]:
    """Calculate deduplicated integer frame indices uniformly spaced across [0, total_frames - 1]."""
    if total_frames <= 0 or num_samples <= 0:
        return []
    if num_samples >= total_frames:
        return list(range(total_frames))

    raw_indices = np.linspace(0, total_frames - 1, num=num_samples, dtype=int)
    seen = set()
    indices = []
    for idx in raw_indices:
        idx_int = int(idx)
        if idx_int not in seen:
            seen.add(idx_int)
            indices.append(idx_int)

    return sorted(indices)


def extract_adaptive_video_frames(
    video_path: Union[str, Path],
    target_frames: Optional[int] = None,
    sample_fps: Optional[float] = DEFAULT_SAMPLE_FPS,
    min_target: int = MIN_TARGET_FRAMES,
    max_target: int = MAX_TARGET_FRAMES,
    quality_filter: bool = True,
    filter_config: Optional[QualityFilterConfig] = None,
    thumbnail_size: tuple[int, int] = (320, 240),
    max_frame_dimension: int = MAX_FRAME_DIMENSION,
    max_duration_seconds: float = MAX_VIDEO_DURATION_SECONDS,
) -> dict[str, Any]:
    """Extract bounded representative frames uniformly across video duration with early downscaling and deduplication.

    Args:
        video_path: Path to target video file.
        target_frames: Optional explicit target frame count. If None, computed from duration * sample_fps.
        sample_fps: Desired sampling rate (default: 2.0 FPS -> ~20 frames for 10s video).
        min_target: Minimum target frame count (default: 4).
        max_target: Maximum target frame count to bound memory/compute (default: 60).
        quality_filter: Whether to filter out dark, bright, or blurry frames.
        filter_config: Thresholds for quality filter.
        thumbnail_size: Target size for UI preview thumbnails.
        max_frame_dimension: Maximum dimension to downscale frames to immediately (default: 512).
        max_duration_seconds: Enforce maximum video duration limit in seconds (default: 30.0).

    Returns:
        Dictionary containing selected_frames, rejected_frames, and metadata.
    """
    v_path = validate_video(video_path)
    metadata = get_video_metadata(v_path, max_duration_seconds=max_duration_seconds)
    total_frames = metadata["frame_count"]
    fps = metadata["fps"] if metadata["fps"] > 0 else 30.0
    duration_sec = metadata.get("duration_seconds", 0.0)

    if total_frames <= 0:
        raise ValueError(f"Video '{v_path.name}' has 0 decodable frames.")

    # Resolve target frames dynamically:
    # 1. If explicit positive target_frames is passed, honor it.
    # 2. Otherwise compute based on duration * sample_fps (targeting 2 FPS -> ~20 frames for 10s).
    parsed_target: Optional[int] = None
    if target_frames is not None:
        try:
            parsed_target = int(target_frames.default if hasattr(target_frames, "default") else target_frames)
        except Exception:
            parsed_target = None

    if parsed_target is not None and parsed_target > 0:
        desired_target = parsed_target
    else:
        eff_fps = float(sample_fps) if (sample_fps is not None and float(sample_fps) > 0) else DEFAULT_SAMPLE_FPS
        if duration_sec > 0:
            desired_target = int(round(duration_sec * eff_fps))
        else:
            desired_target = FALLBACK_TARGET_FRAMES

    desired_target = max(min_target, min(max_target, desired_target))
    effective_target = min(desired_target, total_frames)
    if total_frames < min_target:
        effective_target = total_frames

    q_filter = FrameQualityFilter(filter_config or DEFAULT_VIDEO_FILTER_CONFIG) if quality_filter else None

    # Step 1: Initial candidate pool uniformly distributed across duration (spanning start to finish)
    initial_pool_size = min(total_frames, max(effective_target, int(effective_target * 1.5)))
    candidate_indices = compute_uniform_indices(total_frames, initial_pool_size)

    cap = cv2.VideoCapture(str(v_path))
    if not cap.isOpened():
        raise IOError(f"Could not open video file: {v_path}")

    accepted_pool: list[dict[str, Any]] = []
    rejected_pool: list[dict[str, Any]] = []
    evaluated_indices = set()

    def evaluate_index(idx: int) -> bool:
        evaluated_indices.add(idx)
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame_bgr = cap.read()
        if not ret or frame_bgr is None or frame_bgr.size == 0:
            return False

        t_sec = round(idx / fps, 3)

        # Early downscale to bound memory and CPU footprint (max 512px)
        h, w = frame_bgr.shape[:2]
        if max(h, w) > max_frame_dimension:
            scale = max_frame_dimension / float(max(h, w))
            frame_bgr = cv2.resize(frame_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

        if q_filter is not None:
            q_res = q_filter.evaluate(frame_bgr)
            is_acc = q_res["accepted"]
            q_score = q_res["quality_score"]
            reason = q_res["reason"]
        else:
            is_acc = True
            q_score = 1.0
            reason = "accepted (filter_disabled)"

        # Check for near-identical duplicate frames against the last accepted frame
        is_dup = False
        if is_acc and accepted_pool:
            prev_bgr = accepted_pool[-1].get("frame_bgr")
            if prev_bgr is not None and compute_frame_difference(frame_bgr, prev_bgr) < DUPLICATE_DIFF_THRESHOLD:
                is_dup = True
                # In low-motion or synthetic videos, do not discard if pool would be starved below effective_target
                if len(accepted_pool) >= effective_target:
                    is_acc = False
                    reason = "near-identical duplicate frame skipped"
                else:
                    reason = "accepted (low-motion frame)"

        # Resized RGB & BGR
        full_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(full_rgb)

        # In-memory thumbnail for UI
        thumb_bgr = cv2.resize(frame_bgr, thumbnail_size, interpolation=cv2.INTER_AREA)
        thumb_rgb = cv2.cvtColor(thumb_bgr, cv2.COLOR_BGR2RGB)
        thumb_pil = Image.fromarray(thumb_rgb)

        record = {
            "frame_index": idx,
            "timestamp_seconds": t_sec,
            "accepted": is_acc,
            "is_duplicate": is_dup,
            "reason": reason,
            "quality_score": q_score,
            "thumbnail": thumb_pil,
            "frame_image": frame_pil,
            "frame_bgr": frame_bgr,
        }

        if is_acc:
            accepted_pool.append(record)
            return True
        else:
            rejected_pool.append(record)
            return False

    for idx in candidate_indices:
        evaluate_index(idx)

    # Step 2: Adaptive replenishment if needed
    if len(accepted_pool) < effective_target and len(evaluated_indices) < total_frames:
        step_stride = max(1, total_frames // max(1, effective_target * 3))
        secondary_indices = [
            i for i in range(0, total_frames, step_stride) if i not in evaluated_indices
        ]
        for idx in secondary_indices:
            evaluate_index(idx)
            if len(accepted_pool) >= effective_target:
                break

    cap.release()

    # Step 3: Select final frames
    if len(accepted_pool) > effective_target:
        sub_indices = np.linspace(0, len(accepted_pool) - 1, num=effective_target, dtype=int)
        selected_frames = [accepted_pool[i] for i in sub_indices]
    elif accepted_pool:
        selected_frames = accepted_pool
    else:
        best_rejected = sorted(rejected_pool, key=lambda x: x.get("quality_score", 0.0), reverse=True)
        selected_frames = best_rejected[:effective_target]

    selected_frames = sorted(selected_frames, key=lambda x: x["frame_index"])

    # Release heavy buffers from rejected frames to prevent memory spikes (preserving any chosen fallback frames)
    selected_ids = {id(f) for f in selected_frames}
    for r in rejected_pool:
        if id(r) not in selected_ids:
            r["frame_bgr"] = None
            r["frame_image"] = None

    status_note = None
    if len(selected_frames) < min_target:
        status_note = f"Only {len(selected_frames)} usable frames available across video."

    return {
        "metadata": metadata,
        "selected_frames": selected_frames,
        "rejected_frames": rejected_pool,
        "total_evaluated": len(evaluated_indices),
        "total_decoded": total_frames,
        "target_frames": effective_target,
        "sample_fps": sample_fps or DEFAULT_SAMPLE_FPS,
        "status_note": status_note,
    }


def predict_video(
    video_path: Union[str, Path],
    model: nn.Module,
    idx_to_class: dict[int, str],
    device: torch.device,
    target_frames: Optional[int] = None,
    sample_fps: Optional[float] = DEFAULT_SAMPLE_FPS,
    min_target: int = MIN_TARGET_FRAMES,
    max_target: int = MAX_TARGET_FRAMES,
    quality_filter: bool = True,
    top_k: int = 3,
    filter_config: Optional[QualityFilterConfig] = None,
    blur_threshold: Optional[float] = None,
    save_debug_rois: bool = False,
    debug_dir: Optional[str | Path] = "reports/video_debug",
    detect_disease: bool = True,
    disease_conf_threshold: float = 0.20,
    **kwargs: Any,
) -> dict[str, Any]:
    """Execute complete video inference: sample representative frames, extract tight plant ROIs, predict with Model 1, detect disease with Model 2, and aggregate.

    Pipeline:
        FULL FRAME -> candidate tight plant ROI extraction -> Model 1 crop inference -> Model 2 disease detection on plant ROI -> Aggregation
    """
    effective_blur_threshold = blur_threshold if blur_threshold is not None else DEFAULT_MIN_BLUR_SCORE

    extraction = extract_adaptive_video_frames(
        video_path=video_path,
        target_frames=target_frames,
        sample_fps=sample_fps,
        min_target=min_target,
        max_target=max_target,
        quality_filter=quality_filter,
        filter_config=filter_config or QualityFilterConfig(min_blur_score=effective_blur_threshold),
    )

    metadata = extraction["metadata"]
    selected_frames = extraction["selected_frames"]
    rejected_frames = extraction["rejected_frames"]
    status_note = extraction["status_note"]

    transform = get_eval_transform()
    num_classes = len(idx_to_class)

    frame_records: list[dict[str, Any]] = []
    valid_plant_prob_vectors: list[np.ndarray] = []
    valid_plant_weights: list[float] = []
    valid_plant_classes: list[str] = []
    video_disease_detections: list[dict[str, Any]] = []
    prev_contributed_bgr: Optional[np.ndarray] = None

    model1_inference_count = 0
    prev_best_roi_bgr: Optional[np.ndarray] = None
    prev_best_probs: Optional[np.ndarray] = None
    prev_smoothed_probs: Optional[np.ndarray] = None
    prev_scene_bgr: Optional[np.ndarray] = None

    if save_debug_rois and debug_dir:
        os.makedirs(debug_dir, exist_ok=True)

    for seq_num, f_data in enumerate(selected_frames, start=1):
        idx = f_data["frame_index"]
        t_sec = f_data["timestamp_seconds"]
        q_score = f_data["quality_score"]
        thumb = f_data["thumbnail"]
        frame_img = f_data.get("frame_image")
        frame_bgr = f_data.get("frame_bgr")

        # Save original debug frame only if explicitly requested
        if save_debug_rois and debug_dir and frame_bgr is not None:
            orig_debug_path = os.path.join(debug_dir, f"frame_{seq_num:03d}_idx_{idx:03d}_original.jpg")
            cv2.imwrite(orig_debug_path, frame_bgr)

        # Assess frame usability and extract tight plant-focused candidate regions
        assessment = assess_plant_presence_and_quality(
            frame_bgr if frame_bgr is not None else frame_img,
            min_blur_score=effective_blur_threshold,
        )
        f_status = assessment["status"]
        f_reason = assessment["reason"]
        candidate_rois = assessment.get("rois", [])

        if f_status in ("low_quality", "blurry"):
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "low_quality",
                "predicted_label": "Low Quality",
                "status": "low_quality",
                "confidence": 0.0,
                "percentage": "N/A",
                "reason": f_reason,
                "rejection_reason": f_reason,
                "contributed_to_crop": False,
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": None,
                "roi_annotated_thumbnail": None,
                "roi_box": None,
                "rois_found": 0,
                "assessment": assessment,
                "top_k": [],
                "disease_detections": [],
            })
            f_data["frame_bgr"] = None
            f_data["frame_image"] = None
            continue

        if f_status in ("no_plant_evidence", "unknown") or not candidate_rois:
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "no_plant_evidence",
                "predicted_label": "No Plant Evidence",
                "status": "no_plant_evidence",
                "confidence": 0.0,
                "percentage": "N/A",
                "reason": f_reason or "No plant specimen found in frame",
                "rejection_reason": f_reason or "No plant specimen found in frame",
                "contributed_to_crop": False,
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": None,
                "roi_annotated_thumbnail": None,
                "roi_box": None,
                "rois_found": 0,
                "assessment": assessment,
                "top_k": [],
                "disease_detections": [],
            })
            f_data["frame_bgr"] = None
            f_data["frame_image"] = None
            continue

        # Evaluate candidate plant ROIs with Model 1 (cap to top-2 candidate ROIs by detector score)
        candidate_rois_eval = sorted(candidate_rois, key=lambda r: r.get("score", 0.0), reverse=True)[:2]
        roi_results = []
        for r_idx, roi_dict in enumerate(candidate_rois_eval):
            roi_pil = roi_dict["roi_pil"]
            roi_bgr = roi_dict.get("roi_bgr")

            # Avoid re-running Model 1 inference on duplicate or near-identical plant ROIs
            if (prev_best_roi_bgr is not None
                and roi_bgr is not None
                and compute_frame_difference(roi_bgr, prev_best_roi_bgr) < DUPLICATE_DIFF_THRESHOLD
                and prev_best_probs is not None):
                probs = prev_best_probs
                top_idx = int(np.argmax(probs))
                top_cls_name = idx_to_class[top_idx]
                top_conf = float(probs[top_idx])
            else:
                tensor = transform(roi_pil).unsqueeze(0).to(device)
                with torch.no_grad():
                    logits = model(tensor)
                    probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

                model1_inference_count += 1
                top_idx = int(np.argmax(probs))
                top_cls_name = idx_to_class[top_idx]
                top_conf = float(probs[top_idx])

            roi_results.append({
                "roi_index": r_idx,
                "box": roi_dict["box"],
                "score": roi_dict["score"],
                "plant_density": roi_dict.get("plant_density", 0.5),
                "is_macro": roi_dict.get("is_macro", False),
                "sharpness": roi_dict.get("sharpness", 100.0),
                "probs": probs,
                "top_idx": top_idx,
                "top_class": top_cls_name,
                "top_conf": top_conf,
                "roi_pil": roi_pil,
                "roi_bgr": roi_bgr,
            })

        # Select the best plant ROI for this frame (highest confidence plant classification)
        best_roi = max(roi_results, key=lambda r: r["top_conf"])
        primary_roi = roi_results[0] if roi_results else best_roi
        primary_roi_pil = primary_roi.get("roi_pil") if primary_roi else None
        best_probs = best_roi["probs"]
        best_top_cls = best_roi["top_class"]
        best_top_conf = best_roi["top_conf"]
        best_box = best_roi["box"]
        best_roi_pil = best_roi["roi_pil"]
        best_roi_bgr = best_roi.get("roi_bgr")

        prev_best_roi_bgr = best_roi_bgr
        prev_best_probs = best_probs

        # Temporal smoothing across continuous scenes to stabilize frame-level crop predictions
        scene_diff = compute_frame_difference(frame_bgr, prev_scene_bgr) if (prev_scene_bgr is not None and frame_bgr is not None) else 999.0
        if prev_smoothed_probs is not None and scene_diff < SCENE_CHANGE_DIFF_THRESHOLD:
            smoothed_probs = 0.65 * best_probs + 0.35 * prev_smoothed_probs
        else:
            smoothed_probs = best_probs.copy()
        prev_smoothed_probs = smoothed_probs
        prev_scene_bgr = frame_bgr

        smoothed_top_idx = int(np.argmax(smoothed_probs))
        smoothed_top_cls = idx_to_class[smoothed_top_idx]
        smoothed_top_conf = float(smoothed_probs[smoothed_top_idx])

        # Save ROI debug image only if explicitly requested
        if save_debug_rois and debug_dir and best_roi_bgr is not None:
            roi_debug_path = os.path.join(debug_dir, f"frame_{seq_num:03d}_idx_{idx:03d}_roi.jpg")
            cv2.imwrite(roi_debug_path, best_roi_bgr)

        # Thumbnail of the selected plant crop
        roi_thumb = best_roi_pil.resize((240, 240), Image.Resampling.LANCZOS)
        roi_annotated_thumb = roi_thumb

        # Top-K for this frame (from temporally stabilized probabilities)
        top_k_indices = np.argsort(smoothed_probs)[::-1][:top_k]
        frame_top_k = []
        for r, c in enumerate(top_k_indices, start=1):
            raw_c = idx_to_class[int(c)]
            canonical_c = normalize_crop_id(raw_c) or raw_c
            frame_top_k.append({
                "rank": r,
                "class_name": canonical_c,
                "label": format_class_name(canonical_c),
                "confidence": float(smoothed_probs[c]),
                "percentage": f"{float(smoothed_probs[c]) * 100:.2f}%",
            })

        if smoothed_top_conf < DEFAULT_CONFIDENCE_THRESHOLD:
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "crop_uncertain",
                "predicted_label": "Crop Uncertain",
                "status": "crop_uncertain",
                "confidence": smoothed_top_conf,
                "raw_confidence": best_top_conf,
                "raw_class": best_top_cls,
                "percentage": f"{smoothed_top_conf * 100:.2f}% (Low Conf)",
                "reason": f"Crop identity uncertain ({smoothed_top_conf * 100:.1f}% < {DEFAULT_CONFIDENCE_THRESHOLD * 100:.0f}%)",
                "rejection_reason": f"Crop identity uncertain ({smoothed_top_conf * 100:.1f}% < {DEFAULT_CONFIDENCE_THRESHOLD * 100:.0f}%)",
                "contributed_to_crop": False,
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": roi_thumb,
                "roi_annotated_thumbnail": roi_annotated_thumb,
                "roi_pil": best_roi_pil,
                "primary_roi_pil": primary_roi_pil,
                "roi_box": best_box,
                "rois_found": len(candidate_rois),
                "assessment": assessment,
                "top_k": frame_top_k,
                "disease_detections": [],
            })
        else:
            canonical_best = normalize_crop_id(smoothed_top_cls) or smoothed_top_cls
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": canonical_best,
                "predicted_label": format_class_name(canonical_best),
                "status": "valid_plant_roi",
                "confidence": smoothed_top_conf,
                "raw_confidence": best_top_conf,
                "raw_class": best_top_cls,
                "percentage": f"{smoothed_top_conf * 100:.2f}%",
                "reason": f"Identified from tight plant ROI {best_box}",
                "rejection_reason": None,
                "contributed_to_crop": True,
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": roi_thumb,
                "roi_annotated_thumbnail": roi_annotated_thumb,
                "roi_pil": best_roi_pil,
                "primary_roi_pil": primary_roi_pil,
                "roi_box": best_box,
                "rois_found": len(candidate_rois),
                "assessment": assessment,
                "top_k": frame_top_k,
                "disease_detections": [],
            })

            # Calculate frame weight for robust crop aggregation
            is_macro = best_roi.get("is_macro", False)
            plant_density = best_roi.get("plant_density", 0.5)
            sharpness = best_roi.get("sharpness", 100.0)
            is_dup = (
                prev_contributed_bgr is not None
                and best_roi_bgr is not None
                and compute_frame_difference(best_roi_bgr, prev_contributed_bgr) < DUPLICATE_DIFF_THRESHOLD
            )
            f_weight = (2.0 if is_macro else 1.0) * (0.5 + 0.5 * plant_density) * min(1.5, max(0.5, sharpness / 150.0))
            if is_dup and not is_macro:
                f_weight *= 0.5  # Discount consecutive duplicate non-macro shots

            valid_plant_prob_vectors.append(smoothed_probs)
            valid_plant_weights.append(f_weight)
            valid_plant_classes.append(canonical_best)
            prev_contributed_bgr = best_roi_bgr

        # Release heavy frame buffers immediately after ROI inference to bound memory
        f_data["frame_bgr"] = None
        f_data["frame_image"] = None

    # Step 5: Final Aggregated Video Prediction across all valid frames
    if valid_plant_prob_vectors:
        weights_arr = np.array(valid_plant_weights, dtype=np.float32)
        total_weight = float(np.sum(weights_arr))
        if total_weight > 0:
            norm_weights = weights_arr / total_weight
            mean_prob_vector = np.sum([w * p for w, p in zip(norm_weights, valid_plant_prob_vectors)], axis=0)
        else:
            mean_prob_vector = np.mean(valid_plant_prob_vectors, axis=0)

        from collections import Counter
        crop_counts = Counter(valid_plant_classes)
        crop_support_counts = dict(crop_counts)
        dominant_crop, max_support = crop_counts.most_common(1)[0]
        support_ratio = max_support / len(valid_plant_classes)
        crop_disagreement = round(1.0 - support_ratio, 3)

        sorted_class_indices = np.argsort(mean_prob_vector)[::-1]
        top_c_idx = int(sorted_class_indices[0])
        top_mean_conf = float(mean_prob_vector[top_c_idx])

        final_top_k = []
        for rank, c_idx in enumerate(sorted_class_indices[: min(top_k, num_classes)], start=1):
            raw_c = idx_to_class[int(c_idx)]
            canonical_c = normalize_crop_id(raw_c) or raw_c
            conf = float(mean_prob_vector[c_idx])
            final_top_k.append({
                "rank": rank,
                "class_id": int(c_idx),
                "class_name": canonical_c,
                "label": format_class_name(canonical_c),
                "confidence": conf,
                "percentage": f"{conf * 100:.2f}%",
            })

        # Safeguard: if crop predictions conflict (disagreement > 60% or when multiple frames exist and dominant has < 40% support)
        if crop_disagreement > 0.60 or (len(valid_plant_classes) >= 3 and support_ratio < 0.40):
            final_prediction = {
                "rank": 1,
                "class_id": -1,
                "class_name": "uncertain",
                "label": "Uncertain",
                "confidence": top_mean_conf,
                "percentage": f"{top_mean_conf * 100:.2f}% (Conflicted)",
                "status": "uncertain",
                "reason": f"Conflicting crop evidence across accepted frames (disagreement {crop_disagreement*100:.0f}%, dominant {dominant_crop} has {max_support}/{len(valid_plant_classes)} frames)",
                "valid_frames_count": len(valid_plant_prob_vectors),
                "crop_support_counts": crop_support_counts,
                "crop_disagreement": crop_disagreement,
            }
            final_top_k = [final_prediction]
        elif top_mean_conf >= DEFAULT_CONFIDENCE_THRESHOLD:
            final_prediction = {
                **final_top_k[0],
                "status": "valid",
                "reason": f"Identified from {len(valid_plant_prob_vectors)} tight plant regions across video ({max_support} supporting frames)",
                "valid_frames_count": len(valid_plant_prob_vectors),
                "crop_support_counts": crop_support_counts,
                "crop_disagreement": crop_disagreement,
            }
        else:
            final_prediction = {
                "rank": 1,
                "class_id": -1,
                "class_name": "unknown",
                "label": "Unknown",
                "confidence": top_mean_conf,
                "percentage": "N/A",
                "status": "unknown",
                "reason": "No dominant crop confidence across valid plant regions",
                "valid_frames_count": len(valid_plant_prob_vectors),
                "crop_support_counts": crop_support_counts,
                "crop_disagreement": crop_disagreement,
            }
            final_top_k = [final_prediction]
    else:
        crop_disagreement = 1.0
        crop_support_counts = {}
        blurry_count = sum(1 for f in frame_records if f["status"] in ("blurry", "low_quality"))
        if blurry_count > len(frame_records) // 2:
            final_prediction = {
                "rank": 1,
                "class_id": -1,
                "class_name": "blurry",
                "label": "Blurry",
                "confidence": 0.0,
                "percentage": "N/A",
                "status": "blurry",
                "reason": f"Video frames ({blurry_count}/{len(frame_records)}) are too blurry for plant identification.",
                "valid_frames_count": 0,
                "crop_support_counts": {},
                "crop_disagreement": 1.0,
            }
        else:
            final_prediction = {
                "rank": 1,
                "class_id": -1,
                "class_name": "unknown",
                "label": "Unknown",
                "confidence": 0.0,
                "percentage": "N/A",
                "status": "unknown",
                "reason": "No proper plant, flower, or leaf detected in any video frame.",
                "valid_frames_count": 0,
                "crop_support_counts": {},
                "crop_disagreement": 1.0,
            }
        final_top_k = [final_prediction]
        mean_prob_vector = None

    # Step 6: Model 2 Video-Level Disease Aggregation (Crop-Aware, only on accepted plant frames)
    disease_summary = {}
    final_crop_slug = final_prediction.get("class_name")
    if detect_disease and final_prediction.get("status") in ("valid", "valid_plant_roi") and final_crop_slug and final_crop_slug not in ("unknown", "blurry", "uncertain", "crop_uncertain", "low_quality", "no_plant_evidence"):
        accepted_records = [f for f in frame_records if f.get("contributed_to_crop") and f.get("roi_pil")]
        try:
            from model2.test_model2 import draw_predictions, predict_disease
            for f in accepted_records:
                roi_p = f.get("roi_pil")
                if roi_p is None:
                    continue
                m2_res = predict_disease(roi_p, conf_threshold=disease_conf_threshold)
                f_dets = m2_res.get("detections", [])
                # Filter crop-compatible detections only
                compatible_dets = []
                for det in f_dets:
                    d_slug = det.get("disease", "")
                    if d_slug.startswith(f"{final_crop_slug}__") or "_" not in d_slug:
                        compatible_dets.append(det)
                        video_disease_detections.append({
                            **det,
                            "frame_number": f["frame_number"],
                            "frame_index": f["frame_index"],
                            "timestamp_seconds": f["timestamp_seconds"],
                        })
                f["disease_detections"] = compatible_dets
        except Exception as exc:
            logger.warning(f"Standalone Model 2 disease detection skipped: {exc}")

        if video_disease_detections:
            from collections import Counter
            disease_counts = Counter(d.get("disease_label", d.get("disease")) for d in video_disease_detections)
            dominant_disease_name, count_freq = disease_counts.most_common(1)[0]
            dominant_dets = [d for d in video_disease_detections if d.get("disease_label", d.get("disease")) == dominant_disease_name]
            avg_conf = float(np.mean([d["confidence"] for d in dominant_dets]))
            max_conf = float(np.max([d["confidence"] for d in dominant_dets]))

            disease_summary = {
                "status": "detected",
                "has_disease": True,
                "primary_disease": dominant_disease_name,
                "confidence": round(max_conf, 4),
                "percentage": f"{max_conf * 100:.1f}%",
                "avg_confidence": round(avg_conf, 4),
                "detections_count": len(video_disease_detections),
                "frames_with_disease": len(set(d["frame_number"] for d in video_disease_detections)),
                "detections": video_disease_detections,
                "message": f"Detected {len(video_disease_detections)} disease lesion(s) across {len(set(d['frame_number'] for d in video_disease_detections))} frames. Dominant disease: {dominant_disease_name}.",
            }
        else:
            disease_summary = {
                "status": "healthy" if valid_plant_prob_vectors else "unknown",
                "has_disease": False,
                "primary_disease": "Healthy Specimen / No Disease Lesions Detected",
                "confidence": 1.0 if valid_plant_prob_vectors else 0.0,
                "percentage": "100.0%" if valid_plant_prob_vectors else "N/A",
                "detections_count": 0,
                "frames_with_disease": 0,
                "detections": [],
                "message": "No crop-compatible disease lesions detected across examined plant foliage frames.",
            }
    else:
        disease_summary = {
            "status": "unknown",
            "has_disease": False,
            "primary_disease": "Disease analysis withheld (crop unverified)",
            "confidence": 0.0,
            "percentage": "N/A",
            "detections_count": 0,
            "frames_with_disease": 0,
            "detections": [],
            "message": "Disease classification not run because crop was unverified or no valid plant frames.",
        }

    return {
        "final_prediction": final_prediction,
        "top_k": final_top_k,
        "video": metadata,
        "frames_used": len(frame_records),
        "valid_plant_frames": len(valid_plant_prob_vectors),
        "sampled_frames_count": len(frame_records),
        "accepted_frames_count": len(valid_plant_prob_vectors),
        "frames_rejected": len(rejected_frames) + sum(1 for f in frame_records if not f.get("contributed_to_crop")),
        "crop_disagreement": crop_disagreement,
        "crop_support_counts": crop_support_counts,
        "total_evaluated": extraction["total_evaluated"],
        "total_decoded": extraction.get("total_decoded", metadata.get("frame_count", 0)),
        "total_decoded_frames": extraction.get("total_decoded", metadata.get("frame_count", 0)),
        "model1_inference_count": model1_inference_count,
        "frame_records": frame_records,
        "status_note": status_note,
        "mean_probabilities": mean_prob_vector,
        "model2": disease_summary,
    }
