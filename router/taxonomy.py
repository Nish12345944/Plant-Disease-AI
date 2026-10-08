"""
Centralized Intent Taxonomy and Routing Configuration
======================================================
Defines the official 12-intent taxonomy, confidence thresholds,
knowledge domain mappings, and routing decision rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Intent(str, Enum):
    """The 12 official intent classes for query understanding."""
    IDENTIFY_CROP = "IDENTIFY_CROP"                   # What crop / plant is this?
    CHECK_HEALTH = "CHECK_HEALTH"                     # Is the plant healthy / normal?
    DIAGNOSE_PLANT = "DIAGNOSE_PLANT"                 # What happened / what's wrong with plant?
    IDENTIFY_DISEASE = "IDENTIFY_DISEASE"             # What is the specific disease name?
    SYMPTOMS = "SYMPTOMS"                             # What are the symptoms / signs?
    CAUSE = "CAUSE"                                   # Why did this happen / causes / reasons?
    TREATMENT = "TREATMENT"                           # How to cure / treat / remedies / sprays?
    PREVENTION = "PREVENTION"                         # How to prevent / stop recurrence / protect?
    GENERAL_PLANT_INFO = "GENERAL_PLANT_INFO"         # General cultivation / care / info about crop?
    FOLLOW_UP = "FOLLOW_UP"                           # Contextual follow-up to prior diagnosis
    AMBIGUOUS = "AMBIGUOUS"                           # Low confidence / unclear intent
    INSUFFICIENT_INFORMATION = "INSUFFICIENT_INFO"   # Missing critical data (e.g. query needs image)


# Default confidence thresholds
CONFIDENCE_THRESHOLDS = {
    "high_confidence": 0.85,
    "medium_confidence": 0.60,
    "min_intent_threshold": 0.45,   # Below this, fallback to AMBIGUOUS
    "ambiguous_margin": 0.15,       # If top 2 intents differ by less than this, flag ambiguity
}

# Routing capability mapping: (needs_model1, needs_model2, needs_rag, target_knowledge_domain)
INTENT_ROUTING_MAP = {
    Intent.IDENTIFY_CROP: (True, False, False, "plant_identification"),
    Intent.CHECK_HEALTH: (True, True, False, "health_assessment"),
    Intent.DIAGNOSE_PLANT: (True, True, True, "diagnosis"),
    Intent.IDENTIFY_DISEASE: (True, True, False, "disease_identification"),
    Intent.SYMPTOMS: (True, True, True, "symptom_knowledge"),
    Intent.CAUSE: (True, True, True, "disease_etiology"),
    Intent.TREATMENT: (True, True, True, "treatment_advisory"),
    Intent.PREVENTION: (True, True, True, "prevention_guidelines"),
    Intent.GENERAL_PLANT_INFO: (True, False, True, "general_agronomy"),
    Intent.FOLLOW_UP: (True, True, True, "contextual_follow_up"),
    Intent.AMBIGUOUS: (False, False, False, "clarification"),
    Intent.INSUFFICIENT_INFORMATION: (False, False, False, "clarification"),
}



@dataclass
class ExtractedEntities:
    """Entities extracted from user query and context."""
    crop: Optional[str] = None
    disease: Optional[str] = None
    symptoms: list[str] = field(default_factory=list)
    plant_part: Optional[str] = None
    action: Optional[str] = None
    language: str = "en"

    def to_dict(self) -> dict[str, Any]:
        return {
            "crop": self.crop,
            "disease": self.disease,
            "symptoms": self.symptoms,
            "plant_part": self.plant_part,
            "action": self.action,
            "language": self.language,
        }


@dataclass
class QueryUnderstandingResult:
    """Standardized output contract for the Query Understanding & Intent Router layer."""
    raw_text: str
    normalized_text: str
    intent: str
    intent_confidence: float
    entities: ExtractedEntities
    needs_model1: bool = False
    needs_model2: bool = False
    needs_rag: bool = False
    target_knowledge_domain: str = "general"
    needs_clarification: bool = False
    clarification_reason: Optional[str] = None
    suggested_clarification: Optional[str] = None
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_text": self.raw_text,
            "normalized_text": self.normalized_text,
            "intent": self.intent,
            "intent_confidence": round(float(self.intent_confidence), 4),
            "entities": self.entities.to_dict(),
            "routing_decision": {
                "needs_model1": self.needs_model1,
                "needs_model2": self.needs_model2,
                "needs_rag": self.needs_rag,
                "target_knowledge_domain": self.target_knowledge_domain,
            },
            "needs_clarification": self.needs_clarification,
            "clarification_reason": self.clarification_reason,
            "suggested_clarification": self.suggested_clarification,
            "context": self.context,
        }
