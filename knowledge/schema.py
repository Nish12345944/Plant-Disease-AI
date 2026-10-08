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


class PathogenType(str, Enum):
    FUNGAL = "Fungal"
    BACTERIAL = "Bacterial"
    OOMYCETE = "Oomycete"
    VIRAL = "Viral"
    PEST = "Pest"
    PHYSIOLOGICAL = "Physiological"
    ALGAL = "Algal"


class PlantPart(str, Enum):
    LEAF = "leaf"
    STEM = "stem"
    FRUIT = "fruit"
    FLOWER = "flower"
    ROOT = "root"
    TWIG = "twig"
    HEAD = "head"
    TUBER = "tuber"
    SEED = "seed"
    WHOLE_PLANT = "whole plant"
    PETIOLE = "petiole"
    SHOOT = "shoot"
    CANE = "cane"
    CALYX = "calyx"
    RUNNER = "runner"
    CROWN = "crown"
    SHEATH = "sheath"
    EAR = "ear"
    TASSEL = "tassel"
    STALK = "stalk"
    PANICLE = "panicle"
    NODE = "node"
    COLLAR = "collar"
    GLUME = "glume"
    SPIKELET = "spikelet"
    HEART = "heart"
    HUSK = "husk"
    POD = "pod"


class ChemicalControl:
    def __init__(
        self,
        active_ingredient: str = "",
        target_pathogen: str = "",
        application_method: str = "",
        restrictions: str = "",
        source: str = "",
        application_purpose: str = "",
        limitations: str = "",
        source_id: str = "",
    ):
        self.active_ingredient = active_ingredient
        self.target_pathogen = target_pathogen
        self.application_method = application_method or application_purpose
        self.restrictions = restrictions or limitations
        self.source = source or source_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "active_ingredient": self.active_ingredient,
            "target_pathogen": self.target_pathogen,
            "application_method": self.application_method,
            "restrictions": self.restrictions,
            "source": self.source,
        }


class CulturalControl:
    def __init__(
        self,
        practice: str = "",
        timing: str = "",
        purpose: str = "",
        effectiveness: str = "High",
        description: str = "",
        source_id: str = "",
    ):
        self.practice = practice or description
        self.timing = timing or "Throughout growing season"
        self.purpose = purpose or description
        self.effectiveness = effectiveness
        self.source_id = source_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "practice": self.practice,
            "timing": self.timing,
            "purpose": self.purpose,
            "effectiveness": self.effectiveness,
        }


class BiologicalControl:
    def __init__(
        self,
        agent: str = "",
        target_stage: str = "",
        application_method: str = "",
        source: str = "",
        agent_name: str = "",
        source_id: str = "",
    ):
        self.agent = agent or agent_name
        self.target_stage = target_stage or "Active disease cycle"
        self.application_method = application_method
        self.source = source or source_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent": self.agent,
            "target_stage": self.target_stage,
            "application_method": self.application_method,
            "source": self.source,
        }


class TreatmentPlan:
    def __init__(
        self,
        immediate_actions: Optional[list[str]] = None,
        cultural_controls: Optional[list[Any]] = None,
        biological_controls: Optional[list[Any]] = None,
        chemical_controls: Optional[list[Any]] = None,
        organic_alternatives: Optional[list[str]] = None,
        curative: Optional[list[Any]] = None,
        management: Optional[list[Any]] = None,
        chemical: Optional[list[Any]] = None,
        biological: Optional[list[Any]] = None,
    ):
        self.immediate_actions = immediate_actions or []
        cult = (cultural_controls or []) + (curative or []) + (management or [])
        self.cultural_controls = [c if isinstance(c, CulturalControl) else CulturalControl(description=str(c)) for c in cult]
        bio = (biological_controls or []) + (biological or [])
        self.biological_controls = [b if isinstance(b, BiologicalControl) else BiologicalControl(agent=str(b)) for b in bio]
        chem = (chemical_controls or []) + (chemical or [])
        self.chemical_controls = [ch if isinstance(ch, ChemicalControl) else ChemicalControl(active_ingredient=str(ch)) for ch in chem]
        self.organic_alternatives = organic_alternatives or []

    def to_dict(self) -> dict[str, Any]:
        return {
            "immediate_actions": self.immediate_actions,
            "cultural_controls": [c.to_dict() for c in self.cultural_controls],
            "biological_controls": [b.to_dict() for b in self.biological_controls],
            "chemical_controls": [ch.to_dict() for ch in self.chemical_controls],
            "organic_alternatives": self.organic_alternatives,
        }


class PreventionProtocol:
    def __init__(
        self,
        sanitation_measures: Optional[list[str]] = None,
        cultural_preventions: Optional[list[str]] = None,
        resistant_varieties: str = "",
        monitoring_schedule: str = "",
        cultural_practices: Optional[list[str]] = None,
    ):
        self.sanitation_measures = sanitation_measures or []
        self.cultural_preventions = cultural_preventions or cultural_practices or []
        self.resistant_varieties = resistant_varieties
        self.monitoring_schedule = monitoring_schedule or "Regular weekly scouting"

    def to_dict(self) -> dict[str, Any]:
        return {
            "sanitation_measures": self.sanitation_measures,
            "cultural_preventions": self.cultural_preventions,
            "resistant_varieties": self.resistant_varieties,
            "monitoring_schedule": self.monitoring_schedule,
        }


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

    @property
    def id(self) -> str:
        return self.source_id

    @property
    def name(self) -> str:
        return self.organization or self.title or self.source_id

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


class DiseaseRecord:
    """Authoritative structured disease profile."""

    def __init__(
        self,
        disease_slug: Optional[str] = None,
        common_name: Optional[str] = None,
        crop: Optional[str] = None,
        scientific_name_causal_agent: Optional[str] = None,
        disease_type: Optional[str] = None,
        affected_parts: Optional[list[Any]] = None,
        symptoms: Optional[list[Any]] = None,
        distinguishing_features: Optional[list[Any]] = None,
        causes_and_conditions: Optional[list[Any]] = None,
        spread_and_transmission: Optional[list[Any]] = None,
        recurrence_and_survival: Optional[list[Any]] = None,
        management: Optional[Any] = None,
        prevention: Optional[Any] = None,
        sources: Optional[list[Any]] = None,
        quality_level: str = "HIGH",
        treatment_category: str = "management",
        differential_diagnosis: Optional[list[Any]] = None,
        immediate_actions: Optional[list[Any]] = None,
        treatment_limitations: Optional[Any] = None,
        severity_indicators: Optional[Any] = None,
        resistant_varieties: Optional[Any] = None,
        # Aliases for commodity builders
        id: Optional[str] = None,
        disease_id: Optional[str] = None,
        canonical_name: Optional[str] = None,
        crop_name: Optional[str] = None,
        pathogen_name: Optional[str] = None,
        pathogen_type: Optional[Any] = None,
        symptom_progression: Optional[Any] = None,
        favorable_conditions: Optional[Any] = None,
        development_conditions: Optional[Any] = None,
        spread_transmission: Optional[Any] = None,
        transmission_mode: Optional[Any] = None,
        infection_sources: Optional[Any] = None,
        primary_sources: Optional[list[Any]] = None,
        treatment: Optional[Any] = None,
        treatment_plan: Optional[Any] = None,
        prevention_protocol: Optional[Any] = None,
        similar_diseases: Optional[list[Any]] = None,
        **kwargs: Any,
    ):
        self.disease_slug = str(disease_slug or disease_id or id or "")
        self.common_name = str(common_name or canonical_name or "")
        self.crop = str(crop or crop_name or "")
        self.scientific_name_causal_agent = str(scientific_name_causal_agent or pathogen_name or "")

        # Disease type
        raw_type = disease_type or (pathogen_type.value if hasattr(pathogen_type, "value") else str(pathogen_type or "Fungal"))
        self.disease_type = raw_type

        # Affected parts
        self.affected_parts = [
            p.value if hasattr(p, "value") else str(p) for p in (affected_parts or [])
        ]

        # Extract source IDs helper
        src_ids: list[str] = []
        if sources:
            for s in sources:
                if hasattr(s, "source_id"):
                    src_ids.append(s.source_id)
                elif hasattr(s, "name"):
                    src_ids.append(s.name)
                else:
                    src_ids.append(str(s))
        self.sources = src_ids

        # Symptoms
        norm_symptoms: list[SourcedFact] = []
        for sym in (symptoms or []):
            if isinstance(sym, SourcedFact):
                norm_symptoms.append(sym)
            else:
                norm_symptoms.append(SourcedFact(statement=str(sym), source_ids=src_ids))
        self.symptoms = norm_symptoms

        # Distinguishing features / Symptom progression
        norm_df: list[SourcedFact] = []
        if distinguishing_features:
            for df in distinguishing_features:
                norm_df.append(df if isinstance(df, SourcedFact) else SourcedFact(statement=str(df), source_ids=src_ids))
        elif symptom_progression:
            norm_df.append(SourcedFact(statement=str(symptom_progression), source_ids=src_ids))
        self.distinguishing_features = norm_df

        # Causes and conditions / Favorable conditions / Development conditions
        norm_cc: list[SourcedFact] = []
        if causes_and_conditions:
            for cc in causes_and_conditions:
                norm_cc.append(cc if isinstance(cc, SourcedFact) else SourcedFact(statement=str(cc), source_ids=src_ids))
        elif development_conditions:
            norm_cc.append(SourcedFact(statement=str(development_conditions), source_ids=src_ids))
        elif favorable_conditions:
            norm_cc.append(SourcedFact(statement=str(favorable_conditions), source_ids=src_ids))
        self.causes_and_conditions = norm_cc

        # Spread and transmission / Transmission mode
        norm_st: list[SourcedFact] = []
        if spread_and_transmission:
            for st in spread_and_transmission:
                norm_st.append(st if isinstance(st, SourcedFact) else SourcedFact(statement=str(st), source_ids=src_ids))
        elif spread_transmission:
            norm_st.append(SourcedFact(statement=str(spread_transmission), source_ids=src_ids))
        elif transmission_mode:
            norm_st.append(SourcedFact(statement=str(transmission_mode), source_ids=src_ids))
        self.spread_and_transmission = norm_st

        # Recurrence and survival / Primary sources / Infection sources
        norm_rs: list[SourcedFact] = []
        if recurrence_and_survival:
            for rs in recurrence_and_survival:
                norm_rs.append(rs if isinstance(rs, SourcedFact) else SourcedFact(statement=str(rs), source_ids=src_ids))
        elif infection_sources:
            norm_rs.append(SourcedFact(statement=str(infection_sources), source_ids=src_ids))
        elif primary_sources:
            for ps in primary_sources:
                norm_rs.append(SourcedFact(statement=str(ps), source_ids=src_ids))
        self.recurrence_and_survival = norm_rs

        # Management / Treatment plan / Treatment
        eff_treatment = treatment or treatment_plan
        if isinstance(management, ManagementStrategies):
            self.management = management
        elif eff_treatment is not None:
            cult_facts = [
                SourcedFact(statement=f"{c.practice}: {c.purpose}" if c.purpose and c.purpose != c.practice else str(c.practice), source_ids=[c.source_id] if hasattr(c, "source_id") and c.source_id else src_ids)
                for c in getattr(eff_treatment, "cultural_controls", [])
            ]
            bio_facts = [
                SourcedFact(statement=f"{b.agent} ({b.application_method})" if b.application_method else str(b.agent), source_ids=[b.source] if b.source else src_ids)
                for b in getattr(eff_treatment, "biological_controls", [])
            ]
            chem_facts = [
                SourcedFact(statement=f"{ch.active_ingredient}: {ch.application_method}. {ch.restrictions}".strip(". "), source_ids=[ch.source] if ch.source else src_ids)
                for ch in getattr(eff_treatment, "chemical_controls", [])
            ]
            san_facts = [
                SourcedFact(statement=str(ia), source_ids=src_ids)
                for ia in getattr(eff_treatment, "immediate_actions", [])
            ]
            int_summary = [
                SourcedFact(statement=str(org), source_ids=src_ids)
                for org in getattr(eff_treatment, "organic_alternatives", [])
            ]
            self.management = ManagementStrategies(
                cultural=cult_facts,
                sanitation=san_facts,
                environmental=[],
                biological=bio_facts,
                chemical_guidelines=chem_facts,
                integrated_summary=int_summary,
            )
        else:
            self.management = ManagementStrategies()

        # Prevention / Prevention protocol
        eff_prev = prevention or prevention_protocol
        norm_prev: list[SourcedFact] = []
        if isinstance(eff_prev, list):
            for p in eff_prev:
                norm_prev.append(p if isinstance(p, SourcedFact) else SourcedFact(statement=str(p), source_ids=src_ids))
        elif isinstance(eff_prev, PreventionProtocol):
            for sm in eff_prev.sanitation_measures:
                norm_prev.append(SourcedFact(statement=f"Sanitation: {sm}", source_ids=src_ids))
            for cp in eff_prev.cultural_preventions:
                norm_prev.append(SourcedFact(statement=f"Cultural prevention: {cp}", source_ids=src_ids))
            if eff_prev.monitoring_schedule:
                norm_prev.append(SourcedFact(statement=f"Monitoring: {eff_prev.monitoring_schedule}", source_ids=src_ids))
        self.prevention = norm_prev

        self.quality_level = quality_level
        self.treatment_category = treatment_category

        # Differential diagnosis / Similar diseases
        eff_diff = differential_diagnosis or similar_diseases or []
        norm_diff: list[SourcedFact] = []
        for diff in eff_diff:
            norm_diff.append(diff if isinstance(diff, SourcedFact) else SourcedFact(statement=str(diff), source_ids=src_ids))
        self.differential_diagnosis = norm_diff

        # Immediate actions
        norm_ia: list[SourcedFact] = []
        raw_ia = immediate_actions or (eff_treatment.immediate_actions if eff_treatment else [])
        for ia in raw_ia:
            norm_ia.append(ia if isinstance(ia, SourcedFact) else SourcedFact(statement=str(ia), source_ids=src_ids))
        self.immediate_actions = norm_ia

        # Treatment limitations
        norm_tl: list[SourcedFact] = []
        if treatment_limitations:
            if isinstance(treatment_limitations, list):
                for tl in treatment_limitations:
                    norm_tl.append(tl if isinstance(tl, SourcedFact) else SourcedFact(statement=str(tl), source_ids=src_ids))
            else:
                norm_tl.append(SourcedFact(statement=str(treatment_limitations), source_ids=src_ids))
        self.treatment_limitations = norm_tl

        # Severity indicators
        norm_si: list[SourcedFact] = []
        if severity_indicators:
            if isinstance(severity_indicators, list):
                for si in severity_indicators:
                    norm_si.append(si if isinstance(si, SourcedFact) else SourcedFact(statement=str(si), source_ids=src_ids))
            else:
                norm_si.append(SourcedFact(statement=str(severity_indicators), source_ids=src_ids))
        self.severity_indicators = norm_si

        # Resistant varieties
        norm_rv: list[SourcedFact] = []
        raw_rv = resistant_varieties or (prevention_protocol.resistant_varieties if prevention_protocol else "")
        if raw_rv:
            if isinstance(raw_rv, list):
                for rv in raw_rv:
                    norm_rv.append(rv if isinstance(rv, SourcedFact) else SourcedFact(statement=str(rv), source_ids=src_ids))
            else:
                norm_rv.append(SourcedFact(statement=str(raw_rv), source_ids=src_ids))
        self.resistant_varieties = norm_rv

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
            "quality_level": self.quality_level,
            "treatment_category": self.treatment_category,
            "differential_diagnosis": [f.to_dict() for f in self.differential_diagnosis],
            "immediate_actions": [f.to_dict() for f in self.immediate_actions],
            "treatment_limitations": [f.to_dict() for f in self.treatment_limitations],
            "severity_indicators": [f.to_dict() for f in self.severity_indicators],
            "resistant_varieties": [f.to_dict() for f in self.resistant_varieties],
        }


class CropRecord:
    """General agronomy profile for a supported crop."""

    def __init__(
        self,
        crop_name: Optional[str] = None,
        common_name: Optional[str] = None,
        scientific_name: Optional[str] = None,
        category: str = "Vegetable",
        optimal_growing_conditions: Optional[list[Any]] = None,
        watering_guidelines: Optional[list[Any]] = None,
        common_diseases: Optional[list[str]] = None,
        sources: Optional[list[Any]] = None,
        # Aliases for commodity builders
        crop_id: Optional[str] = None,
        canonical_name: Optional[str] = None,
        botanical_name: Optional[str] = None,
        family: Optional[str] = None,
        growth_stages: Optional[list[str]] = None,
        optimal_ph: Optional[str] = None,
        optimal_temp: Optional[str] = None,
        water_needs: Optional[str] = None,
        known_diseases: Optional[list[str]] = None,
    ):
        self.crop_name = str(crop_name or crop_id or "")
        self.common_name = str(common_name or canonical_name or "")
        self.scientific_name = str(scientific_name or botanical_name or "")
        self.category = str(category or family or "Vegetable")

        # Sources
        src_ids = []
        for s in (sources or []):
            if hasattr(s, "source_id"):
                src_ids.append(s.source_id)
            elif hasattr(s, "name"):
                src_ids.append(s.name)
            else:
                src_ids.append(str(s))
        self.sources = src_ids

        # Optimal growing conditions
        norm_ogc: list[SourcedFact] = []
        if optimal_growing_conditions:
            for ogc in optimal_growing_conditions:
                norm_ogc.append(ogc if isinstance(ogc, SourcedFact) else SourcedFact(statement=str(ogc), source_ids=src_ids))
        else:
            if optimal_temp:
                norm_ogc.append(SourcedFact(statement=f"Optimal temperature: {optimal_temp}", source_ids=src_ids))
            if optimal_ph:
                norm_ogc.append(SourcedFact(statement=f"Optimal soil pH: {optimal_ph}", source_ids=src_ids))
            if growth_stages:
                norm_ogc.append(SourcedFact(statement=f"Growth stages: {', '.join(growth_stages)}", source_ids=src_ids))
        self.optimal_growing_conditions = norm_ogc

        # Watering guidelines
        norm_wg: list[SourcedFact] = []
        if watering_guidelines:
            for wg in watering_guidelines:
                norm_wg.append(wg if isinstance(wg, SourcedFact) else SourcedFact(statement=str(wg), source_ids=src_ids))
        elif water_needs:
            norm_wg.append(SourcedFact(statement=str(water_needs), source_ids=src_ids))
        self.watering_guidelines = norm_wg

        # Common diseases
        self.common_diseases = list(common_diseases or known_diseases or [])

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
