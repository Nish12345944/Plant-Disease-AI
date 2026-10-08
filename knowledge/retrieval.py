"""
Targeted Agricultural Knowledge Retrieval Engine
================================================
Retrieves specific factual subsets from the verified knowledge base based on:
- User Intent (TREATMENT, CAUSE, SYMPTOMS, PREVENTION, DIAGNOSIS, GENERAL_INFO)
- Crop and Disease Slugs
- Extracted Entities and Plant Parts
- Specific follow-up question types ("spread", "recovery", "recurrence", "danger")
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.schema import (
    CropRecord,
    DiseaseRecord,
    SourcedFact,
)
from knowledge.sources import format_source_citation
from router.taxonomy import ExtractedEntities, Intent

logger = logging.getLogger(__name__)


def retrieve_relevant_knowledge(
    intent: str,
    crop: Optional[str],
    disease: Optional[str],
    entities: Optional[ExtractedEntities] = None,
    query_text: str = "",
    kb: Optional[AgriculturalKnowledgeBase] = None,
) -> dict[str, Any]:
    """
    Selects the targeted factual payload required to answer the user query.
    Does NOT return the entire record; only extracts relevant sections.
    """
    if kb is None:
        kb = get_knowledge_base()

    result: dict[str, Any] = {
        "found": False,
        "disease_record": None,
        "crop_record": None,
        "facts": {},
        "source_ids": [],
        "citations": [],
    }

    d_rec: Optional[DiseaseRecord] = kb.get_disease(disease)
    c_rec: Optional[CropRecord] = kb.get_crop(crop)

    if d_rec:
        result["disease_record"] = d_rec
        result["found"] = True
    if c_rec:
        result["crop_record"] = c_rec
        result["found"] = True

    if not result["found"]:
        return result

    collected_sources: list[str] = []
    facts: dict[str, Any] = {}
    query_lower = query_text.lower()

    # -----------------------------------------------------------------------
    # Follow-up Specific Sub-Topic Filtering (Spread, Survival, Danger)
    # -----------------------------------------------------------------------
    is_spread_question = any(w in query_lower for w in ["spread", "spread to other", "infect other", "contagious"])
    is_recurrence_question = any(w in query_lower for w in ["come back", "recur", "next year", "survive winter", "overwinter"])
    is_part_question = any(w in query_lower for w in ["which part", "what part", "fruit affected", "leaf affected"])

    if d_rec:
        if is_spread_question:
            facts["spread_and_transmission"] = [f.to_dict() for f in d_rec.spread_and_transmission]
            for f in d_rec.spread_and_transmission:
                collected_sources.extend(f.source_ids)

        if is_recurrence_question:
            facts["recurrence_and_survival"] = [f.to_dict() for f in d_rec.recurrence_and_survival]
            for f in d_rec.recurrence_and_survival:
                collected_sources.extend(f.source_ids)

        if is_part_question:
            facts["affected_parts"] = d_rec.affected_parts

    # -----------------------------------------------------------------------
    # Intent-Driven Fact Extraction
    # -----------------------------------------------------------------------
    if intent in (Intent.TREATMENT.value, "treatment_information"):
        if d_rec:
            facts["management"] = d_rec.management.to_dict()
            facts["prevention"] = [f.to_dict() for f in d_rec.prevention]
            for cat in ["cultural", "sanitation", "environmental", "biological", "chemical_guidelines", "integrated_summary"]:
                for f in getattr(d_rec.management, cat, []):
                    collected_sources.extend(f.source_ids)
            for f in d_rec.prevention:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.PREVENTION.value,):
        if d_rec:
            facts["prevention"] = [f.to_dict() for f in d_rec.prevention]
            facts["cultural_management"] = [f.to_dict() for f in d_rec.management.cultural]
            for f in d_rec.prevention:
                collected_sources.extend(f.source_ids)
            for f in d_rec.management.cultural:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.CAUSE.value,):
        if d_rec:
            facts["causal_agent"] = d_rec.scientific_name_causal_agent
            facts["disease_type"] = d_rec.disease_type
            facts["causes_and_conditions"] = [f.to_dict() for f in d_rec.causes_and_conditions]
            facts["spread_and_transmission"] = [f.to_dict() for f in d_rec.spread_and_transmission]
            for f in d_rec.causes_and_conditions:
                collected_sources.extend(f.source_ids)
            for f in d_rec.spread_and_transmission:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.SYMPTOMS.value,):
        if d_rec:
            facts["symptoms"] = [f.to_dict() for f in d_rec.symptoms]
            facts["distinguishing_features"] = [f.to_dict() for f in d_rec.distinguishing_features]
            facts["affected_parts"] = d_rec.affected_parts
            for f in d_rec.symptoms:
                collected_sources.extend(f.source_ids)
            for f in d_rec.distinguishing_features:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.IDENTIFY_DISEASE.value,):
        if d_rec:
            facts["disease_name"] = d_rec.common_name
            facts["causal_agent"] = d_rec.scientific_name_causal_agent
            facts["disease_type"] = d_rec.disease_type
            facts["key_symptoms"] = [f.to_dict() for f in d_rec.symptoms[:2]]
            for f in d_rec.symptoms[:2]:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.DIAGNOSE_PLANT.value, "diagnosis"):
        if d_rec:
            facts["disease_name"] = d_rec.common_name
            facts["causal_agent"] = d_rec.scientific_name_causal_agent
            facts["disease_type"] = d_rec.disease_type
            facts["symptoms"] = [f.to_dict() for f in d_rec.symptoms]
            facts["causes_and_conditions"] = [f.to_dict() for f in d_rec.causes_and_conditions[:1]]
            facts["key_management"] = [f.to_dict() for f in d_rec.management.cultural[:2]]
            for f in d_rec.symptoms:
                collected_sources.extend(f.source_ids)
            for f in d_rec.causes_and_conditions[:1]:
                collected_sources.extend(f.source_ids)
            for f in d_rec.management.cultural[:2]:
                collected_sources.extend(f.source_ids)

    elif intent in (Intent.GENERAL_PLANT_INFO.value, "general_plant_information"):
        if c_rec:
            facts["crop_name"] = c_rec.common_name
            facts["scientific_name"] = c_rec.scientific_name
            facts["category"] = c_rec.category
            facts["optimal_conditions"] = [f.to_dict() for f in c_rec.optimal_growing_conditions]
            facts["watering_guidelines"] = [f.to_dict() for f in c_rec.watering_guidelines]
            facts["common_diseases"] = c_rec.common_diseases
            for f in c_rec.optimal_growing_conditions:
                collected_sources.extend(f.source_ids)
            for f in c_rec.watering_guidelines:
                collected_sources.extend(f.source_ids)
        elif d_rec:
            facts["crop_name"] = d_rec.crop.title()
            facts["related_disease"] = d_rec.common_name

    elif intent in (Intent.CHECK_HEALTH.value,):
        if c_rec:
            facts["crop_name"] = c_rec.common_name
            facts["watering_guidelines"] = [f.to_dict() for f in c_rec.watering_guidelines]
            for f in c_rec.watering_guidelines:
                collected_sources.extend(f.source_ids)

    # Clean and deduplicate source citations
    result["facts"] = facts
    result["source_ids"] = list(dict.fromkeys(collected_sources))
    result["citations"] = format_source_citation(result["source_ids"])
    return result
