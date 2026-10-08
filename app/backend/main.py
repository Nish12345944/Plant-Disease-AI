"""FastAPI Main Application for Alexa Farms Multimodal Plant Assistant."""

from __future__ import annotations

import logging
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.backend.config import (
    DEVICE_NAME,
    SUPPORTED_AUDIO_EXTS,
    SUPPORTED_IMAGE_EXTS,
    SUPPORTED_VIDEO_EXTS,
)
from app.backend.services import (
    get_model1,
    get_model2,
    pil_to_base64_data_url,
    process_audio_file,
    process_image_inference,
    process_query_routing,
    process_video_inference,
    start_server_microphone,
    stop_server_microphone,
)
from knowledge.assistant import AgriculturalAssistant
from knowledge.database import get_knowledge_base

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# Active conversational sessions registry
_SESSIONS: dict[str, AgriculturalAssistant] = {}
_DEFAULT_ASSISTANT: Optional[AgriculturalAssistant] = None


def get_session_assistant(session_id: Optional[str] = None) -> AgriculturalAssistant:
    """Retrieve or create an AgriculturalAssistant instance for a conversational session."""
    global _DEFAULT_ASSISTANT, _SESSIONS
    if not session_id or not session_id.strip():
        if _DEFAULT_ASSISTANT is None:
            _DEFAULT_ASSISTANT = AgriculturalAssistant(kb=get_knowledge_base())
        return _DEFAULT_ASSISTANT

    clean_sid = session_id.strip()
    if clean_sid not in _SESSIONS:
        if len(_SESSIONS) > 100:
            oldest = next(iter(_SESSIONS))
            _SESSIONS.pop(oldest, None)
        _SESSIONS[clean_sid] = AgriculturalAssistant(kb=get_knowledge_base())

    return _SESSIONS[clean_sid]

app = FastAPI(
    title="Alexa Farms Multimodal API",
    description="Local Multimodal Testing Interface for Speech, Video, Image, and Text Crop Diagnostics",
    version="1.0.0",
)

# Enable CORS for local Vite development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Warm up Model 1 and Model 2 V4 on startup so subsequent requests are fast."""
    try:
        logger.info("Initializing Model 1 neural weights...")
        get_model1()
        logger.info("Model 1 initialized successfully.")
    except Exception as exc:
        logger.error(f"CRITICAL: Model 1 initialization failed: {exc}", exc_info=True)
        raise exc

    try:
        logger.info("Initializing Model 2 V4 EfficientNet-B2 classifier weights...")
        m2 = get_model2()
        logger.info(f"Model 2 version: V4")
        logger.info(f"Model 2 checkpoint: {m2.checkpoint_path}")
        logger.info(f"Model 2 V4 initialized successfully with {m2.num_classes} classes.")
    except Exception as exc:
        logger.error(f"CRITICAL: Model 2 V4 initialization failed: {exc}", exc_info=True)
        raise exc


@app.get("/")
async def root():
    """Return backend status and API documentation entrypoints."""
    return {
        "service": "Alexa Farms AI Backend",
        "status": "online",
        "device": DEVICE_NAME,
        "api_docs": "/docs",
        "health": "/api/health",
        "frontend_url": "http://localhost:5173",
        "models": {
            "model1": "Plant Identification (Model 1 - EfficientNet-B2 22 crops)",
            "model2": "Disease & Healthy Classification (Model 2 V4 - EfficientNet-B2 117 classes)",
            "audio": "faster-whisper"
        }
    }


@app.get("/api/health")
async def health_check():
    """Return system readiness and device specifications."""
    return {
        "status": "healthy",
        "device": DEVICE_NAME,
        "model1_loaded": True,
        "model2_loaded": True,
        "whisper_model": "faster-whisper-small",
        "supported_media": {
            "images": sorted(list(SUPPORTED_IMAGE_EXTS)),
            "videos": sorted(list(SUPPORTED_VIDEO_EXTS)),
            "audio": sorted(list(SUPPORTED_AUDIO_EXTS)),
        },
    }


# ---------------------------------------------------------------------------
# Audio & Microphone Endpoints
# ---------------------------------------------------------------------------
# Audio & Microphone Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/audio/transcribe")
async def transcribe_audio_endpoint(file: UploadFile = File(...)):
    """Transcribe an audio file (or browser microphone blob) using faster-whisper."""
    ext = Path(file.filename or "recording.wav").suffix.lower()
    if ext and ext not in SUPPORTED_AUDIO_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported: {sorted(list(SUPPORTED_AUDIO_EXTS))}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")

    try:
        res = process_audio_file(file_bytes, original_filename=file.filename or "recording.wav")
        return res
    except Exception as exc:
        logger.error(f"Transcription failure: {exc}")
        raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(exc)}")


@app.post("/api/audio/mic/start")
async def start_mic_endpoint():
    """Start host server-side microphone recording via AudioRecorder."""
    res = start_server_microphone()
    return res


@app.post("/api/audio/mic/stop")
async def stop_mic_endpoint():
    """Stop host server-side microphone recording and transcribe captured audio."""
    res = stop_server_microphone()
    return res


# ---------------------------------------------------------------------------
# Query Routing Endpoint
# ---------------------------------------------------------------------------

class RouteQueryRequest(BaseModel):
    query: str


@app.post("/api/query/route")
async def route_query_endpoint(payload: RouteQueryRequest):
    """Analyze query intent using the deterministic rule-based query router."""
    result = process_query_routing(payload.query)
    routing_meta = {
        "needs_model1": result["needs_model1"],
        "needs_model2": result["needs_model2"],
        "needs_rag": result["needs_rag"],
    }
    return {
        "query": payload.query,
        "intent": result["intent"],
        "routing_metadata": routing_meta,
        "needs_model1": result["needs_model1"],
        "needs_model2": result["needs_model2"],
        "needs_rag": result["needs_rag"],
    }


# ---------------------------------------------------------------------------
# Direct Image & Video Inference Endpoints
# ---------------------------------------------------------------------------

@app.post("/api/inference/image")
async def inference_image_endpoint(file: UploadFile = File(...)):
    """Run Model 1 plant/crop classification on an uploaded image."""
    ext = Path(file.filename or "image.jpg").suffix.lower()
    if ext and ext not in SUPPORTED_IMAGE_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image format '{ext}'. Supported: {sorted(list(SUPPORTED_IMAGE_EXTS))}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image file is empty.")

    try:
        res = process_image_inference(file_bytes)
        return res
    except Exception as exc:
        logger.error(f"Image inference failure: {exc}")
        raise HTTPException(status_code=500, detail=f"Image inference failed: {str(exc)}")


@app.post("/api/inference/video")
async def inference_video_endpoint(
    file: UploadFile = File(...),
    target_frames: int = Form(24),
):
    """Run Model 1 video classification across 16-24 representative frames."""
    ext = Path(file.filename or "video.mp4").suffix.lower()
    if ext and ext not in SUPPORTED_VIDEO_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported video format '{ext}'. Supported: {sorted(list(SUPPORTED_VIDEO_EXTS))}",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded video file is empty.")

    try:
        res = process_video_inference(
            file_bytes,
            original_filename=file.filename or "video.mp4",
            target_frames=target_frames,
        )
        return res
    except Exception as exc:
        logger.error(f"Video inference failure: {exc}")
        raise HTTPException(status_code=500, detail=f"Video inference failed: {str(exc)}")


# ---------------------------------------------------------------------------
# Unified Multimodal Chat Endpoint
# ---------------------------------------------------------------------------

@app.post("/api/chat")
async def unified_chat_endpoint(
    text: Optional[str] = Form(None),
    input_type: Optional[str] = Form(None),
    language: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
    image_file: Optional[UploadFile] = File(None),
    video_file: Optional[UploadFile] = File(None),
    target_frames: int = Form(24),
):
    """Coordinate multimodal inputs (typed text, speech, image, video).

    Executes:
    1. Validate input presence and media file extensions.
    2. Audio speech-to-text if audio is supplied.
    3. Combines typed and transcribed queries.
    4. Runs Model 1 and Model 2 V4 inference if image or video is attached.
    5. Routes query intent using the router.
    6. Executes AgriculturalAssistant for deterministic, grounded agronomic reasoning and knowledge retrieval.
    7. Returns structured user, assistant, vision, and knowledge response objects with debug telemetry.
    """
    message_id = str(uuid.uuid4())

    # Disambiguate generic `file` parameter based on `input_type` or extension
    if file is not None:
        filename = file.filename or ""
        ext = Path(filename).suffix.lower()

        # Handle blob without extension or fallback by input_type
        if not ext:
            if input_type == "image":
                ext = ".jpg"
                image_file = file
            elif input_type == "video":
                ext = ".mp4"
                video_file = file
            elif input_type == "audio":
                ext = ".wav"
                audio_file = file
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Uploaded file has no recognizable extension or input_type.",
                )
        else:
            if ext not in (SUPPORTED_IMAGE_EXTS | SUPPORTED_VIDEO_EXTS | SUPPORTED_AUDIO_EXTS):
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file format '{ext}'. Supported: {sorted(list(SUPPORTED_IMAGE_EXTS | SUPPORTED_VIDEO_EXTS | SUPPORTED_AUDIO_EXTS))}",
                )

            if input_type == "image" or ext in SUPPORTED_IMAGE_EXTS:
                image_file = file
            elif input_type == "video" or ext in SUPPORTED_VIDEO_EXTS:
                video_file = file
            elif input_type == "audio" or ext in SUPPORTED_AUDIO_EXTS:
                audio_file = file

    has_text = bool(text and text.strip())
    has_audio = audio_file is not None
    has_image = image_file is not None
    has_video = video_file is not None

    if not (has_text or has_audio or has_image or has_video):
        raise HTTPException(
            status_code=400,
            detail="No valid input provided. Please provide text, audio, image, or video.",
        )

    # Process Audio if present
    audio_transcription = None
    detected_language = language or "en"
    if audio_file is not None:
        audio_bytes = await audio_file.read()
        if audio_bytes:
            audio_res = process_audio_file(audio_bytes, original_filename=audio_file.filename or "speech.wav")
            audio_transcription = audio_res["text"]
            detected_language = audio_res.get("language") or detected_language

    # Resolve active query text
    typed_clean = (text or "").strip()
    spoken_clean = (audio_transcription or "").strip()

    if typed_clean and spoken_clean:
        if typed_clean.lower() == spoken_clean.lower():
            final_query = typed_clean
        else:
            final_query = f"{typed_clean} (Transcribed: {spoken_clean})"
    elif typed_clean:
        final_query = typed_clean
    elif spoken_clean:
        final_query = spoken_clean
    else:
        # Default prompt when user uploads media without a question
        final_query = "What plant or crop is this?" if (has_image or has_video) else ""

    # Route Intent
    routing = process_query_routing(final_query) if final_query else {
        "intent": "plant_identification" if (has_image or has_video) else "unknown",
        "needs_model1": True if (has_image or has_video) else False,
        "needs_model2": False,
        "needs_rag": False,
    }

    routing_meta = {
        "needs_model1": routing.get("needs_model1", False),
        "needs_model2": routing.get("needs_model2", False),
        "needs_rag": routing.get("needs_rag", False),
    }

    # Model 1 Image & Video Inference execution
    image_result = None
    video_result = None

    if image_file is not None:
        img_bytes = await image_file.read()
        if img_bytes:
            image_result = process_image_inference(img_bytes)

    if video_file is not None:
        vid_bytes = await video_file.read()
        if vid_bytes:
            video_result = process_video_inference(
                vid_bytes,
                original_filename=video_file.filename or "video.mp4",
                target_frames=target_frames,
            )

    # Extract Model 1 & Model 2 result structures
    m1_data = None
    m2_data = None
    annotated_preview = None

    if image_result:
        m1_data = image_result.get("model1", image_result)
        m2_data = image_result.get("model2")
        annotated_preview = image_result.get("annotated_preview_url")

    if video_result:
        m2_data = video_result.get("model2")

    # Standardize visual evidence for the Agricultural Knowledge Assistant
    visual_evidence = None
    if image_result:
        m1 = image_result.get("model1", {}) or {}
        m2 = image_result.get("model2", {}) or {}
        m1_status = m1.get("status", "valid")
        m2_status = m2.get("status", "uncertain")

        if m1_status != "valid":
            eff_status = "uncertain"
        elif m2_status == "healthy":
            eff_status = "healthy"
        elif m2_status == "detected" and m2.get("has_disease"):
            eff_status = "diseased"
        else:
            eff_status = "uncertain"

        crop_name_vis = image_result.get("predicted_crop") or m1.get("predicted_crop")
        disease_slug_vis = m2.get("primary_disease_slug") or m2.get("primary_disease")

        visual_evidence = {
            "crop": crop_name_vis,
            "crop_confidence": image_result.get("confidence") or m1.get("confidence", 0.0),
            "disease": disease_slug_vis,
            "disease_name": m2.get("primary_disease"),
            "disease_confidence": m2.get("confidence", 0.0),
            "status": eff_status,
            "incompatibility_flag": (m2_status == "uncertain" and not m2.get("has_disease")),
        }
    elif video_result:
        m2 = video_result.get("model2", {}) or {}
        vid_status = video_result.get("status", "valid")
        m2_status = m2.get("status", "uncertain")

        if vid_status != "valid":
            eff_status = "uncertain"
        elif m2_status == "healthy":
            eff_status = "healthy"
        elif m2_status == "detected" and m2.get("has_disease"):
            eff_status = "diseased"
        else:
            eff_status = "uncertain"

        visual_evidence = {
            "crop": video_result.get("predicted_crop"),
            "crop_confidence": video_result.get("confidence", 0.0),
            "disease": m2.get("primary_disease_slug") or m2.get("primary_disease"),
            "disease_name": m2.get("primary_disease"),
            "disease_confidence": m2.get("confidence", 0.0),
            "status": eff_status,
            "incompatibility_flag": (m2_status == "uncertain" and not m2.get("has_disease")),
        }

    # Execute deterministic AgriculturalAssistant reasoning and knowledge retrieval
    assistant = get_session_assistant(session_id)
    knowledge_data = None
    knowledge_sources = []

    try:
        kb_resp = assistant.answer_query(
            query=final_query,
            visual_result=visual_evidence,
        )
        assistant_message = kb_resp.text
        knowledge_data = kb_resp.to_dict()
        knowledge_sources = kb_resp.sources
    except Exception as exc:
        logger.error(f"AgriculturalAssistant reasoning error: {exc}", exc_info=True)
        assistant_message = (
            "I encountered an issue processing the agricultural knowledge for your request. "
            "Please try rephrasing your question or check the image clarity."
        )
        knowledge_data = {
            "status": "error",
            "error": str(exc),
            "text": assistant_message,
        }

    inputs_dict = {
        "text": has_text,
        "audio": has_audio,
        "image": has_image,
        "video": has_video,
    }

    # Structured API Response
    return {
        "id": message_id,
        "session_id": session_id,
        "message": assistant_message,
        "query": final_query,
        "original_query": text or final_query,
        "original_transcription": audio_transcription,
        "language": detected_language,
        "inputs": inputs_dict,
        "router": {
            "intent": routing.get("intent", "unknown"),
            "intent_type": routing.get("intent_type", routing.get("intent", "unknown")),
            "routing_metadata": routing_meta,
        },
        "model1": m1_data or image_result,
        "video_inference": video_result,
        "model2": m2_data or {
            "status": "not_applicable",
            "message": "No visual media provided for disease detection.",
        },
        "knowledge": knowledge_data,
        "knowledge_sources": knowledge_sources,
        "annotated_preview_url": annotated_preview,
        "unified_state": {
            "input_types": inputs_dict,
            "language": detected_language,
            "original_text": text or audio_transcription or final_query,
            "normalized_text": final_query,
            "intent": routing.get("intent", "unknown"),
            "routing_metadata": routing_meta,
        },
        "debug": {
            "input_types": inputs_dict,
            "language": detected_language,
            "intent": routing.get("intent", "unknown"),
            "needs_model1": routing_meta["needs_model1"],
            "needs_model2": routing_meta["needs_model2"],
            "needs_rag": routing_meta["needs_rag"],
            "device": DEVICE_NAME,
        },
    }
