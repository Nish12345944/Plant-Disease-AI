"""
Inference script and reusable API for Model 2 (Plant Disease Detection & Localization).
Usage:
    .\\venv\\Scripts\\python.exe model2/test_model2.py <image_path> [--conf 0.25] [--nms 0.65] [--save_annotated path]
"""

import os
import sys
import json
import argparse
import numpy as np
import cv2
import torch
from yolox.exp import Exp
from yolox.utils import postprocess
from yolox.data.data_augment import ValTransform

# Default paths
DEFAULT_MODEL_PATH = "models/model2/best_model.pth"
DEFAULT_CLASS_MAPPING_PATH = "data/processed/model2_dataset/class_mapping.json"

# Cached global model and class mapping
_GLOBAL_MODEL = None
_GLOBAL_CLASS_MAPPING = None
_GLOBAL_DEVICE = None

def get_class_mapping(mapping_path=DEFAULT_CLASS_MAPPING_PATH):
    global _GLOBAL_CLASS_MAPPING
    if _GLOBAL_CLASS_MAPPING is None:
        if not os.path.exists(mapping_path):
            mapping_path = "models/model2/class_mapping.json"
        with open(mapping_path, "r", encoding="utf-8") as f:
            raw_map = json.load(f)
        if "classes" in raw_map and isinstance(raw_map["classes"], list):
            _GLOBAL_CLASS_MAPPING = {i: name for i, name in enumerate(raw_map["classes"])}
        elif "id_to_class" in raw_map:
            _GLOBAL_CLASS_MAPPING = {int(k): v for k, v in raw_map["id_to_class"].items()}
        elif "class_to_idx" in raw_map:
            _GLOBAL_CLASS_MAPPING = {int(v): k for k, v in raw_map["class_to_idx"].items()}
        else:
            _GLOBAL_CLASS_MAPPING = {int(k): v for k, v in raw_map.items()}
    return _GLOBAL_CLASS_MAPPING

def load_model2(model_path=DEFAULT_MODEL_PATH, device=None):
    global _GLOBAL_MODEL, _GLOBAL_DEVICE
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _GLOBAL_DEVICE = device

    if _GLOBAL_MODEL is None:
        exp = Exp()
        exp.num_classes = 115
        exp.depth = 0.33
        exp.width = 0.50
        model = exp.get_model()
        
        if os.path.exists(model_path):
            ckpt = torch.load(model_path, map_location="cpu")
            state_dict = ckpt["model"] if "model" in ckpt else ckpt
            model.load_state_dict(state_dict)
            print(f"[Model 2] Loaded weights from {model_path}")
        else:
            print(f"[Model 2] Warning: Checkpoint {model_path} not found. Running with initialized weights.")

        model.to(device)
        model.eval()
        _GLOBAL_MODEL = model

    return _GLOBAL_MODEL, _GLOBAL_DEVICE

def format_disease_name(raw_name: str) -> str:
    """Format raw disease string like 'apple_black_rot' into 'Apple Black Rot'."""
    return raw_name.replace("_", " ").title()

def predict_disease(image, conf_threshold=0.20, nms_threshold=0.65, model_path=DEFAULT_MODEL_PATH):
    """
    Accepts a single image (numpy array BGR, PIL Image, or file path) and returns structured detections.
    
    Returns:
    {
        "detections": [
            {
                "disease_id": int,
                "disease": str,
                "disease_label": str,
                "confidence": float,
                "percentage": str,
                "bbox": [x1, y1, x2, y2]
            }
        ]
    }
    """
    class_map = get_class_mapping()
    model, device = load_model2(model_path=model_path)
    
    if isinstance(image, str):
        img_raw = cv2.imread(image)
        if img_raw is None:
            raise FileNotFoundError(f"Could not load image from {image}")
    elif isinstance(image, np.ndarray):
        img_raw = image
    else:
        # PIL Image or bytes
        try:
            from PIL import Image
            if isinstance(image, Image.Image):
                rgb_arr = np.array(image.convert("RGB"))
                img_raw = cv2.cvtColor(rgb_arr, cv2.COLOR_RGB2BGR)
            else:
                raise TypeError(f"Unsupported image type: {type(image)}")
        except Exception as exc:
            raise TypeError(f"Could not convert input of type {type(image)} to BGR array: {exc}")

    origin_h, origin_w = img_raw.shape[:2]
    input_size = (640, 640)
    
    # Preprocess image
    preproc = ValTransform(legacy=False)
    img_transformed, _ = preproc(img_raw, None, input_size)
    img_tensor = torch.from_numpy(img_transformed).unsqueeze(0).float().to(device)
    
    with torch.no_grad():
        outputs = model(img_tensor)
        outputs = postprocess(
            outputs,
            num_classes=115,
            conf_thre=conf_threshold,
            nms_thre=nms_threshold,
            class_agnostic=True,
        )

    detections = []
    output = outputs[0]
    if output is not None:
        output = output.cpu().numpy()
        scale = min(input_size[0] / origin_h, input_size[1] / origin_w)
        
        for pred in output:
            box = pred[0:4] / scale
            score = float(pred[4] * pred[5])
            cls_id = int(pred[6])
            
            x1 = max(0.0, float(box[0]))
            y1 = max(0.0, float(box[1]))
            x2 = min(float(origin_w), float(box[2]))
            y2 = min(float(origin_h), float(box[3]))
            
            raw_disease = class_map.get(cls_id, f"disease_{cls_id}")
            formatted_name = format_disease_name(raw_disease)
            
            detections.append({
                "disease_id": cls_id,
                "disease": raw_disease,
                "disease_label": formatted_name,
                "confidence": round(score, 4),
                "percentage": f"{score * 100:.1f}%",
                "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
            })

    # Sort detections by confidence descending
    detections.sort(key=lambda d: d["confidence"], reverse=True)
    return {"detections": detections}

def draw_predictions(image, detections):
    """Draws crisp bounding boxes and labels onto the image."""
    img_annotated = image.copy()
    for det in detections.get("detections", []):
        x1, y1, x2, y2 = [int(round(v)) for v in det["bbox"]]
        conf_str = det.get("percentage") or f"{det.get('confidence', 0.0) * 100:.1f}%"
        label_name = det.get("disease_label") or format_disease_name(det.get("disease", "disease"))
        label_text = f"{label_name} {conf_str}"
        
        # Draw glowing bounding box
        cv2.rectangle(img_annotated, (x1, y1), (x2, y2), (0, 0, 240), 2)
        
        # Draw filled label tag above or inside box
        (tw, th), baseline = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        tag_y = max(th + 6, y1)
        cv2.rectangle(img_annotated, (x1, tag_y - th - 6), (x1 + tw + 8, tag_y + 2), (0, 0, 220), -1)
        cv2.putText(
            img_annotated,
            label_text,
            (x1 + 4, tag_y - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )
    return img_annotated

def main():
    parser = argparse.ArgumentParser(description="Model 2 - Plant Disease Detection & Localization Inference")
    parser.add_argument("image_path", type=str, help="Path to input leaf/plant image")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (e.g. 0.25, 0.40, 0.50)")
    parser.add_argument("--nms", type=float, default=0.65, help="NMS IoU threshold")
    parser.add_argument("--weights", type=str, default=DEFAULT_MODEL_PATH, help="Path to model checkpoint")
    parser.add_argument("--output", type=str, default=None, help="Optional output path to save annotated image")
    args = parser.parse_args()

    result = predict_disease(
        args.image_path,
        conf_threshold=args.conf,
        nms_threshold=args.nms,
        model_path=args.weights,
    )
    
    print(json.dumps(result, indent=2))

    if args.output:
        raw = cv2.imread(args.image_path)
        annotated = draw_predictions(raw, result)
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        cv2.imwrite(args.output, annotated)
        print(f"[Model 2] Annotated image saved to: {args.output}")

if __name__ == "__main__":
    main()
