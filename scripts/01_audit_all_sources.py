from pathlib import Path
from collections import Counter
import re

# ============================================================
# PROJECT PATH
# ============================================================

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")

# ============================================================
# DATASET PATHS
# ============================================================

PLANTWILD = ROOT / "data" / "external" / "PlantWild_v2" / "plantwild_v2"

PLANTSEG = ROOT / "data" / "external" / "plantseg" / "plantseg"

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
# ALIASES
# ============================================================

ALIASES = {
    "eggplant": "brinjal",
    "aubergine": "brinjal",

    "bell_pepper": "capsicum",
    "bell pepper": "capsicum",

    "green_chilli": "chilli",
    "green chili": "chilli",
    "hot_pepper": "chilli",

    "cantaloupe": "muskmelon",

    "lily": "lilium",
}


# ============================================================
# IMAGE EXTENSIONS
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


# ============================================================
# HELPERS
# ============================================================

def count_images(folder):
    if not folder.exists():
        return 0

    return sum(
        1
        for f in folder.rglob("*")
        if f.is_file()
        and f.suffix.lower() in IMAGE_EXTENSIONS
    )


def normalize(text):
    text = text.lower().strip()
    text = text.replace("-", "_")
    text = re.sub(r"\s+", "_", text)
    return text


def print_header(title):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


# ============================================================
# PLANTWILD
# ============================================================

def audit_plantwild():

    counts = Counter()
    diseases = {crop: Counter() for crop in TARGET_CLASSES}

    if not PLANTWILD.exists():
        print("\nPlantWild NOT FOUND:")
        print(PLANTWILD)
        return counts, diseases

    for folder in PLANTWILD.iterdir():

        if not folder.is_dir():
            continue

        folder_name = folder.name.lower()

        crop = None

        # Explicit aliases first
        if folder_name.startswith("eggplant "):
            crop = "brinjal"

        elif folder_name.startswith("bell pepper "):
            crop = "capsicum"

        elif folder_name.startswith("cantaloupe "):
            crop = "muskmelon"

        else:

            # Exact target prefixes
            for target in TARGET_CLASSES:

                pretty = target.replace("_", " ")

                if folder_name.startswith(pretty + " "):
                    crop = target
                    break

        if crop is None:
            continue

        n = count_images(folder)

        counts[crop] += n

        # Everything after crop name = disease
        prefix = crop.replace("_", " ")

        if crop == "brinjal":
            prefix = "eggplant"

        elif crop == "capsicum":
            prefix = "bell pepper"

        elif crop == "muskmelon":
            prefix = "cantaloupe"

        if folder_name.startswith(prefix + " "):
            disease = folder_name[len(prefix) + 1:]
        else:
            disease = folder_name

        diseases[crop][disease] += n

    return counts, diseases


# ============================================================
# PLANTSEG
# ============================================================

PLANTSEG_PREFIXES = {
    "basil": "basil",
    "bell_pepper": "capsicum",
    "blueberry": "blueberry",
    "broccoli": "broccoli",
    "cabbage": "cabbage",
    "cauliflower": "cauliflower",
    "celery": "celery",
    "cucumber": "cucumber",
    "eggplant": "brinjal",
    "lettuce": "lettuce",
    "raspberry": "raspberry",
    "strawberry": "strawberry",
    "tomato": "tomato",
    "zucchini": "zucchini",
}


def plantseg_crop(filename):

    name = filename.lower()

    for prefix, crop in sorted(
        PLANTSEG_PREFIXES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):

        if name.startswith(prefix + "_"):
            return crop

    return None


def audit_plantseg():

    counts = Counter()
    diseases = {crop: Counter() for crop in TARGET_CLASSES}

    if not PLANTSEG.exists():
        print("\nPlantSeg NOT FOUND:")
        print(PLANTSEG)
        return counts, diseases

    for split in ["train", "val", "test"]:

        image_dir = PLANTSEG / "images" / split

        if not image_dir.exists():
            continue

        for file in image_dir.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue

            crop = plantseg_crop(file.name)

            if crop is None:
                continue

            counts[crop] += 1

            filename = file.stem.lower()

            prefix = None

            for p in sorted(
                PLANTSEG_PREFIXES,
                key=len,
                reverse=True
            ):

                if filename.startswith(p + "_"):
                    prefix = p
                    break

            if prefix:
                disease = filename[len(prefix) + 1:]
                diseases[crop][disease] += 1

    return counts, diseases


# ============================================================
# RUN AUDITS
# ============================================================

print_header("39-CLASS MODEL 1 SOURCE AUDIT")

print("\nTarget classes:", len(TARGET_CLASSES))

plantwild_counts, plantwild_diseases = audit_plantwild()

plantseg_counts, plantseg_diseases = audit_plantseg()


# ============================================================
# SUMMARY TABLE
# ============================================================

print_header("DISEASED IMAGE COUNTS")

print(
    f"{'Crop':<20}"
    f"{'PlantWild':>12}"
    f"{'PlantSeg':>12}"
    f"{'Combined':>12}"
)

print("-" * 56)

for crop in TARGET_CLASSES:

    pw = plantwild_counts[crop]
    ps = plantseg_counts[crop]

    print(
        f"{crop:<20}"
        f"{pw:>12}"
        f"{ps:>12}"
        f"{pw + ps:>12}"
    )


# ============================================================
# DISEASE DIVERSITY
# ============================================================

print_header("DISEASE DIVERSITY")

for crop in TARGET_CLASSES:

    diseases = set(plantwild_diseases[crop]) | set(
        plantseg_diseases[crop]
    )

    if not diseases:
        continue

    print(f"\n{crop}")
    print("-" * len(crop))

    for disease in sorted(diseases):

        pw = plantwild_diseases[crop][disease]
        ps = plantseg_diseases[crop][disease]

        print(
            f"  {disease:<55} "
            f"PW={pw:<5} "
            f"PS={ps:<5} "
            f"TOTAL={pw + ps}"
        )


# ============================================================
# MISSING DISEASE SOURCES
# ============================================================

print_header("39-CLASS DISEASE COVERAGE")

print(
    f"{'Crop':<20}"
    f"{'Diseased Images':>18}"
    f"{'Status':>15}"
)

print("-" * 55)

for crop in TARGET_CLASSES:

    total = (
        plantwild_counts[crop]
        + plantseg_counts[crop]
    )

    if total == 0:
        status = "MISSING"
    elif total < 100:
        status = "LOW"
    elif total < 300:
        status = "LIMITED"
    else:
        status = "AVAILABLE"

    print(
        f"{crop:<20}"
        f"{total:>18}"
        f"{status:>15}"
    )


# ============================================================
# FINAL
# ============================================================

print()
print("=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)

print("""
IMPORTANT:
These numbers represent DISEASED images from PlantWild + PlantSeg.

They are NOT the final Model 1 dataset.

Next we will add:
    PlantVillage
    PlantDoc
    Existing healthy/crop datasets

Then we will calculate:

    Crop
    Healthy
    Diseased
    Total
    Disease diversity
    Number of sources

Only after that will we build the final 39-class Model 1 dataset.
""")