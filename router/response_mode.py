"""
Response Mode Classification for Instruction-Driven Agricultural Responses
==========================================================================
Determines what diagnostic information, advice, and frontend cards to display
based strictly on the user's explicit instruction.

MODES SUPPORTED:
- MODE 1: Disease identification ("What disease is this?", "What is wrong with this plant?")
          -> Crop (as context) + Disease name/confidence. No treatment plan or sources.
- MODE 2: Plant/crop identification ("What plant is this?", "Identify this crop.")
          -> Crop name/confidence only. No disease or treatment.
- MODE 3: Treatment/cure ("How do I cure this disease?", "What is the treatment?")
          -> Crop + Disease (as brief context) + Sourced treatment/management advisory.
- MODE 4: General plant information ("Tell me about this plant.", "How often should I water it?")
          -> Crop name + agronomic requirements (watering, soil, care).
- MODE 5: Image/video uploaded WITHOUT instruction (empty text/speech)
          -> Combined analysis: Crop + Disease/Healthy + brief treatment/next steps if diseased.
- MODE 6: Multiple requests in one instruction ("Identify the disease and tell me how to treat it.")
          -> Returns all sections explicitly requested.
- UNRECOGNIZED: Non-empty text that cannot be classified ("Who won the World Cup?")
          -> Safe polite clarification; does NOT fall back to default combined analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ResponseMode(str, Enum):
    DISEASE_IDENTIFICATION = "disease_identification"    # Mode 1
    CROP_IDENTIFICATION = "crop_identification"          # Mode 2
    TREATMENT = "treatment"                              # Mode 3
    GENERAL_PLANT_INFO = "general_plant_info"            # Mode 4
    MEDIA_DEFAULT_ANALYSIS = "media_default_analysis"    # Mode 5
    COMPOSITE_REQUEST = "composite_request"              # Mode 6
    UNRECOGNIZED = "unrecognized_instruction"            # Unrecognized non-empty query


# ---------------------------------------------------------------------------
# Targeted Regex Patterns for Aspect Detection
# ---------------------------------------------------------------------------

CROP_PATTERNS = [
    r"\b(what|which) (plant|crop|flower|tree|specimen|species)\b",
    r"\bidentify (this|the|my)? (plant|crop|flower|species)\b",
    r"\bname of (this|the|my)? (plant|crop|flower)\b",
    r"\bwhat is this (plant|crop|flower)\b",
    r"\bwhich (crop|plant) is (this|shown|it)\b",
    r"\b(what|which) vegetable\b",
    r"\bwhat is this\b",
    r"\b(koun sa paudha|ye koun sa plant|paudhe ka naam)\b",
]

DISEASE_PATTERNS = [
    r"\b(what|which) (disease|infection|fungus|virus|bacteria|blight|rot|spot|pathogen|illness|issue|problem)\b",
    r"\bidentify (the |this |my )?(disease|infection|problem|issue|illness)\b",
    r"\bname (of )?(the |this |my )?(disease|infection|illness|issue)\b",
    r"\bwhat is (wrong|the matter) with (this|the|my)? (plant|crop|leaf|leaves)?\b",
    r"\bwhat happened to (this|the|my)? (plant|crop|leaf|leaves)\b",
    r"\bwhat is affecting (this|the|my)? (plant|crop|leaf|leaves)\b",
    r"\bdiagnose (this|the|my)? (plant|crop|leaf|disease)\b",
    r"\bis (this|the|my)? (plant|crop|leaf|it) (healthy|sick|diseased|infected|damaged|normal)\b",
    r"\b(check (plant |leaf )?health)\b",
    r"\bhealthy or (diseased|sick|infected)\b",
    r"\b(koun si bimari|bimari ka naam|kya bimari hai|kya problem hai)\b",
    r"\b(why are|why is) (the |my )?(leaves|leaf|plant) (yellow|brown|turning|dying)\b",
]

TREATMENT_PATTERNS = [
    r"\b(how (do i|to|can i) (treat|cure|control|manage|get rid of|heal|fix|remedy))\b",
    r"\b(what (should|to|can) i (do|spray|apply|use))\b",
    r"\b(how to get rid of (it|this|the disease|the infection))\b",
    r"\b(treatment|cure|remedy|remedies|medicine|management plan|sprays?|pesticide|fungicide|chemicals?)\b",
    r"\bhow (can i|to|do i) prevent\b",
    r"\b(prevention|preventative|precaution|protection) (tips|methods|guide|measures)?\b",
    r"\bhow (can i|to) (stop|prevent) (it |this )?(from )?spreading\b",
    r"\bhow should i manage\b",
    r"\b(ilaj|ilaaj|upchar|dawa|dawai|chhidkao|bachav|roktham)\b",
]

GENERAL_PATTERNS = [
    r"\btell me about (this|the)? (plant|crop)\b",
    r"\b(growing requirements|cultivation guide|how to grow|how to cultivate)\b",
    r"\bhow often (should i|to) water\b",
    r"\bwatering (schedule|requirements|needs)\b",
    r"\bcare (tips|guide|instructions)|plant care\b",
    r"\bbest (fertilizer|soil) for\b",
    r"\b(sunlight|soil|climate) (requirements|needs)\b",
    r"\b(uses of|benefits of)\b",
]

SYMPTOM_CAUSE_PATTERNS = [
    r"\b(symptom|symptoms|sign|signs|lesion|lesions|indication|indications)\b",
    r"\b(cause|causes|caused by|causal|pathogen|organism)\b",
    r"\b(favorable|conditions?|weather|environment|spread|transmi|overwinter)\b",
    r"\b(lakshan|karan|vajah)\b",
]


@dataclass
class ResponseModeResult:
    mode: ResponseMode
    requested_crop: bool = False
    requested_disease: bool = False
    requested_treatment: bool = False
    requested_general_info: bool = False
    is_instruction_free: bool = False
    is_unrecognized: bool = False
    visible_cards: dict[str, bool] = field(default_factory=lambda: {
        "crop": True,
        "disease": True,
        "treatment": True,
    })
    mode_label: str = "Mode 5: Default Media Analysis"
    clarification_message: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode.value,
            "mode_label": self.mode_label,
            "requested_crop": self.requested_crop,
            "requested_disease": self.requested_disease,
            "requested_treatment": self.requested_treatment,
            "requested_general_info": self.requested_general_info,
            "is_instruction_free": self.is_instruction_free,
            "is_unrecognized": self.is_unrecognized,
            "visible_cards": self.visible_cards,
            "clarification_message": self.clarification_message,
        }


def detect_response_mode(
    text: Optional[str],
    has_media: bool = False,
) -> ResponseModeResult:
    """
    Classifies user instruction into one of 6 deterministic response modes.
    """
    clean_text = (text or "").strip()

    # 1. Genuinely absent instruction
    if not clean_text:
        if has_media:
            return ResponseModeResult(
                mode=ResponseMode.MEDIA_DEFAULT_ANALYSIS,
                is_instruction_free=True,
                requested_crop=True,
                requested_disease=True,
                requested_treatment=True,
                visible_cards={"crop": True, "disease": True, "treatment": True},
                mode_label="Mode 5: Media Upload Without Instruction",
            )
        return ResponseModeResult(
            mode=ResponseMode.UNRECOGNIZED,
            is_instruction_free=True,
            is_unrecognized=True,
            visible_cards={"crop": False, "disease": False, "treatment": False},
            mode_label="No Input",
            clarification_message="Please upload a plant photo or ask a question.",
        )

    norm = clean_text.lower()

    # 2. Check for requested aspects
    c_match = any(re.search(p, norm) for p in CROP_PATTERNS)
    d_match = any(re.search(p, norm) for p in DISEASE_PATTERNS)
    t_match = any(re.search(p, norm) for p in TREATMENT_PATTERNS)
    g_match = any(re.search(p, norm) for p in GENERAL_PATTERNS)

    active_aspects = []
    if c_match:
        active_aspects.append("crop")
    if d_match:
        active_aspects.append("disease")
    if t_match:
        active_aspects.append("treatment")
    if g_match:
        active_aspects.append("general")

    # 3. Composite Request (Mode 6): Multiple explicit requests
    if len(active_aspects) >= 2:
        vis_crop = "crop" in active_aspects or "disease" in active_aspects or "treatment" in active_aspects
        vis_disease = "disease" in active_aspects or "treatment" in active_aspects
        vis_treatment = "treatment" in active_aspects
        return ResponseModeResult(
            mode=ResponseMode.COMPOSITE_REQUEST,
            requested_crop="crop" in active_aspects,
            requested_disease="disease" in active_aspects,
            requested_treatment="treatment" in active_aspects,
            requested_general_info="general" in active_aspects,
            visible_cards={
                "crop": vis_crop,
                "disease": vis_disease,
                "treatment": vis_treatment,
            },
            mode_label="Mode 6: Multiple Requests in One Instruction",
        )

    # 4. Single aspect matching
    if len(active_aspects) == 1:
        aspect = active_aspects[0]
        if aspect == "crop":
            return ResponseModeResult(
                mode=ResponseMode.CROP_IDENTIFICATION,
                requested_crop=True,
                visible_cards={"crop": True, "disease": False, "treatment": False},
                mode_label="Mode 2: Plant/Crop Identification",
            )
        elif aspect == "disease":
            # Per Mode 1 requirement: The crop name must be included with the disease name
            return ResponseModeResult(
                mode=ResponseMode.DISEASE_IDENTIFICATION,
                requested_crop=True,
                requested_disease=True,
                visible_cards={"crop": True, "disease": True, "treatment": False},
                mode_label="Mode 1: Disease Identification",
            )
        elif aspect == "treatment":
            # Per Mode 3 requirement: Crop name and identified disease as brief context
            return ResponseModeResult(
                mode=ResponseMode.TREATMENT,
                requested_crop=True,
                requested_disease=True,
                requested_treatment=True,
                visible_cards={"crop": True, "disease": True, "treatment": True},
                mode_label="Mode 3: Treatment & Management Advisory",
            )
        elif aspect == "general":
            return ResponseModeResult(
                mode=ResponseMode.GENERAL_PLANT_INFO,
                requested_crop=True,
                requested_general_info=True,
                visible_cards={"crop": True, "disease": False, "treatment": False},
                mode_label="Mode 4: General Plant Care & Cultivation",
            )

    # 5. Check if query is agricultural context (e.g., named crop or disease entity)
    # Check words against known plant vocabulary
    known_agri_keywords = {
        "tomato", "potato", "apple", "grape", "corn", "maize", "rice", "wheat",
        "citrus", "orange", "lemon", "soybean", "bell pepper", "pepper", "capsicum",
        "eggplant", "brinjal", "strawberry", "blueberry", "cherry", "peach",
        "leaf", "leaves", "stem", "fruit", "root", "foliage", "seedling",
        "blight", "rust", "rot", "scab", "mildew", "wilt", "spot", "virus",
    }
    has_agri_word = any(kw in norm for kw in known_agri_keywords)

    if has_agri_word:
        # User named a plant or symptom without explicit verb (e.g., "Tomato" or "Eggplant leaves")
        if has_media:
            # Default to media diagnosis with full context
            return ResponseModeResult(
                mode=ResponseMode.MEDIA_DEFAULT_ANALYSIS,
                requested_crop=True,
                requested_disease=True,
                requested_treatment=True,
                visible_cards={"crop": True, "disease": True, "treatment": True},
                mode_label="Mode 5: Media Analysis with Crop Context",
            )
        else:
            return ResponseModeResult(
                mode=ResponseMode.GENERAL_PLANT_INFO,
                requested_crop=True,
                requested_general_info=True,
                visible_cards={"crop": True, "disease": False, "treatment": False},
                mode_label="Mode 4: General Crop Information",
            )

    # 6. Unrecognized instruction (non-empty, non-agricultural)
    # Strict requirement: Do not silently switch to default combined analysis!
    return ResponseModeResult(
        mode=ResponseMode.UNRECOGNIZED,
        is_unrecognized=True,
        visible_cards={"crop": False, "disease": False, "treatment": False},
        mode_label="Unrecognized Instruction",
        clarification_message=(
            "I couldn't relate your instruction to plant identification, disease diagnosis, or crop care. "
            "You can ask me to identify a plant, check for visible disease symptoms, or explain treatments and care guidelines."
        ),
    )
