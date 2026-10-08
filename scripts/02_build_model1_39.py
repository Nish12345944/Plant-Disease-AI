from pathlib import Path
from collections import Counter, defaultdict
import shutil
import random
import hashlib
import re
import ast

import numpy as np
from PIL import Image


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
)

EXTERNAL = ROOT / "data" / "external"

OUTPUT = (
    ROOT
    / "data"
    / "final"
    / "model1_39"
)


# ============================================================
# 39 TARGET CLASSES
# ============================================================

TARGET_CLASSES = [

    # Fruit
    "muskmelon",
    "raspberry",
    "blueberry",
    "strawberry",
    "papaya",
    "watermelon",
    "dragon_fruit",
    "kiwifruit",
    "blackberry",

    # Vegetable
    "brinjal",
    "tomato",
    "okra",
    "cabbage",
    "cauliflower",
    "cucumber",
    "broccoli",
    "zucchini",
    "chilli",
    "capsicum",
    "lettuce",
    "spinach",
    "kale",

    # Herbs
    "mint",
    "coriander",
    "basil",
    "parsley",
    "celery",
    "dill",
    "chives",
    "oregano",
    "thyme",
    "rosemary",

    # Flowers
    "rose",
    "gerbera",
    "carnation",
    "dutch_rose",
    "lilium",
    "orchid",
    "chrysanthemum",
]


# ============================================================
# SETTINGS
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

# Maximum images per class
MAX_PER_CLASS = 1000

# ============================================================
# PER-SOURCE CAP
#
# Why this exists:
#
# The PlantVillage tomato folder alone holds ~16,000 lab photos,
# while plantwild_v2 has only 902 real field tomato photos.
#
# The old code shuffled every source together and then truncated
# to MAX_PER_CLASS, which kept ~94% PlantVillage tomato. The model
# therefore learned "clean white background = tomato" instead of
# "tomato", and scored only 12.9% on real tomato photos while
# scoring 100% on PlantVillage ones.
#
# This cap limits how many images any single source may contribute
# to one class.
#
# It is applied ONLY to classes that draw from more than one
# source. A single-source class has nothing to balance, so all of
# its images are kept.
# ============================================================

MAX_PER_SOURCE = 400

# ============================================================
# NEAR-DUPLICATE GROUPING
#
# plantwild / PlantDoc contain many consecutive frames of the same
# leaf. When those frames are split across train and test, the test
# score is inflated because the test image is almost identical to a
# training image.
#
# Images whose dHash is within this Hamming distance are treated as
# one scene and are always kept in the SAME split.
# ============================================================

NEAR_DUPLICATE_DISTANCE = 6

# ============================================================
# GROCERY / MARKET "PRODUCE" DATASETS
#
# frenchbean_source  -> Roboflow "indian-fresh-produce"
#                       29 classes, including Avocado, Brown Eggs,
#                       White Eggs, organic eggs
#
# frenchbean_source2 -> Roboflow "indian-produce-v1"
#                       28 classes, including Bananas, apples,
#                       ginger, mushroom, raddish
#
# These are market produce photos, not plant / leaf photos, so they
# are NOT general training data.
#
# They are excluded from every class that already has real plant
# imagery, and used only for crops that would otherwise have zero
# images at all.
# ============================================================

PRODUCE_SOURCE_NAMES = {

    "frenchbean_source",

    "frenchbean_source2",
}

PRODUCE_FALLBACK_CLASSES = {

    "chilli",

    "okra",

    "mint",

    "spinach",
}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

random.seed(SEED)


# ============================================================
# SOURCE DATASETS
# ============================================================

SOURCES = [

    EXTERNAL / "PlantVillage_dataset",

    EXTERNAL / "PlantDoc_dataset",

    EXTERNAL / "plantwild_v2",

    EXTERNAL / "plantseg",

    EXTERNAL / "frenchbean_source",

    EXTERNAL / "frenchbean_source2",

    EXTERNAL / "Fruits Model.v1i.yolov11",

    EXTERNAL / "muskmelon_source",
]


# ============================================================
# ALIASES
# ============================================================

ALIASES = {

    "eggplant": "brinjal",

    "aubergine": "brinjal",

    "bell_pepper": "capsicum",

    "bell pepper": "capsicum",

    "bellpepper": "capsicum",

    "green_chilli": "chilli",

    "green chili": "chilli",

    "green_chili": "chilli",

    "hot_pepper": "chilli",

    "cantaloupe": "muskmelon",

    "lily": "lilium",
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = text.replace(
        "-",
        "_"
    )

    text = text.replace(
        " ",
        "_"
    )

    text = re.sub(
        r"_+",
        "_",
        text
    )

    return text.strip("_")


# ============================================================
# CROP DETECTION
# ============================================================

def detect_crop(path_text):

    text = normalize(
        path_text
    )

    # IMPORTANT:
    # Check watermelon before muskmelon/cantaloupe.
    if "watermelon" in text:

        return "watermelon"


    # Check aliases
    for alias, target in ALIASES.items():

        alias_norm = normalize(
            alias
        )

        if alias_norm in text:

            return target


    # Check target classes
    # Longest first to reduce partial matching issues.
    for target in sorted(
        TARGET_CLASSES,
        key=len,
        reverse=True
    ):

        target_norm = normalize(
            target
        )

        if target_norm in text:

            return target


    return None


# ============================================================
# CONDITION DETECTION
#
# CONDITION IS ONLY METADATA.
#
# Model 1 target:
#
# IMAGE -> CROP
#
# NOT:
#
# IMAGE -> HEALTHY/DISEASED
# ============================================================

def detect_condition(path_text):

    text = normalize(
        path_text
    )


    # --------------------------------------------------------
    # HEALTHY
    # --------------------------------------------------------

    if "healthy" in text:

        return "healthy"


    healthy_words = [
        "fresh",
        "normal",
    ]

    for word in healthy_words:

        if normalize(word) in text:

            return "healthy"


    # --------------------------------------------------------
    # DISEASED
    # --------------------------------------------------------

    disease_words = [

        "disease",
        "diseased",

        "blight",

        "spot",

        "rust",

        "mildew",

        "mosaic",

        "virus",

        "viral",

        "bacterial",

        "bacteria",

        "wilt",

        "rot",

        "scorch",

        "anthracnose",

        "canker",

        "mold",

        "mould",

        "leaf_mold",

        "septoria",

        "target_spot",

        "powdery",

        "downy",

        "phytophthora",

        "cercospora",

        "alternaria",

        "fusarium",

        "fire_blight",

        "gray_mold",

        "grey_mold",

        "yellow_leaf_curl",

        "black_rot",

        "mummy_berry",

        "frogeye",

        "leafroll",

        "ring_spot",

        "sheath_blight",

        "phomopsis",

        "end_rot",
    ]


    for word in disease_words:

        if normalize(word) in text:

            return "diseased"


    return "unknown"


# ============================================================
# FILE HASH
# ============================================================

def file_hash(path):

    h = hashlib.md5()

    try:

        with open(
            path,
            "rb"
        ) as f:

            while True:

                chunk = f.read(
                    1024 * 1024
                )

                if not chunk:

                    break

                h.update(
                    chunk
                )

        return h.hexdigest()


    except Exception:

        return None


# ============================================================
# PARSE YOLO YAML
# ============================================================

def parse_yolo_yaml(
    yaml_path
):

    """
    Supports:

    names:
      0: tomato
      1: cucumber

    OR:

    names: ['tomato', 'cucumber']
    """

    try:

        text = yaml_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except Exception:

        return {}


    names = {}

    lines = text.splitlines()

    inside_names = False


    for line in lines:

        stripped = line.strip()


        # ----------------------------------------------------
        # names:
        # ----------------------------------------------------

        if stripped.startswith(
            "names:"
        ):

            inside_names = True

            remainder = (
                stripped[
                    len("names:"):
                ].strip()
            )


            # Inline list
            if remainder.startswith(
                "["
            ):

                try:

                    parsed = ast.literal_eval(
                        remainder
                    )

                    if isinstance(
                        parsed,
                        list
                    ):

                        for i, name in enumerate(
                            parsed
                        ):

                            names[i] = str(
                                name
                            )

                        return names

                except Exception:

                    pass


            continue


        # ----------------------------------------------------
        # Content under names
        # ----------------------------------------------------

        if inside_names:

            # Example:
            # 0: tomato

            if (
                stripped
                and not stripped.startswith("-")
                and ":" in stripped
            ):

                key, value = (
                    stripped.split(
                        ":",
                        1
                    )
                )

                key = key.strip()


                if key.isdigit():

                    value = value.strip()

                    value = value.strip(
                        "'\""
                    )

                    names[
                        int(key)
                    ] = value

                    continue


                # Another YAML section
                break


            # Example:
            # - tomato
            if stripped.startswith(
                "-"
            ):

                value = stripped[
                    1:
                ].strip()

                value = value.strip(
                    "'\""
                )

                names[
                    len(names)
                ] = value


    return names


# ============================================================
# YOLO DATASET SCANNING
# ============================================================

def scan_yolo_dataset(
    source
):

    records = []


    yaml_files = list(
        source.rglob(
            "*.yaml"
        )
    )

    yaml_files += list(
        source.rglob(
            "*.yml"
        )
    )


    if not yaml_files:

        return records


    # ========================================================
    # FIND YOLO LABEL
    # ========================================================

    def find_label(
        image_path
    ):

        candidates = []


        # ----------------------------------------------
        # Same folder
        # ----------------------------------------------

        candidates.append(
            image_path.with_suffix(
                ".txt"
            )
        )


        # ----------------------------------------------
        # images -> labels
        # ----------------------------------------------

        parts = list(
            image_path.parts
        )

        for i, part in enumerate(
            parts
        ):

            if part.lower() == "images":

                new_parts = parts.copy()

                new_parts[i] = "labels"

                label_path = Path(
                    *new_parts
                ).with_suffix(
                    ".txt"
                )

                candidates.append(
                    label_path
                )


        for candidate in candidates:

            if candidate.exists():

                return candidate


        return None


    # ========================================================
    # PROCESS EACH YAML
    # ========================================================

    for yaml_path in yaml_files:

        names = parse_yolo_yaml(
            yaml_path
        )


        if not names:

            continue


        # ----------------------------------------------------
        # Map YOLO IDs to our crop classes
        # ----------------------------------------------------

        class_map = {}


        for class_id, class_name in names.items():

            crop = detect_crop(
                class_name
            )

            if crop is not None:

                class_map[
                    class_id
                ] = crop


        if not class_map:

            continue


        print()
        print(
            f"YOLO dataset: "
            f"{yaml_path}"
        )

        print(
            "YOLO classes found:"
        )


        for class_id, crop in class_map.items():

            print(
                f"  {class_id} -> {crop}"
            )


        # ----------------------------------------------------
        # Find images
        # ----------------------------------------------------

        image_files = [

            f

            for f in source.rglob("*")

            if (

                f.is_file()

                and f.suffix.lower()
                in IMAGE_EXTENSIONS

                and "annotations"
                not in [
                    p.lower()
                    for p in f.parts
                ]

            )
        ]


        dataset_records = 0


        # ----------------------------------------------------
        # Process images
        # ----------------------------------------------------

        for image_path in image_files:

            label_path = find_label(
                image_path
            )


            if label_path is None:

                continue


            try:

                lines = (
                    label_path.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).splitlines()
                )

            except Exception:

                continue


            class_ids = set()


            for line in lines:

                parts = (
                    line.strip().split()
                )


                if not parts:

                    continue


                try:

                    class_id = int(
                        parts[0]
                    )

                    class_ids.add(
                        class_id
                    )

                except Exception:

                    continue


            if not class_ids:

                continue


            # ------------------------------------------------
            # Convert YOLO IDs to crop names
            # ------------------------------------------------

            crops = {

                class_map[class_id]

                for class_id in class_ids

                if class_id in class_map

            }


            # ------------------------------------------------
            # Only use unambiguous images
            # ------------------------------------------------

            if len(crops) != 1:

                continue


            crop = next(
                iter(crops)
            )


            condition = detect_condition(
                str(image_path)
            )


            records.append({

                "path": image_path,

                "crop": crop,

                "condition": condition,

                "source": source.name,

            })


            dataset_records += 1


        print(
            f"  YOLO records added: "
            f"{dataset_records}"
        )


    return records


# ============================================================
# NORMAL DATASET SCANNING
# ============================================================

def scan_normal_dataset(
    source
):

    records = []


    files = [

        f

        for f in source.rglob("*")

        if (

            f.is_file()

            and f.suffix.lower()
            in IMAGE_EXTENSIONS

            and "annotations"
            not in [
                p.lower()
                for p in f.parts
            ]

        )
    ]


    print(
        f"  Images found: "
        f"{len(files)}"
    )


    for file in files:

        # ----------------------------------------------------
        # Only inspect the path INSIDE this dataset.
        #
        # Passing the absolute path meant the source folder name
        # leaked into the label. Every image stored under
        # ".../muskmelon_source/..." was labelled "muskmelon"
        # purely because of the folder it sat in.
        # ----------------------------------------------------

        try:

            inner_text = str(
                file.relative_to(source)
            )

        except ValueError:

            inner_text = file.name


        crop = detect_crop(
            inner_text
        )


        if crop is None:

            continue


        condition = detect_condition(
            inner_text
        )


        records.append({

            "path": file,

            "crop": crop,

            "condition": condition,

            "source": source.name,

        })


    return records


# ============================================================
# COLLECT DATA
# ============================================================

records = []


print()
print("=" * 80)
print(
    "BUILDING MODEL 1 - 39 CLASS DATASET"
)
print("=" * 80)


for source in SOURCES:


    if not source.exists():

        print(
            f"[SKIP] {source}"
        )

        continue


    print()
    print(
        f"Scanning: "
        f"{source.name}"
    )


    # --------------------------------------------------------
    # YOLO DATA
    # --------------------------------------------------------

    yolo_records = scan_yolo_dataset(
        source
    )


    if yolo_records:

        print(
            f"  YOLO records: "
            f"{len(yolo_records)}"
        )

        records.extend(
            yolo_records
        )


    # --------------------------------------------------------
    # Normal folder datasets
    # --------------------------------------------------------

    normal_records = scan_normal_dataset(
        source
    )


    records.extend(
        normal_records
    )


print()
print(
    f"Candidate records: "
    f"{len(records)}"
)


# ============================================================
# EXACT DUPLICATE REMOVAL
# ============================================================

print()
print("=" * 80)
print(
    "REMOVING EXACT DUPLICATES"
)
print("=" * 80)


size_groups = defaultdict(
    list
)


for record in records:

    try:

        size = record[
            "path"
        ].stat().st_size

        size_groups[
            size
        ].append(
            record
        )

    except Exception:

        pass


candidate_groups = [

    group

    for group in size_groups.values()

    if len(group) > 1

]


num_candidates = sum(
    len(group)
    for group in candidate_groups
)


print(
    f"Files requiring duplicate "
    f"check: {num_candidates}"
)


seen_hashes = set()

unique_records = []

duplicate_count = 0


for group in candidate_groups:

    for record in group:

        h = file_hash(
            record["path"]
        )


        if h is None:

            continue


        if h in seen_hashes:

            duplicate_count += 1

            continue


        seen_hashes.add(
            h
        )

        unique_records.append(
            record
        )


# Files with unique sizes
for size, group in size_groups.items():

    if len(group) == 1:

        unique_records.append(
            group[0]
        )


records = unique_records


print(
    f"Exact duplicates removed: "
    f"{duplicate_count}"
)

print(
    f"Unique images: "
    f"{len(records)}"
)


# ============================================================
# CONDITION REPORT
# ============================================================

print()
print("=" * 80)
print(
    "CONDITION DISTRIBUTION"
)
print("=" * 80)


condition_counts = Counter(

    r["condition"]

    for r in records

)


for condition, count in condition_counts.items():

    print(
        f"{condition:<12}: "
        f"{count}"
    )


# ============================================================
# GROUP BY CROP
# ============================================================

groups = defaultdict(
    list
)


for record in records:

    groups[
        record["crop"]
    ].append(
        record
    )


# ============================================================
# LIMIT EACH CLASS
# ============================================================

selected = []


produce_filtered = 0

source_capped = []


for crop in TARGET_CLASSES:

    items = list(
        groups.get(
            crop,
            []
        )
    )


    # --------------------------------------------------------
    # Drop grocery / market produce photos from normal classes
    #
    # They are only kept for crops that would otherwise be empty.
    # --------------------------------------------------------

    if crop not in PRODUCE_FALLBACK_CLASSES:

        kept = []

        for record in items:

            if (
                record["source"]
                in PRODUCE_SOURCE_NAMES
            ):

                produce_filtered += 1

                continue

            kept.append(
                record
            )

        items = kept


    # --------------------------------------------------------
    # Group by source dataset
    # --------------------------------------------------------

    by_source = defaultdict(
        list
    )

    for record in items:

        by_source[
            record["source"]
        ].append(
            record
        )


    # --------------------------------------------------------
    # Cap each source
    #
    # Only for classes that draw from more than one source.
    # A single-source class has nothing to balance, so all of its
    # images are kept.
    # --------------------------------------------------------

    multi_source = (
        len(by_source) > 1
    )

    items = []

    for source_name in sorted(
        by_source
    ):

        source_items = by_source[
            source_name
        ]

        random.shuffle(
            source_items
        )

        if multi_source:

            dropped = (

                len(source_items)
                - MAX_PER_SOURCE

            )

            if dropped > 0:

                source_capped.append(
                    (crop, source_name, dropped)
                )

            source_items = source_items[
                :MAX_PER_SOURCE
            ]

        items.extend(
            source_items
        )


    random.shuffle(
        items
    )


    items = items[
        :MAX_PER_CLASS
    ]


    selected.extend(
        items
    )


# ============================================================
# FILTERING REPORT
# ============================================================

print()
print("=" * 80)
print("SOURCE FILTERING")
print("=" * 80)


print(
    f"Grocery produce images removed: "
    f"{produce_filtered}"
)

print(
    "  (produce photos are kept only for: "
    + ", ".join(
        sorted(PRODUCE_FALLBACK_CLASSES)
    )
    + ")"
)


print()
print(
    f"Per-source cap: {MAX_PER_SOURCE} "
    f"(multi-source classes only)"
)


if source_capped:

    print()

    print(
        f"{'CLASS':<20}"
        f"{'SOURCE':<24}"
        f"{'DROPPED':>10}"
    )

    print("-" * 56)

    for crop, source_name, dropped in source_capped:

        print(
            f"{crop:<20}"
            f"{source_name:<24}"
            f"{dropped:>10}"
        )

else:

    print(
        "  (no source exceeded the cap)"
    )


# ============================================================
# AVAILABLE DATA REPORT
# ============================================================

print()
print("=" * 80)
print(
    "AVAILABLE DATA"
)
print("=" * 80)


print(
    f"{'CLASS':<20}"
    f"{'HEALTHY':>12}"
    f"{'DISEASED':>12}"
    f"{'UNKNOWN':>12}"
    f"{'TOTAL':>12}"
)


print(
    "-" * 72
)


selected_counts = Counter()


for record in selected:

    selected_counts[
        (
            record["crop"],
            record["condition"]
        )
    ] += 1


missing = []


for crop in TARGET_CLASSES:

    healthy = selected_counts[
        (
            crop,
            "healthy"
        )
    ]


    diseased = selected_counts[
        (
            crop,
            "diseased"
        )
    ]


    unknown = selected_counts[
        (
            crop,
            "unknown"
        )
    ]


    total = (
        healthy
        + diseased
        + unknown
    )


    print(
        f"{crop:<20}"
        f"{healthy:>12}"
        f"{diseased:>12}"
        f"{unknown:>12}"
        f"{total:>12}"
    )


    if total == 0:

        missing.append(
            crop
        )


# ============================================================
# MISSING CLASSES
# ============================================================

print()
print("=" * 80)
print(
    "MISSING CLASSES"
)
print("=" * 80)


if missing:

    for crop in missing:

        print(
            f"  {crop}"
        )

else:

    print(
        "NONE - all 39 classes available"
    )


# ============================================================
# AVAILABLE CLASSES
# ============================================================

AVAILABLE_CLASSES = [

    crop

    for crop in TARGET_CLASSES

    if any(
        r["crop"] == crop
        for r in selected
    )

]


print()
print("=" * 80)
print(
    "BUILDING DATASET"
)
print("=" * 80)


print(
    f"Available classes: "
    f"{len(AVAILABLE_CLASSES)}"
)


for crop in AVAILABLE_CLASSES:

    print(
        f"  {crop}"
    )


if missing:

    print()
    print(
        f"Skipping "
        f"{len(missing)} "
        f"missing classes:"
    )


    for crop in missing:

        print(
            f"  - {crop}"
        )


print()
print(
    "Proceeding with available classes."
)


# ============================================================
# CLEAN OLD OUTPUT
# ============================================================

if OUTPUT.exists():

    print()
    print(
        f"Removing old dataset: "
        f"{OUTPUT}"
    )

    shutil.rmtree(
        OUTPUT
    )


# ============================================================
# CREATE FOLDERS
# ============================================================

for split in [
    "train",
    "val",
    "test"
]:

    for crop in AVAILABLE_CLASSES:

        (
            OUTPUT
            / split
            / crop
        ).mkdir(
            parents=True,
            exist_ok=True
        )


# ============================================================
# TRAIN / VAL / TEST SPLIT
# ============================================================

print()
print("=" * 80)
print(
    "CREATING TRAIN / VAL / TEST"
)
print("=" * 80)


final_counts = Counter()


# ============================================================
# NEAR-DUPLICATE HELPERS
#
# dHash is used because it needs nothing beyond Pillow + numpy,
# which are already installed.
# ============================================================

_HASH_CACHE = {}


def dhash(path):

    """64-bit difference hash. Returns None if unreadable."""

    if path in _HASH_CACHE:

        return _HASH_CACHE[path]

    value = None

    try:

        image = Image.open(
            path
        ).convert(
            "L"
        ).resize(
            (9, 8)
        )

        pixels = np.asarray(
            image,
            dtype=np.int16
        )

        bits = (
            pixels[:, 1:]
            > pixels[:, :-1]
        )

        packed = np.packbits(
            bits.reshape(-1)
        )

        value = int.from_bytes(
            packed.tobytes(),
            "big"
        )

    except Exception:

        value = None

    _HASH_CACHE[path] = value

    return value


def cluster_records(records):

    """Group near-identical images with union-find.

    Images inside the same group are always placed in the same
    split, so the test set never contains a near-copy of a
    training image.
    """

    count = len(records)

    parent = list(
        range(count)
    )

    def find(index):

        while parent[index] != index:

            parent[index] = parent[
                parent[index]
            ]

            index = parent[index]

        return index

    def union(first, second):

        root_a = find(first)
        root_b = find(second)

        if root_a != root_b:

            parent[root_b] = root_a

    hashes = [
        dhash(r["path"])
        for r in records
    ]

    usable = [

        index

        for index, value in enumerate(hashes)

        if value is not None

    ]

    for position, index in enumerate(usable):

        for other in usable[position + 1:]:

            distance = (
                hashes[index]
                ^ hashes[other]
            ).bit_count()

            if distance <= NEAR_DUPLICATE_DISTANCE:

                union(index, other)

    clusters = defaultdict(
        list
    )

    for index in range(count):

        clusters[
            find(index)
        ].append(
            records[index]
        )

    return list(
        clusters.values()
    )


def split_quotas(count):

    """Target train/val/test sizes for a group of `count` images."""

    if count >= 7:

        n_train = max(
            1,
            int(count * TRAIN_RATIO)
        )

        n_val = max(
            1,
            int(count * VAL_RATIO)
        )

        n_test = (
            count
            - n_train
            - n_val
        )

        if n_test < 1:

            n_test = 1

            n_train -= 1

    elif count == 6:

        n_train, n_val, n_test = 4, 1, 1

    elif count == 5:

        n_train, n_val, n_test = 3, 1, 1

    elif count == 4:

        n_train, n_val, n_test = 2, 1, 1

    elif count == 3:

        n_train, n_val, n_test = 1, 1, 1

    elif count == 2:

        n_train, n_val, n_test = 1, 1, 0

    elif count == 1:

        n_train, n_val, n_test = 1, 0, 0

    else:

        n_train, n_val, n_test = 0, 0, 0

    return {

        "train": n_train,

        "val": n_val,

        "test": n_test,
    }


def allocate(clusters, quotas):

    """Place whole clusters into splits without splitting a group."""

    remaining = dict(
        quotas
    )

    result = {

        "train": [],

        "val": [],

        "test": [],
    }

    ordered = sorted(
        clusters,
        key=len,
        reverse=True
    )

    for cluster in ordered:

        fits = [

            name

            for name in [
                "val",
                "test",
                "train"
            ]

            if remaining[name] >= len(cluster)

        ]

        if not fits:

            # Group too big for any remaining quota.
            # Training is the safe home for it.

            result["train"].extend(
                cluster
            )

            remaining["train"] -= len(cluster)

            continue

        best = max(

            fits,

            key=lambda name: (

                remaining[name]
                / max(quotas[name], 1)

            )

        )

        result[best].extend(
            cluster
        )

        remaining[best] -= len(cluster)

    return result



for crop in AVAILABLE_CLASSES:

    items = [

        r

        for r in selected

        if r["crop"] == crop

    ]


    random.shuffle(
        items
    )


    # ========================================================
    # SPLIT PER SOURCE DATASET
    #
    # Every source contributes to train, val AND test in the same
    # ratio. This keeps val/test representative of the real mix
    # instead of being dominated by whichever source is largest.
    #
    # Inside each source, near-identical images are grouped and the
    # whole group is placed in ONE split, so a test image is never
    # a near-copy of a training image.
    # ========================================================

    by_source = defaultdict(
        list
    )

    for record in items:

        by_source[
            record["source"]
        ].append(
            record
        )


    splits = {

        "train": [],

        "val": [],

        "test": [],
    }


    for source_name in sorted(
        by_source
    ):

        group = by_source[
            source_name
        ]

        clusters = cluster_records(
            group
        )

        allocated = allocate(
            clusters,
            split_quotas(len(group))
        )


        for split_name in splits:

            splits[
                split_name
            ].extend(
                allocated[split_name]
            )


    # ========================================================
    # COPY FILES
    # ========================================================

    for split, split_items in splits.items():

        for index, record in enumerate(
            split_items
        ):

            src = record[
                "path"
            ]


            condition = record[
                "condition"
            ]


            dst_name = (

                f"{record['source']}_"

                f"{condition}_"

                f"{index:06d}_"

                f"{src.name}"

            )


            dst = (

                OUTPUT

                / split

                / crop

                / dst_name

            )


            try:

                shutil.copy2(
                    src,
                    dst
                )


                final_counts[
                    (
                        split,
                        crop
                    )
                ] += 1


            except Exception as e:

                print(
                    f"[COPY ERROR] "
                    f"{src}: {e}"
                )


# ============================================================
# FINAL REPORT
# ============================================================

print()
print("=" * 80)
print(
    "FINAL MODEL 1 DATASET"
)
print("=" * 80)


grand_total = 0


for split in [
    "train",
    "val",
    "test"
]:

    total = sum(

        final_counts[
            (
                split,
                crop
            )
        ]

        for crop in AVAILABLE_CLASSES

    )


    grand_total += total


    print(
        f"{split.upper():<10}: "
        f"{total}"
    )


print(
    f"{'TOTAL':<10}: "
    f"{grand_total}"
)


# ============================================================
# PER-CLASS SPLIT REPORT
# ============================================================

print()
print(
    "PER-CLASS SPLIT:"
)


print(
    f"{'CLASS':<20}"
    f"{'TRAIN':>10}"
    f"{'VAL':>10}"
    f"{'TEST':>10}"
)


print(
    "-" * 50
)


for crop in AVAILABLE_CLASSES:

    train_count = final_counts[
        (
            "train",
            crop
        )
    ]

    val_count = final_counts[
        (
            "val",
            crop
        )
    ]

    test_count = final_counts[
        (
            "test",
            crop
        )
    ]


    print(
        f"{crop:<20}"
        f"{train_count:>10}"
        f"{val_count:>10}"
        f"{test_count:>10}"
    )


# ============================================================
# OUTPUT
# ============================================================

print()
print(
    "Dataset created at:"
)

print(
    OUTPUT
)


print()
print("=" * 80)
print(
    "DONE"
)
print("=" * 80)
