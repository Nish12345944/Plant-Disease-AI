from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms
import gradio as gr


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
print("MODEL 1 - UPLOAD TEST")
print("=" * 60)

print("Device:", DEVICE)

if torch.cuda.is_available():

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================================
# LOAD MODEL
# ============================================================

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
# PREDICTION FUNCTION
# ============================================================

def predict(image):

    if image is None:

        return "Please upload an image.", {}


    image = image.convert(
        "RGB"
    )


    tensor = transform(
        image
    ).unsqueeze(
        0
    ).to(
        DEVICE
    )


    with torch.no_grad():

        output = model(
            tensor
        )

        probabilities = torch.softmax(
            output,
            dim=1
        )[0]


    # Top 5
    top_probs, top_indices = torch.topk(
        probabilities,
        min(5, num_classes)
    )


    results = {}

    for probability, index in zip(
        top_probs,
        top_indices
    ):

        crop = class_names[
            index.item()
        ]

        results[crop] = float(
            probability.item()
        )


    predicted = class_names[
        top_indices[0].item()
    ]

    confidence = (
        top_probs[0].item()
        * 100
    )


    result_text = (
        f"Predicted Crop: {predicted}\n"
        f"Confidence: {confidence:.2f}%"
    )


    return result_text, results


# ============================================================
# GRADIO UI
# ============================================================

demo = gr.Interface(

    fn=predict,

    inputs=gr.Image(
        type="pil",
        label="Upload Plant Image"
    ),

    outputs=[

        gr.Textbox(
            label="Prediction"
        ),

        gr.Label(
            num_top_classes=5,
            label="Top 5 Predictions"
        )

    ],

    title="Plant Crop Identification - Model 1",

    description=(
        "Upload a plant image. "
        "EfficientNet-B2 will identify the crop."
    )

)


# ============================================================
# START
# ============================================================

demo.launch()