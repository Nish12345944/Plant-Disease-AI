from pathlib import Path
import sys

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
)

MODEL_PATH = (
    ROOT
    / "models"
    / "model1_efficientnet_b2.pth"
)

DATASET_DIR = (
    ROOT
    / "data"
    / "final"
    / "model1_39"
)

# Usage:
#   python scripts\06_eval_model1_per_class.py            (test split)
#   python scripts\06_eval_model1_per_class.py train
#   python scripts\06_eval_model1_per_class.py val

SPLIT = (
    sys.argv[1].lower()
    if len(sys.argv) > 1
    else "test"
)

if SPLIT not in {
    "train",
    "val",
    "test",
}:

    print(
        "ERROR: split must be one of: "
        "train, val, test"
    )

    sys.exit(1)

TEST_DIR = DATASET_DIR / SPLIT

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
}

BATCH_SIZE = 16


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("=" * 68)
print(f"MODEL 1 - PER-CLASS {SPLIT.upper()} EVALUATION")
print("=" * 68)

print("Device:", DEVICE)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================================
# LOAD CHECKPOINT
# ============================================================

print()
print("Loading model...")

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

class_names = checkpoint[
    "class_names"
]

num_classes = len(
    class_names
)

print(
    "Number of classes:",
    num_classes
)

print(
    "Classes:",
    class_names
)


# ============================================================
# MODEL
# ============================================================

model = models.efficientnet_b2(
    weights=None
)

in_features = (
    model.classifier[1].in_features
)

model.classifier[1] = nn.Linear(
    in_features,
    num_classes
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(
    DEVICE
)

model.eval()


# ============================================================
# TRANSFORM
# ============================================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(

        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]

    )

])


# ============================================================
# EVALUATE
# ============================================================

if not TEST_DIR.exists():

    raise FileNotFoundError(
        f"Test directory not found:\n"
        f"{TEST_DIR}"
    )


correct = {
    crop: 0
    for crop in class_names
}

total = {
    crop: 0
    for crop in class_names
}

confidences = {
    crop: []
    for crop in class_names
}


for true_class in class_names:

    folder = TEST_DIR / true_class

    if not folder.exists():

        continue

    paths = sorted(

        path

        for path in folder.iterdir()

        if path.is_file()

        and path.suffix.lower() in IMAGE_EXTENSIONS

    )

    for start in range(
        0,
        len(paths),
        BATCH_SIZE
    ):

        chunk = paths[
            start:start + BATCH_SIZE
        ]

        tensors = []

        for path in chunk:

            try:

                image = Image.open(
                    path
                ).convert(
                    "RGB"
                )

            except Exception as e:

                print(
                    f"[SKIP] {path}: {e}"
                )

                continue

            tensors.append(
                transform(image)
            )

        if not tensors:

            continue

        batch = torch.stack(
            tensors
        ).to(
            DEVICE
        )

        with torch.no_grad():

            outputs = model(
                batch
            )

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

        top_probs, top_indices = torch.topk(
            probabilities,
            1,
            dim=1
        )

        for index in range(
            len(tensors)
        ):

            predicted = class_names[
                top_indices[index][0].item()
            ]

            confidence = float(
                top_probs[index][0].item()
            )

            total[true_class] += 1

            confidences[
                true_class
            ].append(
                confidence
            )

            if predicted == true_class:

                correct[true_class] += 1


# ============================================================
# REPORT
# ============================================================

print()
print("=" * 68)

print(
    f"{'CLASS':<15}"
    f"{'TEST':>6}"
    f"{'CORRECT':>9}"
    f"{'ACC %':>9}"
    f"{'MEAN CONF %':>13}"
)

print("-" * 68)


overall_correct = 0
overall_total = 0

strong = []
weak = []
tiny = []


for crop in class_names:

    if total[crop] == 0:

        print(
            f"{crop:<15}"
            f"{0:>6}"
            f"{0:>9}"
            f"{'n/a':>9}"
            f"{'n/a':>13}"
        )

        continue

    accuracy = (
        correct[crop]
        / total[crop]
        * 100
    )

    mean_confidence = (

        sum(
            confidences[crop]
        )
        / len(confidences[crop])
        * 100

    )

    overall_correct += correct[crop]

    overall_total += total[crop]

    print(
        f"{crop:<15}"
        f"{total[crop]:>6}"
        f"{correct[crop]:>9}"
        f"{accuracy:>8.1f}%"
        f"{mean_confidence:>12.1f}%"
    )

    if total[crop] <= 2:

        tiny.append(
            (crop, accuracy, total[crop])
        )

    elif accuracy >= 95:

        strong.append(
            (crop, accuracy, total[crop])
        )

    elif accuracy < 80:

        weak.append(
            (crop, accuracy, total[crop])
        )


print("-" * 68)

print(
    f"{'OVERALL':<15}"
    f"{overall_total:>6}"
    f"{overall_correct:>9}"
    f"{overall_correct / overall_total * 100:>8.1f}%"
)

print("=" * 68)


# ============================================================
# SUMMARY GROUPS
# ============================================================

print()
print("STRONG CLASSES (>=95% test accuracy, >2 test images):")

if not strong:

    print("  none")

for crop, accuracy, count in sorted(
    strong,
    key=lambda item: -item[1]
):

    print(
        f"  {crop:<15}"
        f"{accuracy:>6.1f}%"
        f"   (n={count})"
    )


print()
print("WEAK CLASSES (<80% test accuracy, >2 test images):")

if not weak:

    print("  none")

for crop, accuracy, count in sorted(
    weak,
    key=lambda item: item[1]
):

    print(
        f"  {crop:<15}"
        f"{accuracy:>6.1f}%"
        f"   (n={count})"
    )


print()
print("TINY CLASSES (<=2 test images - metrics unreliable):")

if not tiny:

    print("  none")

for crop, accuracy, count in tiny:

    print(
        f"  {crop:<15}"
        f"{accuracy:>6.1f}%"
        f"   (n={count})"
    )


print()
print("=" * 68)
