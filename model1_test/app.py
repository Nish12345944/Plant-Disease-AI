"""Model 1 - Plant/Crop Classifier (Local Streamlit Testing Interface).

Loads trained EfficientNet-B2 checkpoint from models/model1/best_model.pth,
runs offline inference with CUDA/CPU auto-detection, and displays Top-1 & Top-3
predictions with confidence percentages.
"""

import json
from pathlib import Path

import streamlit as st
import torch
import torch.nn as nn
from PIL import Image, UnidentifiedImageError
from torchvision import transforms
from torchvision.models import efficientnet_b2

# Setup Paths relative to project root
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent
MODELS_DIR = PROJECT_ROOT / "models" / "model1"

CHECKPOINT_PATH = MODELS_DIR / "best_model.pth"
CLASS_MAPPING_PATH = MODELS_DIR / "class_mapping.json"
CONFIG_PATH = MODELS_DIR / "config.json"

st.set_page_config(
    page_title="Model 1 - Plant/Crop Classifier",
    page_icon="🌿",
    layout="centered",
)

def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

@st.cache_resource(show_spinner=False)
def load_classifier():
    """Loads and caches the model, class mapping, and configuration."""
    if not CHECKPOINT_PATH.exists():
        raise FileNotFoundError(f"Checkpoint not found at: {CHECKPOINT_PATH}")
    if not CLASS_MAPPING_PATH.exists():
        raise FileNotFoundError(f"Class mapping not found at: {CLASS_MAPPING_PATH}")
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found at: {CONFIG_PATH}")

    # Load mappings
    with open(CLASS_MAPPING_PATH, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)
    idx_to_class = {int(k): v for k, v in mapping_data["idx_to_class"].items()}
    num_classes = len(idx_to_class)

    # Load config
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    device = get_device()

    # Reconstruct exact EfficientNet-B2 architecture
    model = efficientnet_b2()
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)

    # Load weights
    checkpoint = torch.load(CHECKPOINT_PATH, map_location=device, weights_only=False)
    if "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model = model.to(device)
    model.eval()

    # Exact preprocessing transform used during evaluation
    img_size = config.get("image_size", [224, 224])[0]
    norm_mean = config.get("normalization", {}).get("mean", [0.485, 0.456, 0.406])
    norm_std = config.get("normalization", {}).get("std", [0.229, 0.224, 0.225])

    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=norm_mean, std=norm_std),
    ])

    return model, idx_to_class, config, transform, device

def main():
    st.title("🌿 Model 1 - Plant/Crop Classifier")
    st.caption("Local offline test interface for 22-class EfficientNet-B2 classifier.")

    # Device indicator badge
    current_device = get_device()
    device_str = "CUDA (GPU Acceleration)" if current_device.type == "cuda" else "CPU"
    st.info(f"**Inference Device:** `{device_str}`")

    # Load model resources
    try:
        model, idx_to_class, config, transform, device = load_classifier()
    except Exception as e:
        st.error(f"❌ Failed to load Model 1 resources: {e}")
        st.stop()

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image file to classify...",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
        help="Upload a leaf, flower, fruit, or plant stem photo."
    )

    if uploaded_file is not None:
        try:
            # Validate and open image
            image = Image.open(uploaded_file)
            image_rgb = image.convert("RGB")
        except UnidentifiedImageError:
            st.error("❌ The uploaded file is corrupted or not a valid image.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error reading image: {e}")
            st.stop()

        # Display image preview
        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Image Preview")
            st.image(image_rgb, caption=f"{uploaded_file.name} ({image.size[0]}x{image.size[1]})", use_container_width=True)

        with col2:
            st.subheader("Inference")
            st.write("Click below to run classification:")
            predict_clicked = st.button("🔍 Predict", type="primary", use_container_width=True)

            if predict_clicked:
                with st.spinner("Analyzing plant/crop image..."):
                    try:
                        # Preprocess image
                        tensor = transform(image_rgb).unsqueeze(0).to(device)

                        # Inference
                        with torch.no_grad():
                            with torch.amp.autocast(device_type="cuda" if device.type == "cuda" else "cpu"):
                                outputs = model(tensor)
                                probs = torch.softmax(outputs, dim=1)[0]

                        # Top predictions
                        top_probs, top_indices = torch.topk(probs, k=min(3, len(idx_to_class)))

                        top1_class = idx_to_class[top_indices[0].item()]
                        top1_conf = top_probs[0].item() * 100.0

                        # Results presentation
                        st.success("### Classification Results")
                        st.markdown(f"**Predicted Plant/Crop:** `{top1_class}`")
                        st.markdown(f"**Confidence:** `{top1_conf:.2f}%`")

                        st.markdown("---")
                        st.markdown("#### Top-3 Predictions:")
                        for rank, (p, idx) in enumerate(zip(top_probs, top_indices), 1):
                            c_name = idx_to_class[idx.item()]
                            c_conf = p.item() * 100.0
                            st.write(f"**{rank}.** `{c_name}` — **{c_conf:.2f}%**")

                        # Progress bar for top-1
                        st.progress(min(1.0, top1_conf / 100.0))

                    except Exception as e:
                        st.error(f"❌ Inference error occurred: {e}")

if __name__ == "__main__":
    main()
