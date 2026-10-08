"""
Query Understanding & Intent Router Layer
=========================================
Processes multimodal agricultural inputs:
  USER INPUT -> TEXT NORMALIZATION -> ENTITY EXTRACTION -> INTENT CLASSIFICATION -> CONTEXT-AWARE ROUTING

Maintains 100% backward compatibility for existing pipeline/services while exposing
the rich 12-intent taxonomy, confidence calibration, and entity context.
"""

from __future__ import annotations

import logging
from typing import Any, Optional, Union

from router.entity_extractor import extract_entities
from router.intent_classifier import classify_intent_from_text
from router.normalizer import normalize_text
from router.taxonomy import (
    INTENT_ROUTING_MAP,
    ExtractedEntities,
    Intent,
    QueryUnderstandingResult,
)

logger = logging.getLogger(__name__)

# Backward-compatibility intent string mappings for legacy callers
LEGACY_INTENT_MAP = {
    Intent.IDENTIFY_CROP: "plant_identification",
    Intent.CHECK_HEALTH: "disease_detection",
    Intent.DIAGNOSE_PLANT: "disease_detection",
    Intent.IDENTIFY_DISEASE: "disease_detection",
    Intent.SYMPTOMS: "disease_detection",
    Intent.CAUSE: "treatment_information",
    Intent.TREATMENT: "treatment_information",
    Intent.PREVENTION: "treatment_information",
    Intent.GENERAL_PLANT_INFO: "general_plant_information",
    Intent.FOLLOW_UP: "treatment_information",
    Intent.AMBIGUOUS: "unknown",
    Intent.INSUFFICIENT_INFORMATION: "unknown",
}

INTENTS = tuple(i.value for i in Intent)


def classify_intent(query: str) -> str:
    """Legacy helper: classifies raw string into legacy intent name."""
    res = route_multimodal_query(text=query)
    return LEGACY_INTENT_MAP.get(Intent(res.intent), "unknown")



def generate_clarification_message(
    intent: Intent,
    entities: ExtractedEntities,
    has_visual_context: bool,
    reason: Optional[str] = None,
) -> str:
    """Generates helpful, non-hallucinatory guidance when intent is ambiguous or information is missing."""
    if intent == Intent.INSUFFICIENT_INFORMATION or not has_visual_context:
        return (
            "Please tell me what you want to know—for example, whether the plant is healthy, "
            "what disease it has, or how to treat it. You can also upload a clear leaf photo for automated diagnosis."
        )
    return (
        "I couldn't quite understand your request. You can ask me to identify the plant, "
        "check if it is healthy, diagnose leaf spots or damage, or suggest disease treatment and prevention."
    )


def route_multimodal_query(
    text: Optional[str] = None,
    visual_result: Optional[dict[str, Any]] = None,
    session_context: Optional[dict[str, Any]] = None,
    image_path: Optional[str] = None,
    video_path: Optional[str] = None,
    audio_transcript: Optional[str] = None,
) -> QueryUnderstandingResult:
    """
    Main entry point for multimodal query understanding and intent routing.
    """
    # 1. Combine typed text and audio transcript if present
    query_text = (text or "").strip()
    if not query_text and audio_transcript:
        query_text = audio_transcript.strip()

    has_visual = visual_result is not None or image_path is not None or video_path is not None

    # 2. Text Normalization
    normalized_text, language = normalize_text(query_text)

    # 3. Entity Extraction
    entities = extract_entities(normalized_text, language=language)

    # 4. Merge Visual Context into Entities if missing from text
    active_context = {}
    if visual_result:
        crop_from_vis = visual_result.get("crop")
        disease_from_vis = visual_result.get("disease")
        status_from_vis = visual_result.get("status")

        if crop_from_vis and not entities.crop:
            entities.crop = crop_from_vis.lower()
        if disease_from_vis and not entities.disease:
            entities.disease = disease_from_vis

        active_context = {
            "crop": crop_from_vis,
            "disease": disease_from_vis,
            "status": status_from_vis,
            "crop_confidence": visual_result.get("crop_confidence"),
            "disease_confidence": visual_result.get("disease_confidence"),
        }

    # Merge session context if available
    if session_context:
        for k, v in session_context.items():
            if k not in active_context and v is not None:
                active_context[k] = v

    # 5. Intent Classification
    intent, confidence, needs_clarification, reason = classify_intent_from_text(
        normalized_text=normalized_text,
        entities=entities,
        has_visual_context=has_visual,
    )

    # 6. Resolve Routing Capabilities
    m1, m2, rag, domain = INTENT_ROUTING_MAP.get(
        intent, (False, False, False, "general")
    )

    # If visual result is ALREADY provided, ML inference was already run
    if visual_result:
        m1 = False
        m2 = False

    clarification_msg = None
    if needs_clarification:
        clarification_msg = generate_clarification_message(
            intent=intent,
            entities=entities,
            has_visual_context=has_visual,
            reason=reason,
        )

    return QueryUnderstandingResult(
        raw_text=query_text,
        normalized_text=normalized_text,
        intent=intent.value,
        intent_confidence=confidence,
        entities=entities,
        needs_model1=m1,
        needs_model2=m2,
        needs_rag=rag,
        target_knowledge_domain=domain,
        needs_clarification=needs_clarification,
        clarification_reason=reason,
        suggested_clarification=clarification_msg,
        context=active_context,
    )


def route_query(query: Union[str, dict[str, Any]]) -> dict[str, Any]:
    """
    Backward-compatible wrapper returning the classic dictionary format
    while attaching the full QueryUnderstandingResult.
    """
    if isinstance(query, dict):
        text = query.get("text", "")
        vis = query.get("visual_result")
        ctx = query.get("session_context")
    else:
        text = str(query) if query is not None else ""
        vis = None
        ctx = None

    result = route_multimodal_query(
        text=text,
        visual_result=vis,
        session_context=ctx,
    )

    # Map to legacy intent name if needed by older callers
    legacy_intent = LEGACY_INTENT_MAP.get(Intent(result.intent), "unknown")

    return {
        "intent": legacy_intent,
        "official_intent": result.intent,
        "intent_confidence": result.intent_confidence,
        "needs_model1": result.needs_model1,
        "needs_model2": result.needs_model2,
        "needs_rag": result.needs_rag,
        "entities": result.entities.to_dict(),
        "normalized_text": result.normalized_text,
        "needs_clarification": result.needs_clarification,
        "clarification_reason": result.clarification_reason,
        "suggested_clarification": result.suggested_clarification,
        "context": result.context,
    }


if __name__ == "__main__":
    import sys
    test_q = " ".join(sys.argv[1:]) or "my tamato patte are yelow what happend"
    res = route_multimodal_query(text=test_q)
    import pprint
    pprint.pprint(res.to_dict())
