"""
Export Script: Model 1 & Model 2 V2 to ONNX (FP32, FP16, INT8)
=============================================================
Exports trained PyTorch checkpoints to ONNX for mobile deployment (Flutter + ONNX Runtime Mobile).

Exports:
  Model 1 (Crop Classifier, 22 classes):
    - models/model1/mobile/model1_fp32.onnx
    - models/model1/mobile/model1_fp16.onnx
    - models/model1/mobile/model1_int8.onnx
    - models/model1/mobile/class_mapping.json
    - models/model1/mobile/labels.txt
    - models/model1/mobile/model_metadata.json

  Model 2 V2 (Disease Classifier, 117 classes):
    - models/model2_classifier_v2/mobile/model2_fp32.onnx
    - models/model2_classifier_v2/mobile/model2_fp16.onnx
    - models/model2_classifier_v2/mobile/model2_int8.onnx
    - models/model2_classifier_v2/mobile/class_mapping.json
    - models/model2_classifier_v2/mobile/crop_disease_mapping.json
    - models/model2_classifier_v2/mobile/labels.txt
    - models/model2_classifier_v2/mobile/model_metadata.json
"""

import os
import sys
import json
import shutil
from pathlib import Path

# Force UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import torch
import torch.nn as nn
from torchvision.models import efficientnet_b2
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType
import onnxconverter_common

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()


def load_model1():
    chk_path = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
    map_path = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"
    with open(map_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    
    idx_to_class = {int(k): v for k, v in mapping["idx_to_class"].items()}
    num_classes = len(idx_to_class)
    
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    
    chk = torch.load(chk_path, map_location="cpu", weights_only=False)
    state = chk.get("model_state_dict", chk)
    model.load_state_dict(state)
    model.eval()
    return model, mapping, num_classes


def load_model2_v2():
    chk_path = PROJECT_ROOT / "models" / "model2_classifier_v2" / "best_model.pth"
    map_path = PROJECT_ROOT / "models" / "model2_classifier_v2" / "class_mapping.json"
    with open(map_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
        
    idx_to_class = {int(k): v for k, v in mapping["id_to_class"].items()}
    num_classes = len(idx_to_class)
    
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, num_classes)
    )
    
    chk = torch.load(chk_path, map_location="cpu", weights_only=False)
    state = chk.get("model_state_dict", chk)
    model.load_state_dict(state)
    model.eval()
    return model, mapping, num_classes


def export_model(
    model: nn.Module,
    input_size: tuple[int, int],
    output_dir: Path,
    base_name: str,
    num_classes: int,
    metadata: dict,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    fp32_path = output_dir / f"{base_name}_fp32.onnx"
    fp16_path = output_dir / f"{base_name}_fp16.onnx"
    int8_path = output_dir / f"{base_name}_int8.onnx"

    h, w = input_size
    dummy_input = torch.randn(1, 3, h, w, dtype=torch.float32)

    print(f"\n--- Exporting {base_name.upper()} (FP32) ---")
    print(f"Input Shape: (1, 3, {h}, {w}) | Classes: {num_classes}")

    # Export to FP32 ONNX using legacy dynamo=False for highest mobile / ORT runtime stability
    torch.onnx.export(
        model,
        dummy_input,
        str(fp32_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["logits"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "logits": {0: "batch_size"},
        },
        dynamo=False,
    )

    # Check FP32 model
    onnx_model = onnx.load(str(fp32_path))
    onnx.checker.check_model(onnx_model)
    fp32_size_mb = fp32_path.stat().st_size / (1024 * 1024)
    print(f"  [OK] Saved FP32 ONNX: {fp32_path} ({fp32_size_mb:.2f} MB)")

    # Export to FP16 ONNX
    print(f"\n--- Converting {base_name.upper()} to FP16 ---")
    try:
        fp16_model = onnxconverter_common.convert_float_to_float16(
            onnx_model,
            keep_io_types=True,  # Keeps float32 inputs/outputs for mobile pipeline compatibility
        )
        onnx.save(fp16_model, str(fp16_path))
        fp16_size_mb = fp16_path.stat().st_size / (1024 * 1024)
        print(f"  [OK] Saved FP16 ONNX: {fp16_path} ({fp16_size_mb:.2f} MB)")
    except Exception as exc:
        print(f"  [WARN] FP16 conversion failed: {exc}")
        fp16_path = None
        fp16_size_mb = None

    # Export to INT8 ONNX via Dynamic Quantization
    print(f"\n--- Quantizing {base_name.upper()} to INT8 ---")
    try:
        quantize_dynamic(
            model_input=str(fp32_path),
            model_output=str(int8_path),
            weight_type=QuantType.QUInt8,
        )
        int8_size_mb = int8_path.stat().st_size / (1024 * 1024)
        print(f"  [OK] Saved INT8 ONNX: {int8_path} ({int8_size_mb:.2f} MB)")
    except Exception as exc:
        print(f"  [WARN] INT8 dynamic quantization failed: {exc}")
        int8_path = None
        int8_size_mb = None

    # Save metadata and labels
    meta_path = output_dir / "model_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"  [OK] Saved Metadata: {meta_path}")

    return {
        "fp32": str(fp32_path),
        "fp16": str(fp16_path) if fp16_path else None,
        "int8": str(int8_path) if int8_path else None,
        "sizes_mb": {
            "fp32": fp32_size_mb,
            "fp16": fp16_size_mb,
            "int8": int8_size_mb,
        }
    }


def main():
    print("=" * 80)
    print("STARTING MOBILE MODEL EXPORT (MODEL 1 & MODEL 2 V2)")
    print("=" * 80)

    # 1. Process Model 1
    m1_model, m1_mapping, m1_num_classes = load_model1()
    m1_out_dir = PROJECT_ROOT / "models" / "model1" / "mobile"
    
    # Write mapping and labels.txt for Model 1
    m1_out_dir.mkdir(parents=True, exist_ok=True)
    with open(m1_out_dir / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(m1_mapping, f, indent=2)
    
    with open(m1_out_dir / "labels.txt", "w", encoding="utf-8") as f:
        for idx in range(m1_num_classes):
            f.write(f"{m1_mapping['idx_to_class'][str(idx)]}\n")

    m1_metadata = {
        "model_name": "model1_crop_classifier",
        "architecture": "EfficientNet-B2",
        "num_classes": m1_num_classes,
        "input_tensor": "input",
        "output_tensor": "logits",
        "input_shape": [1, 3, 224, 224],
        "image_size": [224, 224],
        "normalization": {
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225]
        },
        "opset_version": 17,
        "supported_runtimes": ["onnxruntime", "onnxruntime-mobile", "flutter_onnx"]
    }

    m1_res = export_model(
        model=m1_model,
        input_size=(224, 224),
        output_dir=m1_out_dir,
        base_name="model1",
        num_classes=m1_num_classes,
        metadata=m1_metadata
    )

    # 2. Process Model 2 V2
    m2_model, m2_mapping, m2_num_classes = load_model2_v2()
    m2_out_dir = PROJECT_ROOT / "models" / "model2_classifier_v2" / "mobile"
    
    # Write mapping, crop disease map, and labels.txt for Model 2 V2
    m2_out_dir.mkdir(parents=True, exist_ok=True)
    with open(m2_out_dir / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump(m2_mapping, f, indent=2)

    crop_disease_src = PROJECT_ROOT / "data" / "processed" / "model2_classifier_v2_crop_disease_mapping.json"
    if not crop_disease_src.exists():
        crop_disease_src = PROJECT_ROOT / "data" / "processed" / "model2_classifier_crop_disease_mapping.json"
    shutil.copy(crop_disease_src, m2_out_dir / "crop_disease_mapping.json")

    with open(m2_out_dir / "labels.txt", "w", encoding="utf-8") as f:
        for idx in range(m2_num_classes):
            f.write(f"{m2_mapping['id_to_class'][str(idx)]}\n")

    m2_metadata = {
        "model_name": "model2_disease_classifier_v2",
        "architecture": "EfficientNet-B2",
        "num_classes": m2_num_classes,
        "input_tensor": "input",
        "output_tensor": "logits",
        "input_shape": [1, 3, 260, 260],
        "image_size": [260, 260],
        "normalization": {
            "mean": [0.485, 0.456, 0.406],
            "std": [0.229, 0.224, 0.225]
        },
        "healthy_class_id": 0,
        "opset_version": 17,
        "supported_runtimes": ["onnxruntime", "onnxruntime-mobile", "flutter_onnx"]
    }

    m2_res = export_model(
        model=m2_model,
        input_size=(260, 260),
        output_dir=m2_out_dir,
        base_name="model2",
        num_classes=m2_num_classes,
        metadata=m2_metadata
    )

    print("\n" + "=" * 80)
    print("ALL MODELS SUCCESSFULLY EXPORTED TO MOBILE FOLDERS:")
    print(f"Model 1 Export Dir: {m1_out_dir}")
    print(f"  FP32: {m1_res['sizes_mb']['fp32']:.2f} MB")
    if m1_res['sizes_mb']['fp16']:
        print(f"  FP16: {m1_res['sizes_mb']['fp16']:.2f} MB")
    if m1_res['sizes_mb']['int8']:
        print(f"  INT8: {m1_res['sizes_mb']['int8']:.2f} MB")

    print(f"Model 2 V2 Export Dir: {m2_out_dir}")
    print(f"  FP32: {m2_res['sizes_mb']['fp32']:.2f} MB")
    if m2_res['sizes_mb']['fp16']:
        print(f"  FP16: {m2_res['sizes_mb']['fp16']:.2f} MB")
    if m2_res['sizes_mb']['int8']:
        print(f"  INT8: {m2_res['sizes_mb']['int8']:.2f} MB")
    print("=" * 80)


if __name__ == "__main__":
    main()
