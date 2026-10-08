"""
Intermediate Answer Planning Engine
===================================
Constructs structured section plans for the deterministic response builder
based on reasoning decisions, user intent, and retrieved verified facts.
"""

from __future__ import annotations

from typing import Any

from knowledge.schema import AnswerPlan, SourceRecord, StructuredReasoningResult
from router.taxonomy import Intent


def plan_answer(
    intent: str,
    reasoning: StructuredReasoningResult,
    retrieved_data: dict[str, Any],
) -> AnswerPlan:
    """
    Formulates a structured answer plan specifying which sections to render.
    """
    sections: list[str] = []
    facts = retrieved_data.get("facts", {})
    sources: list[SourceRecord] = retrieved_data.get("citations", [])

    # Case 1: Clarification needed or Incompatible
    if reasoning.status == "clarification_needed" or reasoning.is_incompatible_rejected:
        return AnswerPlan(
            intent=intent,
            target_sections=["clarification_notice"],
            retrieved_facts={"clarification_prompt": reasoning.clarification_prompt},
            uncertainty_banner="Additional Information Required",
        )

    # Case 2: Healthy confirmation
    if reasoning.status == "healthy":
        sections = ["healthy_confirmation", "crop_care_guidance"]
        return AnswerPlan(
            intent=intent,
            target_sections=sections,
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Case 3: Uncertain visual evidence
    if reasoning.status == "uncertain":
        sections = ["uncertainty_notice", "observed_possibilities", "verification_advice"]
        return AnswerPlan(
            intent=intent,
            target_sections=sections,
            retrieved_facts=facts,
            sources_cited=sources,
            uncertainty_banner="Diagnostic Uncertainty: Low Model Confidence",
        )

    # Case 4: Knowledge not in verified KB
    if reasoning.status == "unverified" or not reasoning.kb_found:
        return AnswerPlan(
            intent=intent,
            target_sections=["unverified_notice"],
            retrieved_facts={
                "crop": reasoning.resolved_crop,
                "disease": reasoning.resolved_disease,
            },
            uncertainty_banner="Verified Agricultural Record Not Found",
        )

    # Case 5: Standard Grounded Knowledge Answering
    if intent in (Intent.TREATMENT.value, "treatment_information"):
        sections = [
            "condition_identification",
            "cultural_management",
            "sanitation_practices",
            "environmental_controls",
            "biological_options",
            "chemical_guidance",
            "prevention_summary",
        ]
    elif intent in (Intent.PREVENTION.value,):
        sections = [
            "condition_identification",
            "preventive_measures",
            "cultural_practices",
        ]
    elif intent in (Intent.CAUSE.value,):
        sections = [
            "condition_identification",
            "causal_agent_and_type",
            "favorable_conditions",
            "spread_mechanism",
        ]
    elif intent in (Intent.SYMPTOMS.value,):
        sections = [
            "condition_identification",
            "primary_symptoms",
            "distinguishing_features",
            "affected_plant_parts",
        ]
    elif intent in (Intent.IDENTIFY_DISEASE.value,):
        sections = [
            "condition_identification",
            "causal_agent_and_type",
            "key_symptoms_summary",
        ]
    elif intent in (Intent.DIAGNOSE_PLANT.value, "diagnosis"):
        sections = [
            "diagnosis_summary",
            "observed_symptoms",
            "primary_cause",
            "immediate_action_steps",
        ]
    elif intent in (Intent.GENERAL_PLANT_INFO.value, "general_plant_information"):
        sections = [
            "crop_overview",
            "optimal_growing_conditions",
            "watering_and_soil",
            "common_disease_risks",
        ]
    elif intent in (Intent.IDENTIFY_CROP.value, "plant_identification"):
        sections = [
            "crop_identification",
            "optimal_growing_conditions",
        ]
    elif intent in (Intent.CHECK_HEALTH.value,):
        sections = [
            "health_evaluation",
            "watering_and_soil",
        ]
    else:
        # Default overview
        sections = [
            "condition_identification",
            "primary_symptoms",
            "management_overview",
        ]

    return AnswerPlan(
        intent=intent,
        target_sections=sections,
        retrieved_facts=facts,
        sources_cited=sources,
    )
