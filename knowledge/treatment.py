"""
Agricultural Treatment and Cure Extraction Engine
=================================================
Extracts, structures, and enforces agricultural safety rules for disease-specific
treatment, cure status, immediate actions, management options, application precautions,
and prevention protocols.

Features:
- Distinguishes curable (Yes), manageable (Manageable), and viral/vascular (No established cure) conditions.
- Concise 5-section structure: Curable?, Cure / Treatment, Precautions, Prevention, Sources.
- One bullet = one short sentence. Plain language for farmers.
- Strict protection against false cures for healthy foliage and uncertain diagnoses.
- Clickable disease-specific agricultural reference links (1–3 authoritative sources).
- Verified chemical guidelines with mandatory PPE, label adherence, and regional registration notices.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from knowledge.database import AgriculturalKnowledgeBase, get_knowledge_base
from knowledge.schema import DiseaseRecord, SourcedFact
from knowledge.sources import format_source_citation

logger = logging.getLogger(__name__)

# Canonical incurable diseases (viral pathogens, systemic vascular wilts, and phytoplasmas)
INCURABLE_DISEASES = {
    "apple__mosaic_virus",
    "banana__bunchy_top",
    "banana__panama_disease",
    "bean__mosaic_virus",
    "bell_pepper__leaf_curl",
    "citrus__greening_disease",
    "cucumber__bacterial_wilt",
    "eggplant__little_leaf",
    "potato__mosaic_virus",
    "potato__spindle_tuber_viroid",
    "rose__mosaic_virus",
    "soybean__mosaic_virus",
    "squash__mosaic_virus",
    "tobacco__mosaic_virus",
    "tomato__mosaic_virus",
    "tomato__yellow_leaf_curl_virus",
    "zucchini__mosaic_virus",
    "zucchini__yellow_mosaic_virus",
}

# Naturally curable or eradicable conditions under timely intervention (surface mildews, insect pests)
CURABLE_DISEASES = {
    "bell_pepper__powdery_mildew",
    "cauliflower__pest_damage",
    "cherry__powdery_mildew",
    "cucumber__powdery_mildew",
    "eggplant__pest_damage",
    "ginger__pest_damage",
    "potato__pest_damage",
    "rose__pest_damage",
    "rose__powdery_mildew",
    "spinach__pest_damage",
    "squash__powdery_mildew",
    "strawberry__powdery_mildew",
    "tomato__powdery_mildew",
    "wheat__powdery_mildew",
    "zucchini__powdery_mildew",
}


def _fact_to_str(item: Any) -> str:
    """Safely convert a SourcedFact or string or dict to clean text."""
    if item is None:
        return ""
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, SourcedFact):
        return item.statement.strip()
    if isinstance(item, dict):
        return (item.get("statement") or item.get("practice") or item.get("agent") or item.get("active_ingredient") or str(item)).strip()
    if hasattr(item, "statement"):
        return str(item.statement).strip()
    if hasattr(item, "practice"):
        return str(item.practice).strip()
    return str(item).strip()


def _to_concise_sentence(text: str) -> str:
    """Format an action or recommendation into a single, punchy, clear sentence."""
    if not text:
        return ""
    t = text.strip()
    # Strip common category prefixes
    for prefix in (
        "cultural prevention:", "cultural practices:", "cultural practice:", "cultural controls:", "cultural control:", "cultural:",
        "sanitation measures:", "sanitation measure:", "sanitary measures:", "sanitary removal:", "sanitation:",
        "immediate actions:", "immediate action:", "immediate:", "action:",
        "chemical controls:", "chemical guidelines:", "chemical:", "biological options:",
        "biological:", "prevention protocols:", "prevention:", "note:",
        "1.", "2.", "3.", "4.", "•", "-", "*", "▸"
    ):
        if t.lower().startswith(prefix):
            t = t[len(prefix):].strip()

    # Strip wordy preambles
    for preamble in (
        "it is recommended to ", "farmers should ", "growers should ",
        "please ensure to ", "ensure to ", "care should be taken to ",
        "make sure to ", "growers are advised to ", "producers should ",
        "sanitary removal and deep burial/burning of ",
    ):
        if t.lower().startswith(preamble):
            t = t[len(preamble):].strip()

    # Take first complete sentence if multiple exist
    if ". " in t:
        t = t.split(". ")[0].strip()

    # Clean ending punctuation
    t = t.rstrip(",;:- ")
    if t and not t.endswith((".", "!", "?")):
        t += "."

    if t:
        t = t[0].upper() + t[1:]
    return t


def get_disease_treatment(
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    status: Optional[str] = None,
    d_rec: Optional[DiseaseRecord] = None,
    kb: Optional[AgriculturalKnowledgeBase] = None,
) -> dict[str, Any]:
    """Retrieve concise, structured treatment and cure guidance for a crop-disease combination.

    Enforces:
    1. Healthy plants receive NO disease cures (treatment contraindicated).
    2. Uncertain predictions receive NO disease cures (treatment withheld pending verification).
    3. Supported diseases resolve to evidence-backed curable (Yes), manageable (Manageable),
       or viral/vascular (No established cure) categories.
    4. Exactly 5 sections: Curable?, Cure / Treatment, Precautions, Prevention, Sources.
    5. One bullet = one short sentence. Plain language.
    6. Clickable disease-specific sources (1–3 authoritative links).
    """
    clean_crop = (crop or "").strip().lower()
    clean_disease = (disease or "").strip().lower()
    clean_status = (status or "").strip().lower()

    # -------------------------------------------------------------------------
    # CASE 1: Healthy Foliage Protection (No Disease Treatment)
    # -------------------------------------------------------------------------
    if clean_status == "healthy" or clean_disease in ("healthy", "healthy_specimen", "no_disease"):
        crop_display = clean_crop.replace("_", " ").title() if clean_crop else "Plant"
        return {
            "has_treatment": False,
            "can_it_be_cured": "not_applicable",
            "curable_simple": "Not applicable",
            "curable_reason": f"Your {crop_display.lower()} foliage appears healthy with no signs of active disease; curative sprays are contraindicated.",
            "cure_treatment": [],
            "precautions": [
                "Do not apply disease fungicides or chemical sprays to healthy foliage.",
                "Unnecessary pesticide sprays increase costs and can harm beneficial garden insects.",
            ],
            "prevention": [
                "Water directly at the root zone using drip irrigation to keep leaves dry.",
                "Maintain recommended plant spacing and sunlight exposure for good airflow.",
                "Scout lower leaves weekly to catch any early discoloration promptly.",
            ],
            "sources": [],
            # Compatibility fields
            "curability_title": "Not Applicable (Healthy Foliage)",
            "curability_badge": "healthy",
            "curability_description": f"The visual analysis indicates healthy {crop_display.lower()} foliage with no symptoms of active disease. Curative chemical sprays are contraindicated and unnecessary.",
            "immediate_actions": [
                "Maintain baseline cultural care and regular scouting.",
                "Irrigate directly at the root zone via drip or soaker hoses to keep leaves dry.",
                "Do not apply disease fungicides or curative chemicals to healthy foliage.",
            ],
            "treatment_options": {
                "cultural": ["Maintain recommended plant spacing and sunlight exposure for optimal airflow."],
                "sanitation": ["Keep field borders free from weeds that harbor pests."],
                "biological": [],
                "chemical": [],
            },
            "application_precautions": [
                "Disease treatment is not needed for healthy plants. Always confirm registration and label directions for any future applications."
            ],
            "crop": clean_crop,
            "disease": "healthy",
            "disease_name": "Healthy Specimen / No Disease Detected",
            "is_healthy": True,
            "is_uncertain": False,
        }

    # -------------------------------------------------------------------------
    # CASE 2: Uncertain / Low-Confidence Prediction Shielding
    # -------------------------------------------------------------------------
    if clean_status == "uncertain" or clean_disease in ("uncertain", "inconclusive", "unknown", ""):
        crop_display = clean_crop.replace("_", " ").title() if clean_crop else "Plant"
        candidate_name = clean_disease.replace("_", " ").title() if clean_disease else "Suspected condition"
        return {
            "has_treatment": False,
            "can_it_be_cured": "uncertain",
            "curable_simple": "Diagnosis inconclusive",
            "curable_reason": f"Symptoms on this {crop_display.lower()} are ambiguous or confidence is low; treatment is withheld to prevent harmful misapplication.",
            "cure_treatment": [],
            "precautions": [
                "Never apply chemical fungicides or pesticides on an unconfirmed diagnosis.",
                "Always check product labels and local registration before applying any agricultural treatment.",
            ],
            "prevention": [
                "Provide a sharper, well-lit close-up photo of the affected leaves or stems to confirm diagnosis.",
                "Check whether leaf spots have concentric rings, water-soaked edges, or powdery residue.",
                "Consult your local university agricultural extension service for on-site confirmation.",
            ],
            "sources": [],
            # Compatibility fields
            "curability_title": "Diagnosis Inconclusive — Treatment Withheld",
            "curability_badge": "uncertain",
            "curability_description": f"Visual symptoms on this {crop_display.lower()} are ambiguous or confidence is below threshold. Curative treatments are withheld pending confirmation.",
            "immediate_actions": [
                "Inspect both upper and lower leaf surfaces for distinct disease signs.",
                "Take a clearer photo in bright natural light.",
            ],
            "treatment_options": {
                "cultural": ["Isolate suspect potted plants while verifying symptoms."],
                "sanitation": [],
                "biological": [],
                "chemical": [],
            },
            "application_precautions": [
                "Never apply chemical fungicides or pesticides on an unconfirmed diagnosis. Always check approved labels and regional registration."
            ],
            "crop": clean_crop,
            "disease": clean_disease or "uncertain",
            "disease_name": f"Inconclusive ({candidate_name})" if candidate_name != "Suspected Condition" else "Inconclusive",
            "is_healthy": False,
            "is_uncertain": True,
        }

    # -------------------------------------------------------------------------
    # CASE 3: Resolve Disease Record from Knowledge Base
    # -------------------------------------------------------------------------
    if kb is None:
        kb = get_knowledge_base()

    if d_rec is None:
        d_rec = kb.get_disease(clean_disease, crop=clean_crop)
        if d_rec is None and "__" in clean_disease:
            _, d_part = clean_disease.split("__", 1)
            d_rec = kb.get_disease(d_part, crop=clean_crop)

    # Missing Knowledge Record fallback
    if d_rec is None:
        disease_display = clean_disease.replace("_", " ").title()
        crop_display = clean_crop.replace("_", " ").title() if clean_crop else "Crop"
        citations = format_source_citation([], disease_slug=clean_disease, crop=clean_crop, disease=clean_disease)
        return {
            "has_treatment": False,
            "can_it_be_cured": "unavailable",
            "curable_simple": "Treatment data unavailable",
            "curable_reason": f"Verified treatment and management protocols for '{disease_display}' on {crop_display} are not currently available in the local verified repository.",
            "cure_treatment": [
                f"Prune or remove visibly affected foliage during dry weather to prevent secondary spread.",
                f"Consult your local agricultural extension service for verified management of {disease_display}.",
            ],
            "precautions": [
                "Do not apply unverified chemical products without official local approval.",
                "Always check that products are registered and follow pesticide label directions strictly.",
            ],
            "prevention": [
                "Rotate crops with non-susceptible plant families every 2 to 3 years.",
                "Scout crops weekly and water at ground level to keep leaves dry.",
            ],
            "sources": citations[:3],
            # Compatibility fields
            "curability_title": "Treatment Data Unavailable",
            "curability_badge": "unavailable",
            "curability_description": f"Verified treatment and management protocols for '{disease_display}' on {crop_display} are not currently available in the local repository.",
            "immediate_actions": [f"Consult your regional agricultural extension service for verified management of {disease_display}."],
            "treatment_options": {
                "cultural": ["Maintain good airflow and avoid overhead leaf wetting."],
                "sanitation": ["Sanitize pruning tools between cuts."],
                "biological": [],
                "chemical": [],
            },
            "application_precautions": [
                "Do not apply unverified chemicals. Confirm regional registration and label directions."
            ],
            "crop": clean_crop,
            "disease": clean_disease,
            "disease_name": disease_display,
            "is_healthy": False,
            "is_uncertain": False,
        }

    # -------------------------------------------------------------------------
    # CASE 4: Structured Verified Treatment Protocol
    # -------------------------------------------------------------------------
    slug = d_rec.disease_slug.lower()
    dis_type = (d_rec.disease_type or "").strip().lower()
    path_name = (d_rec.scientific_name_causal_agent or "").lower()

    # Determine curability status
    is_incurable = (
        slug in INCURABLE_DISEASES
        or dis_type == "viral"
        or "virus" in slug
        or "virus" in path_name
        or "viroid" in path_name
        or "phytoplasma" in path_name
        or slug in ("banana__panama_disease", "citrus__greening_disease", "cucumber__bacterial_wilt")
    )
    is_curable = (
        slug in CURABLE_DISEASES
        or d_rec.treatment_category.lower() in ("curable", "curative", "curative treatment")
        or "powdery_mildew" in slug
        or "pest_damage" in slug
    )

    crop_name_disp = (d_rec.crop or clean_crop or "plant").replace("_", " ").title()

    if is_incurable:
        can_it_be_cured = "no established cure"
        curable_simple = "No established cure"
        curable_reason = "Viral and systemic vascular infections cannot be cured; remove infected plants to protect healthy ones."
        curability_title = "No Established Cure (Viral / Vascular)"
        curability_badge = "no_cure"
        curability_description = (
            "Viral infections and systemic vascular wilts cannot be cured once established inside plant tissues. "
            "Treatment focuses on eradicating infected specimens, strict sanitation, and controlling insect vectors."
        )
    elif is_curable:
        can_it_be_cured = "curable"
        curable_simple = "Yes"
        curable_reason = "Can be cured or completely eradicated if targeted treatment is applied promptly at the first sign of symptoms."
        curability_title = "Curable"
        curability_badge = "curable"
        curability_description = (
            "This condition can be cured, controlled, or completely eradicated if targeted non-chemical and "
            "approved treatments are applied promptly at the first sign of symptoms."
        )
    else:
        can_it_be_cured = "manageable"
        curable_simple = "Manageable"
        curable_reason = "Damaged plant tissue cannot be cured, but the disease can be contained to protect healthy new growth."
        curability_title = "Manageable Disease"
        curability_badge = "manageable"
        curability_description = (
            "While existing necrotic lesions cannot be reversed on damaged tissue, the infection can be contained, "
            "suppressed, and new plant growth protected through integrated management."
        )

    # -------------------------------------------------------------------------
    # BUILD CONCISE SECTION 2: CURE / TREATMENT (2–4 concise bullets)
    # -------------------------------------------------------------------------
    cure_treatment: list[str] = []

    if is_incurable:
        # Incurable viral / vascular protocol
        cure_treatment.append("Promptly pull and safely destroy infected plants away from the field; do not compost them.")
        cure_treatment.append("Control sap-feeding insect vectors like whiteflies, aphids, or leafhoppers using approved sticky traps or insecticidal soaps.")
        cure_treatment.append("Disinfect all pruning shears, knives, and equipment with a 10% bleach or alcohol solution between cuts.")
    else:
        # 1. Actionable sanitation / pruning step from immediate_actions or sanitation
        san_step = None
        for ia in d_rec.immediate_actions:
            txt = _to_concise_sentence(_fact_to_str(ia))
            if txt and not any(w in txt.lower() for w in ("spray", "chemical", "fungicide", "label")):
                san_step = txt
                break
        if not san_step:
            for s in d_rec.management.sanitation:
                txt = _to_concise_sentence(_fact_to_str(s))
                if txt:
                    san_step = txt
                    break
        if not san_step:
            san_step = "Prune and dispose of infected leaves or rotting fruit during dry weather; never compost them."
        cure_treatment.append(san_step)

        # 2. Moisture / canopy cultural management step
        cult_step = None
        for c in d_rec.management.cultural:
            txt = _to_concise_sentence(_fact_to_str(c))
            if txt and txt != san_step and not any(w in txt.lower() for w in ("rotation", "resistant", "seed")):
                # Avoid picking another removal/destroy step if we already have one
                if any(w in txt.lower() for w in ("remove", "destroy", "prune", "burial", "burn", "canker")) and any(w in san_step.lower() for w in ("remove", "destroy", "prune", "burial", "burn")):
                    continue
                cult_step = txt
                break
        if not cult_step:
            cult_step = "Water only at the plant base using drip irrigation to keep foliage completely dry."
        cure_treatment.append(cult_step)

        # 3. Chemical / biological guidance (only if supported by verified record)
        chem_step = None
        if d_rec.management.chemical_guidelines:
            raw_ch = _fact_to_str(d_rec.management.chemical_guidelines[0])
            txt = _to_concise_sentence(raw_ch)
            if txt:
                # Format to a clear, actionable sentence
                if any(k in txt.lower() for k in ("chlorothalonil", "mancozeb", "copper", "fungicide", "protectant")):
                    cleaned_act = txt.split(":")[0].replace(" / ", " or ")
                    if ":" in txt:
                        timing = txt.split(":", 1)[1].strip()
                        txt = f"Apply an approved protectant fungicide ({cleaned_act}) {timing}"
                        if not txt.endswith("."):
                            txt += "."
                    txt = _to_concise_sentence(txt)
                if "approved" not in txt.lower() and "registered" not in txt.lower():
                    txt = txt.rstrip(".") + " (use only products registered for this crop in your region)."
                chem_step = txt
        elif d_rec.management.biological:
            raw_b = _fact_to_str(d_rec.management.biological[0])
            txt = _to_concise_sentence(raw_b)
            if txt:
                chem_step = txt

        if chem_step and chem_step not in cure_treatment:
            cure_treatment.append(chem_step)

        # 4. If fewer than 3 bullets, add canopy / staking practice
        if len(cure_treatment) < 3:
            canopy_step = "Stake or trellis plants and ensure generous spacing to maximize sunlight and airflow."
            if canopy_step not in cure_treatment:
                cure_treatment.append(canopy_step)

    # Deduplicate while preserving order and limit to 2–4 bullets
    seen_ct = set()
    final_cure_treatment = []
    for item in cure_treatment:
        cleaned = _to_concise_sentence(item)
        norm = cleaned.lower()
        if norm and norm not in seen_ct:
            seen_ct.add(norm)
            final_cure_treatment.append(cleaned)
    cure_treatment = final_cure_treatment[:4]
    if len(cure_treatment) < 2:
        cure_treatment.append("Prune visibly diseased foliage promptly to protect healthy surrounding growth.")

    # -------------------------------------------------------------------------
    # BUILD CONCISE SECTION 3: PRECAUTIONS (1–3 concise bullets)
    # -------------------------------------------------------------------------
    precautions: list[str] = [
        "Always follow the pesticide label strictly for required protective equipment (PPE), dilution rates, and harvest waiting times.",
        "Verify that any chemical or biological product is legally registered and approved for this crop in your region.",
    ]
    if is_incurable:
        precautions.append("Do not apply chemical fungicides or antibiotics, as they cannot cure viral infections or systemic vascular wilts.")
    else:
        precautions.append("Rotate chemical mode-of-action groups (FRAC/IRAC) across applications to prevent resistance development.")
    precautions = precautions[:3]

    # -------------------------------------------------------------------------
    # BUILD CONCISE SECTION 4: PREVENTION (2–4 concise bullets)
    # -------------------------------------------------------------------------
    prevention: list[str] = []

    # Check disease record prevention
    for p in d_rec.prevention:
        txt = _to_concise_sentence(_fact_to_str(p))
        if txt and txt.lower() not in seen_ct and not any(w in txt.lower() for w in ("spray", "chemical", "label")):
            prevention.append(txt)

    # Standard evidence-based prevention practices if record has generic or few entries
    standard_preventions = [
        f"Rotate {crop_name_disp.lower()} crops with non-susceptible plant families every 2 to 3 years.",
        "Plant certified disease-free seeds, clean transplants, or resistant crop varieties.",
        "Space plants generously to promote good ventilation and rapid leaf drying.",
        "Clean up and destroy all fallen leaf litter and plant residue after the final harvest.",
    ]
    for sp in standard_preventions:
        if len(prevention) >= 4:
            break
        if sp.lower() not in [p.lower() for p in prevention] and sp.lower() not in seen_ct:
            prevention.append(sp)

    # Deduplicate and limit to 2–4 bullets
    seen_prev = set()
    final_prevention = []
    for item in prevention:
        cleaned = _to_concise_sentence(item)
        norm = cleaned.lower()
        if norm and norm not in seen_prev and norm not in seen_ct:
            seen_prev.add(norm)
            final_prevention.append(cleaned)
    prevention = final_prevention[:4]
    if len(prevention) < 2:
        prevention.append("Practice multi-year crop rotation out of the host plant family.")
        prevention.append("Use certified clean seeds and transplants to avoid introducing pathogens.")

    # -------------------------------------------------------------------------
    # BUILD CONCISE SECTION 5: SOURCES (1–3 clickable links)
    # -------------------------------------------------------------------------
    citations = format_source_citation(
        d_rec.sources,
        disease_slug=d_rec.disease_slug,
        crop=d_rec.crop,
        disease=d_rec.common_name,
        d_rec=d_rec,
    )
    final_sources = citations[:3]

    # Compatibility lists for existing test suites
    raw_immediate_actions = [_fact_to_str(ia) for ia in d_rec.immediate_actions if _fact_to_str(ia)]
    if not raw_immediate_actions:
        raw_immediate_actions = cure_treatment[:2]

    cultural_opts = [_fact_to_str(c) for c in d_rec.management.cultural if _fact_to_str(c)]
    if not cultural_opts:
        cultural_opts = ["Maintain generous plant spacing for canopy airflow."]

    sanitation_opts = [_fact_to_str(s) for s in d_rec.management.sanitation if _fact_to_str(s)]
    if not sanitation_opts:
        sanitation_opts = ["Remove infected plant debris away from production areas."]

    biological_opts = [_fact_to_str(b) for b in d_rec.management.biological if _fact_to_str(b)]
    chemical_opts = [_fact_to_str(ch) for ch in d_rec.management.chemical_guidelines if _fact_to_str(ch)]

    return {
        # Core simplified 5-section layout payload
        "has_treatment": True,
        "can_it_be_cured": can_it_be_cured,
        "curable_simple": curable_simple,
        "curable_reason": curable_reason,
        "cure_treatment": cure_treatment,
        "precautions": precautions,
        "prevention": prevention,
        "sources": final_sources,
        # Backward-compatible fields
        "curability_title": curability_title,
        "curability_badge": curability_badge,
        "curability_description": curability_description,
        "immediate_actions": raw_immediate_actions,
        "treatment_options": {
            "cultural": cultural_opts,
            "sanitation": sanitation_opts,
            "biological": biological_opts,
            "chemical": chemical_opts,
        },
        "application_precautions": precautions,
        "crop": d_rec.crop,
        "disease": d_rec.disease_slug,
        "disease_name": d_rec.common_name,
        "is_healthy": False,
        "is_uncertain": False,
    }


def get_disease_insights(
    crop: Optional[str] = None,
    disease: Optional[str] = None,
    status: Optional[str] = None,
    d_rec: Optional[DiseaseRecord] = None,
    kb: Optional[AgriculturalKnowledgeBase] = None,
) -> dict[str, Any]:
    """Retrieve structured disease insights (Key Symptoms, Pathogen/Causes, Favorable Conditions).

    Enforces:
    1. Returns has_insights=False for healthy or uncertain plants.
    2. Retrieves verified facts from DiseaseRecord without hallucinating or rewriting facts.
    3. Hides or leaves empty sections where data is not available.
    """
    empty_payload = {
        "has_insights": False,
        "disease_name": None,
        "crop": crop,
        "symptoms": [],
        "distinguishing_features": [],
        "affected_parts": [],
        "pathogen": None,
        "disease_type": None,
        "favorable_conditions": [],
        "spread_mechanism": [],
    }

    if status in ("healthy", "uncertain") or (disease and disease.lower() in ("healthy", "no disease detected", "uncertain", "none")):
        return empty_payload

    if d_rec is None and disease:
        if kb is None:
            from knowledge.database import AgriculturalKnowledgeBase
            kb = AgriculturalKnowledgeBase()
        d_rec = kb.get_disease(disease, crop=crop)

    if not d_rec:
        return empty_payload

    # 1. Symptoms: extract clean statements without bullet characters
    raw_symptoms = [_fact_to_str(s) for s in d_rec.symptoms if _fact_to_str(s)]
    clean_symptoms = []
    seen_s = set()
    for s in raw_symptoms:
        cleaned = s.lstrip("•-* ▸").strip()
        norm = cleaned.lower()
        if norm and norm not in seen_s:
            seen_s.add(norm)
            clean_symptoms.append(cleaned)

    # Distinguishing features
    raw_features = [_fact_to_str(df).lstrip("•-* ▸").strip() for df in d_rec.distinguishing_features if _fact_to_str(df)]

    # Affected parts
    affected_parts = [p.strip() for p in d_rec.affected_parts if isinstance(p, str) and p.strip()]

    # 2. Pathogen / Classification
    pathogen = (d_rec.scientific_name_causal_agent or "").strip()
    disease_type = (d_rec.disease_type or "").strip()

    # 3. Favorable Conditions
    raw_conditions = [_fact_to_str(cc) for cc in d_rec.causes_and_conditions if _fact_to_str(cc)]
    clean_conditions = []
    seen_c = set()
    for c in raw_conditions:
        cleaned = c.lstrip("•-* ▸").strip()
        norm = cleaned.lower()
        if norm and norm not in seen_c:
            seen_c.add(norm)
            clean_conditions.append(cleaned)

    # Spread / transmission
    raw_spread = [_fact_to_str(sp).lstrip("•-* ▸").strip() for sp in d_rec.spread_and_transmission if _fact_to_str(sp)]

    has_insights = bool(clean_symptoms or pathogen or clean_conditions)

    return {
        "has_insights": has_insights,
        "disease_name": d_rec.common_name,
        "crop": d_rec.crop,
        "symptoms": clean_symptoms[:5],
        "distinguishing_features": raw_features[:3],
        "affected_parts": affected_parts,
        "pathogen": pathogen or None,
        "disease_type": disease_type or None,
        "favorable_conditions": clean_conditions[:4],
        "spread_mechanism": raw_spread[:2],
    }

