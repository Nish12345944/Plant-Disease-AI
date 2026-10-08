"""Query Understanding / Intent Router for the Disease_prediction project.

Provides:
- 12-intent classification taxonomy
- Text normalization & Hinglish term handling
- Structured entity extraction
- Context-aware routing
- Full backward-compatibility wrapper
"""

from router.taxonomy import (
    Intent,
    ExtractedEntities,
    QueryUnderstandingResult,
)
from router.normalizer import normalize_text
from router.entity_extractor import extract_entities
from router.intent_classifier import classify_intent_from_text
from router.query_router import (
    INTENTS,
    classify_intent,
    route_query,
    route_multimodal_query,
)

__all__ = [
    "Intent",
    "INTENTS",
    "ExtractedEntities",
    "QueryUnderstandingResult",
    "normalize_text",
    "extract_entities",
    "classify_intent_from_text",
    "classify_intent",
    "route_query",
    "route_multimodal_query",
]
