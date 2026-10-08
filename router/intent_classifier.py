"""
Intent Classification Engine for Agricultural Query Understanding
==================================================================
Deterministic, fast, multi-pattern intent classifier with calibrated confidence
scoring, ambiguity detection, and clarification reasoning.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple

from router.taxonomy import (
    CONFIDENCE_THRESHOLDS,
    ExtractedEntities,
    Intent,
)

# Core Intent Phrase Patterns (Ordered by specificity)
INTENT_PATTERNS = {
    Intent.CAUSE: [
        r"\b(why (did|is|are|does|happened|has))\b",
        r"\b(why did this disease happen)\b",
        r"\b(what (causes|caused|is the cause of|is the reason for))\b",
        r"\b(cause|causes|reason|reasons|karan) of\b",
        r"\b(kyun (hua|hota hai))\b",
    ],
    Intent.IDENTIFY_DISEASE: [
        r"\b(what|which) (disease|infection|fungus|virus|bacteria|problem)\b",
        r"\b(name (of |the )?(disease|infection))\b",
        r"\b(identify (the |this )?(disease|infection))\b",
        r"\b(which disease|what disease)\b",
        r"\b(koun si bimari|kon si bimari)\b",
    ],
    Intent.TREATMENT: [
        r"\b(how (do i|to|can i) (treat|cure|control|manage|get rid of|heal|fix))\b",
        r"\b(what (should|to|can) i (do|spray|apply|use))\b",
        r"\b(which|what) (pesticide|fungicide|insecticide|medicine|spray|chemical|treatment|remedy)\b",
        r"\b(treatment|cure|remedy|solution|medicine|dawa|dawai|upchar|ilaj) (for|of|kya)\b",
        r"\b(how to (treat|cure|remedy))\b",
        r"\b(kya (karu|kare|karna chahiye|ilaj|dawa))\b",
        r"\b(ilaj|ilaaj|upchar|dawai|chhidkao)\b",
        r"\b(what to do|what do)\b",
    ],
    Intent.PREVENTION: [
        r"\b(how (can i|to) (prevent|avoid|stop|protect|reduce))\b",
        r"\b(prevention|preventative|precaution|protection) (tips|methods|guide|measures)\b",
        r"\b(how to (stop|protect) (from|spreading))\b",
        r"\b(roktham|bachav|kaise bache)\b",
    ],
    Intent.SYMPTOMS: [
        r"\b(what are the (symptoms|signs|indicators))\b",
        r"\b(symptoms|signs|indicators|lakshan) of\b",
        r"\b(how to (identify|recognize|spot) (the disease|symptoms))\b",
    ],
    Intent.CHECK_HEALTH: [
        r"\b(is (my|this|the)? (plant|crop|leaf|specimen) (healthy|normal|okay|fine|sick))\b",
        r"\b(healthy or (diseased|sick|infected|damaged))\b",
        r"\b(check (plant |leaf )?health)\b",
        r"\b(is it healthy)\b",
        r"\b(kya ye healthy hai|kya plant sahi hai)\b",
    ],
    Intent.IDENTIFY_CROP: [
        r"\b(what|which) (plant|crop|flower|tree|specimen|species) (is this|is it)\b",
        r"\b(name of (this|the) (plant|crop|flower))\b",
        r"\b(identify (this|the) (plant|crop|flower))\b",
        r"\b(what is this (plant|crop|flower))\b",
        r"\b(koun sa paudha|ye koun sa plant hai)\b",
    ],
    Intent.DIAGNOSE_PLANT: [
        r"\b(what (happened|is wrong with|is affecting) (to|with)? (my|this)? (plant|leaves|crop)?)\b",
        r"\b(leaves (are|turning|have) (yellow|brown|spots|drying|falling))\b",
        r"\b(plant (is )?(dying|sick|drying|damaged|not growing))\b",
        r"\b(patte (sukh|peele|kharab|gir) rhe)\b",
        r"\b(kya hua|kya ho gya|kya problem hai)\b",
        r"\b(plant kharab)\b",
    ],
    Intent.GENERAL_PLANT_INFO: [
        r"\b(tell me about|information about|info on|details about|guide for)\b",
        r"\b(how to (grow|plant|care for|water|cultivate))\b",
        r"\b(care (tips|guide)|watering schedule|best fertilizer for|fertilizer|fertiliser|manure|compost)\b",
        r"\b(uses of|benefits of)\b",
    ],

}


def classify_intent_from_text(
    normalized_text: str,
    entities: ExtractedEntities,
    has_visual_context: bool = False,
) -> Tuple[Intent, float, bool, Optional[str]]:
    """
    Classifies intent from normalized text and extracted entities.
    Returns: (intent, confidence, needs_clarification, clarification_reason)
    """
    if not normalized_text or not normalized_text.strip():
        if has_visual_context:
            return Intent.DIAGNOSE_PLANT, 0.85, False, None
        return Intent.INSUFFICIENT_INFORMATION, 0.0, True, "No question or image provided."

    text = " " + normalized_text.lower() + " "
    tokens = text.strip().split()

    # Exact Ambiguity check (only when standalone without actionable intent)
    exact_ambiguous_phrases = {"what do", "not good", "plant problem", "problem", "help", "bad", "kharab", "kya"}
    if text.strip() in exact_ambiguous_phrases:
        if has_visual_context:
            return Intent.DIAGNOSE_PLANT, 0.70, False, None
        return (
            Intent.AMBIGUOUS,
            0.30,
            True,
            "User intent is ambiguous or too brief without visual or conversational context."
        )

    matched_scores: dict[Intent, float] = {}

    for intent, patterns in INTENT_PATTERNS.items():
        score = 0.0
        for pat in patterns:
            if re.search(pat, text):
                score += 1.0
        if score > 0:
            matched_scores[intent] = score

    # Factor in Entity Actions with high weighting
    if entities.action:
        if entities.action == "cause":
            matched_scores[Intent.CAUSE] = matched_scores.get(Intent.CAUSE, 0.0) + 2.0
        elif entities.action == "treatment":
            matched_scores[Intent.TREATMENT] = matched_scores.get(Intent.TREATMENT, 0.0) + 2.0
        elif entities.action == "prevention":
            matched_scores[Intent.PREVENTION] = matched_scores.get(Intent.PREVENTION, 0.0) + 2.0
        elif entities.action == "identification":
            matched_scores[Intent.IDENTIFY_CROP] = matched_scores.get(Intent.IDENTIFY_CROP, 0.0) + 1.5
        elif entities.action == "symptoms":
            matched_scores[Intent.SYMPTOMS] = matched_scores.get(Intent.SYMPTOMS, 0.0) + 2.0
        elif entities.action == "diagnosis":
            matched_scores[Intent.DIAGNOSE_PLANT] = matched_scores.get(Intent.DIAGNOSE_PLANT, 0.0) + 1.2

    # Factor in Symptom Mentions without explicit action (e.g. "tomato leaves are yellow") -> DIAGNOSE_PLANT
    if entities.symptoms and not matched_scores:
        matched_scores[Intent.DIAGNOSE_PLANT] = 1.0

    # If disease is named with no explicit action -> IDENTIFY_DISEASE / DIAGNOSE_PLANT
    if entities.disease and not matched_scores:
        matched_scores[Intent.IDENTIFY_DISEASE] = 0.9

    # If no intent matched:
    if not matched_scores:
        # Check if crop only is mentioned (e.g. "tomato", "tell me about tomato")
        if entities.crop and len(tokens) <= 3:
            return Intent.GENERAL_PLANT_INFO, 0.75, False, None
        
        if has_visual_context:
            return Intent.DIAGNOSE_PLANT, 0.65, False, None

        return (
            Intent.AMBIGUOUS,
            0.35,
            True,
            "Could not determine intent with sufficient confidence."
        )

    # Sort matches by score
    sorted_matches = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
    best_intent, best_score = sorted_matches[0]

    # Calibrate confidence score
    confidence = min(0.98, 0.70 + (best_score * 0.10))

    # Check minimum confidence threshold
    min_thresh = CONFIDENCE_THRESHOLDS["min_intent_threshold"]
    if confidence < min_thresh:
        return (
            Intent.AMBIGUOUS,
            confidence,
            True,
            f"Classification confidence ({confidence:.2f}) below threshold ({min_thresh:.2f})."
        )

    return best_intent, confidence, False, None
