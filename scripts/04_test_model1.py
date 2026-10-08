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


# ============================================================
# DEVICE
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("=" * 60)
print("MODEL 1 - IMAGE TEST")
print("=" * 60)

print(
    "Device:",
    DEVICE
)

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
# GET IMAGE PATH
# ============================================================

if len(sys.argv) < 2:

    print()
    print(
        "Usage:"
    )

    print(
        "python scripts\\04_test_model1.py "
        "\"path\\to\\image.jpg\""
    )

    sys.exit(1)


image_path = Path(
    sys.argv[1]
)


if not image_path.exists():

    print()
    print(
        "ERROR: Image not found:"
    )

    print(
        image_path
    )

    sys.exit(1)


# ============================================================
# LOAD IMAGE
# ============================================================

try:

    image = Image.open(
        image_path
    ).convert(
        "RGB"
    )

except Exception as e:

    print(
        "ERROR loading image:",
        e
    )

    sys.exit(1)


# ============================================================
# PREDICTION
# ============================================================

input_tensor = transform(
    image
).unsqueeze(
    0
).to(
    DEVICE
)


with torch.no_grad():

    outputs = model(
        input_tensor
    )

    probabilities = torch.softmax(
        outputs,
        dim=1
    )[0]


# ============================================================
# TOP 5
# ============================================================

top_k = min(
    5,
    num_classes
)

top_probs, top_indices = torch.topk(
    probabilities,
    top_k
)


# ============================================================
# RESULTS
# ============================================================

print()
print("=" * 60)
print("PREDICTION")
print("=" * 60)

print()
print(
    "Image:",
    image_path
)

print()

for rank, (
    probability,
    index
) in enumerate(
    zip(
        top_probs,
        top_indices
    ),
    start=1
):

    crop = class_names[
        index.item()
    ]

    confidence = (
        probability.item()
        * 100
    )

    print(
        f"{rank}. "
        f"{crop:<20}"
        f"{confidence:6.2f}%"
    )


print()
print("=" * 60)

predicted_class = class_names[
    top_indices[0].item()
]

predicted_confidence = (
    top_probs[0].item()
    * 100
)

print(
    f"FINAL PREDICTION: "
    f"{predicted_class}"
)

print(
    f"CONFIDENCE: "
    f"{predicted_confidence:.2f}%"
)

print("=" * 60)