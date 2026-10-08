"""
Entity Extraction Layer for Agricultural Query Understanding
============================================================
Extracts structured agricultural entities (crop, disease, symptoms,
plant part, action, and language) using the official Model 1 / Model 2 taxonomy.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from router.taxonomy import ExtractedEntities

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
CROP_DISEASE_MAP_FILE = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_crop_disease_mapping.json"
if not CROP_DISEASE_MAP_FILE.exists():
    CROP_DISEASE_MAP_FILE = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"

# Load Crop-Disease Taxonomy
if CROP_DISEASE_MAP_FILE.exists():
    with open(CROP_DISEASE_MAP_FILE, "r", encoding="utf-8") as f:
        TAXONOMY_CROP_MAP: dict[str, list[str]] = json.load(f)
else:
    TAXONOMY_CROP_MAP = {}

# Known Crop list (lowercase)
KNOWN_CROPS = sorted(list({k.lower() for k in TAXONOMY_CROP_MAP.keys()} | {
    "tomato", "potato", "cucumber", "apple", "banana", "bell pepper", "capsicum",
    "corn", "soybean", "wheat", "rice", "grape", "eggplant", "cabbage", "cauliflower",
    "broccoli", "strawberry", "blueberry", "raspberry", "peach", "plum", "cherry",
    "citrus", "coffee", "garlic", "ginger", "lettuce", "celery", "carrot", "zucchini",
    "squash", "basil", "maple", "tobacco", "rose", "spinach", "marigold", "turnip",
    "anthurium", "carnation", "chrysanthemum", "geranium", "gerbera", "gypsophila",
    "lilium", "melon", "orchid", "french bean", "bean"
}), key=len, reverse=True)

# Common symptoms mapping to canonical symptom descriptor
SYMPTOM_PATTERNS = {
    "yellowing": ["yellow", "yellowing", "yellowed", "chlorosis", "peela", "peele"],
    "brown_spots": ["brown spot", "brown spots", "brown lesion", "brown lesions", "dark spot", "dark spots"],
    "spots": ["spot", "spots", "dhabbe", "daag", "lesion", "lesions", "specks", "dots"],
    "wilting": ["wilt", "wilting", "drooping", "murjha", "murjhaya"],
    "drying": ["dry", "drying", "dried", "sukha", "sukh"],
    "curling": ["curl", "curling", "curled", "twisted", "leaf curl"],
    "rot": ["rot", "rotting", "rotted", "decay", "sadan"],
    "powdery_coating": ["white powder", "white powdery", "powder", "mold", "fungus"],
    "holes": ["hole", "holes", "cheed", "chhidra"],
    "blight": ["blight", "blighted", "scorched", "burnt"],
    "stunting": ["stunt", "stunted", "small leaf", "short"],
}

# Plant parts
PLANT_PARTS = {
    "leaf": ["leaf", "leaves", "foliage", "patta", "patte", "patti"],
    "fruit": ["fruit", "fruits", "fal", "phal", "pod", "pods", "berry", "berries"],
    "stem": ["stem", "stems", "branch", "branches", "tana", "tane", "stalk"],
    "flower": ["flower", "flowers", "bloom", "blooms", "phool", "blossom"],
    "root": ["root", "roots", "jad", "jade"],
}

# Action keywords
ACTION_PATTERNS = {
    "treatment": ["treat", "treatment", "cure", "medicine", "spray", "dawai", "ilaj", "remedy", "control", "pesticide", "fungicide", "what to do", "what do", "kya karu", "kya kare"],
    "prevention": ["prevent", "prevention", "protect", "stop", "roktham", "bachav", "avoid"],
    "identification": ["identify", "recognize", "what is this", "name of", "which plant", "which crop"],
    "cause": ["why", "cause", "causes", "caused", "reason", "karan", "kyun"],
    "symptoms": ["symptom", "symptoms", "sign", "signs", "lakshan"],
    "diagnosis": ["diagnose", "diagnosis", "what happened", "what is wrong", "kya hua", "problem"],
}


def extract_entities(normalized_text: str, language: str = "en") -> ExtractedEntities:
    """
    Extracts structured entities from normalized query text.
    """
    entities = ExtractedEntities(language=language)
    text = " " + normalized_text.lower() + " "

    # 1. Extract Crop
    for crop in KNOWN_CROPS:
        pattern = r"\b" + re.escape(crop) + r"\b"
        if re.search(pattern, text):
            entities.crop = crop
            break

    # 2. Extract Plant Part
    for part, aliases in PLANT_PARTS.items():
        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, text):
                entities.plant_part = part
                break
        if entities.plant_part:
            break

    # 3. Extract Symptoms
    found_symptoms = []
    for symptom_name, aliases in SYMPTOM_PATTERNS.items():
        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, text):
                found_symptoms.append(symptom_name)
                break
    entities.symptoms = found_symptoms

    # 4. Extract Action
    for action_name, aliases in ACTION_PATTERNS.items():
        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, text):
                entities.action = action_name
                break
        if entities.action:
            break

    # 5. Extract Disease (if explicitly mentioned in taxonomy or knowledge base)
    all_disease_candidates: list[tuple[str, str, str]] = []
    
    for crop_title, disease_list in TAXONOMY_CROP_MAP.items():
        for disease_slug in disease_list:
            if disease_slug == "healthy" or "__" not in disease_slug:
                continue
            c_part, d_name = disease_slug.split("__", 1)
            clean_d_name = d_name.replace("_", " ")
            all_disease_candidates.append((crop_title.lower(), disease_slug, clean_d_name))

    # Add well-known pilot diseases if not already present
    pilot_extra = [
        ("cucumber", "cucumber__downy_mildew", "downy mildew"),
        ("squash", "squash__powdery_mildew", "powdery mildew"),
        ("ginger", "ginger__sheath_blight", "sheath blight"),
        ("ginger", "ginger__leaf_spot", "leaf spot"),
        ("garlic", "garlic__rust", "rust"),
        ("banana", "banana__cordana_leaf_spot", "cordana leaf spot"),
    ]
    for c_p, slug, clean_d in pilot_extra:
        if not any(cand[1] == slug for cand in all_disease_candidates):
            all_disease_candidates.append((c_p, slug, clean_d))

    # Match diseases (prioritizing longer names first)
    all_disease_candidates.sort(key=lambda x: len(x[2]), reverse=True)

    for c_title, disease_slug, clean_d_name in all_disease_candidates:
        if re.search(r"\b" + re.escape(clean_d_name) + r"\b", text):
            if entities.crop:
                if entities.crop == c_title:
                    entities.disease = disease_slug
                    break
            else:
                # Do not invent/force an unmentioned crop; let session context/dialogue resolve crop
                entities.disease = clean_d_name
                break

    return entities

