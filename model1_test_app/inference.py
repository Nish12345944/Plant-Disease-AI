"""Model 1 Inference Engine.

Loads the trained EfficientNet-B2 checkpoint, dynamically resolves class mapping,
applies the exact training-time preprocessing transforms, and performs Top-K
plant/crop classification inference.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional, Union

import cv2
import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b2

logger = logging.getLogger(__name__)

# Default model artifacts
DEFAULT_CHECKPOINT_PATH = Path("models/model1/best_model.pth")
DEFAULT_MAPPING_PATH = Path("models/model1/class_mapping.json")
DEFAULT_CONFIG_PATH = Path("models/model1/config.json")

# Exact ImageNet normalization parameters used in training
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]
DEFAULT_IMAGE_SIZE = (224, 224)
DEFAULT_CONFIDENCE_THRESHOLD = 0.25


def get_eval_transform(
    image_size: tuple[int, int] = DEFAULT_IMAGE_SIZE,
    mean: list[float] = IMAGENET_MEAN,
    std: list[float] = IMAGENET_STD,
) -> transforms.Compose:
    """Exact preprocessing transform used during Model 1 validation and testing.

    Args:
        image_size: Target (height, width) tuple (default: 224, 224).
        mean: Normalization channel means.
        std: Normalization channel standard deviations.

    Returns:
        torchvision.transforms.Compose pipeline.
    """
    return transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std),
    ])


def load_model(
    checkpoint_path: Union[str, Path] = DEFAULT_CHECKPOINT_PATH,
    mapping_path: Union[str, Path] = DEFAULT_MAPPING_PATH,
    config_path: Optional[Union[str, Path]] = DEFAULT_CONFIG_PATH,
    device: Optional[torch.device] = None,
) -> tuple[nn.Module, dict[int, str], dict[str, int], torch.device, str]:
    """Load EfficientNet-B2 checkpoint and dynamic class mapping.

    Args:
        checkpoint_path: Path to best_model.pth.
        mapping_path: Path to class_mapping.json.
        config_path: Path to config.json (optional).
        device: Target torch.device. If None, auto-selects CUDA if available, else CPU.

    Returns:
        Tuple of (model, idx_to_class, class_to_idx, device, device_name).
    """
    chk_path = Path(checkpoint_path).resolve()
    map_path = Path(mapping_path).resolve()

    if not chk_path.exists():
        raise FileNotFoundError(f"Model 1 checkpoint not found at: {chk_path}")
    if not map_path.exists():
        raise FileNotFoundError(f"Class mapping file not found at: {map_path}")

    # Determine device
    if device is None:
        if torch.cuda.is_available():
            device = torch.device("cuda")
            device_name = f"CUDA — {torch.cuda.get_device_name(0)}"
        else:
            device = torch.device("cpu")
            device_name = "CPU"
    else:
        device_name = str(device).upper()

    # Load dynamic class mapping
    with open(map_path, "r", encoding="utf-8") as f:
        mapping_data = json.load(f)

    # Handle string vs integer keys in idx_to_class
    idx_to_class: dict[int, str] = {
        int(k): v for k, v in mapping_data.get("idx_to_class", {}).items()
    }
    class_to_idx: dict[str, int] = mapping_data.get("class_to_idx", {})
    num_classes = len(idx_to_class)

    if num_classes == 0:
        raise ValueError(f"No classes found in class mapping file: {map_path}")

    # Initialize EfficientNet-B2 architecture
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)

    # Load weights
    checkpoint = torch.load(chk_path, map_location=device, weights_only=False)

    if "model_state_dict" in checkpoint:
        model.load_state_dict(checkpoint["model_state_dict"])
    else:
        model.load_state_dict(checkpoint)

    model = model.to(device)
    model.eval()

    logger.info(
        f"Model 1 loaded successfully on {device_name} with {num_classes} classes."
    )
    return model, idx_to_class, class_to_idx, device, device_name


def format_class_name(raw_name: str) -> str:
    """Format raw class identifiers like 'cherry_tomato' to 'Cherry Tomato'."""
    return raw_name.replace("_", " ").title()


def predict_image(
    image_input: Union[str, Path, Image.Image, np.ndarray, bytes],
    model: nn.Module,
    idx_to_class: dict[int, str],
    device: torch.device,
    top_k: int = 5,
    transform: Optional[transforms.Compose] = None,
    validate_plant: bool = True,
    min_confidence: float = DEFAULT_CONFIDENCE_THRESHOLD,
    min_blur_score: float = 6.0,
) -> dict[str, Any]:
    """Perform plant/crop classification on a standalone uploaded image.

    Pipeline:
        1. Load & validate basic dimensions/format.
        2. Non-destructive corruption/blur check (only reject severely corrupted or completely ruined frames).
        3. Model 1 preprocessing & neural inference.
        4. Probability distribution & confidence check.
    """
    if transform is None:
        transform = get_eval_transform()

    # Load and normalize PIL image
    if isinstance(image_input, (str, Path)):
        img = Image.open(str(image_input))
    elif isinstance(image_input, bytes):
        import io
        img = Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, np.ndarray):
        if image_input.ndim == 3 and image_input.shape[2] == 3:
            img = Image.fromarray(image_input)
        elif image_input.ndim == 2:
            img = Image.fromarray(image_input).convert("RGB")
        else:
            raise ValueError(f"Unsupported image array shape: {image_input.shape}")
    elif isinstance(image_input, Image.Image):
        img = image_input
    else:
        raise TypeError(f"Unsupported image input type: {type(image_input)}")

    # Ensure 3-channel RGB
    if getattr(img, "is_animated", False):
        img.seek(0)
    img_rgb = img.convert("RGB")

    w, h = img_rgb.size
    if w == 0 or h == 0:
        return {
            "predicted_class": "unknown",
            "predicted_label": "Unknown",
            "status": "unknown",
            "confidence": 0.0,
            "percentage": "N/A",
            "reason": "Zero-size or empty image file",
            "top_k": [],
            "image_size": (w, h),
        }

    # Basic non-destructive blur check
    np_rgb = np.array(img_rgb)
    gray = cv2.cvtColor(np_rgb, cv2.COLOR_RGB2GRAY)
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    if validate_plant and blur_score < min_blur_score:
        return {
            "predicted_class": "blurry",
            "predicted_label": "Blurry",
            "status": "blurry",
            "confidence": 0.0,
            "percentage": "N/A",
            "reason": f"Severely blurry image (sharpness {blur_score:.1f} < {min_blur_score})",
            "top_k": [],
            "image_size": (w, h),
        }

    # Direct Model 1 Preprocessing & Inference
    tensor = transform(img_rgb).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    num_classes = len(idx_to_class)
    k = min(top_k, num_classes)
    top_indices = np.argsort(probs)[::-1][:k]

    top_k_list = []
    for rank, idx in enumerate(top_indices, start=1):
        raw_cls = idx_to_class[int(idx)]
        confidence = float(probs[idx])
        top_k_list.append({
            "rank": rank,
            "class_id": int(idx),
            "class_name": raw_cls,
            "label": format_class_name(raw_cls),
            "confidence": confidence,
            "percentage": f"{confidence * 100:.2f}%",
        })

    top_pred = top_k_list[0]

    # Rejection of completely out-of-distribution / ambiguous inputs
    if validate_plant and top_pred["confidence"] < min_confidence:
        return {
            "predicted_class": "unknown",
            "predicted_label": "Unknown",
            "status": "unknown",
            "confidence": top_pred["confidence"],
            "percentage": f"{top_pred['confidence'] * 100:.2f}% (Low Confidence)",
            "reason": f"Low identification confidence ({top_pred['confidence'] * 100:.1f}% < {min_confidence * 100:.0f}%)",
            "top_k": top_k_list,
            "all_probabilities": probs,
            "image_size": (w, h),
        }

    return {
        "predicted_class": top_pred["class_name"],
        "predicted_label": top_pred["label"],
        "status": "valid",
        "confidence": top_pred["confidence"],
        "percentage": top_pred["percentage"],
        "reason": "Plant successfully identified",
        "top_k": top_k_list,
        "all_probabilities": probs,
        "image_size": (w, h),
    }
