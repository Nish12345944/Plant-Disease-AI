"""
Knowledge Data Models and Reasoning Schemas
============================================
Defines the formal data contracts for:
- Source Registry & Provenance
- Crop & Disease Knowledge Records
- Management & Prevention Strategies
- Dialogue Context & State
- Reasoning Decisions & Answer Plans
- Final Agent Responses
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class SourceTier(str, Enum):
    TIER_1 = "TIER_1"  # Gov / USDA / FAO / National Research / Peer-reviewed
    TIER_2 = "TIER_2"  # University Extension / Recognized Agricultural Institutes
    TIER_3 = "TIER_3"  # General Agronomy Reference (Reviewed)


@dataclass
class SourceRecord:
    """Provenance record for every stored factual claim."""
    source_id: str
    title: str
    organization: str
    url_or_doi: Optional[str] = None
    publication_year: Optional[int] = None
    source_tier: SourceTier = SourceTier.TIER_1
    notes: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "organization": self.organization,
            "url_or_doi": self.url_or_doi,
            "publication_year": self.publication_year,
            "source_tier": self.source_tier.value,
            "notes": self.notes,
        }


@dataclass
class SourcedFact:
    """Individual factual statement linked to source provenance IDs."""
    statement: str
    source_ids: list[str] = field(default_factory=list)
    detail: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "statement": self.statement,
            "source_ids": self.source_ids,
            "detail": self.detail,
        }


@dataclass
class ManagementStrategies:
    """Structured agricultural management approaches."""
    cultural: list[SourcedFact] = field(default_factory=list)
    sanitation: list[SourcedFact] = field(default_factory=list)
    environmental: list[SourcedFact] = field(default_factory=list)
    biological: list[SourcedFact] = field(default_factory=list)
    chemical_guidelines: list[SourcedFact] = field(default_factory=list)
    integrated_summary: list[SourcedFact] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "cultural": [f.to_dict() for f in self.cultural],
            "sanitation": [f.to_dict() for f in self.sanitation],
            "environmental": [f.to_dict() for f in self.environmental],
            "biological": [f.to_dict() for f in self.biological],
            "chemical_guidelines": [f.to_dict() for f in self.chemical_guidelines],
            "integrated_summary": [f.to_dict() for f in self.integrated_summary],
        }


@dataclass
class DiseaseRecord:
    """Authoritative structured disease profile."""
    disease_slug: str                       # e.g. "tomato__early_blight"
    common_name: str                        # e.g. "Early Blight"
    crop: str                               # e.g. "tomato"
    scientific_name_causal_agent: str       # e.g. "Alternaria solani"
    disease_type: str                       # e.g. "Fungal"
    affected_parts: list[str] = field(default_factory=list)
    symptoms: list[SourcedFact] = field(default_factory=list)
    distinguishing_features: list[SourcedFact] = field(default_factory=list)
    causes_and_conditions: list[SourcedFact] = field(default_factory=list)
    spread_and_transmission: list[SourcedFact] = field(default_factory=list)
    recurrence_and_survival: list[SourcedFact] = field(default_factory=list)
    management: ManagementStrategies = field(default_factory=ManagementStrategies)
    prevention: list[SourcedFact] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "disease_slug": self.disease_slug,
            "common_name": self.common_name,
            "crop": self.crop,
            "scientific_name_causal_agent": self.scientific_name_causal_agent,
            "disease_type": self.disease_type,
            "affected_parts": self.affected_parts,
            "symptoms": [f.to_dict() for f in self.symptoms],
            "distinguishing_features": [f.to_dict() for f in self.distinguishing_features],
            "causes_and_conditions": [f.to_dict() for f in self.causes_and_conditions],
            "spread_and_transmission": [f.to_dict() for f in self.spread_and_transmission],
            "recurrence_and_survival": [f.to_dict() for f in self.recurrence_and_survival],
            "management": self.management.to_dict(),
            "prevention": [f.to_dict() for f in self.prevention],
            "sources": self.sources,
        }


@dataclass
class CropRecord:
    """General agronomy profile for a supported crop."""
    crop_name: str
    common_name: str
    scientific_name: Optional[str] = None
    category: str = "Vegetable"
    optimal_growing_conditions: list[SourcedFact] = field(default_factory=list)
    watering_guidelines: list[SourcedFact] = field(default_factory=list)
    common_diseases: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "crop_name": self.crop_name,
            "common_name": self.common_name,
            "scientific_name": self.scientific_name,
            "category": self.category,
            "optimal_growing_conditions": [f.to_dict() for f in self.optimal_growing_conditions],
            "watering_guidelines": [f.to_dict() for f in self.watering_guidelines],
            "common_diseases": self.common_diseases,
            "sources": self.sources,
        }


@dataclass
class DialogueTurn:
    """A single turn in conversational history."""
    turn_id: int
    user_query: str
    normalized_query: str
    intent: str
    crop: Optional[str] = None
    disease: Optional[str] = None
    status: Optional[str] = None
    system_response: str = ""


@dataclass
class DialogueState:
    """Short-term conversational context tracker."""
    turns: list[DialogueTurn] = field(default_factory=list)
    current_crop: Optional[str] = None
    current_disease: Optional[str] = None
    current_status: Optional[str] = None
    last_intent: Optional[str] = None
    last_visual_evidence: Optional[dict[str, Any]] = None

    def add_turn(
        self,
        user_query: str,
        normalized_query: str,
        intent: str,
        crop: Optional[str],
        disease: Optional[str],
        status: Optional[str],
        system_response: str,
    ):
        turn_id = len(self.turns) + 1
        turn = DialogueTurn(
            turn_id=turn_id,
            user_query=user_query,
            normalized_query=normalized_query,
            intent=intent,
            crop=crop or self.current_crop,
            disease=disease or self.current_disease,
            status=status or self.current_status,
            system_response=system_response,
        )
        self.turns.append(turn)
        if crop:
            self.current_crop = crop
        if disease:
            self.current_disease = disease
        if status:
            self.current_status = status
        self.last_intent = intent

        # Retain last 10 turns to avoid memory leak
        if len(self.turns) > 10:
            self.turns = self.turns[-10:]

    def resolve_reference(self, text: str) -> tuple[Optional[str], Optional[str]]:
        """Resolves pronouns like 'it', 'this', 'why' against active dialogue state."""
        text_lower = text.lower()
        pronoun_markers = ["it", "this", "that", "why", "how", "cure it", "treat it", "spread", "prevent it", "happen"]
        has_pronoun = any(re.search(r"\b" + re.escape(p) + r"\b", text_lower) for p in pronoun_markers)
        if has_pronoun or len(text.split()) <= 3:
            return self.current_crop, self.current_disease
        return None, None


@dataclass
class StructuredReasoningResult:
    """Outcome of rule-based agricultural reasoning."""
    applicable_rule: str
    status: str                         # "healthy", "diseased", "uncertain", "general_info", "clarification_needed"
    resolved_crop: Optional[str] = None
    resolved_disease: Optional[str] = None
    confidence_level: str = "high"       # "high", "moderate", "low", "unverified"
    visual_evidence_used: bool = False
    is_incompatible_rejected: bool = False
    kb_found: bool = False
    clarification_prompt: Optional[str] = None
    reasoning_notes: list[str] = field(default_factory=list)


@dataclass
class AnswerPlan:
    """Intermediate structured plan for natural language composition."""
    intent: str
    target_sections: list[str]          # e.g. ["diagnosis_summary", "symptoms_observed", "management_steps", "prevention_tips"]
    retrieved_facts: dict[str, Any] = field(default_factory=dict)
    sources_cited: list[SourceRecord] = field(default_factory=list)
    uncertainty_banner: Optional[str] = None
    caution_notes: list[str] = field(default_factory=list)


@dataclass
class FinalAgentResponse:
    """Final output object returned by the conversational engine."""
    text: str
    intent: str
    crop: Optional[str]
    disease: Optional[str]
    status: str
    sources: list[dict[str, Any]]
    reasoning_rule: str
    needs_clarification: bool = False
    structured_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "intent": self.intent,
            "crop": self.crop,
            "disease": self.disease,
            "status": self.status,
            "sources": self.sources,
            "reasoning_rule": self.reasoning_rule,
            "needs_clarification": self.needs_clarification,
            "structured_data": self.structured_data,
        }
