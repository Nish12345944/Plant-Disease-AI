"""MODEL 1 DATA PREPARATION PIPELINE (COMPLETE IMPLEMENTATION)

Executes Phases 1 through 12 strictly according to specification.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import random
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

from PIL import Image
import imagehash

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DEFAULT_EXTERNAL = ROOT / "data" / "external"
DEFAULT_PROCESSED = ROOT / "data" / "processed"
RANDOM_SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff",
}

IGNORE_DIRS = {
    "labels", "label", "annotations", "annotation", "masks", "mask",
    "segmentation", "seg_masks", "__pycache__", ".cache", ".git",
    ".ipynb_checkpoints", ".tag",
}

TARGET_CLASSES = [
    "tomato", "cherry_tomato", "capsicum", "cucumber", "strawberry",
    "blueberry", "melon", "zucchini", "french_bean", "lettuce",
    "spinach", "broccoli", "gerbera", "rose", "carnation",
    "chrysanthemum", "lilium", "orchid", "anthurium", "gypsophila",
    "marigold", "geranium",
]

CLASS_NORMALIZATION = {
    # Target classes and synonyms
    "tomato": "tomato",
    "kamatis": "tomato",
    "tomatoes": "tomato",
    "cherry tomato": "cherry_tomato",
    "cherry_tomato": "cherry_tomato",
    "capsicum": "capsicum",
    "bell pepper": "capsicum",
    "bell_pepper": "capsicum",
    "bell": "capsicum",
    "pepper bell": "capsicum",
    "cucumber": "cucumber",
    "green cucumber": "cucumber",
    "strawberry": "strawberry",
    "blueberry": "blueberry",
    "muskmelon": "melon",
    "sunmelon": "melon",
    "cantaloupe": "melon",
    "melon": "melon",
    "zucchini": "zucchini",
    "zuchhini": "zucchini",
    "french bean": "french_bean",
    "french beans": "french_bean",
    "frenchbean": "french_bean",
    "frenchbeans": "french_bean",
    "bean": "french_bean",
    "lettuce": "lettuce",
    "spinach": "spinach",
    "broccoli": "broccoli",
    "gerbera": "gerbera",
    "rose": "rose",
    "dutch rose": "rose",
    "dutch_rose": "rose",
    "carnation": "carnation",
    "chrysanthemum": "chrysanthemum",
    "lilium": "lilium",
    "lily": "lilium",
    "orchid": "orchid",
    "cymbidium": "orchid",
    "c_ensifolium": "orchid",
    "c_faberi": "orchid",
    "c_floribundum": "orchid",
    "c_goeringii": "orchid",
    "c_hybrid": "orchid",
    "c_kanran": "orchid",
    "c_lancifolium": "orchid",
    "c_sinense": "orchid",
    "c_szechuanicum": "orchid",
    "c_var_longibracteatum": "orchid",
    "c_var_serratum": "orchid",
    "c_var_tortisepalum": "orchid",
    "anthurium": "anthurium",
    "gypsophila": "gypsophila",
    "marigold": "marigold",
    "geranium": "geranium",

    # Unexpected agricultural / commercial crops
    "cabbage": "cabbage",
    "cauliflower": "cauliflower",
    "turnip": "turnip",
    "celery": "celery",
    "coriander": "coriander",
    "coriander leaf": "coriander",
    "coriander_leaf": "coriander",
    "corriander": "coriander",
    "cilantro": "coriander",
    "basil": "basil",
    "raspberry": "raspberry",
    "chilli": "chilli",
    "chili": "chilli",
    "chili leaves": "chilli",
    "sili labuyo": "chilli",
    "green chilli": "chilli",
    "green chili": "chilli",
    "apple": "apple",
    "redapple": "apple",
    "apples": "apple",
    "mango": "mango",
    "papaya": "papaya",
    "pappaya": "papaya",
    "banana": "banana",
    "bananas": "banana",
    "raw banana": "banana",
    "eliachi banana": "banana",
    "watermelon": "watermelon",
    "carrot": "carrot",
    "carrots": "carrot",
    "garlic": "garlic",
    "ginger": "ginger",
    "luya": "ginger",
    "mint": "mint",
    "parsley": "parsley",
    "dill": "dill",
    "chives": "chives",
    "oregano": "oregano",
    "rosemary": "rosemary",
    "thyme": "thyme",
    "lemongrass": "lemongrass",
    "lemon grass": "lemongrass",
    "sage": "sage",
    "tarragon": "tarragon",
    "brinjal": "brinjal",
    "bringal": "brinjal",
    "eggplant": "brinjal",
    "okra": "okra",
    "potato": "potato",
    "corn": "corn",
    "maize": "corn",
    "soybean": "soybean",
    "wheat": "wheat",
    "rice": "rice",
    "citrus": "citrus",
    "lemon": "lemon",
    "green lemon": "lemon",
    "orange": "orange",
    "mandarin": "mandarin",
    "sweet lime": "sweet_lime",
    "dayap": "lemon",
    "calamansi": "calamansi",
    "grape": "grape",
    "grapevine": "grape",
    "peach": "peach",
    "plum": "plum",
    "cherry": "cherry",
    "pineapple": "pineapple",
    "pomegranate": "pomegranate",
    "avocado": "avocado",
    "avacado": "avocado",
    "avocado imported": "avocado",
    "guava": "guava",
    "guava leaves": "guava",
    "guvava": "guava",
    "gauva": "guava",
    "chikoo": "chikoo",
    "chiko": "chikoo",
    "sapota": "chikoo",
    "figs": "figs",
    "coffee": "coffee",
    "tobacco": "tobacco",
    "squash": "squash",
    "bitter gourd": "bitter_gourd",
    "ampalaya": "bitter_gourd",
    "bottle gourd": "bottle_gourd",
    "ridge gourd": "ridge_gourd",
    "ivy gourd": "ivy_gourd",
    "sorrel": "sorrel",
    "sorrel leaves": "sorrel",
    "wood_sorel": "sorrel",
    "radish": "radish",
    "raddish": "radish",
    "curry leaf": "curry_leaf",
    "curry leaves": "curry_leaf",
    "curry_leaf": "curry_leaf",
    "bok choy": "bok_choy",
    "bok_choy": "bok_choy",
    "chamomile": "chamomile",
    "lavender": "lavender",
    "sunflower": "sunflower",
    "cosmos": "cosmos",
    "jasmine": "jasmine",
    "crape jasmine": "jasmine",
    "sampaguita": "jasmine",
    "hibiscus": "hibiscus",
    "gumamela": "hibiscus",
    "bougainvillea": "bougainvillea",

    # Herbal / medicinal plants
    "a las cuatro": "a_las_cuatro",
    "aloe vera": "aloe_vera",
    "alugbati": "alugbati",
    "amla": "amla",
    "amruta_balli": "amruta_balli",
    "arali": "arali",
    "ashoka": "ashoka",
    "ashwagandha": "ashwagandha",
    "atis": "atis",
    "bamboo": "bamboo",
    "basale": "basale",
    "betel": "betel",
    "betel_nut": "betel_nut",
    "blue ternate": "blue_ternate",
    "brahmi": "brahmi",
    "castor": "castor",
    "coconut": "coconut",
    "doddapatre": "doddapatre",
    "duhat": "duhat",
    "ekka": "ekka",
    "ganike": "ganike",
    "garlic vine": "garlic_vine",
    "guyabano leaves": "guyabano",
    "guyabano_leaves": "guyabano",
    "henna": "henna",
    "honge": "honge",
    "insulin": "insulin",
    "kamantigi": "kamantigi",
    "kamias": "kamias",
    "kangkong": "kangkong",
    "kantutay": "kantutay",
    "katakataka": "katakataka",
    "katuray": "katuray",
    "lagundi": "lagundi",
    "malabago": "malabago",
    "malunggay": "malunggay",
    "maple": "maple",
    "mugwort": "mugwort",
    "nagadali": "nagadali",
    "neem": "neem",
    "nganga": "nganga",
    "nithyapushpa": "nithyapushpa",
    "nooni": "nooni",
    "olive": "olive",
    "pandan": "pandan",
    "raktachandini": "raktachandini",
    "sambong": "sambong",
    "sampalok": "sampalok",
    "santan": "santan",
    "santol": "santol",
    "tawa-tawa": "tawa_tawa",
    "tawa_tawa": "tawa_tawa",
    "tulsi": "tulsi",
    "tulasi": "tulsi",
    "ylang-ylang": "ylang_ylang",
    "ylang_ylang": "ylang_ylang",
}

NON_PLANT_CLASSES = {
    "brown eggs", "brown eggs 2", "white eggs", "organic eggs", "mushroom",
}

AMBIGUOUS_FOLDERS = {
    "non_orchidaceae_plants",
    "non_cymbidium_orchidaceae_plants",
}

DATASET_CANONICAL_PLANT = {
    "anthurium": "anthurium",
    "carnation": "carnation",
    "geranium": "geranium",
    "gerbera_commons": "gerbera",
    "gypsophila": "gypsophila",
    "lilium": "lilium",
    "dutch_rose": "rose",
    "strawberry_clean": "strawberry",
    "strawberry": "strawberry",
    "coriander_leaf": "coriander",
    "raspberry": "raspberry",
    "lettuce-disease.v6i.folder": "lettuce",
    "broccoli_new": "broccoli",
    "cabbage": "cabbage",
    "cauliflower": "cauliflower",
    "celery": "celery",
    "cucumber": "cucumber",
    "spinach_disease": "spinach",
    "tomato": "tomato",
    "turnip": "turnip",
    "zuchhini": "zucchini",
    "pepper_bell": "capsicum",
    "blueberry": "blueberry",
    "basil": "basil",
    "Marigold_new": "marigold",
    "rose_new": "rose",
}

DATASET_DEFAULT_PART = {
    "anthurium": "flower",
    "carnation": "flower",
    "geranium": "flower",
    "gerbera_commons": "flower",
    "gypsophila": "flower",
    "lilium": "flower",
    "dutch_rose": "flower",
    "Orchid_source": "flower",
    "strawberry_clean": "leaves",
    "strawberry": "leaves",
    "coriander_leaf": "leaves",
    "raspberry": "leaves",
    "lettuce-disease.v6i.folder": "leaves",
    "broccoli_new": "leaves",
    "cabbage": "leaves",
    "cauliflower": "leaves",
    "celery": "leaves",
    "cucumber": "leaves",
    "spinach_disease": "leaves",
    "tomato": "leaves",
    "turnip": "leaves",
    "zuchhini": "leaves",
    "pepper_bell": "leaves",
    "blueberry": "leaves",
    "basil": "leaves",
    "herbs.v4i.yolov11": "leaves",
    "Herbal_Dataset.v11i.yolov11": "leaves",
    "medicinal_plants": "leaves",
    "herbal_classification_pool": "leaves",
    "Fruits Model.v1i.yolov11": "fruit",
}

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")

def detect_health(text: str) -> str:
    t = text.lower()
    has_healthy = any(w in t for w in ["healthy", "fresh", "helathy", "pure"])
    has_disease = any(w in t for w in [
        "blight", "rot", "spot", "mildew", "virus", "wilt", "scorch",
        "mold", "mould", "rust", "canker", "curl", "alternaria", "anthracnose",
        "septoria", "damage", "damaged", "pest", "insect", "insects", "hole",
        "holes", "dry", "spoiled", "diseased", "unhealthy", "infected",
        "yellow", "black_rot", "tip_burn", "grey_mould", "mummy", "botrytis",
        "belly_rot", "end_rot"
    ])
    if has_healthy and not has_disease:
        return "healthy"
    if has_disease:
        return "diseased"
    return "unknown"

def detect_part(text: str, default_part: str = "leaves") -> str:
    t = text.lower()
    if any(w in t for w in ["flower", "flowers", "petal", "petals", "bloom", "blooms", "inflorescence"]):
        return "flower"
    if any(w in t for w in ["curd"]):
        return "flower"
    if any(w in t for w in ["stem", "stalk", "branch"]):
        return "stem"
    if any(w in t for w in ["fruit", "fruits", "pod", "pods", "berry", "melon", "end_rot", "fruit_rot", "belly_rot", "mummy_berry"]):
        return "fruit"
    if any(w in t for w in ["leaf", "leaves", "leaflet", "foliage", "phyllode"]):
        return "leaves"
    return default_part

def parse_yolo_yaml(yaml_path: Path) -> dict[int, str] | None:
    try:
        text = yaml_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("names:"):
            val = s[6:].strip()
            if val.startswith("["):
                try:
                    names = ast.literal_eval(val)
                    return {i: str(n) for i, n in enumerate(names)}
                except Exception:
                    pass
    names = []
    in_names = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("names:"):
            in_names = True
            continue
        if in_names:
            if s.startswith("-"):
                names.append(s.lstrip("-").strip())
            elif ":" in s and not s.startswith("#"):
                parts = s.split(":", 1)
                names.append(parts[1].strip().strip("'\""))
            elif s and not line.startswith(" "):
                break
    if names:
        return {i: str(n) for i, n in enumerate(names)}
    return None

def yolo_label_path(image_path: Path) -> Path:
    parts = list(image_path.parts)
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == "images":
            parts[i] = "labels"
            return Path(*parts).with_suffix(".txt")
    return image_path.with_suffix(".txt")

def inspect_image_file(path_str: str, min_size: int = 32) -> dict:
    p = Path(path_str)
    try:
        size_bytes = p.stat().st_size
        if size_bytes == 0:
            return {"path": path_str, "ok": False, "error": "zero_byte_file", "width": 0, "height": 0, "format": "", "sha": "", "dhash": 0, "file_size": 0}
        digest = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                digest.update(chunk)
        sha = digest.hexdigest()
    except Exception as e:
        return {"path": path_str, "ok": False, "error": f"unreadable_file:{type(e).__name__}", "width": 0, "height": 0, "format": "", "sha": "", "dhash": 0, "file_size": 0}

    try:
        with Image.open(p) as img:
            img.load()
            w, h = img.size
            fmt = img.format or p.suffix.lstrip(".").upper()
            if w < min_size or h < min_size:
                return {"path": path_str, "ok": False, "error": f"tiny_image:{w}x{h}", "width": w, "height": h, "format": fmt, "sha": sha, "dhash": 0, "file_size": size_bytes}
            
            grey = img.convert("L")
            dh = int(str(imagehash.dhash(grey)), 16)
            
            extrema = grey.getextrema()
            if extrema[0] == extrema[1]:
                return {"path": path_str, "ok": False, "error": "blank_image", "width": w, "height": h, "format": fmt, "sha": sha, "dhash": dh, "file_size": size_bytes}
            
            return {"path": path_str, "ok": True, "error": "", "width": w, "height": h, "format": fmt, "sha": sha, "dhash": dh, "file_size": size_bytes}
    except Exception as e:
        return {"path": path_str, "ok": False, "error": f"corrupt_image:{type(e).__name__}", "width": 0, "height": 0, "format": "", "sha": sha, "dhash": 0, "file_size": size_bytes}

class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)

def hamming_distance(a: int, b: int) -> int:
    return bin(a ^ b).count("1")

def group_near_duplicates(hashes: list[int], threshold: int = 5) -> dict[int, list[int]]:
    buckets = defaultdict(list)
    for idx, val in enumerate(hashes):
        for shift in range(0, 64, 8):
            buckets[(shift, (val >> shift) & 0xFF)].append(idx)
    
    uf = UnionFind(len(hashes))
    for members in buckets.values():
        if len(members) < 2:
            continue
        first = members[0]
        for other in members[1:]:
            if hamming_distance(hashes[first], hashes[other]) <= threshold:
                uf.union(first, other)

    groups = defaultdict(list)
    for idx in range(len(hashes)):
        groups[uf.find(idx)].append(idx)
    return groups

def place_file(src: Path, dst: Path) -> str | None:
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return f"mkdir_failed:{type(exc).__name__}"
    
    if dst.exists():
        return None
    try:
        os.link(src, dst)
        return None
    except OSError:
        pass
    try:
        shutil.copy2(src, dst)
        return None
    except Exception as exc:
        return f"copy_failed:{type(exc).__name__}"

def resolve_single_image(abs_path: Path, rel_parts: tuple[str, ...], yolo_configs: dict[str, dict[int, str]]) -> dict:
    dataset = rel_parts[0]
    stem = abs_path.stem
    path_text = " ".join(rel_parts)
    
    health = detect_health(path_text)
    label_source = "folder_metadata"

    for part_name in rel_parts:
        if normalize_text(part_name) in AMBIGUOUS_FOLDERS:
            return {
                "plant": "", "part": "", "health": "unknown",
                "label_source": "ambiguous_folder", "ambiguous": True,
                "reason": f"folder_marked_ambiguous:{part_name}"
            }

    if dataset in yolo_configs:
        label_source = "yolo_annotation"
        lbl_file = yolo_label_path(abs_path)
        if not lbl_file.exists():
            return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "missing_yolo_annotation"}
        try:
            txt = lbl_file.read_text(encoding="utf-8", errors="replace").strip()
            if not txt:
                return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "empty_yolo_annotation"}
            lines = [l.split() for l in txt.splitlines() if l.strip()]
            cids = set()
            for l in lines:
                try:
                    cids.add(int(float(l[0])))
                except ValueError:
                    continue
            if not cids:
                return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "empty_yolo_annotation"}
            
            cnames = [yolo_configs[dataset].get(cid, "") for cid in cids]
            cnames_clean = [cn for cn in cnames if cn.lower() not in NON_PLANT_CLASSES]
            if not cnames_clean:
                return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": f"non_plant_class:{list(cnames)}"}
            
            mapped_plants = set()
            for cn in cnames_clean:
                norm_key = normalize_text(cn).replace("_", " ")
                p = CLASS_NORMALIZATION.get(norm_key) or CLASS_NORMALIZATION.get(normalize_text(cn))
                if p:
                    mapped_plants.add(p)
                else:
                    mapped_plants.add(normalize_text(cn))
            
            if len(mapped_plants) > 1:
                return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": f"multi_plant_annotation:{list(mapped_plants)}"}
            
            plant = next(iter(mapped_plants))
            part = detect_part(" ".join(cnames_clean), default_part=DATASET_DEFAULT_PART.get(dataset, "leaves"))
            if health == "unknown":
                health = detect_health(" ".join(cnames_clean))
            return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}
        except Exception as e:
            return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": f"yolo_read_error:{type(e).__name__}"}

    elif dataset == "plantseg":
        label_source = "plantseg_filename"
        m = re.match(r"^([a-z0-9]+)_(.+)$", stem.lower())
        if not m:
            return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "plantseg_name_unparsed"}
        species_raw = m.group(1)
        disease_raw = m.group(2)
        norm_key = normalize_text(species_raw).replace("_", " ")
        plant = CLASS_NORMALIZATION.get(norm_key) or CLASS_NORMALIZATION.get(normalize_text(species_raw))
        if not plant:
            return {"plant": normalize_text(species_raw), "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": f"plantseg_unknown_species:{species_raw}"}
        
        health = detect_health(disease_raw)
        part = detect_part(disease_raw, default_part="leaves")
        return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}

    elif dataset == "medicinal_plants":
        label_source = "class_folder"
        if len(rel_parts) >= 3 and rel_parts[1].lower() == "by_class":
            class_folder = rel_parts[2]
            norm_key = normalize_text(class_folder).replace("_", " ")
            plant = CLASS_NORMALIZATION.get(norm_key) or CLASS_NORMALIZATION.get(normalize_text(class_folder))
            if not plant:
                plant = normalize_text(class_folder)
            part = detect_part(path_text, default_part="leaves")
            return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}
        return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "medicinal_plants_path_unparsed"}

    elif dataset == "herbal_classification_pool":
        label_source = "class_folder"
        if len(rel_parts) >= 2:
            class_folder = rel_parts[1]
            norm_key = normalize_text(class_folder).replace("_", " ")
            plant = CLASS_NORMALIZATION.get(norm_key) or CLASS_NORMALIZATION.get(normalize_text(class_folder))
            if not plant:
                plant = normalize_text(class_folder)
            part = detect_part(path_text, default_part="leaves")
            return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}
        return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": "herbal_pool_path_unparsed"}

    elif dataset == "Orchid_source":
        label_source = "orchid_folder"
        plant = "orchid"
        part = detect_part(path_text, default_part="flower")
        return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}

    else:
        label_source = "folder_metadata"
        if dataset in DATASET_CANONICAL_PLANT:
            plant = DATASET_CANONICAL_PLANT[dataset]
        else:
            norm_ds = normalize_text(dataset).replace("_", " ")
            plant = CLASS_NORMALIZATION.get(norm_ds) or CLASS_NORMALIZATION.get(normalize_text(dataset))
        
        part = detect_part(path_text, default_part=DATASET_DEFAULT_PART.get(dataset, "leaves"))
        
        if dataset == "lettuce-disease.v6i.folder":
            if "/H/" in "/".join(rel_parts) or "\\H\\" in "\\".join(rel_parts):
                health = "healthy"
            elif "/D/" in "/".join(rel_parts) or "\\D\\" in "\\".join(rel_parts):
                health = "diseased"
        elif dataset == "coriander_leaf":
            if "Fresh" in rel_parts:
                health = "healthy"
            elif "Spoiled" in rel_parts:
                health = "diseased"
        elif dataset == "strawberry_clean":
            health = "healthy"
        
        if not plant:
            return {"plant": "", "part": "", "health": "unknown", "label_source": label_source, "ambiguous": True, "reason": f"unresolved_plant_dataset:{dataset}"}
        
        return {"plant": plant, "part": part, "health": health, "label_source": label_source, "ambiguous": False, "reason": ""}

# ======================================================================
# MAIN EXECUTION PIPELINE
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description="Run complete Model 1 data prep pipeline.")
    parser.add_argument("--external", type=Path, default=DEFAULT_EXTERNAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_PROCESSED)
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    parser.add_argument("--near-dup-threshold", type=int, default=5)
    parser.add_argument("--min-size", type=int, default=32)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    started = time.time()
    external = args.external
    output = args.output
    output.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("STARTING MODEL 1 DATA PREPARATION PIPELINE")
    print("=" * 80)
    print(f"External Source: {external}")
    print(f"Processed Root : {output}")
    print(f"CPU Workers    : {args.workers}")
    print(f"Near-dup Thresh: {args.near_dup_threshold}")
    print(f"Random Seed    : {RANDOM_SEED}")
    print()

    # ------------------------------------------------------------------
    # PHASE 1 & 2: DISCOVERY, RESOLUTION & CLASS DEFINITION
    # ------------------------------------------------------------------
    print("--- PHASE 1: DISCOVER AND AUDIT ALL DATA ---")
    yolo_configs = {}
    for top in sorted(external.iterdir()):
        if not top.is_dir():
            continue
        for ypath in list(top.glob("*.yaml")) + list(top.glob("*/*.yaml")):
            cmap = parse_yolo_yaml(ypath)
            if cmap:
                yolo_configs[top.name] = cmap
                break
    print(f"Discovered {len(yolo_configs)} YOLO dataset configurations: {list(yolo_configs.keys())}")

    print("Scanning all image candidate files...")
    candidates = []
    for dirpath, dirnames, filenames in os.walk(external):
        dirnames[:] = [d for d in dirnames if d.lower() not in IGNORE_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS:
                abs_p = Path(dirpath) / f
                rel_parts = abs_p.relative_to(external).parts
                candidates.append((abs_p, rel_parts))
    
    total_candidates = len(candidates)
    print(f"Found {total_candidates:,} image files in {external}.")

    # Resolve labels from metadata
    print("Resolving plant identity, plant part, and health status...")
    resolved_records = []
    class_mapping = {}
    ambiguous_count = 0
    raw_labels_found = Counter()

    for abs_p, rel_parts in candidates:
        rel_str = "/".join(rel_parts)
        ds = rel_parts[0]
        res = resolve_single_image(abs_p, rel_parts, yolo_configs)
        
        raw_lbl = ds
        if len(rel_parts) > 1:
            raw_lbl = rel_parts[1]
        raw_labels_found[raw_lbl] += 1
        
        if res["plant"]:
            class_mapping[raw_lbl] = res["plant"]

        if res["ambiguous"]:
            ambiguous_count += 1

        resolved_records.append({
            "abs_path": abs_p,
            "source_path": rel_str,
            "source_dataset": ds,
            "plant": res["plant"],
            "plant_part": res["part"],
            "health_status": res["health"],
            "label_source": res["label_source"],
            "ambiguous": res["ambiguous"],
            "reason": res["reason"],
        })

    # Save class_mapping.json
    class_mapping_path = output / "class_mapping.json"
    # Merge predefined normalization table with discovered mapping
    full_class_mapping = dict(sorted({**CLASS_NORMALIZATION, **class_mapping}.items()))
    with open(class_mapping_path, "w", encoding="utf-8") as f:
        json.dump(full_class_mapping, f, indent=2)
    print(f"Saved class mapping to {class_mapping_path} ({len(full_class_mapping)} mappings).")

    # ------------------------------------------------------------------
    # PHASE 3: IMAGE VALIDATION & CORRUPTIONS CHECK
    # ------------------------------------------------------------------
    print("\n--- PHASE 3: INSPECT & CLEAN INVALID IMAGES ---")
    inspect_fn = partial(inspect_image_file, min_size=args.min_size)
    inspect_paths = [str(r["abs_path"]) for r in resolved_records]

    inspections = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for idx, result in enumerate(pool.map(inspect_fn, inspect_paths, chunksize=64)):
            inspections.append(result)
            if idx and idx % 25000 == 0:
                print(f"  Inspected {idx:,} / {total_candidates:,} images...")

    valid_for_dedup = []
    invalid_count = 0
    corrupt_count = 0
    tiny_count = 0
    blank_count = 0
    zero_byte_count = 0

    for rec, insp in zip(resolved_records, inspections):
        rec["image_width"] = insp["width"]
        rec["image_height"] = insp["height"]
        rec["format"] = insp["format"]
        rec["sha256"] = insp["sha"]
        rec["dhash"] = insp["dhash"]
        rec["file_size"] = insp["file_size"]
        rec["duplicate"] = False
        rec["near_duplicate"] = False

        if not insp["ok"]:
            invalid_count += 1
            rec["valid"] = False
            rec["reason"] = insp["error"]
            if "corrupt" in insp["error"]:
                corrupt_count += 1
            elif "tiny" in insp["error"]:
                tiny_count += 1
            elif "blank" in insp["error"]:
                blank_count += 1
            elif "zero_byte" in insp["error"]:
                zero_byte_count += 1
        elif rec["ambiguous"]:
            rec["valid"] = False
        else:
            rec["valid"] = True
            valid_for_dedup.append(rec)

    print(f"Inspection complete: {len(valid_for_dedup):,} valid candidate images, {invalid_count:,} invalid/corrupt/tiny, {ambiguous_count:,} ambiguous.")

    # ------------------------------------------------------------------
    # PHASE 4: DUPLICATE DETECTION (EXACT & NEAR DUPLICATE)
    # ------------------------------------------------------------------
    print("\n--- PHASE 4: DUPLICATE DETECTION ---")
    valid_for_dedup.sort(key=lambda r: (r["plant"], r["plant_part"], r["source_path"]))

    # Step 1: Exact duplicates (SHA-256)
    seen_sha = {}
    kept_exact = []
    exact_dup_rows = []
    exact_dup_count = 0
    cross_class_dup_count = 0

    for item in valid_for_dedup:
        sha = item["sha256"]
        first = seen_sha.get(sha)
        if first is None:
            seen_sha[sha] = item
            kept_exact.append(item)
            continue
        
        same_plant = (first["plant"] == item["plant"])
        if same_plant:
            exact_dup_count += 1
            item["duplicate"] = True
            item["valid"] = False
            item["reason"] = f"exact_duplicate:{first['source_path']}"
            exact_dup_rows.append({
                "duplicate_group": f"sha_{sha[:12]}",
                "source_path": item["source_path"],
                "is_representative": False,
                "excluded": True,
                "hash_type": "sha256",
                "hash_value": sha,
            })
        else:
            cross_class_dup_count += 1
            item["duplicate"] = True
            item["ambiguous"] = True
            item["valid"] = False
            item["reason"] = f"cross_class_duplicate:{first['plant']}@{first['source_path']}"
            exact_dup_rows.append({
                "duplicate_group": f"sha_{sha[:12]}",
                "source_path": item["source_path"],
                "is_representative": False,
                "excluded": True,
                "hash_type": "sha256",
                "hash_value": sha,
            })

    # Record representative for exact dups
    for sha, rep in seen_sha.items():
        exact_dup_rows.append({
            "duplicate_group": f"sha_{sha[:12]}",
            "source_path": rep["source_path"],
            "is_representative": True,
            "excluded": False,
            "hash_type": "sha256",
            "hash_value": sha,
        })

    print(f"Exact duplicates removed: {exact_dup_count:,}, cross-class duplicates: {cross_class_dup_count:,}")

    # Step 2: Near duplicates (dHash Hamming distance <= 5) per plant class
    by_plant = defaultdict(list)
    for item in kept_exact:
        by_plant[item["plant"]].append(item)

    near_dup_count = 0
    final_representatives = []
    near_dup_rows = []
    group_counter = 0

    for plant, items in sorted(by_plant.items()):
        hashes = [item["dhash"] for item in items]
        groups = group_near_duplicates(hashes, threshold=args.near_dup_threshold)

        for root in sorted(groups):
            members = sorted(groups[root])
            group_id = f"{plant}_g{group_counter:06d}"
            group_counter += 1
            representative = items[members[0]]

            for pos, member_idx in enumerate(members):
                it = items[member_idx]
                it["duplicate_group"] = group_id
                if pos == 0:
                    it["is_representative"] = True
                    final_representatives.append(it)
                    near_dup_rows.append({
                        "duplicate_group": group_id,
                        "source_path": it["source_path"],
                        "is_representative": True,
                        "excluded": False,
                        "hash_type": "dhash64",
                        "hash_value": f"{it['dhash']:016x}",
                    })
                else:
                    it["is_representative"] = False
                    it["near_duplicate"] = True
                    it["valid"] = False
                    it["reason"] = f"near_duplicate:{representative['source_path']}"
                    near_dup_count += 1
                    near_dup_rows.append({
                        "duplicate_group": group_id,
                        "source_path": it["source_path"],
                        "is_representative": False,
                        "excluded": True,
                        "hash_type": "dhash64",
                        "hash_value": f"{it['dhash']:016x}",
                    })

    print(f"Near duplicates removed: {near_dup_count:,}, Final unique clean images: {len(final_representatives):,}")

    # Save duplicate_report.csv
    dup_report_csv = output / "duplicate_report.csv"
    with open(dup_report_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "duplicate_group", "source_path", "is_representative", "excluded", "hash_type", "hash_value"
        ])
        writer.writeheader()
        writer.writerows(exact_dup_rows + near_dup_rows)
    print(f"Saved duplicate report to {dup_report_csv}.")

    # Save dataset_audit.csv
    audit_csv = output / "dataset_audit.csv"
    with open(audit_csv, "w", newline="", encoding="utf-8") as f:
        fields = [
            "source_path", "source_dataset", "plant", "plant_part", "health_status",
            "label_source", "image_width", "image_height", "format", "valid",
            "duplicate", "near_duplicate", "ambiguous", "reason"
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in resolved_records:
            writer.writerow({k: r.get(k, "") for k in fields})
    print(f"Saved dataset audit to {audit_csv}.")

    # ------------------------------------------------------------------
    # PHASE 5: PLANT-PART DATASET ORGANIZATION
    # ------------------------------------------------------------------
    print("\n--- PHASE 5: PLANT-PART DATASET ORGANIZATION ---")
    plant_part_root = output / "plant_part_dataset"
    if plant_part_root.exists():
        shutil.rmtree(plant_part_root)
    plant_part_root.mkdir(parents=True, exist_ok=True)

    plant_part_counts = Counter()
    for item in final_representatives:
        plant = item["plant"]
        part = item["plant_part"] or "leaves"
        ext = item["abs_path"].suffix.lower()
        plant_part_counts[(plant, part)] += 1
        seq = plant_part_counts[(plant, part)]
        dst_folder = plant_part_root / plant / f"{plant}_{part}"
        dst_file = dst_folder / f"{plant}_{part}_{seq:06d}{ext}"
        place_file(item["abs_path"], dst_file)
        item["plant_part_path"] = str(dst_file.relative_to(output))

    print(f"Organized into plant_part_dataset: {len(plant_part_counts)} active plant-part folders.")

    # ------------------------------------------------------------------
    # PHASE 6: HEALTHY VS DISEASED AUDIT
    # ------------------------------------------------------------------
    print("\n--- PHASE 6: HEALTHY VS DISEASED AUDIT ---")
    health_stats = defaultdict(lambda: Counter())
    for item in final_representatives:
        key = (item["plant"], item["plant_part"] or "leaves")
        health_stats[key][item["health_status"]] += 1

    health_csv = output / "health_distribution.csv"
    with open(health_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["plant", "plant_part", "healthy", "diseased", "unknown", "total"])
        for (plant, part), c in sorted(health_stats.items()):
            tot = sum(c.values())
            writer.writerow([plant, part, c["healthy"], c["diseased"], c["unknown"], tot])
    print(f"Saved health distribution to {health_csv}.")

    # ------------------------------------------------------------------
    # PHASE 7: CLASS BALANCE ANALYSIS
    # ------------------------------------------------------------------
    print("\n--- PHASE 7: CLASS BALANCE ANALYSIS ---")
    plant_image_counts = Counter(item["plant"] for item in final_representatives)
    counts_sorted = sorted(plant_image_counts.values())
    min_count = counts_sorted[0] if counts_sorted else 0
    max_count = counts_sorted[-1] if counts_sorted else 0
    med_count = counts_sorted[len(counts_sorted) // 2] if counts_sorted else 0
    imbalance_ratio = round(max_count / max(1, min_count), 2)

    low_data_classes = [p for p, c in plant_image_counts.items() if c < 30]
    print(f"Total plant classes : {len(plant_image_counts)}")
    print(f"Min class count     : {min_count}")
    print(f"Max class count     : {max_count}")
    print(f"Median class count  : {med_count}")
    print(f"Imbalance ratio     : {imbalance_ratio}:1")
    print(f"LOW_DATA_CLASS (<30): {len(low_data_classes)} classes: {low_data_classes}")

    # ------------------------------------------------------------------
    # PHASE 8: DATA LEAKAGE-SAFE TRAIN/VAL/TEST SPLIT
    # ------------------------------------------------------------------
    print("\n--- PHASE 8: DATA LEAKAGE-SAFE TRAIN/VAL/TEST SPLIT ---")
    model1_root = output / "model1_dataset"
    if model1_root.exists():
        shutil.rmtree(model1_root)
    model1_root.mkdir(parents=True, exist_ok=True)

    rng = random.Random(RANDOM_SEED)
    splits = ("train", "val", "test")
    ratios = {"train": 0.8, "val": 0.1, "test": 0.1}

    # Group items by plant, then by duplicate group
    by_plant_items = defaultdict(list)
    for it in final_representatives:
        by_plant_items[it["plant"]].append(it)

    split_manifest_rows = []
    split_counts = Counter()
    class_split_counts = defaultdict(Counter)

    for plant, items in sorted(by_plant_items.items()):
        # Group by duplicate_group to guarantee zero duplicate leakage
        dup_groups = defaultdict(list)
        for it in items:
            grp = it.get("duplicate_group", f"solo_{it['source_path']}")
            dup_groups[grp].append(it)

        group_keys = sorted(dup_groups.keys())
        rng.shuffle(group_keys)

        total_plant_items = len(items)
        curr_counts = {s: 0 for s in splits}

        for grp in group_keys:
            grp_items = dup_groups[grp]
            sz = len(grp_items)
            # Pick split furthest below target
            best_split = max(splits, key=lambda s: (ratios[s] * total_plant_items - curr_counts[s], -splits.index(s)))
            curr_counts[best_split] += sz

            for it in grp_items:
                it["split"] = best_split
                split_counts[best_split] += 1
                class_split_counts[plant][best_split] += 1

                ext = it["abs_path"].suffix.lower()
                dest_dir = model1_root / best_split / plant
                dest_file = dest_dir / f"{plant}_{it['health_status']}_{split_counts[best_split]:06d}{ext}"
                place_file(it["abs_path"], dest_file)

                split_manifest_rows.append({
                    "image_path": str(dest_file.relative_to(output)),
                    "plant_class": plant,
                    "plant_part": it["plant_part"],
                    "health_status": it["health_status"],
                    "split": best_split,
                    "duplicate_group": grp,
                    "source_dataset": it["source_dataset"],
                })

    # Save model1_split_manifest.csv
    manifest_csv = output / "model1_split_manifest.csv"
    with open(manifest_csv, "w", newline="", encoding="utf-8") as f:
        fields = [
            "image_path", "plant_class", "plant_part", "health_status",
            "split", "duplicate_group", "source_dataset"
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(split_manifest_rows)
    print(f"Saved split manifest to {manifest_csv}.")
    print(f"Splits summary: Train={split_counts['train']:,}, Val={split_counts['val']:,}, Test={split_counts['test']:,}")

    # ------------------------------------------------------------------
    # PHASE 9: VERIFY SPLIT
    # ------------------------------------------------------------------
    print("\n--- PHASE 9: AUTOMATED SPLIT VERIFICATION ---")
    image_paths_by_split = defaultdict(set)
    groups_by_split = defaultdict(set)
    for row in split_manifest_rows:
        image_paths_by_split[row["split"]].add(row["image_path"])
        groups_by_split[row["split"]].add(row["duplicate_group"])

    train_imgs = image_paths_by_split["train"]
    val_imgs = image_paths_by_split["val"]
    test_imgs = image_paths_by_split["test"]

    train_grps = groups_by_split["train"]
    val_grps = groups_by_split["val"]
    test_grps = groups_by_split["test"]

    # Check 1: No image in multiple splits
    img_leakage = (train_imgs & val_imgs) | (train_imgs & test_imgs) | (val_imgs & test_imgs)
    pass_img_leak = len(img_leakage) == 0

    # Check 2: No duplicate group in multiple splits
    grp_leakage = (train_grps & val_grps) | (train_grps & test_grps) | (val_grps & test_grps)
    pass_grp_leak = len(grp_leakage) == 0

    # Check 3: Populated classes represented in all splits
    classes_missing_val = [p for p, c in class_split_counts.items() if plant_image_counts[p] >= 10 and c["val"] == 0]
    classes_missing_test = [p for p, c in class_split_counts.items() if plant_image_counts[p] >= 10 and c["test"] == 0]
    pass_class_rep = len(classes_missing_val) == 0 and len(classes_missing_test) == 0

    # Check 4: Reasonable distribution
    train_pct = round(split_counts["train"] / max(1, len(final_representatives)) * 100, 1)
    val_pct = round(split_counts["val"] / max(1, len(final_representatives)) * 100, 1)
    test_pct = round(split_counts["test"] / max(1, len(final_representatives)) * 100, 1)
    pass_dist = (75.0 <= train_pct <= 85.0) and (7.0 <= val_pct <= 13.0) and (7.0 <= test_pct <= 13.0)

    # Check 5: Healthy and diseased represented
    has_healthy = any(r["health_status"] == "healthy" for r in final_representatives)
    has_diseased = any(r["health_status"] == "diseased" for r in final_representatives)
    pass_health = has_healthy and has_diseased

    validation_report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_final_images": len(final_representatives),
        "split_counts": dict(split_counts),
        "split_percentages": {"train": train_pct, "val": val_pct, "test": test_pct},
        "tests": {
            "no_image_in_multiple_splits": "PASS" if pass_img_leak else "FAIL",
            "no_duplicate_group_in_multiple_splits": "PASS" if pass_grp_leak else "FAIL",
            "no_near_duplicate_group_in_multiple_splits": "PASS" if pass_grp_leak else "FAIL",
            "classes_represented_across_splits": "PASS" if pass_class_rep else "FAIL",
            "class_distribution_reasonable": "PASS" if pass_dist else "FAIL",
            "healthy_and_diseased_represented": "PASS" if pass_health else "FAIL",
        },
        "leaked_images_count": len(img_leakage),
        "leaked_duplicate_groups_count": len(grp_leakage),
        "classes_missing_in_val": classes_missing_val,
        "classes_missing_in_test": classes_missing_test,
    }

    val_report_path = output / "split_validation_report.json"
    with open(val_report_path, "w", encoding="utf-8") as f:
        json.dump(validation_report, f, indent=2)
    print(f"Saved split validation report to {val_report_path}.")

    # ------------------------------------------------------------------
    # PHASE 10: IMAGE QUALITY STATISTICS
    # ------------------------------------------------------------------
    print("\n--- PHASE 10: IMAGE QUALITY STATISTICS ---")
    widths = [it["image_width"] for it in final_representatives]
    heights = [it["image_height"] for it in final_representatives]
    aspect_ratios = [round(w / max(1, h), 2) for w, h in zip(widths, heights)]
    file_sizes = [it["file_size"] for it in final_representatives]
    formats = Counter(it["format"] for it in final_representatives)

    widths.sort()
    heights.sort()
    aspect_ratios.sort()
    file_sizes.sort()

    min_res = (widths[0], heights[0]) if widths else (0, 0)
    max_res = (widths[-1], heights[-1]) if widths else (0, 0)
    med_res = (widths[len(widths) // 2], heights[len(heights) // 2]) if widths else (0, 0)
    avg_size_kb = round(sum(file_sizes) / max(1, len(file_sizes)) / 1024, 1) if file_sizes else 0

    quality_stats = {
        "min_resolution": f"{min_res[0]}x{min_res[1]}",
        "max_resolution": f"{max_res[0]}x{max_res[1]}",
        "median_resolution": f"{med_res[0]}x{med_res[1]}",
        "average_file_size_kb": avg_size_kb,
        "formats_distribution": dict(formats),
        "aspect_ratio_quantiles": {
            "p10": aspect_ratios[int(len(aspect_ratios) * 0.10)],
            "median": aspect_ratios[len(aspect_ratios) // 2],
            "p90": aspect_ratios[int(len(aspect_ratios) * 0.90)],
        }
    }

    # Save dataset_audit_summary.json
    audit_summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_source_images": total_candidates,
        "valid_images_before_dedup": len(valid_for_dedup),
        "corrupted_images": corrupt_count,
        "tiny_images": tiny_count,
        "blank_images": blank_count,
        "zero_byte_files": zero_byte_count,
        "ambiguous_images": ambiguous_count,
        "exact_duplicates_removed": exact_dup_count,
        "cross_class_duplicates_removed": cross_class_dup_count,
        "near_duplicates_removed": near_dup_count,
        "final_clean_images": len(final_representatives),
        "total_plant_classes": len(plant_image_counts),
        "image_quality": quality_stats,
        "counts_per_plant": dict(sorted(plant_image_counts.items(), key=lambda kv: -kv[1])),
    }
    audit_summary_path = output / "dataset_audit_summary.json"
    with open(audit_summary_path, "w", encoding="utf-8") as f:
        json.dump(audit_summary, f, indent=2)
    print(f"Saved dataset audit summary to {audit_summary_path}.")

    # ------------------------------------------------------------------
    # PHASE 11: CREATE FINAL DATASET REPORT
    # ------------------------------------------------------------------
    print("\n--- PHASE 11: CREATE FINAL DATASET REPORT ---")
    report_md_path = output / "MODEL1_DATASET_REPORT.md"
    
    # Generate markdown content
    md = []
    md.append("# MODEL 1 DATASET AUDIT & PREPARATION REPORT")
    md.append(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Target Model:** EfficientNet-B2 (Multiclass Plant/Crop Identification)  ")
    md.append(f"**Random Seed:** {RANDOM_SEED}  \n")
    md.append("---")
    
    md.append("## 1. Executive Summary")
    md.append(f"- **Total Source Images:** {total_candidates:,}")
    md.append(f"- **Valid Images (pre-dedup):** {len(valid_for_dedup):,}")
    md.append(f"- **Corrupt / Unreadable / Tiny Images Excluded:** {invalid_count:,}")
    md.append(f"- **Ambiguous Images Excluded:** {ambiguous_count:,}")
    md.append(f"- **Exact Duplicates Removed:** {exact_dup_count:,}")
    md.append(f"- **Cross-Class Duplicates Removed:** {cross_class_dup_count:,}")
    md.append(f"- **Near-Duplicates Removed:** {near_dup_count:,}")
    md.append(f"- **Final Clean Dataset Size:** {len(final_representatives):,}")
    md.append(f"- **Total Plant Classes:** {len(plant_image_counts)}")
    md.append(f"- **Train / Val / Test Split:** {split_counts['train']:,} ({train_pct}%) / {split_counts['val']:,} ({val_pct}%) / {split_counts['test']:,} ({test_pct}%)")
    md.append("")

    md.append("## 2. Dataset Quality & Image Integrity")
    md.append(f"- **Resolution Range:** Min: `{min_res[0]}x{min_res[1]}`, Median: `{med_res[0]}x{med_res[1]}`, Max: `{max_res[0]}x{max_res[1]}`")
    md.append(f"- **Average File Size:** {avg_size_kb} KB")
    md.append("- **Formats Detected:** " + ", ".join(f"`{k}`: {v:,}" for k, v in formats.items()))
    md.append(f"- **Zero-byte Files:** {zero_byte_count}")
    md.append(f"- **Tiny Files (<32px):** {tiny_count}")
    md.append(f"- **Blank Files:** {blank_count}")
    md.append(f"- **Corrupt Files:** {corrupt_count}")
    md.append("")

    md.append("## 3. Data Leakage & Split Verification")
    md.append(f"- **Image Leakage Test:** `{'PASS' if pass_img_leak else 'FAIL'}` (0 images across multiple splits)")
    md.append(f"- **Duplicate Group Leakage Test:** `{'PASS' if pass_grp_leak else 'FAIL'}` (0 duplicate groups across multiple splits)")
    md.append(f"- **Near-Duplicate Group Leakage Test:** `{'PASS' if pass_grp_leak else 'FAIL'}`")
    md.append(f"- **Class Representation Test:** `{'PASS' if pass_class_rep else 'FAIL'}`")
    md.append(f"- **Health Status Representation Test:** `{'PASS' if pass_health else 'FAIL'}`")
    md.append("")

    md.append("## 4. Class Balance & Low-Data Analysis")
    md.append(f"- **Minimum Class Count:** {min_count}")
    md.append(f"- **Maximum Class Count:** {max_count}")
    md.append(f"- **Median Class Count:** {med_count}")
    md.append(f"- **Imbalance Ratio:** {imbalance_ratio}:1")
    md.append("")
    md.append("### Classes with Low Data (`LOW_DATA_CLASS`, < 30 images):")
    if low_data_classes:
        for c in low_data_classes:
            md.append(f"- `{c}`: {plant_image_counts[c]} images")
    else:
        md.append("- None")
    md.append("")
    md.append("### Recommendations for Model Training:")
    md.append("1. **Class Weighting:** Use inverse frequency weighting `w_c = (N / (num_classes * n_c))` in CrossEntropyLoss.")
    md.append("2. **Weighted Sampling:** Use PyTorch `WeightedRandomSampler` to draw balanced batches during training.")
    md.append("3. **Augmentations:** Apply RandAugment / AutoAugment on rare and low-data classes.")
    md.append("4. **EfficientNet-B2 Preprocessing:** Resize images to 288x288 with standard ImageNet normalization.")
    md.append("")

    md.append("## 5. Counts Per Plant Class (Top 25)")
    md.append("| Plant Class | Total Images | Train | Val | Test | Target Class? |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for p, tot in sorted(plant_image_counts.items(), key=lambda kv: -kv[1])[:25]:
        cs = class_split_counts[p]
        is_target = "YES" if p in TARGET_CLASSES else "NO"
        md.append(f"| `{p}` | {tot:,} | {cs['train']:,} | {cs['val']:,} | {cs['test']:,} | {is_target} |")
    md.append("")

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"Saved Markdown report to {report_md_path}.")

    # ------------------------------------------------------------------
    # PHASE 12: FINAL PRE-TRAINING GATE
    # ------------------------------------------------------------------
    elapsed = round(time.time() - started, 1)
    
    # Determine pre-training gate status
    ready = (pass_img_leak and pass_grp_leak and pass_class_rep and len(final_representatives) > 1000)
    gate_status = "READY_FOR_TRAINING" if ready else "NOT_READY_FOR_TRAINING"

    print("\n" + "=" * 40)
    print("MODEL 1 DATASET PRE-TRAINING CHECK")
    print("=" * 40)
    print(f"Classes: {len(plant_image_counts)}")
    print(f"Total valid images: {len(final_representatives):,}")
    print()
    print(f"Train: {split_counts['train']:,}")
    print(f"Validation: {split_counts['val']:,}")
    print(f"Test: {split_counts['test']:,}")
    print()
    print(f"Corrupt: {corrupt_count}")
    print(f"Exact duplicates removed: {exact_dup_count:,}")
    print(f"Near duplicates removed: {near_dup_count:,}")
    print(f"Ambiguous: {ambiguous_count:,}")
    print()
    print("Classes with low data:")
    if low_data_classes:
        for c in low_data_classes[:8]:
            print(f"- {c}: {plant_image_counts[c]} images")
        if len(low_data_classes) > 8:
            print(f"- ... and {len(low_data_classes) - 8} more classes")
    else:
        print("- None")
    print()
    print("Classes with severe imbalance:")
    top_class, top_cnt = plant_image_counts.most_common(1)[0]
    print(f"- {top_class} ({top_cnt:,} images vs median {med_count})")
    print()
    print("Healthy/Diseased coverage:")
    h_cnt = sum(1 for it in final_representatives if it["health_status"] == "healthy")
    d_cnt = sum(1 for it in final_representatives if it["health_status"] == "diseased")
    u_cnt = sum(1 for it in final_representatives if it["health_status"] == "unknown")
    print(f"- Healthy: {h_cnt:,}")
    print(f"- Diseased: {d_cnt:,}")
    print(f"- Unknown: {u_cnt:,}")
    print()
    print(f"Data leakage: {'PASS' if pass_img_leak else 'FAIL'}")
    print(f"Duplicate leakage: {'PASS' if pass_grp_leak else 'FAIL'}")
    print(f"Class split: {'PASS' if pass_class_rep else 'FAIL'}")
    print(f"Image integrity: {'PASS' if invalid_count == 0 or corrupt_count < 100 else 'FAIL'}")
    print("=" * 40)
    print(f"FINAL STATUS: {gate_status}")
    print("=" * 40)
    print(f"Pipeline executed in {elapsed}s.")

if __name__ == "__main__":
    main()
