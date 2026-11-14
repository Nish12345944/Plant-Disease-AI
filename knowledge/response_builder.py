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

    has_explicit_crop = bool(crop and crop.strip().lower() not in ("unknown", "plant", "none", ""))
    if not has_explicit_crop:
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
    treatment = facts.get("treatment") or get_disease_treatment(
        crop=crop if has_explicit_crop else None,
        disease=disease,
        status=status or reasoning.status,
    )

    # 5.1 Disease Overview / Condition Identification Header
    if "disease_overview" in sections or (not visual_evidence and ("condition_identification" in sections or "diagnosis_summary" in sections)):
        causal = facts.get("causal_agent")
        type_str = facts.get("disease_type")
        d_name = disease_title or facts.get("disease_name") or "Plant Disease"
        if not has_explicit_crop and d_name:
            for ckw in ("Tomato ", "Potato ", "Apple ", "Grape ", "Corn ", "Cucumber ", "Pepper ", "Bell Pepper ", "Bean ", "Cherry "):
                if d_name.startswith(ckw):
                    d_name = d_name[len(ckw):].strip()

        if has_explicit_crop:
            lines.append(f"**{d_name}** on **{crop_title}**:")
        else:
            lines.append(f"**{d_name}**:")

        if causal and type_str:
            lines.append(f"\n**Overview:**\n**{d_name}** is a {type_str.lower()} disease caused by the pathogen *{causal}*.")
        elif causal:
            lines.append(f"\n**Overview:**\n**{d_name}** is caused by the pathogen *{causal}*.")

    # 5.2 Diagnostic Symptoms Section (omitted when visual evidence cards already show diagnosis)
    if not visual_evidence and ("primary_symptoms" in sections or "observed_symptoms" in sections):
        symptom_list = facts.get("symptoms", []) or facts.get("key_symptoms", [])
        if symptom_list:
            lines.append("\n**Key Diagnostic Symptoms:**")
            for s in symptom_list[:4]:
                txt = s if isinstance(s, str) else s.get("statement", str(s))
                lines.append(f"• {txt}")

        dist_list = facts.get("distinguishing_features", [])
        if dist_list and "distinguishing_features" in sections:
            lines.append("\n**Distinguishing Characteristics:**")
            for d in dist_list[:2]:
                txt = d if isinstance(d, str) else d.get("statement", str(d))
                lines.append(f"• {txt}")

        parts = facts.get("affected_parts", [])
        if parts and "affected_plant_parts" in sections:
            lines.append(f"• **Affected Plant Parts:** {', '.join(parts).title()}")

    # 5.3 Causes & Environmental Conditions
    if not visual_evidence and ("favorable_conditions" in sections or "primary_cause" in sections or "causal_agent_and_type" in sections):
        cond_list = facts.get("causes_and_conditions", [])
        if cond_list:
            lines.append("\n**Causes & Favorable Environmental Conditions:**")
            for c in cond_list[:2]:
                txt = c if isinstance(c, str) else c.get("statement", str(c))
                lines.append(f"• {txt}")

    # 5.4 Spread & Transmission
    if not visual_evidence and ("spread_mechanism" in sections):
        spread_list = facts.get("spread_and_transmission", [])
        if spread_list:
            lines.append("\n**Spread & Transmission:**")
            for sp in spread_list[:2]:
                txt = sp if isinstance(sp, str) else sp.get("statement", str(sp))
                lines.append(f"• {txt}")

    # 5.5 Recurrence & Survival
    if not visual_evidence and ("recurrence_and_survival" in sections):
        recur_list = facts.get("recurrence_and_survival", [])
        if recur_list:
            lines.append("\n**Overwintering & Recurrence:**")
            for r in recur_list[:2]:
                txt = r if isinstance(r, str) else r.get("statement", str(r))
                lines.append(f"• {txt}")

    # 5.6 Treatment Context Header
    if "treatment_context_header" in sections:
        if disease_title:
            if has_explicit_crop:
                lines.append(f"Treatment and management for **{disease_title}** on **{crop_title}**:")
            else:
                lines.append(f"Treatment and management for **{disease_title}**:")
                lines.append("*(Note: Recommendations can vary by host crop. If treating a specific plant, please specify the crop name.)*")
        else:
            lines.append(f"Management and care guidance for **{crop_title}**:")

    # 5.7 Curability Section (Treatment Section 1)
    if "curability_section" in sections:
        curable_simple = treatment.get("curable_simple") or (
            "Yes" if treatment.get("can_it_be_cured") == "curable"
            else "No established cure" if treatment.get("can_it_be_cured") == "no established cure"
            else "Manageable"
        )
        curable_reason = treatment.get("curable_reason") or treatment.get("curability_description") or ""
        lines.append(f"\n**1. Curable?**\n• **{curable_simple}:** {curable_reason}")

    # 5.8 Treatment & Control Options (Treatment Section 2)
    if "treatment_control_options" in sections or "cultural_management" in sections or "chemical_guidance" in sections:
        lines.append("\n**2. Treatment & Control Options:**")
        cure_items = treatment.get("cure_treatment") or treatment.get("immediate_actions") or []
        if cure_items:
            for item in cure_items[:4]:
                txt = item if isinstance(item, str) else item.get("statement", str(item))
                lines.append(f"• {txt}")
        else:
            mgmt = facts.get("management", {})
            for cat in ["cultural", "sanitation", "biological", "chemical_guidelines"]:
                for entry in mgmt.get(cat, [])[:1]:
                    lines.append(f"• {entry['statement']}")

    # 5.9 Precautions Section (Treatment Section 3)
    if "precautions_section" in sections:
        prec_items = treatment.get("precautions") or treatment.get("application_precautions") or []
        if prec_items:
            lines.append("\n**3. Precautions:**")
            for p in prec_items[:3]:
                txt = p if isinstance(p, str) else p.get("statement", str(p))
                lines.append(f"• {txt}")

    # 5.10 Prevention Context Header
    if "prevention_context_header" in sections:
        if disease_title:
            if has_explicit_crop:
                lines.append(f"Prevention guidelines for **{disease_title}** on **{crop_title}**:")
            else:
                lines.append(f"Prevention guidelines for **{disease_title}**:")
                lines.append("*(Note: Prevention guidelines can vary by host crop. If managing a specific plant, please specify the crop name.)*")
        else:
            lines.append(f"Prevention guidelines for **{crop_title}**:")

    # 5.11 Prevention Guidelines (Treatment Section 4 or Standalone Prevention)
    if "prevention_section" in sections or "prevention_guidelines" in sections or "prevention_summary" in sections or "preventive_measures" in sections:
        prev_items = treatment.get("prevention") or facts.get("prevention") or []
        if prev_items:
            sec_title = "**4. Prevention Guidelines:**" if "treatment_context_header" in sections else "**Prevention Guidelines:**"
            lines.append(f"\n{sec_title}")
            for p in prev_items[:4]:
                txt = p if isinstance(p, str) else p.get("statement", str(p))
                lines.append(f"• {txt}")

    # 5.12 Crop Overview / Agronomy Section
    if "crop_overview" in sections or "crop_identification" in sections:
        if has_explicit_crop or (not disease_title and facts.get("crop_name")):
            c_name = facts.get("crop_name", crop_title)
            sc_name = facts.get("scientific_name")
            cat = facts.get("category", "")
            lines.append(f"\n**Crop Profile:** {c_name} (*{sc_name or ''}*) — {cat}")

            opts = facts.get("optimal_conditions", [])
            if opts:
                lines.append("\n**Optimal Growing Conditions:**")
                for o in opts[:3]:
                    lines.append(f"• {o['statement']}")

            waters = facts.get("watering_guidelines", [])
            if waters:
                lines.append("\n**Watering & Soil Guidelines:**")
                for w in waters[:3]:
                    lines.append(f"• {w['statement']}")

            common_d = facts.get("common_diseases", [])
            if common_d and "common_disease_risks" in sections:
                clean_d = [cd.split('__')[1].replace('_', ' ').title() if '__' in cd else cd for cd in common_d]
                lines.append(f"\n**Common Disease Vulnerabilities:** {', '.join(clean_d)}")

    # 5.13 Citations Grounding Footer (Section 5: Sources)
    if sources and "unrecognized_notice" not in sections and "clarification_notice" not in sections:
        lines.append("\n---")
        citation_texts = [f"{s['title']} ({s['organization']})" for s in sources]
        lines.append(f"**Authoritative Sources:** {'; '.join(citation_texts[:3])}")

    final_text = "\n".join(lines)

    return FinalAgentResponse(
        text=final_text,
        intent=plan.intent,
        crop=crop if has_explicit_crop else None,
        disease=disease,
        status=status or reasoning.status,
        sources=sources,
        reasoning_rule=reasoning.applicable_rule,
        needs_clarification=False,
        structured_data={
            "crop": crop if has_explicit_crop else None,
            "disease": disease,
            "status": status or reasoning.status,
            "facts_retrieved_count": len(facts),
            "treatment": treatment if ("curability_section" in sections or "treatment_control_options" in sections) else None,
        },
    )
