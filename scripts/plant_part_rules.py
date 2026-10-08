"""Rule base for the plant-part dataset cleanup pipeline.

Given an image path inside ``data/external`` this module decides which
canonical *plant* and which plant *part* (leaves / flower / fruit) the
image belongs to.

Design principles (see the task brief):
  * Prefer explicit metadata (folder names, YOLO class names, YAML files,
    filename conventions) over any visual guessing.
  * When the part cannot be derived from metadata, fall back to a small,
    documented set of per-dataset defaults (the "pragmatic" policy) and
    record that the part was an assumption.
  * When neither plant nor part can be resolved, return an ``ambiguous``
    decision instead of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

# ----------------------------------------------------------------------
# Files / folders we care about
# ----------------------------------------------------------------------

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff",
}

# Directories that never hold "real" photographs (masks, labels, caches).
IGNORE_DIRS = {
    "labels", "label", "annotations", "annotation", "masks", "mask",
    "segmentation", "seg_masks", "__pycache__", ".cache", ".git",
    ".ipynb_checkpoints", ".tag",
}

# Folder tokens that carry no plant/part information.
IGNORE_TOKENS = {
    "train", "training", "valid", "val", "validation", "test", "testing",
    "eval", "evaluation", "images", "image", "imgs", "img", "color",
    "colour", "data", "dataset", "datasets", "original", "augmented",
    "aug", "augs", "rgb", "jpg", "jpeg", "png", "yolo", "yolov5",
    "yolov8", "yolov11", "v1i", "v4i", "v6i", "v11i", "folder",
    "source", "source2", "new", "raw", "resized", "cropped", "crop",
    "by_class", "classes", "class",
}


def resolve_yolo_class(dataset, class_name):
    """Return ``(plant, part, reason)`` for one YOLO class name.

    ``reason`` is set when the class cannot be used (non-plant or no part).
    """
    table = YOLO_CLASS_MAP.get(dataset)
    if table is not None:
        if class_name not in table:
            return None, None, f"unmapped_yolo_class:{class_name}"
        value = table[class_name]
        if value is None:
            return None, None, f"non_plant_class:{class_name}"
        plant, part = value
        if part is None:
            return plant, None, f"part_not_in_taxonomy:{class_name}"
        return plant, part, None

    # Auto mapping: class name *is* the plant label.
    # Drop trailing condition words first ("Lettuce-Diseased" -> "Lettuce").
    lookup_name = class_name
    class_tokens = tokenize(class_name)
    while class_tokens and class_tokens[-1] in _CLASS_CONDITION_WORDS:
        class_tokens.pop()
    if class_tokens and len(class_tokens) < len(tokenize(class_name)):
        lookup_name = " ".join(class_tokens)

    hit = (match_phrase(tokenize(lookup_name), ALIAS_PHRASES)
           or match_phrase(class_tokens, ALIAS_PHRASES))
    plant = hit[1] if hit else normalize(class_name)
    part = YOLO_DATASET_DEFAULT_PART.get(dataset)
    if part is None:
        return plant, None, f"part_unknown_class:{class_name}"
    return plant, part, None


def normalize(text: str) -> str:
    """Lowercase and collapse every non-alphanumeric run to one ``_``."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def tokenize(text: str) -> list:
    """Split a folder/file name into normalised tokens."""
    return [t for t in normalize(text).split("_") if t]


def _phrase_table(pairs) -> dict:
    """``{"bell pepper": "capsicum"}`` -> ``{("bell","pepper"): "capsicum"}``."""
    table = {}
    for phrase, value in pairs.items():
        key = tuple(tokenize(phrase))
        if key:
            table[key] = value
    return table


def match_phrase(tokens: list, table: dict) -> Optional[tuple]:
    """Return ``(length, value)`` for the longest phrase found in *tokens*."""
    best = None
    max_len = max((len(k) for k in table), default=0)
    for size in range(min(max_len, len(tokens)), 0, -1):
        for start in range(0, len(tokens) - size + 1):
            key = tuple(tokens[start:start + size])
            if key in table:
                if best is None or size > best[0]:
                    best = (size, table[key])
        if best is not None:
            return best
    return None


# ----------------------------------------------------------------------
# Plant aliases -> canonical plant name
# ----------------------------------------------------------------------

ALIASES = {
    # flowers / ornamentals
    "anthurium": "anthurium",
    "carnation": "carnation",
    "geranium": "geranium",
    "gerbera": "gerbera",
    "gypsophila": "gypsophila",
    "lilium": "lilium",
    "lily": "lilium",
    "orchid": "orchid",
    "cymbidium": "orchid",
    "marigold": "marigold",
    "rose": "rose",
    "dutch rose": "rose",
    "chrysanthemum": "chrysanthemum",
    "sunflower": "sunflower",
    "hibiscus": "hibiscus",
    "jasmine": "jasmine",
    "bougainvillea": "bougainvillea",

    # vegetables / herbs / crops
    "basil": "basil",
    "bean": "frenchbean",
    "bok choy": "bok_choy",
    "frenchbean": "frenchbean",
    "french bean": "frenchbean",
    "french beans": "frenchbean",
    "bell pepper": "capsicum",
    "bell": "capsicum",
    "pepper bell": "capsicum",
    "capsicum": "capsicum",
    "bitter gourd": "bitter_gourd",
    "bottle gourd": "bottle_gourd",
    "ridge gourd": "ridge_gourd",
    "ivy gourd": "ivy_gourd",
    "brinjal": "brinjal",
    "bringal": "brinjal",
    "eggplant": "brinjal",
    "broccoli": "broccoli",
    "cabbage": "cabbage",
    "carrot": "carrot",
    "cauliflower": "cauliflower",
    "celery": "celery",
    "cherry tomato": "cherry_tomato",
    "chilli": "chilli",
    "chili": "chilli",
    "green chilli": "chilli",
    "green chili": "chilli",
    "sili labuyo": "chilli",
    "chives": "chives",
    "coriander": "coriander",
    "cilantro": "coriander",
    "corriander": "coriander",
    "corn": "corn",
    "maize": "corn",
    "cucumber": "cucumber",
    "green cucumber": "cucumber",
    "curry leaf": "curry_leaf",
    "curry leaves": "curry_leaf",
    "dill": "dill",
    "garlic": "garlic",
    "ginger": "ginger",
    "lemongrass": "lemongrass",
    "lemon grass": "lemongrass",
    "lettuce": "lettuce",
    "mint": "mint",
    "okra": "okra",
    "oregano": "oregano",
    "parsley": "parsley",
    "potato": "potato",
    "radish": "radish",
    "raddish": "radish",
    "rosemary": "rosemary",
    "sage": "sage",
    "sorrel": "sorrel",
    "spinach": "spinach",
    "squash": "squash",
    "tarragon": "tarragon",
    "thyme": "thyme",
    "tomato": "tomato",
    "kamatis": "tomato",
    "turnip": "turnip",
    "zucchini": "zucchini",
    "zuchhini": "zucchini",
    "aloe vera": "aloe_vera",

    # fruits
    "apple": "apple",
    "redapple": "apple",
    "avocado": "avocado",
    "banana": "banana",
    "eliachi banana": "banana",
    "raw banana": "banana",
    "blueberry": "blueberry",
    "cherry": "cherry",
    "chikoo": "chikoo",
    "sapota": "chikoo",
    "figs": "figs",
    "grape": "grape",
    "grapevine": "grape",
    "guava": "guava",
    "guvava": "guava",
    "gauva": "guava",
    "lemon": "lemon",
    "green lemon": "lemon",
    "mandarin": "mandarin",
    "mango": "mango",
    "muskmelon": "muskmelon",
    "sunmelon": "muskmelon",
    "cantaloupe": "muskmelon",
    "melon": "muskmelon",
    "orange": "orange",
    "papaya": "papaya",
    "pappaya": "papaya",
    "peach": "peach",
    "pineapple": "pineapple",
    "plum": "plum",
    "pomegranate": "pomegranate",
    "raspberry": "raspberry",
    "strawberry": "strawberry",
    "sweet lime": "sweet_lime",
    "watermelon": "watermelon",

    # other crops / trees
    "citrus": "citrus",
    "coffee": "coffee",
    "maple": "maple",
    "rice": "rice",
    "soybean": "soybean",
    "tobacco": "tobacco",
    "wheat": "wheat",
    "neem": "neem",
    "tulsi": "tulsi",
    "henna": "henna",
    "castor": "castor",
}


# ----------------------------------------------------------------------
# Part keywords / disease -> part mapping
# ----------------------------------------------------------------------

LEAF_TOKENS = {"leaf", "leaves", "leaflet", "foliage", "phyllode"}
FLOWER_TOKENS = {
    "flower", "flowers", "floret", "florets", "petal", "petals",
    "bloom", "blooms", "inflorescence", "curd",
}
FRUIT_TOKENS = {"fruit", "fruits", "pod", "pods", "produce"}

LEAF_KEYWORDS = _phrase_table({t: "leaves" for t in LEAF_TOKENS})
FLOWER_KEYWORDS = _phrase_table({t: "flower" for t in FLOWER_TOKENS})
FRUIT_KEYWORDS = _phrase_table({t: "fruit" for t in FRUIT_TOKENS})

# Conditions that always imply the leaf is the subject.
LEAF_DISEASE_TOKENS = {
    "blight", "mildew", "spot", "spots", "rust", "mosaic", "virus", "wilt",
    "scorch", "mold", "mould", "mites", "smut", "canker", "curl", "rot",
    "damage", "damaged", "disease", "insect", "insects", "hole", "holes",
    "dry", "healthy", "pure", "infected", "pest", "bacterial", "fungal",
    "powdery", "downy", "septoria", "alternaria", "tip", "burn", "blotch",
    "streak", "scab", "anthracnose", "sigatoka",
}
LEAF_DISEASE_PHRASES = _phrase_table({t: "leaves" for t in LEAF_DISEASE_TOKENS})

# Conditions that point at the fruit.
FRUIT_DISEASE_TOKENS = {
    "blossom end rot", "end rot", "fruit rot", "mummy berry",
    "berry blotch", "brown rot",
}
FRUIT_DISEASE_PHRASES = _phrase_table({t: "fruit" for t in FRUIT_DISEASE_TOKENS})

# ----------------------------------------------------------------------
# Dataset level defaults
# ----------------------------------------------------------------------

# Canonical plant for a whole dataset (used when no folder/class says it).
DATASET_PLANT = {
    "anthurium": "anthurium",
    "carnation": "carnation",
    "geranium": "geranium",
    "gerbera_commons": "gerbera",
    "gypsophila": "gypsophila",
    "lilium": "lilium",
    "dutch_rose": "rose",
    "strawberry_clean": "strawberry",
    "coriander_leaf": "coriander",
    "raspberry": "raspberry",
    "lettuce_disease_v6i_folder": "lettuce",
    "broccoli_clean": "broccoli",
    "broccoli_new": "broccoli",
    "cabbage": "cabbage",
    "cauliflower": "cauliflower",
    "celery": "celery",
    "cucumber": "cucumber",
    "spinach_disease": "spinach",
    "strawberry": "strawberry",
    "tomato": "tomato",
    "turnip": "turnip",
    "zuchhini": "zucchini",
    "bell_pepper": "capsicum",
    "blueberry": "blueberry",
    "basil": "basil",
    "orchid_source": "orchid",
}

# Documented (pragmatic) part assumption for datasets whose metadata only
# gives the plant, never the part.
DATASET_DEFAULT_PART = {
    "anthurium": "flower",
    "carnation": "flower",
    "geranium": "flower",
    "gerbera_commons": "flower",
    "gypsophila": "flower",
    "lilium": "flower",
    "dutch_rose": "flower",
    "orchid_source": "flower",
    "strawberry_clean": "leaves",
    "coriander_leaf": "leaves",
    "lettuce_disease_v6i_folder": "leaves",
    "broccoli_clean": "leaves",
    "broccoli_new": "leaves",
    "cabbage": "leaves",
    "cauliflower": "leaves",
    "celery": "leaves",
    "cucumber": "leaves",
    "spinach_disease": "leaves",
    "strawberry": "leaves",
    "tomato": "leaves",
    "turnip": "leaves",
    "zuchhini": "leaves",
    "bell_pepper": "leaves",
    "blueberry": "leaves",
    "raspberry": "leaves",
}

# Datasets whose class folder name *is* the plant label (classification pools).
CLASS_FOLDER_DATASETS = {
    "herbal_classification_pool",
    "medicinal_plants",
    "orchid_source",
}
# Dataset -> documented default part for class-folder datasets.
CLASS_FOLDER_DEFAULT_PART = {
    "herbal_classification_pool": "leaves",
    "medicinal_plants": "leaves",
    "orchid_source": "flower",
}

# Explicit (dataset, folder) -> part overrides; "ambiguous" wins over rules.
EXPLICIT_PART = {
    ("bell_pepper", "bell_pepper_blossom_end_rot"): "fruit",
    ("blueberry", "blueberry_fruit_disease"): "fruit",
    ("blueberry", "blueberry_anthracnose"): "fruit",
    ("blueberry", "blueberry_botrytis_blight"): "fruit",
    ("blueberry", "blueberry_mummy_berry"): "fruit",
    ("strawberry", "strawberry_anthracnose"): "fruit",
    ("celery", "celery_anthracnose"): "leaves",
    ("spinach_disease", "anthracnose"): "leaves",
    ("cauliflower", "cauliflower_bacterial_soft_rot"): "ambiguous",
    ("coriander_leaf", "fresh"): "leaves",
    ("coriander_leaf", "spoiled"): "leaves",
}

# Folder names that force an ambiguous decision (plant/part not determinable).
AMBIGUOUS_FOLDERS = {
    "non_orchidaceae_plants",
    "non_cymbidium_orchidaceae_plants",
}

ALIAS_PHRASES = _phrase_table(ALIASES)


# ----------------------------------------------------------------------
# YOLO detection datasets
# ----------------------------------------------------------------------

# dataset -> {class name: (plant, part) | None | (plant, None)}
#   None            -> the class is not a plant (e.g. eggs) -> excluded
#   (plant, None)   -> plant known, no leaves/flower/fruit part -> excluded
YOLO_CLASS_MAP = {
    "frenchbean_source": {
        "Avocado": ("avocado", "fruit"),
        "Avocado Imported": ("avocado", "fruit"),
        "Bitter gourd": ("bitter_gourd", "fruit"),
        "Brinjal": ("brinjal", "fruit"),
        "Brown Eggs": None,
        "Brown Eggs 2": None,
        "Capsicum": ("capsicum", "fruit"),
        "Carrot": ("carrot", None),
        "Chikoo": ("chikoo", "fruit"),
        "Eliachi Banana": ("banana", "fruit"),
        "Figs": ("figs", "fruit"),
        "Frenchbeans": ("frenchbean", "fruit"),
        "Green Chilli": ("chilli", "fruit"),
        "Green Cucumber": ("cucumber", "fruit"),
        "Green lemon": ("lemon", "fruit"),
        "Guvava": ("guava", "fruit"),
        "Mandarin": ("mandarin", "fruit"),
        "Mango": ("mango", "fruit"),
        "Muskmelon": ("muskmelon", "fruit"),
        "Orange": ("orange", "fruit"),
        "Papaya": ("papaya", "fruit"),
        "Pineapple": ("pineapple", "fruit"),
        "Pomegranate": ("pomegranate", "fruit"),
        "RedApple": ("apple", "fruit"),
        "Sunmelon": ("muskmelon", "fruit"),
        "Tomato": ("tomato", "fruit"),
        "Watermelon": ("watermelon", "fruit"),
        "White Eggs": None,
        "organic eggs": None,
    },
    "frenchbean_source2": {
        "Bananas": ("banana", "fruit"),
        "French beans": ("frenchbean", "fruit"),
        "apples": ("apple", "fruit"),
        "bitter gourd": ("bitter_gourd", "fruit"),
        "bottle gourd": ("bottle_gourd", "fruit"),
        "bringal": ("brinjal", "fruit"),
        "cabbage": ("cabbage", "leaves"),
        "capsicum": ("capsicum", "fruit"),
        "carrots": ("carrot", None),
        "cauliflower": ("cauliflower", "flower"),
        "corn": ("corn", "fruit"),
        "corriander": ("coriander", "leaves"),
        "cucumber": ("cucumber", "fruit"),
        "curry leaves": ("curry_leaf", "leaves"),
        "ginger": ("ginger", None),
        "green chilli": ("chilli", "fruit"),
        "ivy gourd": ("ivy_gourd", "fruit"),
        "lemon": ("lemon", "fruit"),
        "mint": ("mint", "leaves"),
        "mushroom": None,
        "okra": ("okra", "fruit"),
        "orange": ("orange", "fruit"),
        "raddish": ("radish", None),
        "raw banana": ("banana", "fruit"),
        "ridge gourd": ("ridge_gourd", "fruit"),
        "sorrel leaves": ("sorrel", "leaves"),
        "spinach": ("spinach", "leaves"),
        "tomatoes": ("tomato", "fruit"),
    },
    "fruits_model_v1i_yolov11": {
        "Apple": ("apple", "fruit"),
        "Mango": ("mango", "fruit"),
        "Muskmelon": ("muskmelon", "fruit"),
    },
    "muskmelon_source": {
        "apple": ("apple", "fruit"),
        "banana": ("banana", "fruit"),
        "mango": ("mango", "fruit"),
        "muskmelon": ("muskmelon", "fruit"),
        "papaya": ("papaya", "fruit"),
        "pineapple": ("pineapple", "fruit"),
        "pomegranate": ("pomegranate", "fruit"),
        "sweet lime": ("sweet_lime", "fruit"),
        "watermelon": ("watermelon", "fruit"),
    },
}

# YOLO datasets whose class name is the plant and whose part is assumed.
YOLO_DATASET_DEFAULT_PART = {
    "herbal_dataset_v11i_yolov11": "leaves",
    "herbs_v4i_yolov11": "leaves",
    "bok_choy_lettuce_spinach_diseased_yolov8": "leaves",
}

# Trailing words that describe condition, not the plant itself.
_CLASS_CONDITION_WORDS = {"diseased", "healthy", "unhealthy", "infected"}

# ----------------------------------------------------------------------
# PlantSeg (segmentation) - labels live in the file name
# ----------------------------------------------------------------------

PLANTSEG_DATASETS = {"plantseg"}
PLANTSEG_FRUIT_TOKENS = {
    "blossom_end_rot", "fruit_rot", "end_rot", "mummy_berry",
    "berry_blotch", "brown_rot",
}


@dataclass
class Decision:
    """Outcome of resolving one image."""

    plant: Optional[str] = None
    part: Optional[str] = None
    source: str = ""
    reason: Optional[str] = None

    @property
    def ok(self) -> bool:
        return bool(self.plant and self.part) and self.reason is None

    @property
    def ambiguous(self) -> bool:
        return self.reason is not None



# ----------------------------------------------------------------------
# Path based resolution (folder datasets)
# ----------------------------------------------------------------------

def _ancestors(rel_parts):
    """Folder names from the dataset root down to the image's parent folder."""
    return [p for p in rel_parts[:-1]]


def _class_folder(ancestors):
    """Deepest ancestor folder that is a real label folder (not a split)."""
    for name in reversed(ancestors[1:]):
        norm = normalize(name)
        if norm and norm not in IGNORE_TOKENS:
            return norm
    return None


def resolve_plant(dataset, ancestors):
    """Return ``(plant, source, reason)``."""
    for name in reversed(ancestors):
        norm = normalize(name)
        if norm in AMBIGUOUS_FOLDERS:
            return None, "ambiguous_folder", f"folder_marked_ambiguous:{norm}"

    for name in reversed(ancestors):
        hit = match_phrase(tokenize(name), ALIAS_PHRASES)
        if hit:
            return hit[1], "path_alias", None

    if dataset in DATASET_PLANT:
        return DATASET_PLANT[dataset], "dataset_name", None

    if dataset in CLASS_FOLDER_DATASETS:
        cls = _class_folder(ancestors)
        if cls:
            hit = match_phrase(tokenize(cls), ALIAS_PHRASES)
            if hit:
                return hit[1], "class_folder_alias", None
            return cls, "class_folder", None

    return None, "unresolved", "plant_unknown"


def resolve_part(dataset, ancestors):
    """Return ``(part, source, reason)``."""
    for name in reversed(ancestors):
        norm = normalize(name)
        tokens = tokenize(name)

        override = EXPLICIT_PART.get((dataset, norm))
        if override is not None:
            if override == "ambiguous":
                return None, "explicit", f"part_not_in_taxonomy:{norm}"
            return override, "explicit", None

        for table, part in (
            (LEAF_KEYWORDS, "leaves"),
            (FLOWER_KEYWORDS, "flower"),
            (FRUIT_KEYWORDS, "fruit"),
        ):
            if match_phrase(tokens, table):
                return part, "folder_keyword", None

        if match_phrase(tokens, FRUIT_DISEASE_PHRASES):
            return "fruit", "disease_phrase", None
        if match_phrase(tokens, LEAF_DISEASE_PHRASES):
            return "leaves", "disease_phrase", None

    if dataset in CLASS_FOLDER_DEFAULT_PART:
        return (
            CLASS_FOLDER_DEFAULT_PART[dataset],
            "class_folder_default(assumed)",
            None,
        )
    if dataset in DATASET_DEFAULT_PART:
        return DATASET_DEFAULT_PART[dataset], "dataset_default(assumed)", None

    return None, "unresolved", "part_unknown"


def resolve_by_path(rel_parts):
    """Resolve a folder-dataset image from its relative path parts."""
    dataset = normalize(rel_parts[0])
    ancestors = _ancestors(rel_parts)

    plant, p_src, p_reason = resolve_plant(dataset, ancestors)
    part, q_src, q_reason = resolve_part(dataset, ancestors)

    reason = p_reason or q_reason
    if reason:
        # keep whichever plant we did manage to detect for the audit
        return Decision(
            plant=plant,
            part=part,
            source=f"{p_src}|{q_src}",
            reason=reason,
        )
    return Decision(plant=plant, part=part, source=f"{p_src}|{q_src}")


# ----------------------------------------------------------------------
# PlantSeg resolution (plant + disease are encoded in the file name)
# ----------------------------------------------------------------------

_PLANTSEG_MAIN = re.compile(r"^([a-z]+)_(.+?)_\d+$")
_PLANTSEG_ALT = re.compile(r"^([a-z]+)_(.+)$")


def resolve_plantseg(filename_stem):
    """Resolve a plantseg image from ``<species>_<disease>_<n>`` naming."""
    stem = filename_stem.lower()
    match = _PLANTSEG_MAIN.match(stem) or _PLANTSEG_ALT.match(stem)
    if not match:
        return Decision(source="plantseg", reason="plantseg_name_unparsed")

    species_raw, disease_raw = match.group(1), match.group(2)
    disease_raw = re.sub(r"\s*\(\d+\)\s*$", "", disease_raw).strip()

    hit = match_phrase(tokenize(species_raw), ALIAS_PHRASES)
    plant = hit[1] if hit else None
    if plant is None:
        return Decision(
            plant=normalize(species_raw), part=None, source="plantseg",
            reason="plantseg_unknown_species",
        )

    if any(tok in disease_raw for tok in PLANTSEG_FRUIT_TOKENS):
        part = "fruit"
    else:
        part = "leaves"

    return Decision(plant=plant, part=part, source="plantseg_filename")
