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

from model1_test_app.inference import format_class_name, get_eval_transform
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
TARGET_FRAMES_DEFAULT = 24
MIN_TARGET_FRAMES = 16
MAX_TARGET_FRAMES = 24

__all__ = [
    "TARGET_FRAMES_DEFAULT",
    "MIN_TARGET_FRAMES",
    "MAX_TARGET_FRAMES",
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
    target_frames: int = TARGET_FRAMES_DEFAULT,
    min_target: int = MIN_TARGET_FRAMES,
    quality_filter: bool = True,
    filter_config: Optional[QualityFilterConfig] = None,
    thumbnail_size: tuple[int, int] = (320, 240),
) -> dict[str, Any]:
    """Extract 16-24 representative frames uniformly across video duration with adaptive replenishment.

    Args:
        video_path: Path to target video file.
        target_frames: Desired target frame count (default: 24).
        min_target: Minimum target frame count (default: 16).
        quality_filter: Whether to filter out dark, bright, or blurry frames.
        filter_config: Thresholds for quality filter.
        thumbnail_size: Target size for UI preview thumbnails.

    Returns:
        Dictionary containing selected_frames, rejected_frames, and metadata.
    """
    v_path = validate_video(video_path)
    metadata = get_video_metadata(v_path)
    total_frames = metadata["frame_count"]
    fps = metadata["fps"] if metadata["fps"] > 0 else 30.0

    if total_frames <= 0:
        raise ValueError(f"Video '{v_path.name}' has 0 decodable frames.")

    effective_target = min(target_frames, total_frames)
    if total_frames < min_target:
        effective_target = total_frames

    q_filter = FrameQualityFilter(filter_config or DEFAULT_VIDEO_FILTER_CONFIG) if quality_filter else None

    # Step 1: Initial candidate pool uniformly distributed across duration
    initial_pool_size = min(total_frames, max(effective_target + 12, int(effective_target * 1.5)))
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

        if q_filter is not None:
            q_res = q_filter.evaluate(frame_bgr)
            is_acc = q_res["accepted"]
            q_score = q_res["quality_score"]
            reason = q_res["reason"]
        else:
            is_acc = True
            q_score = 1.0
            reason = "accepted (filter_disabled)"

        # Full-size RGB & BGR
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
        step_stride = max(1, total_frames // (effective_target * 3))
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
        best_rejected = sorted(rejected_pool, key=lambda x: x["quality_score"], reverse=True)
        selected_frames = best_rejected[:effective_target]

    selected_frames = sorted(selected_frames, key=lambda x: x["frame_index"])

    status_note = None
    if len(selected_frames) < min_target:
        status_note = f"Only {len(selected_frames)} usable frames available across video."

    return {
        "metadata": metadata,
        "selected_frames": selected_frames,
        "rejected_frames": rejected_pool,
        "total_evaluated": len(evaluated_indices),
        "status_note": status_note,
    }


def predict_video(
    video_path: Union[str, Path],
    model: nn.Module,
    idx_to_class: dict[int, str],
    device: torch.device,
    target_frames: int = TARGET_FRAMES_DEFAULT,
    min_target: int = MIN_TARGET_FRAMES,
    quality_filter: bool = True,
    top_k: int = 3,
    filter_config: Optional[QualityFilterConfig] = None,
    blur_threshold: Optional[float] = None,
    save_debug_rois: bool = True,
    debug_dir: Optional[str | Path] = "reports/video_debug",
    detect_disease: bool = True,
    disease_conf_threshold: float = 0.20,
) -> dict[str, Any]:
    """Execute complete video inference: sample 16-24 frames, extract tight plant ROIs, predict with Model 1, detect disease with Model 2, and aggregate.

    Pipeline:
        FULL FRAME -> candidate tight plant ROI extraction -> Model 1 crop inference -> Model 2 disease detection on plant ROI -> Aggregation
    """
    effective_blur_threshold = blur_threshold if blur_threshold is not None else DEFAULT_MIN_BLUR_SCORE

    extraction = extract_adaptive_video_frames(
        video_path=video_path,
        target_frames=target_frames,
        min_target=min_target,
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
    video_disease_detections: list[dict[str, Any]] = []

    if save_debug_rois and debug_dir:
        os.makedirs(debug_dir, exist_ok=True)

    for seq_num, f_data in enumerate(selected_frames, start=1):
        idx = f_data["frame_index"]
        t_sec = f_data["timestamp_seconds"]
        q_score = f_data["quality_score"]
        thumb = f_data["thumbnail"]
        frame_img = f_data["frame_image"]
        frame_bgr = f_data.get("frame_bgr")

        # Save original debug frame
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

        if f_status == "blurry":
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "blurry",
                "predicted_label": "Blurry",
                "status": "blurry",
                "confidence": 0.0,
                "percentage": "N/A",
                "reason": f_reason,
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
            continue

        if f_status == "unknown" or not candidate_rois:
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "unknown",
                "predicted_label": "Unknown",
                "status": "unknown",
                "confidence": 0.0,
                "percentage": "N/A",
                "reason": f_reason or "No plant specimen found in frame",
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
            continue

        # Evaluate candidate plant ROIs with Model 1
        roi_results = []
        for r_idx, roi_dict in enumerate(candidate_rois):
            roi_pil = roi_dict["roi_pil"]
            roi_bgr = roi_dict.get("roi_bgr")
            tensor = transform(roi_pil).unsqueeze(0).to(device)

            with torch.no_grad():
                logits = model(tensor)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

            top_idx = int(np.argmax(probs))
            top_cls_name = idx_to_class[top_idx]
            top_conf = float(probs[top_idx])

            roi_results.append({
                "roi_index": r_idx,
                "box": roi_dict["box"],
                "score": roi_dict["score"],
                "probs": probs,
                "top_idx": top_idx,
                "top_class": top_cls_name,
                "top_conf": top_conf,
                "roi_pil": roi_pil,
                "roi_bgr": roi_bgr,
            })

        # Select the best plant ROI for this frame (highest confidence plant classification)
        best_roi = max(roi_results, key=lambda r: r["top_conf"])
        best_probs = best_roi["probs"]
        best_top_cls = best_roi["top_class"]
        best_top_conf = best_roi["top_conf"]
        best_box = best_roi["box"]
        best_roi_pil = best_roi["roi_pil"]
        best_roi_bgr = best_roi.get("roi_bgr")

        # Save ROI debug image
        if save_debug_rois and debug_dir and best_roi_bgr is not None:
            roi_debug_path = os.path.join(debug_dir, f"frame_{seq_num:03d}_idx_{idx:03d}_roi.jpg")
            cv2.imwrite(roi_debug_path, best_roi_bgr)

        # Thumbnail of the selected plant crop
        roi_thumb = best_roi_pil.resize((240, 240), Image.Resampling.LANCZOS)
        roi_annotated_thumb = roi_thumb

        # Model 2 Disease Detection on the SAME Plant ROI
        frame_disease_detections = []
        if detect_disease and best_roi_pil is not None:
            try:
                from model2.test_model2 import draw_predictions, predict_disease
                m2_res = predict_disease(best_roi_pil, conf_threshold=disease_conf_threshold)
                frame_disease_detections = m2_res.get("detections", [])
                for det in frame_disease_detections:
                    video_disease_detections.append({
                        **det,
                        "frame_number": seq_num,
                        "frame_index": idx,
                        "timestamp_seconds": t_sec,
                    })
                if frame_disease_detections and best_roi_bgr is not None:
                    annotated_bgr = draw_predictions(best_roi_bgr, m2_res)
                    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)
                    roi_annotated_thumb = Image.fromarray(annotated_rgb).resize((240, 240), Image.Resampling.LANCZOS)
            except Exception as exc:
                logger.warning(f"Frame {idx} Model 2 disease detection skipped: {exc}")

        # Top-K for this frame
        top_k_indices = np.argsort(best_probs)[::-1][:top_k]
        frame_top_k = [
            {
                "rank": r,
                "class_name": idx_to_class[int(c)],
                "label": format_class_name(idx_to_class[int(c)]),
                "confidence": float(best_probs[c]),
                "percentage": f"{float(best_probs[c]) * 100:.2f}%",
            }
            for r, c in enumerate(top_k_indices, start=1)
        ]

        if best_top_conf < DEFAULT_CONFIDENCE_THRESHOLD:
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": "unknown",
                "predicted_label": "Unknown",
                "status": "unknown",
                "confidence": best_top_conf,
                "percentage": f"{best_top_conf * 100:.2f}% (Low Conf)",
                "reason": f"Low identification confidence ({best_top_conf * 100:.1f}% < {DEFAULT_CONFIDENCE_THRESHOLD * 100:.0f}%)",
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": roi_thumb,
                "roi_annotated_thumbnail": roi_annotated_thumb,
                "roi_box": best_box,
                "rois_found": len(candidate_rois),
                "assessment": assessment,
                "top_k": frame_top_k,
                "disease_detections": frame_disease_detections,
            })
        else:
            frame_records.append({
                "frame_number": seq_num,
                "frame_index": idx,
                "timestamp_seconds": t_sec,
                "predicted_class": best_top_cls,
                "predicted_label": format_class_name(best_top_cls),
                "status": "valid",
                "confidence": best_top_conf,
                "percentage": f"{best_top_conf * 100:.2f}%",
                "reason": f"Identified from tight plant ROI {best_box}",
                "quality_score": q_score,
                "thumbnail": thumb,
                "roi_thumbnail": roi_thumb,
                "roi_annotated_thumbnail": roi_annotated_thumb,
                "roi_box": best_box,
                "rois_found": len(candidate_rois),
                "assessment": assessment,
                "top_k": frame_top_k,
                "disease_detections": frame_disease_detections,
            })
            valid_plant_prob_vectors.append(best_probs)

    # Step 5: Final Aggregated Video Prediction across all valid frames
    if valid_plant_prob_vectors:
        mean_prob_vector = np.mean(valid_plant_prob_vectors, axis=0)
        sorted_class_indices = np.argsort(mean_prob_vector)[::-1]
        top_c_idx = int(sorted_class_indices[0])
        top_mean_conf = float(mean_prob_vector[top_c_idx])

        final_top_k = []
        for rank, c_idx in enumerate(sorted_class_indices[: min(top_k, num_classes)], start=1):
            raw_c = idx_to_class[int(c_idx)]
            conf = float(mean_prob_vector[c_idx])
            final_top_k.append({
                "rank": rank,
                "class_id": int(c_idx),
                "class_name": raw_c,
                "label": format_class_name(raw_c),
                "confidence": conf,
                "percentage": f"{conf * 100:.2f}%",
            })

        if top_mean_conf >= DEFAULT_CONFIDENCE_THRESHOLD:
            final_prediction = {
                **final_top_k[0],
                "status": "valid",
                "reason": f"Identified from {len(valid_plant_prob_vectors)} tight plant regions across video",
                "valid_frames_count": len(valid_plant_prob_vectors),
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
            }
            final_top_k = [final_prediction]
    else:
        blurry_count = sum(1 for f in frame_records if f["status"] == "blurry")
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
            }
        final_top_k = [final_prediction]
        mean_prob_vector = None

    # Step 6: Model 2 Video-Level Disease Aggregation
    disease_summary = {}
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
            "message": "No disease lesions detected across examined plant foliage frames.",
        }

    return {
        "final_prediction": final_prediction,
        "top_k": final_top_k,
        "video": metadata,
        "frames_used": len(frame_records),
        "valid_plant_frames": len(valid_plant_prob_vectors),
        "frames_rejected": len(rejected_frames),
        "total_evaluated": extraction["total_evaluated"],
        "frame_records": frame_records,
        "status_note": status_note,
        "mean_probabilities": mean_prob_vector,
        "model2": disease_summary,
    }
