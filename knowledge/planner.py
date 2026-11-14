"""
Intermediate Answer Planning Engine
===================================
Constructs structured section plans for the deterministic response builder
based on reasoning decisions, user intent, and retrieved verified facts.
"""

from __future__ import annotations

from typing import Any, Optional

from knowledge.schema import AnswerPlan, SourceRecord, StructuredReasoningResult
from router.taxonomy import Intent


def plan_answer(
    intent: str,
    reasoning: StructuredReasoningResult,
    retrieved_data: dict[str, Any],
    response_mode: Optional[str] = None,
) -> AnswerPlan:
    """
    Formulates a structured answer plan specifying which sections to render based
    on the user's specific response mode and retrieved agricultural facts.
    """
    facts = retrieved_data.get("facts", {})
    sources: list[SourceRecord] = retrieved_data.get("citations", [])

    # Case 0: Unrecognized Instruction
    if response_mode == "unrecognized_instruction":
        return AnswerPlan(
            intent=intent,
            target_sections=["unrecognized_notice"],
            retrieved_facts={},
            sources_cited=[],
        )

    # Case 1: Clarification needed or Incompatible Protection (Strict Priority)
    if reasoning.status == "clarification_needed" or reasoning.is_incompatible_rejected:
        return AnswerPlan(
            intent=intent,
            target_sections=["clarification_notice"],
            retrieved_facts={"clarification_prompt": reasoning.clarification_prompt},
            uncertainty_banner="Additional Information Required",
        )

    # Case 2: Knowledge not in verified KB
    if reasoning.status == "unverified" or not reasoning.kb_found:
        return AnswerPlan(
            intent=intent,
            target_sections=["unverified_notice"],
            retrieved_facts={
                "crop": reasoning.resolved_crop,
                "disease": reasoning.resolved_disease,
                "unverified_query": facts.get("unverified_query"),
            },
            sources_cited=sources,
            uncertainty_banner="Verified Agricultural Record Not Found",
        )

    # Case 3: Uncertain visual evidence
    if reasoning.status == "uncertain":
        if response_mode == "treatment" or intent in (Intent.TREATMENT.value, "treatment_information"):
            return AnswerPlan(
                intent=intent,
                target_sections=["uncertain_treatment_guidance"],
                retrieved_facts=facts,
                sources_cited=sources,
            )
        return AnswerPlan(
            intent=intent,
            target_sections=["uncertainty_notice", "observed_possibilities", "verification_advice"],
            retrieved_facts=facts,
            sources_cited=sources,
            uncertainty_banner="Diagnostic Uncertainty: Low Model Confidence",
        )

    # Case 4: Healthy confirmation
    if reasoning.status == "healthy":
        if response_mode == "disease_identification":
            return AnswerPlan(
                intent=intent,
                target_sections=["disease_healthy_identification_only"],
                retrieved_facts=facts,
                sources_cited=[],
            )
        return AnswerPlan(
            intent=intent,
            target_sections=["healthy_confirmation", "crop_care_guidance"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Case 5: Mode-Specific Single-Aspect Dispatches
    if response_mode == "crop_identification":
        return AnswerPlan(
            intent=intent,
            target_sections=["crop_identification_only"],
            retrieved_facts=facts,
            sources_cited=[],
        )

    if response_mode == "disease_identification":
        # If visual inference was used (e.g. Mode 1 with uploaded image: "What disease is this?")
        if reasoning.visual_evidence_used:
            return AnswerPlan(
                intent=intent,
                target_sections=["disease_identification_only"],
                retrieved_facts=facts,
                sources_cited=[],
            )
        # If pure text question ("What is early blight?"): explain disease and key symptoms
        return AnswerPlan(
            intent=intent,
            target_sections=["disease_overview", "primary_symptoms"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Prevention Intent (prioritize over generic treatment if intent is PREVENTION)
    if intent in (Intent.PREVENTION.value,):
        return AnswerPlan(
            intent=intent,
            target_sections=["prevention_context_header", "prevention_guidelines"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Disease explanation / symptom inquiries without treatment request
    if intent in (Intent.IDENTIFY_DISEASE.value, Intent.SYMPTOMS.value):
        return AnswerPlan(
            intent=intent,
            target_sections=["disease_overview", "primary_symptoms"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Treatment request (Mode 3 or TREATMENT intent)
    if response_mode == "treatment" or intent in (Intent.TREATMENT.value, "treatment_information"):
        return AnswerPlan(
            intent=intent,
            target_sections=[
                "treatment_context_header",
                "curability_section",
                "treatment_control_options",
                "precautions_section",
                "prevention_section",
            ],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    if response_mode == "general_plant_info" or intent in (Intent.GENERAL_PLANT_INFO.value, "general_plant_information"):
        # If user asked about a disease rather than a crop, show disease overview
        if reasoning.resolved_disease and not reasoning.resolved_crop:
            return AnswerPlan(
                intent=intent,
                target_sections=["disease_overview", "primary_symptoms"],
                retrieved_facts=facts,
                sources_cited=sources,
            )
        return AnswerPlan(
            intent=intent,
            target_sections=["crop_overview", "optimal_growing_conditions", "watering_and_soil"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    if intent in (Intent.CAUSE.value,):
        return AnswerPlan(
            intent=intent,
            target_sections=[
                "condition_identification",
                "causal_agent_and_type",
                "favorable_conditions",
                "spread_mechanism",
            ],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    if intent in (Intent.DIAGNOSE_PLANT.value, "diagnosis"):
        return AnswerPlan(
            intent=intent,
            target_sections=[
                "diagnosis_summary",
                "observed_symptoms",
                "primary_cause",
                "immediate_action_steps",
            ],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    if intent in (Intent.IDENTIFY_CROP.value, "plant_identification"):
        return AnswerPlan(
            intent=intent,
            target_sections=["crop_identification", "optimal_growing_conditions"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    if intent in (Intent.CHECK_HEALTH.value,):
        return AnswerPlan(
            intent=intent,
            target_sections=["health_evaluation", "watering_and_soil"],
            retrieved_facts=facts,
            sources_cited=sources,
        )

    # Default overview
    return AnswerPlan(
        intent=intent,
        target_sections=[
            "condition_identification",
            "primary_symptoms",
            "management_overview",
        ],
        retrieved_facts=facts,
        sources_cited=sources,
    )
