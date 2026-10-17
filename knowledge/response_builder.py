"""
Deterministic Natural-Language Response Builder (No-LLM)
=========================================================
Composes grounded, human-readable conversational responses from verified
factual answer plans without generative hallucination or cloud LLM dependencies.
"""

from __future__ import annotations

from typing import Any, Optional

from knowledge.schema import AnswerPlan, FinalAgentResponse, StructuredReasoningResult
from knowledge.treatment import get_disease_treatment
from router.taxonomy import Intent


def build_response(
    plan: AnswerPlan,
    reasoning: StructuredReasoningResult,
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    status: Optional[str] = None,
    visual_evidence: Optional[dict[str, Any]] = None,
) -> FinalAgentResponse:
    """
    Renders structured sections of the answer plan into polished natural language.
    """
    facts = plan.retrieved_facts
    sections = plan.target_sections
    sources = plan.sources_cited
    lines: list[str] = []

    if not crop:
        crop_title = "Plant"
    else:
        clean_c = crop.lower().strip()
        if clean_c in ("bellpepper", "capsicum", "bell_pepper"):
            crop_title = "Bell Pepper"
        elif clean_c in ("french_bean", "bean"):
            crop_title = "French Bean"
        elif clean_c == "cherry_tomato":
            crop_title = "Cherry Tomato"
        else:
            crop_title = clean_c.replace("_", " ").title()
    disease_title = None
    if disease:
        if "__" in disease:
            disease_title = disease.split("__", 1)[1].replace("_", " ").title()
        else:
            disease_title = disease.replace("_", " ").title()

    # -----------------------------------------------------------------------
    # 0. Mode-Specific Single-Topic Dispatches
    # -----------------------------------------------------------------------
    if "unrecognized_notice" in sections:
        msg = (
            "I couldn't relate your instruction to plant identification, disease diagnosis, or crop care. "
            "You can ask me to identify a plant, check for visible disease symptoms, or explain treatments and care guidelines."
        )
        return FinalAgentResponse(
            text=msg,
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="clarification_needed",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=True,
            structured_data={"clarification_prompt": msg},
        )

    # MODE 2: Plant/crop identification only ("What plant is this?")
    if "crop_identification_only" in sections:
        conf_str = ""
        if visual_evidence and visual_evidence.get("crop_confidence"):
            conf_str = f" ({visual_evidence['crop_confidence']*100:.1f}% confidence)"
        lines.append(f"This plant is identified as **{crop_title}**{conf_str}.")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=None,
            status="healthy" if reasoning.status == "healthy" else "identified",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=False,
            structured_data={"crop": crop, "treatment": None},
        )

    # MODE 1: Disease identification only ("What disease is this?", "What is wrong with this plant?")
    if "disease_identification_only" in sections:
        lines.append(f"PLANT: {crop_title}")
        lines.append(f"DISEASE: {disease_title or 'No Disease Detected'}")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="diseased",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=False,
            structured_data={
                "crop": crop,
                "disease": disease,
                "treatment": None,
            },
        )

    if "disease_healthy_identification_only" in sections:
        lines.append(f"PLANT: {crop_title}")
        lines.append("DISEASE: No Disease Detected (Healthy Specimen)")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=None,
            status="healthy",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=False,
            structured_data={"crop": crop, "status": "healthy", "treatment": None},
        )

    if "disease_uncertain_identification_only" in sections:
        lines.append(f"PLANT: {crop_title}")
        lines.append("DISEASE: Inconclusive / Uncertain")
        lines.append(f"Visual symptoms for this {crop_title} are ambiguous or below the diagnostic confidence threshold.")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="uncertain",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=True,
            structured_data={"crop": crop, "status": "uncertain", "treatment": None},
        )

    # MODE 3 (Uncertain variant): Communicate uncertainty instead of certain treatment
    if "uncertain_treatment_guidance" in sections:
        lines.append(f"The disease diagnosis for this {crop_title.lower()} is uncertain (low model confidence).")
        lines.append("To avoid crop injury from incorrect treatment, verify symptoms before applying chemical sprays.")
        lines.append("\n**Recommended Safe Next Steps:**")
        lines.append("• Isolate affected foliage and ensure leaves remain dry.")
        lines.append("• Inspect whether leaf lesions have concentric rings, water-soaking, or spore masses.")
        lines.append("• Provide a well-lit, close-up photograph of upper and lower leaf surfaces.")
        lines.append("• Consult your local agricultural extension service for confirmed diagnosis.")
        if sources:
            lines.append("\n---")
            citation_texts = [f"{s['title']} ({s['organization']})" for s in sources]
            lines.append(f"**Authoritative Sources:** {'; '.join(citation_texts[:3])}")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="uncertain",
            sources=sources,
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=True,
            structured_data={"crop": crop, "disease": disease, "status": "uncertain", "treatment": None},
        )

    # -----------------------------------------------------------------------
    # 1. Special Case: Clarification Notice / Ambiguity / Missing Info
    # -----------------------------------------------------------------------
    if "clarification_notice" in sections:
        prompt = facts.get("clarification_prompt") or (
            "Please provide additional details or upload a clear photo of the plant leaf so I can assist you accurately."
        )
        return FinalAgentResponse(
            text=prompt,
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status=reasoning.status,
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=True,
            structured_data={"clarification_prompt": prompt},
        )

    # -----------------------------------------------------------------------
    # 2. Special Case: Healthy Confirmation
    # -----------------------------------------------------------------------
    if "healthy_confirmation" in sections:
        conf_str = ""
        if visual_evidence and visual_evidence.get("disease_confidence"):
            conf_str = f" ({visual_evidence['disease_confidence']*100:.1f}% confidence)"

        lines.append(f"Your {crop_title.lower()} appears to be healthy{conf_str}. No symptoms of active disease or fungal lesions were detected.")
        lines.append("\n**Recommended General Maintenance:**")
        lines.append("• Maintain regular baseline watering directly at the soil base using drip or soaker hoses.")
        lines.append("• Ensure proper sunlight and good air circulation to keep foliage dry.")
        lines.append("• Disease treatment or chemical sprays are not needed for healthy plants.")

        citations = [f"{s['title']} ({s['organization']})" for s in sources]
        if citations:
            lines.append(f"\n*Grounded in: {', '.join(citations[:2])}*")

        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=None,
            status="healthy",
            sources=sources,
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=False,
            structured_data={
                "status": "healthy",
                "crop": crop,
                "treatment": facts.get("treatment") or get_disease_treatment(crop=crop, status="healthy"),
            },
        )

    # -----------------------------------------------------------------------
    # 3. Special Case: Uncertain Visual Evidence
    # -----------------------------------------------------------------------
    if "uncertainty_notice" in sections:
        lines.append(f"The visual analysis for this {crop_title.lower()} is uncertain.")
        if disease_title:
            lines.append(f"While symptoms have some similarity to **{disease_title}**, the model confidence is low.")
        lines.append("\n**Recommended Verification Steps:**")
        lines.append("• Inspect whether leaf spots have defined margins, powdery growth, or concentric rings.")
        lines.append("• Check if the problem is confined to lower leaves or spreading to new growth.")
        lines.append("• Provide a well-lit, close-up photograph of both the upper and lower leaf surface.")

        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="uncertain",
            sources=[],
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=True,
            structured_data={
                "status": "uncertain",
                "candidate_disease": disease,
                "treatment": facts.get("treatment") or get_disease_treatment(crop=crop, disease=disease, status="uncertain"),
            },
        )

    # -----------------------------------------------------------------------
    # 4. Special Case: Unverified Knowledge Notice
    # -----------------------------------------------------------------------
    if "unverified_notice" in sections:
        item_name = disease_title or crop_title
        lines.append(f"Information on **{item_name}** is not yet present in my verified local database.")
        lines.append("To ensure safety, please consult authoritative agricultural extension resources:")
        citations = [f"{s['title']} ({s['organization']})" for s in sources]
        if citations:
            lines.append(f"\n*Grounded in: {', '.join(citations[:2])}*")
        return FinalAgentResponse(
            text="\n".join(lines),
            intent=plan.intent,
            crop=crop,
            disease=disease,
            status="unverified",
            sources=sources,
            reasoning_rule=reasoning.applicable_rule,
            needs_clarification=False if sources else True,
            structured_data={"unverified_item": item_name},
        )

    # -----------------------------------------------------------------------
    # 5. Standard Domain-Specific Composition
    # -----------------------------------------------------------------------

    # Condition Identification Header:
    # Omitted when visual_evidence is present because the structured Plant Identification
    # and Disease Detection cards already display the crop, condition, and confidence.
    if not visual_evidence and ("condition_identification" in sections or "diagnosis_summary" in sections):
        causal = facts.get("causal_agent")
        type_str = facts.get("disease_type")

        intro = f"The identified condition on your **{crop_title}** is **{disease_title or 'Disease'}**."
        if causal and type_str:
            intro += f" It is a {type_str.lower()} disease caused by the pathogen *{causal}*."
        lines.append(intro)

    # Symptoms Section
    if not visual_evidence and ("primary_symptoms" in sections or "observed_symptoms" in sections or "symptoms" in facts):
        symptom_list = facts.get("symptoms", [])
        if symptom_list:
            lines.append("\n**Key Diagnostic Symptoms:**")
            for s in symptom_list:
                lines.append(f"• {s['statement']}")

        dist_list = facts.get("distinguishing_features", [])
        if dist_list and "distinguishing_features" in sections:
            lines.append("\n**Distinguishing Characteristics:**")
            for d in dist_list:
                lines.append(f"• {d['statement']}")

        parts = facts.get("affected_parts", [])
        if parts and "affected_plant_parts" in sections:
            lines.append(f"• **Affected Plant Parts:** {', '.join(parts).title()}")

    # Causes and Environmental Conditions
    if not visual_evidence and ("favorable_conditions" in sections or "causes_and_conditions" in facts or "primary_cause" in sections):
        cond_list = facts.get("causes_and_conditions", [])
        if cond_list:
            lines.append("\n**Causes & Favorable Environmental Conditions:**")
            for c in cond_list:
                lines.append(f"• {c['statement']}")

    # Spread and Transmission
    if not visual_evidence and ("spread_mechanism" in sections or "spread_and_transmission" in facts):
        spread_list = facts.get("spread_and_transmission", [])
        if spread_list:
            lines.append("\n**Spread & Transmission:**")
            for sp in spread_list:
                lines.append(f"• {sp['statement']}")

    # Recurrence and Survival
    if not visual_evidence and ("recurrence_and_survival" in facts):
        recur_list = facts.get("recurrence_and_survival", [])
        if recur_list:
            lines.append("\n**Overwintering & Recurrence:**")
            for r in recur_list:
                lines.append(f"• {r['statement']}")

    # Management / Treatment Sections (included when text-only OR when treatment is explicitly requested)
    if not visual_evidence or "treatment_context_header" in sections:
        if "treatment_context_header" in sections:
            if disease_title:
                lines.append(f"Management and treatment guidance for **{disease_title}** on **{crop_title}**:")
            else:
                lines.append(f"Management and care guidance for **{crop_title}**:")

        mgmt = facts.get("management", {})
        if mgmt:
            lines.append("\n**Recommended Management & Treatment Strategies:**")

            cultural = mgmt.get("cultural", [])
            if cultural:
                lines.append("\n*1. Cultural Practices:*")
                for cult in cultural:
                    lines.append(f"• {cult['statement']}")

            sanitation = mgmt.get("sanitation", [])
            if sanitation:
                lines.append("\n*2. Field Sanitation:*")
                for san in sanitation:
                    lines.append(f"• {san['statement']}")

            env = mgmt.get("environmental", [])
            if env:
                lines.append("\n*3. Moisture & Canopy Control:*")
                for e in env:
                    lines.append(f"• {e['statement']}")

            bio = mgmt.get("biological", [])
            if bio:
                lines.append("\n*4. Biological Options:*")
                for b in bio:
                    lines.append(f"• {b['statement']}")

            chem = mgmt.get("chemical_guidelines", [])
            if chem:
                lines.append("\n*5. Sourced Chemical & Fungicide Guidance:*")
                for ch in chem:
                    lines.append(f"• {ch['statement']}")
                    if ch.get("detail"):
                        lines.append(f"  *Note:* {ch['detail']}")

    # Prevention Section (included when text-only OR when treatment/prevention is explicitly requested)
    if not visual_evidence or "treatment_context_header" in sections or "preventive_measures" in sections:
        prev_list = facts.get("prevention", [])
        if prev_list and ("prevention_summary" in sections or "preventive_measures" in sections):
            lines.append("\n**Prevention Guidelines:**")
            for p in prev_list:
                lines.append(f"• {p['statement']}")

    # Crop Overview / Agronomy Section
    if "crop_overview" in sections or "crop_identification" in sections:
        c_name = facts.get("crop_name", crop_title)
        sc_name = facts.get("scientific_name")
        cat = facts.get("category", "")
        lines.append(f"**Crop Profile:** {c_name} (*{sc_name or ''}*) — {cat}")

        opts = facts.get("optimal_conditions", [])
        if opts:
            lines.append("\n**Optimal Growing Conditions:**")
            for o in opts:
                lines.append(f"• {o['statement']}")

        waters = facts.get("watering_guidelines", [])
        if waters:
            lines.append("\n**Watering & Soil Guidelines:**")
            for w in waters:
                lines.append(f"• {w['statement']}")

        common_d = facts.get("common_diseases", [])
        if common_d and "common_disease_risks" in sections:
            clean_d = [cd.split('__')[1].replace('_', ' ').title() if '__' in cd else cd for cd in common_d]
            lines.append(f"\n**Common Disease Vulnerabilities:** {', '.join(clean_d)}")

    # Citations Grounding Footer
    if sources:
        lines.append("\n---")
        citation_texts = [f"{s['title']} ({s['organization']})" for s in sources]
        lines.append(f"**Authoritative Sources:** {'; '.join(citation_texts[:3])}")

    final_text = "\n".join(lines)

    return FinalAgentResponse(
        text=final_text,
        intent=plan.intent,
        crop=crop,
        disease=disease,
        status=status or reasoning.status,
        sources=sources,
        reasoning_rule=reasoning.applicable_rule,
        needs_clarification=False,
        structured_data={
            "crop": crop,
            "disease": disease,
            "status": status or reasoning.status,
            "facts_retrieved_count": len(facts),
            "treatment": facts.get("treatment") or get_disease_treatment(crop=crop, disease=disease, status=status or reasoning.status),
        },
    )
