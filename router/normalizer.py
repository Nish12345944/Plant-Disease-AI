"""
Text Normalization Layer for Agricultural Query Understanding
============================================================
Handles spelling mistakes, Hinglish / transliterated Hindi agricultural terms,
informal phrasing, punctuation stripping, singular/plural normalization,
and language tagging.
"""

from __future__ import annotations

import re
from typing import Tuple

# Common crop name spelling mistakes and multilingual synonyms
CROP_SPELLING_MAP = {
    "tamato": "tomato",
    "tomoto": "tomato",
    "tomatos": "tomato",
    "tomatoes": "tomato",
    "tomaato": "tomato",
    "tamatar": "tomato",
    "tamatr": "tomato",
    
    "pototo": "potato",
    "patato": "potato",
    "potatos": "potato",
    "potatoes": "potato",
    "aalu": "potato",
    "aloo": "potato",
    
    "cucamber": "cucumber",
    "cucmber": "cucumber",
    "kheera": "cucumber",
    "khira": "cucumber",
    
    "cabbag": "cabbage",
    "cabage": "cabbage",
    "bandgobhi": "cabbage",
    "patta gobhi": "cabbage",
    "pattagobhi": "cabbage",
    
    "cauliflowr": "cauliflower",
    "caulifolwer": "cauliflower",
    "phoolgobhi": "cauliflower",
    "phulgobhi": "cauliflower",
    "gobhi": "cauliflower",
    
    "brocoli": "broccoli",
    "brocili": "broccoli",
    "hari gobhi": "broccoli",
    
    "peper": "bell pepper",
    "shimla mirch": "bell pepper",
    "shimlamirch": "bell pepper",
    "capsicum": "capsicum",
    
    "soya": "soybean",
    "soyabean": "soybean",
    "soya bean": "soybean",
    "bhat": "soybean",
    
    "brinjal": "eggplant",
    "baingan": "eggplant",
    "baigan": "eggplant",
    "bhata": "eggplant",
    
    "adrak": "ginger",
    "adrakh": "ginger",
    "gingr": "ginger",
    
    "lahsun": "garlic",
    "lasun": "garlic",
    "lehsun": "garlic",
    "garlick": "garlic",
    
    "kela": "banana",
    "kele": "banana",
    "banan": "banana",
    
    "seb": "apple",
    "aple": "apple",
    "appl": "apple",
    
    "gehun": "wheat",
    "gehu": "wheat",
    "kanak": "wheat",
    "wheet": "wheat",
    
    "makka": "corn",
    "makki": "corn",
    "bhutta": "corn",
    "chhalli": "corn",
    "maize": "corn",
    
    "angoor": "grape",
    "angur": "grape",
    
    "tarbooj": "watermelon",
    "kharbooza": "melon",
    
    "palak": "spinach",
    "spinich": "spinach",
    
    "strawbery": "strawberry",
    "strawberri": "strawberry",
    
    "chawal": "rice",
    "dhan": "rice",
    "paddy": "rice",
}

# Agricultural vocabulary and Hinglish term mapping
TERM_NORMALIZATION_MAP = {
    # Plant Parts
    "leafs": "leaves",
    "leafes": "leaves",
    "patta": "leaf",
    "patte": "leaves",
    "patti": "leaf",
    "pattiyan": "leaves",
    "fal": "fruit",
    "phal": "fruit",
    "phool": "flower",
    "tana": "stem",
    "tane": "stem",
    "jad": "root",
    "jade": "roots",
    "jaden": "roots",

    # Symptoms & Problems
    "yelow": "yellow",
    "yello": "yellow",
    "peela": "yellow",
    "peele": "yellow",
    "peeli": "yellow",
    "brwon": "brown",
    "broun": "brown",
    "bhura": "brown",
    "bhure": "brown",
    "dhabba": "spot",
    "dhabbe": "spots",
    "daag": "spots",
    "dag": "spot",
    "chitte": "spots",
    "sukha": "drying",
    "sukh": "drying",
    "sukh rhe": "drying",
    "sukh raha": "drying",
    "sukh rahi": "drying",
    "sukhi": "dried",
    "murjha": "wilting",
    "murjhaya": "wilting",
    "murjhana": "wilting",
    "kharab": "damaged",
    "kharab ho": "damaged",
    "sadan": "rot",
    "sad": "rot",
    "sad raha": "rotting",
    "jal": "burnt",
    "jal gaya": "scorched",
    "chhidra": "holes",
    "keeda": "pest",
    "keede": "pests",
    "kide": "pests",
    "kida": "pest",

    # Actions, Intent & Questions
    "bimari": "disease",
    "bimaari": "disease",
    "rog": "disease",
    "takleef": "problem",
    "ilaj": "treatment",
    "ilaaj": "treatment",
    "dawa": "medicine",
    "dawai": "medicine",
    "upchar": "treatment",
    "upay": "remedy",
    "remedi": "remedy",
    "treet": "treat",
    "tret": "treat",
    "happend": "happened",
    "hapend": "happened",
    "kya hua": "what happened",
    "kya ho gaya": "what happened",
    "kya ho gya": "what happened",
    "kya karu": "what should i do",
    "kya kare": "what to do",
    "kya karna chahiye": "what should be done",
    "roktham": "prevention",
    "bachav": "prevention",
    "kaise bache": "how to prevent",
    "chhidkao": "spray",
    "chidkao": "spray",
    "chhidakna": "spray",
}


def normalize_text(text: str) -> Tuple[str, str]:
    """
    Normalizes input text by fixing common spelling mistakes,
    translating Hinglish/Hindi agricultural terms to standard English equivalents,
    stripping punctuation, and returning (normalized_text, detected_language).
    """
    if not isinstance(text, str) or not text.strip():
        return "", "en"

    raw_clean = text.strip().lower()
    
    # Distinct Hinglish markers (unambiguous Hindi words)
    strong_hinglish_markers = {
        "kya", "hua", "karu", "kare", "patte", "patta", "patti", "bimari", "ilaj", 
        "dawai", "sukh", "rhe", "raha", "rahi", "hai", "kaise", "mera", 
        "gya", "gaya", "mein", "peele", "peela", "bhura", "keede", "upchar", "bachav"
    }
    tokens = set(re.findall(r"\b[a-z0-9]+\b", raw_clean))
    is_hinglish = bool(tokens & strong_hinglish_markers) or (" me " in f" {raw_clean} " and (" ilaj " in f" {raw_clean} " or " bimari " in f" {raw_clean} "))
    lang = "hi-Latn" if is_hinglish else "en"

    # Multi-word phrase replacements first
    working_text = " " + raw_clean + " "
    
    for term, norm in TERM_NORMALIZATION_MAP.items():
        if " " in term:
            pattern = r"\b" + re.escape(term) + r"\b"
            working_text = re.sub(pattern, norm, working_text)

    for crop, norm in CROP_SPELLING_MAP.items():
        if " " in crop:
            pattern = r"\b" + re.escape(crop) + r"\b"
            working_text = re.sub(pattern, norm, working_text)

    # Word-by-word token replacement
    words = working_text.split()
    normalized_words = []
    for w in words:
        clean_w = re.sub(r"[^a-z0-9]", "", w)
        if not clean_w:
            continue
        
        if clean_w in CROP_SPELLING_MAP:
            normalized_words.append(CROP_SPELLING_MAP[clean_w])
        elif clean_w in TERM_NORMALIZATION_MAP:
            normalized_words.append(TERM_NORMALIZATION_MAP[clean_w])
        else:
            normalized_words.append(clean_w)

    final_normalized = " ".join(normalized_words)
    return final_normalized, lang
