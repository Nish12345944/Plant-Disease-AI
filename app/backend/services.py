"""Service Layer for Alexa Farms Multimodal Backend.

Coordinates:
- Speech-to-text transcription via faster-whisper (audio/test_audio.py)
- Microphone recording via AudioRecorder (audio/recorder.py)
- Model 1 EfficientNet-B2 single-image and video inference (model1_test_app)
- Model 2 V4 EfficientNet-B2 Disease & Healthy classification with crop-disease compatibility (models/model2_classifier_v4)
- Query understanding and intent classification (router/query_router.py)
- Unified multimodal chat routing
- Standardized output contracts for plant disease diagnostics
- Telemetry data extraction for developer panel
"""

from __future__ import annotations

import base64
import io
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Optional

import numpy as np
import torch
from PIL import Image

from app.backend.config import (
    CROP_DISEASE_MAPPING,
    DEVICE,
    DEVICE_NAME,
    MODEL1_CHECKPOINT,
    MODEL1_CLASS_MAPPING,
    MODEL1_CONFIG,
    MODEL2_CHECKPOINT,
    MODEL2_CLASS_MAPPING,
    MODEL2_CONFIG,
    TEMP_MEDIA_DIR,
)
from audio.recorder import AudioRecorder
from audio.test_audio import transcribe_audio
from model1_test_app.inference import load_model, predict_image
from model1_test_app.video_inference import TARGET_FRAMES_DEFAULT, predict_video
from models.model2_classifier_v4.predict import (
    Model2DiseaseClassifierV4,
    format_disease_name_clean,
    format_human_readable,
)
from router.query_router import route_query

logger = logging.getLogger(__name__)

# Cached model singletons
_MODEL1 = None
_IDX_TO_CLASS = None
_CLASS_TO_IDX = None

_MODEL2_V4: Optional[Model2DiseaseClassifierV4] = None

# Active server-side microphone recorder singleton
_ACTIVE_RECORDER: Optional[AudioRecorder] = None


def get_model1():
    """Retrieve or initialize the cached Model 1 neural network."""
    global _MODEL1, _IDX_TO_CLASS, _CLASS_TO_IDX
    if _MODEL1 is None:
        if not MODEL1_CHECKPOINT.exists():
            raise FileNotFoundError(f"CRITICAL: Model 1 checkpoint not found at: {MODEL1_CHECKPOINT}")
        logger.info(f"Loading Model 1 from {MODEL1_CHECKPOINT} onto {DEVICE_NAME}...")
        _MODEL1, _IDX_TO_CLASS, _CLASS_TO_IDX, _, _ = load_model(
            checkpoint_path=MODEL1_CHECKPOINT,
            mapping_path=MODEL1_CLASS_MAPPING,
            config_path=MODEL1_CONFIG,
            device=DEVICE,
        )
        logger.info("Model 1 initialized successfully.")
    return _MODEL1, _IDX_TO_CLASS, _CLASS_TO_IDX


def get_model2() -> Model2DiseaseClassifierV4:
    """Retrieve or initialize the cached Model 2 V4 disease & healthy classifier."""
    global _MODEL2_V4
    if _MODEL2_V4 is None:
        if not MODEL2_CHECKPOINT.exists():
            raise FileNotFoundError(f"CRITICAL: Model 2 V4 checkpoint not found at: {MODEL2_CHECKPOINT}")
        logger.info(f"Loading Model 2 V4 from {MODEL2_CHECKPOINT} onto {DEVICE_NAME}...")
        _MODEL2_V4 = Model2DiseaseClassifierV4(
            checkpoint_path=MODEL2_CHECKPOINT,
            class_mapping_path=MODEL2_CLASS_MAPPING,
            crop_disease_map_path=CROP_DISEASE_MAPPING,
            device=str(DEVICE),
            uncertainty_threshold=0.40,
            margin_threshold=0.05,
        )
        logger.info(f"Model 2 V4 initialized successfully with {_MODEL2_V4.num_classes} classes from {_MODEL2_V4.checkpoint_path}.")
    return _MODEL2_V4


def pil_to_base64_data_url(pil_img: Image.Image, format: str = "JPEG", quality: int = 85) -> str:
    """Convert a PIL Image into a base64 Data URL for clean frontend display."""
    buffered = io.BytesIO()
    if pil_img.mode in ("RGBA", "P"):
        pil_img = pil_img.convert("RGB")
    pil_img.save(buffered, format=format, quality=quality)
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/{format.lower()};base64,{img_b64}"


# ---------------------------------------------------------------------------
# Audio & Microphone Services
# ---------------------------------------------------------------------------

def process_audio_file(file_bytes: bytes, original_filename: str = "audio.wav") -> dict[str, Any]:
    """Transcribe an audio file using the existing faster-whisper pipeline."""
    suffix = Path(original_filename).suffix.lower() or ".wav"
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, dir=TEMP_MEDIA_DIR, delete=False) as tmp:
            tmp.write(file_bytes)
            temp_path = tmp.name

        result = transcribe_audio(temp_path)
        dur = result.segments[-1].end if getattr(result, "segments", None) else 0.0
        return {
            "status": "success",
            "text": (result.text or "").strip(),
            "language": result.language,
            "language_probability": round(result.language_probability, 3),
            "duration_sec": round(dur, 2),
            "segments_count": len(result.segments) if getattr(result, "segments", None) else 0,
            "device": DEVICE_NAME,
        }
    except Exception as exc:
        logger.error(f"Error in process_audio_file: {exc}")
        return {"status": "error", "text": "", "error": str(exc)}
    finally:
        if temp_path and Path(temp_path).exists():
            try:
                Path(temp_path).unlink()
            except OSError:
                pass


def start_server_microphone() -> dict[str, Any]:
    """Start server-side microphone capture."""
    global _ACTIVE_RECORDER
    if _ACTIVE_RECORDER is not None and _ACTIVE_RECORDER.is_recording:
        return {"status": "already_recording", "message": "Microphone recording is already active."}

    try:
        _ACTIVE_RECORDER = AudioRecorder()
        _ACTIVE_RECORDER.start()
        return {"status": "recording_started", "message": "Host microphone recording started."}
    except Exception as exc:
        logger.error(f"Error starting microphone: {exc}")
        return {"status": "error", "message": f"Failed to start microphone: {str(exc)}"}


def stop_server_microphone() -> dict[str, Any]:
    """Stop server-side microphone capture and transcribe."""
    global _ACTIVE_RECORDER
    if _ACTIVE_RECORDER is None or not _ACTIVE_RECORDER.is_recording:
        return {"status": "not_recording", "text": "", "message": "Microphone is not currently recording."}

    temp_wav_path = None
    try:
        temp_wav_path, duration = _ACTIVE_RECORDER.stop()
        if not temp_wav_path or not Path(temp_wav_path).exists():
            return {"status": "error", "text": "", "message": "No audio was captured from microphone."}

        result = transcribe_audio(temp_wav_path)
        return {
            "status": "success",
            "text": (result.text or "").strip(),
            "language": result.language,
            "language_probability": round(result.language_probability, 3),
            "duration_sec": round(duration, 2),
        }
    except Exception as exc:
        logger.error(f"Error stopping/transcribing microphone audio: {exc}")
        return {"status": "error", "text": "", "error": str(exc)}
    finally:
        if temp_wav_path and Path(temp_wav_path).exists():
            try:
                Path(temp_wav_path).unlink()
            except OSError:
                pass
        _ACTIVE_RECORDER = None


# ---------------------------------------------------------------------------
# Image & Video Inference Services (Model 1 + Model 2 V4 Combined)
# ---------------------------------------------------------------------------

def process_image_inference(file_bytes: bytes, conf_threshold: float = 0.20) -> dict[str, Any]:
    """Perform hierarchical Model 1 (Plant Identification) and Model 2 V4 (Crop-Aware Disease Classification) inference."""
    m1_model, idx_to_class, _ = get_model1()
    m2_classifier = get_model2()

    pil_img = Image.open(io.BytesIO(file_bytes))
    m1_result = predict_image(
        image_input=pil_img,
        model=m1_model,
        idx_to_class=idx_to_class,
        device=DEVICE,
        top_k=5,
        validate_plant=True,
    )

    preview_b64 = pil_to_base64_data_url(pil_img, format="JPEG", quality=85)
    crop_name = m1_result.get("predicted_label") or m1_result.get("predicted_class", "unknown")
    crop_confidence = m1_result.get("confidence", 0.0)
    top_list = m1_result.get("top_k", [])
    is_plant = m1_result.get("status") == "valid"

    # Stage 2: Model 2 V4 Crop-Aware Disease / Healthy Classification
    try:
        m2_res = m2_classifier.predict_crop_aware(
            image_input=pil_img,
            crop_name=crop_name if is_plant else None,
            crop_confidence=crop_confidence,
        )

        final_status = m2_res["status"]
        final_disease = m2_res["disease"]
        disease_conf = m2_res["disease_confidence"]

        if final_status == "healthy":
            model2_dict = {
                "status": "healthy",
                "has_disease": False,
                "primary_disease": "Healthy Specimen / No Disease Detected",
                "primary_disease_slug": None,
                "primary_disease_id": 0,
                "confidence": disease_conf,
                "percentage": f"{disease_conf * 100:.1f}%",
                "primary_bbox": None,
                "detections_count": 0,
                "detections": [],
                "raw_top1": m2_res["raw_top1"],
                "top_compatible": m2_res["top_compatible"],
                "raw_top10": m2_res["raw_top10"],
                "annotated_preview_url": preview_b64,
                "message": f"Verified healthy foliage for {crop_name.title()}." if is_plant else "Healthy specimen.",
            }
        elif final_status == "diseased" and final_disease:
            clean_title = format_disease_name_clean(final_disease) or final_disease
            model2_dict = {
                "status": "detected",
                "has_disease": True,
                "primary_disease": clean_title,
                "primary_disease_slug": final_disease,
                "primary_disease_id": m2_classifier.class_to_id.get(final_disease, 1),
                "confidence": disease_conf,
                "percentage": f"{disease_conf * 100:.1f}%",
                "primary_bbox": None,
                "detections_count": 1,
                "detections": [
                    {
                        "disease": final_disease,
                        "disease_label": clean_title,
                        "confidence": disease_conf,
                        "percentage": f"{disease_conf * 100:.1f}%",
                    }
                ],
                "raw_top1": m2_res["raw_top1"],
                "top_compatible": m2_res["top_compatible"],
                "raw_top10": m2_res["raw_top10"],
                "annotated_preview_url": preview_b64,
                "message": f"Diagnosed {clean_title} on {crop_name.title()} ({disease_conf * 100:.1f}% confidence).",
            }
        else:
            model2_dict = {
                "status": "uncertain",
                "has_disease": False,
                "primary_disease": None,
                "primary_disease_slug": None,
                "primary_disease_id": None,
                "confidence": 0.0,
                "percentage": "N/A",
                "primary_bbox": None,
                "detections_count": 0,
                "detections": [],
                "raw_top1": m2_res["raw_top1"],
                "top_compatible": m2_res["top_compatible"],
                "raw_top10": m2_res["raw_top10"],
                "annotated_preview_url": preview_b64,
                "message": f"Condition uncertain on {crop_name.title()}. Crop-disease compatibility or confidence threshold not met.",
            }
    except Exception as exc:
        logger.error(f"Model 2 V4 image inference failed: {exc}", exc_info=True)
        model2_dict = {
            "status": "error",
            "has_disease": False,
            "primary_disease": "Inference Error",
            "confidence": 0.0,
            "percentage": "0.0%",
            "detections_count": 0,
            "detections": [],
            "annotated_preview_url": preview_b64,
            "message": f"Disease classification encountered an issue: {str(exc)}",
        }

    model1_dict = {
        "status": m1_result.get("status", "valid"),
        "predicted_crop": crop_name,
        "predicted_class": m1_result.get("predicted_class", "unknown"),
        "predicted_label": crop_name,
        "confidence": crop_confidence,
        "percentage": m1_result.get("percentage", "N/A"),
        "is_plant": is_plant,
        "reason": m1_result.get("reason", ""),
        "message": m1_result.get("reason", ""),
        "top3": top_list[:3],
        "top_k": top_list,
        "image_size": m1_result.get("image_size"),
        "preview_url": preview_b64,
    }

    # Standardized Diagnosis Contract
    standardized_diagnosis = {
        "crop": crop_name if is_plant else None,
        "crop_confidence": round(float(crop_confidence), 4),
        "status": model2_dict["status"],
        "disease": model2_dict.get("primary_disease_slug"),
        "disease_confidence": round(float(model2_dict.get("confidence", 0.0)), 4),
    }

    return {
        **model1_dict,
        "model1": model1_dict,
        "model2": model2_dict,
        "standardized_diagnosis": standardized_diagnosis,
        "annotated_preview_url": preview_b64,
    }


def process_video_inference(
    file_bytes: bytes,
    original_filename: str = "video.mp4",
    target_frames: int = TARGET_FRAMES_DEFAULT,
    disease_conf_threshold: float = 0.20,
) -> dict[str, Any]:
    """Execute video inference across representative frames with Model 1 and Model 2 V4."""
    model, idx_to_class, _ = get_model1()
    m2_classifier = get_model2()

    suffix = Path(original_filename).suffix.lower() or ".mp4"
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, dir=TEMP_MEDIA_DIR, delete=False) as tmp:
            tmp.write(file_bytes)
            temp_path = Path(tmp.name)

        v_res = predict_video(
            video_path=temp_path,
            model=model,
            idx_to_class=idx_to_class,
            device=DEVICE,
            target_frames=target_frames,
            quality_filter=True,
            top_k=3,
            detect_disease=False,
        )

        final_pred = v_res["final_prediction"]
        crop_label = final_pred.get("label", "Unknown")
        crop_conf = final_pred.get("confidence", 0.0)

        # Multi-frame Model 2 V4 disease classification across valid plant frames
        frame_results = []
        all_disease_detections = []
        disease_candidates: dict[str, dict[str, Any]] = {}
        healthy_frames_count = 0
        uncertain_frames_count = 0
        valid_plant_frames = 0

        for f in v_res["frame_records"]:
            thumb_b64 = pil_to_base64_data_url(f["thumbnail"], format="JPEG", quality=75) if f.get("thumbnail") else None
            roi_thumb_b64 = pil_to_base64_data_url(f["roi_thumbnail"], format="JPEG", quality=80) if f.get("roi_thumbnail") else None

            f_status = f.get("status", "valid")
            roi_img = f.get("roi_thumbnail") or f.get("thumbnail")

            f_disease_slug = None
            f_disease_label = None
            f_disease_conf = 0.0
            f_disease_status = "uncertain"
            f_detections = []

            # Only run disease classification on valid plant frames
            if f_status == "valid" and roi_img is not None:
                valid_plant_frames += 1
                m2_res = m2_classifier.predict_crop_aware(
                    image_input=roi_img,
                    crop_name=crop_label,
                    crop_confidence=crop_conf,
                )
                f_disease_status = m2_res.get("status", "uncertain")
                f_disease_conf = float(m2_res.get("disease_confidence", 0.0))

                if f_disease_status == "diseased" and m2_res.get("disease"):
                    f_disease_slug = m2_res["disease"]
                    f_disease_label = format_disease_name_clean(f_disease_slug) or f_disease_slug
                    det_dict = {
                        "disease": f_disease_slug,
                        "disease_label": f_disease_label,
                        "confidence": round(f_disease_conf, 4),
                        "percentage": f"{f_disease_conf * 100:.1f}%",
                        "bbox": f.get("roi_box"),
                        "frame_index": f["frame_index"],
                        "frame_number": f["frame_number"],
                        "timestamp_seconds": f["timestamp_seconds"],
                    }
                    f_detections.append(det_dict)
                    all_disease_detections.append(det_dict)

                    if f_disease_slug not in disease_candidates:
                        disease_candidates[f_disease_slug] = {
                            "label": f_disease_label,
                            "count": 0,
                            "confidences": [],
                        }
                    disease_candidates[f_disease_slug]["count"] += 1
                    disease_candidates[f_disease_slug]["confidences"].append(f_disease_conf)
                elif f_disease_status == "healthy":
                    healthy_frames_count += 1
                else:
                    uncertain_frames_count += 1

            frame_results.append({
                "frame_idx": f["frame_index"],
                "frame_number": f["frame_number"],
                "timestamp_sec": f["timestamp_seconds"],
                "timestamp_seconds": f["timestamp_seconds"],
                "quality_status": f_status,
                "status": f_status,
                "predicted_crop": f["predicted_label"],
                "predicted_class": f["predicted_class"],
                "predicted_label": f["predicted_label"],
                "confidence": f["confidence"],
                "percentage": f["percentage"],
                "filter_reason": f.get("reason", ""),
                "reason": f.get("reason", ""),
                "quality_score": f.get("quality_score", 1.0),
                "thumbnail": thumb_b64,
                "thumbnail_url": thumb_b64,
                "roi_thumbnail": roi_thumb_b64,
                "roi_thumbnail_url": roi_thumb_b64,
                "roi_annotated_thumbnail_url": roi_thumb_b64,
                "roi_box": f.get("roi_box"),
                "rois_found": f.get("rois_found", 0),
                "top_k": f.get("top_k", []),
                "disease": f_disease_slug,
                "disease_label": f_disease_label,
                "disease_confidence": round(f_disease_conf, 4),
                "disease_status": f_disease_status,
                "disease_detections": f_detections,
            })

        # Temporal Disease Aggregation across valid plant frames
        min_support_count = 3 if valid_plant_frames >= 10 else 2
        min_support_ratio = 0.20

        ranked_diseases = []
        for slug, dinfo in disease_candidates.items():
            cnt = dinfo["count"]
            confs = dinfo["confidences"]
            score = sum(confs)
            max_c = max(confs)
            avg_c = score / cnt
            ratio = cnt / valid_plant_frames if valid_plant_frames > 0 else 0.0

            if cnt >= min_support_count and ratio >= min_support_ratio:
                ranked_diseases.append({
                    "slug": slug,
                    "label": dinfo["label"],
                    "count": cnt,
                    "ratio": ratio,
                    "score": score,
                    "max_conf": max_c,
                    "avg_conf": avg_c,
                })

        ranked_diseases.sort(key=lambda x: x["score"], reverse=True)

        if ranked_diseases:
            top_dis = ranked_diseases[0]
            top_conf = top_dis["max_conf"]
            m2_summary = {
                "status": "detected",
                "has_disease": True,
                "primary_disease": top_dis["label"],
                "primary_disease_slug": top_dis["slug"],
                "confidence": round(top_conf, 4),
                "percentage": f"{top_conf * 100:.1f}%",
                "avg_confidence": round(top_dis["avg_conf"], 4),
                "supporting_frames": top_dis["count"],
                "evaluated_frames": valid_plant_frames,
                "detections_count": len(all_disease_detections),
                "detections": all_disease_detections,
                "message": f"Diagnosed {top_dis['label']} on {crop_label} ({top_conf * 100:.1f}% confidence across {top_dis['count']}/{valid_plant_frames} supporting frames).",
            }
        elif valid_plant_frames > 0:
            if healthy_frames_count >= (valid_plant_frames * 0.40):
                m2_summary = {
                    "status": "healthy",
                    "has_disease": False,
                    "primary_disease": "Healthy Specimen / No Disease Detected",
                    "primary_disease_slug": None,
                    "confidence": 1.0,
                    "percentage": "100.0%",
                    "supporting_frames": healthy_frames_count,
                    "evaluated_frames": valid_plant_frames,
                    "detections_count": 0,
                    "detections": [],
                    "message": f"Verified healthy foliage for {crop_label} across {valid_plant_frames} video frames.",
                }
            else:
                m2_summary = {
                    "status": "uncertain",
                    "has_disease": False,
                    "primary_disease": "Condition Uncertain / Inconclusive Symptoms",
                    "primary_disease_slug": None,
                    "confidence": 0.0,
                    "percentage": "N/A",
                    "supporting_frames": 0,
                    "evaluated_frames": valid_plant_frames,
                    "detections_count": 0,
                    "detections": [],
                    "message": f"Condition uncertain across {valid_plant_frames} frames for {crop_label}. Crop-disease compatibility or confidence threshold not met.",
                }
        else:
            m2_summary = {
                "status": "uncertain",
                "has_disease": False,
                "primary_disease": None,
                "primary_disease_slug": None,
                "confidence": 0.0,
                "percentage": "N/A",
                "supporting_frames": 0,
                "evaluated_frames": 0,
                "detections_count": 0,
                "detections": [],
                "message": "No valid plant frames available for disease analysis.",
            }

        video_duration = v_res["video"].get("duration_seconds", 0.0)

        return {
            "status": final_pred.get("status", "valid"),
            "predicted_crop": crop_label,
            "predicted_class": final_pred.get("class_name", "unknown"),
            "predicted_label": crop_label,
            "confidence": crop_conf,
            "percentage": final_pred.get("percentage", "N/A"),
            "frames_processed": v_res["frames_used"],
            "frames_used": v_res["frames_used"],
            "valid_frames_count": v_res.get("valid_plant_frames", 0),
            "valid_plant_frames": v_res.get("valid_plant_frames", 0),
            "frames_rejected": v_res["frames_rejected"],
            "total_evaluated": v_res["total_evaluated"],
            "video_duration_sec": video_duration,
            "video_name": Path(original_filename).name,
            "video_metadata": v_res["video"],
            "status_note": v_res.get("status_note"),
            "top_k": v_res["top_k"],
            "final_prediction": final_pred,
            "frame_results": frame_results,
            "frame_records": frame_results,
            "model2": m2_summary,
        }
    finally:
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Query Routing & Multimodal Dispatch Service
# ---------------------------------------------------------------------------

def process_query_routing(query: str) -> dict[str, Any]:
    """Route a natural language query using the deterministic query router."""
    if not query or not query.strip():
        return {
            "intent": "unknown",
            "needs_model1": False,
            "needs_model2": False,
            "needs_rag": False,
        }
    return route_query(query.strip())
