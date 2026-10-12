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
    PROJECT_ROOT,
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
    """Verify services and securely ensure model checkpoints on startup.
    Lazy loads heavy neural models to conserve memory unless EAGER_LOAD_MODELS=true.
    """
    from app.backend.config import EAGER_LOAD_MODELS, MODEL1_CHECKPOINT, MODEL2_CHECKPOINT
    from app.backend.weights_manager import ensure_model_checkpoints

    # Securely synchronize configured model checkpoints from private storage
    try:
        checkpoint_status = ensure_model_checkpoints()
        for name, info in checkpoint_status.items():
            logger.info(f"Checkpoint '{name}' status: {info.get('status')} (available={info.get('available')})")
    except Exception as exc:
        logger.warning(f"Checkpoint synchronization note: {exc}")

    # Verify Knowledge Base in-memory repository
    try:
        get_knowledge_base()
        logger.info("Agricultural Knowledge Base verified and ready.")
    except Exception as exc:
        logger.warning(f"Knowledge base initialization note: {exc}")

    if EAGER_LOAD_MODELS:
        logger.info("EAGER_LOAD_MODELS=true: Pre-warming neural models on startup...")
        try:
            get_model1()
            logger.info("Model 1 initialized successfully.")
        except Exception as exc:
            logger.error(f"Model 1 eager initialization failed: {exc}")
        try:
            m2 = get_model2()
            logger.info("Model 2 V4 initialized successfully.")
        except Exception as exc:
            logger.error(f"Model 2 V4 eager initialization failed: {exc}")
    else:
        logger.info(
            "Lazy model loading active (Render Free / Low-Memory optimization). "
            "Neural models will initialize on the first image/video inference request."
        )
        if not MODEL1_CHECKPOINT.exists():
            logger.warning(f"Note: Model 1 checkpoint not detected at: {MODEL1_CHECKPOINT}")
        if not MODEL2_CHECKPOINT.exists():
            logger.warning(f"Note: Model 2 checkpoint not detected at: {MODEL2_CHECKPOINT}")


@app.get("/api")
async def api_root():
    """Return backend status and API documentation entrypoints."""
    return {
        "service": "Alexa Farms AI Backend",
        "status": "online",
        "device": DEVICE_NAME,
        "api_docs": "/docs",
        "health": "/health",
        "frontend_url": "http://localhost:5173",
        "models": {
            "model1": "Plant Identification (Model 1 - EfficientNet-B2 22 crops)",
            "model2": "Disease & Healthy Classification (Model 2 V4 - EfficientNet-B2 117 classes)",
            "audio": "faster-whisper",
        },
    }


@app.get("/health")
@app.get("/api/health")
async def health_check():
    """Return lightweight system readiness, device specifications, and checkpoint status without model inference."""
    import app.backend.services as srv
    from app.backend.config import (
        MODEL1_CHECKPOINT,
        MODEL2_CHECKPOINT,
        WHISPER_MODEL_SIZE,
    )
    return {
        "status": "healthy",
        "service": "Alexa Farms AI Backend",
        "device": DEVICE_NAME,
        "models": {
            "model1": {
                "name": "EfficientNet-B2 Crop Identifier",
                "loaded": srv._MODEL1 is not None,
                "checkpoint": str(MODEL1_CHECKPOINT),
                "available": MODEL1_CHECKPOINT.exists(),
            },
            "model2": {
                "name": "EfficientNet-B2 V4 Disease Classifier",
                "loaded": srv._MODEL2_V4 is not None,
                "checkpoint": str(MODEL2_CHECKPOINT),
                "available": MODEL2_CHECKPOINT.exists(),
            },
            "audio": {
                "model_size": WHISPER_MODEL_SIZE,
                "available": srv.transcribe_audio is not None,
            },
            "knowledge_base": "ready",
            "router": "ready",
        },
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
    except FileNotFoundError as exc:
        logger.warning(f"Image inference unavailable: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"Inference model checkpoint unavailable: {str(exc)}",
        )
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
    except FileNotFoundError as exc:
        logger.warning(f"Video inference unavailable: {exc}")
        raise HTTPException(
            status_code=503,
            detail=f"Inference model checkpoint unavailable: {str(exc)}",
        )
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
            try:
                image_result = process_image_inference(img_bytes)
            except FileNotFoundError as exc:
                logger.warning(f"Image inference skipped (checkpoint missing): {exc}")
                image_result = {
                    "status": "unavailable",
                    "predicted_crop": None,
                    "confidence": 0.0,
                    "message": f"Vision model checkpoint unavailable: {str(exc)}",
                }
            except Exception as exc:
                logger.error(f"Image inference processing failure: {exc}", exc_info=True)
                image_result = {
                    "status": "error",
                    "predicted_crop": None,
                    "confidence": 0.0,
                    "message": f"Image processing failed: {str(exc)}",
                }

    if video_file is not None:
        vid_bytes = await video_file.read()
        if vid_bytes:
            try:
                video_result = process_video_inference(
                    vid_bytes,
                    original_filename=video_file.filename or "video.mp4",
                    target_frames=target_frames,
                )
            except FileNotFoundError as exc:
                logger.warning(f"Video inference skipped (checkpoint missing): {exc}")
                video_result = {
                    "status": "unavailable",
                    "predicted_crop": None,
                    "confidence": 0.0,
                    "message": f"Video model checkpoint unavailable: {str(exc)}",
                }
            except Exception as exc:
                logger.error(f"Video inference processing failure: {exc}", exc_info=True)
                video_result = {
                    "status": "error",
                    "predicted_crop": None,
                    "confidence": 0.0,
                    "message": f"Video processing failed: {str(exc)}",
                }

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
    vision_unavailable = False

    if image_result:
        if image_result.get("status") in ("unavailable", "error"):
            vision_unavailable = True
            visual_evidence = None
        else:
            m1 = image_result.get("model1", image_result) or {}
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
            has_valid_crop_evidence = bool(crop_name_vis and crop_name_vis.strip().lower() not in ("unknown", "plant", ""))
            has_valid_disease_evidence = bool(disease_slug_vis and disease_slug_vis.strip().lower() not in ("unknown", ""))

            visual_evidence = {
                "crop": crop_name_vis if has_valid_crop_evidence else None,
                "crop_confidence": image_result.get("confidence") or m1.get("confidence", 0.0),
                "disease": disease_slug_vis if has_valid_disease_evidence else None,
                "disease_name": m2.get("primary_disease"),
                "disease_confidence": m2.get("confidence", 0.0),
                "status": eff_status,
                "incompatibility_flag": bool(has_valid_crop_evidence and has_valid_disease_evidence and m2_status == "uncertain" and not m2.get("has_disease")),
            }
    elif video_result:
        if video_result.get("status") in ("unavailable", "error"):
            vision_unavailable = True
            visual_evidence = None
        else:
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

            crop_name_vid = video_result.get("predicted_crop")
            disease_slug_vid = m2.get("primary_disease_slug") or m2.get("primary_disease")
            has_valid_crop_vid = bool(crop_name_vid and crop_name_vid.strip().lower() not in ("unknown", "plant", ""))
            has_valid_disease_vid = bool(disease_slug_vid and disease_slug_vid.strip().lower() not in ("unknown", ""))

            visual_evidence = {
                "crop": crop_name_vid if has_valid_crop_vid else None,
                "crop_confidence": video_result.get("confidence", 0.0),
                "disease": disease_slug_vid if has_valid_disease_vid else None,
                "disease_name": m2.get("primary_disease"),
                "disease_confidence": m2.get("confidence", 0.0),
                "status": eff_status,
                "incompatibility_flag": bool(has_valid_crop_vid and has_valid_disease_vid and m2_status == "uncertain" and not m2.get("has_disease")),
            }

    # Execute deterministic AgriculturalAssistant reasoning and knowledge retrieval
    assistant = get_session_assistant(session_id)
    knowledge_data = None
    knowledge_sources = []

    if vision_unavailable and not typed_clean and not spoken_clean:
        media_label = "video" if has_video else "plant"
        assistant_message = (
            f"Visual {media_label} identification is currently unavailable on this deployment because "
            "the neural model checkpoint is not mounted on this server instance. However, you can describe "
            "your crop and symptoms in text, and I can identify diseases and recommend treatments using the knowledge base!"
        )
        knowledge_data = {
            "status": "checkpoint_unavailable",
            "text": assistant_message,
        }
    else:
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


# ---------------------------------------------------------------------------
# Monolith Static Frontend Serving (Docker / Single-Service Deployments)
# ---------------------------------------------------------------------------
from fastapi.staticfiles import StaticFiles

FRONTEND_DIST = PROJECT_ROOT / "app" / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")
else:
    @app.get("/")
    async def root_fallback():
        return await api_root()
