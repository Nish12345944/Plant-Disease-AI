"""
Structured Rule-Based Agricultural Reasoning Engine
===================================================
Applies deterministic, safety-enforced reasoning rules combining:
- User Intent & Query Entities
- Model 1 & Model 2 Visual Inference Evidence
- Dialogue State & Anaphora Resolution
- Verified Knowledge Base Availability
- Crop-Disease Compatibility Verification
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.schema import StructuredReasoningResult
from router.taxonomy import ExtractedEntities, Intent

logger = logging.getLogger(__name__)


def reason_agricultural_query(
    intent: str,
    raw_query: str,
    entities: ExtractedEntities,
    visual_result: Optional[dict[str, Any]] = None,
    dialogue_crop: Optional[str] = None,
    dialogue_disease: Optional[str] = None,
    dialogue_status: Optional[str] = None,
    kb: Optional[AgriculturalKnowledgeBase] = None,
) -> StructuredReasoningResult:
    """
    Executes the 7 core agricultural reasoning rules.
    """
    if kb is None:
        kb = get_knowledge_base()

    notes: list[str] = []

    # 1. Resolve Effective Crop and Disease Entities
    effective_crop = entities.crop or dialogue_crop
    effective_disease = entities.disease or dialogue_disease
    effective_status = dialogue_status

    visual_used = False
    if visual_result:
        visual_used = True
        v_crop = visual_result.get("crop")
        v_disease = visual_result.get("disease")
        v_status = visual_result.get("status")
        v_conf = visual_result.get("disease_confidence", 1.0)

        if v_crop:
            effective_crop = v_crop.lower()
        if v_disease:
            effective_disease = v_disease.lower()
        if v_status:
            effective_status = v_status.lower()

    # -----------------------------------------------------------------------
    # RULE 1: Healthy Specimen Confirmation -> No Disease Treatment
    # -----------------------------------------------------------------------
    if effective_status == "healthy":
        notes.append("Visual evidence indicates a healthy specimen. Disease treatment is contraindicated.")
        return StructuredReasoningResult(
            applicable_rule="RULE_1_HEALTHY_CONFIRMATION",
            status="healthy",
            resolved_crop=effective_crop,
            resolved_disease=None,
            confidence_level="high",
            visual_evidence_used=visual_used,
            kb_found=kb.get_crop(effective_crop) is not None,
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 3: Crop-Disease Incompatibility Protection
    # -----------------------------------------------------------------------
    if visual_result and visual_result.get("incompatibility_flag"):
        notes.append("Visual inference detected a conflict between the identified crop and disease signature.")
        return StructuredReasoningResult(
            applicable_rule="RULE_3_INCOMPATIBLE_REJECTION",
            status="uncertain",
            resolved_crop=effective_crop,
            resolved_disease=None,
            confidence_level="low",
            visual_evidence_used=True,
            is_incompatible_rejected=True,
            clarification_prompt="The observed symptoms appear incompatible with standard diseases for this crop. Please provide another photo or check the crop type.",
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 2: Uncertain / Low-Confidence Visual Evidence
    # -----------------------------------------------------------------------
    _vis_is_uncertain = visual_result and (
        visual_result.get("uncertain")
        or visual_result.get("is_uncertain")
    )
    _vis_confidence = visual_result and min(
        visual_result.get("disease_confidence", 1.0),
        visual_result.get("confidence", 1.0),
    )
    if effective_status == "uncertain" or _vis_is_uncertain or (_vis_confidence is not None and _vis_confidence < 0.60):
        notes.append("Visual inference confidence is below diagnostic threshold. Model result is uncertain.")
        return StructuredReasoningResult(
            applicable_rule="RULE_2_UNCERTAIN_VISUAL_EVIDENCE",
            status="uncertain",
            resolved_crop=effective_crop,
            resolved_disease=effective_disease,
            confidence_level="low",
            visual_evidence_used=visual_used,
            clarification_prompt="The symptoms are ambiguous or low confidence. Please verify with additional clear photos of the affected leaves.",
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 4: Treatment Requested Without Identified Disease
    # -----------------------------------------------------------------------
    if intent in (Intent.TREATMENT.value, Intent.PREVENTION.value) and not effective_disease:
        notes.append("User requested treatment/prevention but no specific disease was identified or provided.")
        return StructuredReasoningResult(
            applicable_rule="RULE_4_MISSING_DISEASE_FOR_TREATMENT",
            status="clarification_needed",
            resolved_crop=effective_crop,
            resolved_disease=None,
            confidence_level="unverified",
            visual_evidence_used=visual_used,
            clarification_prompt="To recommend appropriate management, I need to know which disease is affecting the plant or see a photo of the affected leaves.",
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 5: Ambiguous Query or Insufficient Information
    # -----------------------------------------------------------------------
    if intent in (Intent.AMBIGUOUS.value, Intent.INSUFFICIENT_INFORMATION.value) and not visual_used and not effective_disease:
        notes.append("Query is ambiguous and no prior conversational or visual context is present.")
        return StructuredReasoningResult(
            applicable_rule="RULE_5_AMBIGUOUS_QUERY",
            status="clarification_needed",
            resolved_crop=effective_crop,
            resolved_disease=None,
            confidence_level="low",
            visual_evidence_used=False,
            clarification_prompt="Please tell me what you want to know—for example, whether the plant is healthy, what disease it has, or how to treat it. You can also upload a photo.",
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 7: Missing / Unverified Knowledge Base Record
    # -----------------------------------------------------------------------
    has_kb = False
    if effective_disease:
        d_rec = kb.get_disease(effective_disease)
        if d_rec is not None:
            has_kb = True
            effective_disease = d_rec.disease_slug
            effective_crop = effective_crop or d_rec.crop
    elif effective_crop:
        has_kb = kb.get_crop(effective_crop) is not None

    if (effective_disease or effective_crop) and not has_kb:
        notes.append(f"Target condition '{effective_disease or effective_crop}' is not yet in the verified knowledge base.")
        return StructuredReasoningResult(
            applicable_rule="RULE_7_KNOWLEDGE_UNAVAILABLE",
            status="unverified",
            resolved_crop=effective_crop,
            resolved_disease=effective_disease,
            confidence_level="unverified",
            visual_evidence_used=visual_used,
            kb_found=False,
            reasoning_notes=notes,
        )

    # -----------------------------------------------------------------------
    # RULE 6: Standard Grounded Knowledge & Anaphora Resolution
    # -----------------------------------------------------------------------
    notes.append(f"Successfully grounded intent '{intent}' for crop '{effective_crop}' and disease '{effective_disease}'.")
    return StructuredReasoningResult(
        applicable_rule="RULE_6_GROUNDED_RETRIEVAL",
        status="diseased" if effective_disease else ("general_info" if effective_crop else "general"),
        resolved_crop=effective_crop,
        resolved_disease=effective_disease,
        confidence_level="high",
        visual_evidence_used=visual_used,
        kb_found=has_kb,
        reasoning_notes=notes,
    )
