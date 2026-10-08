"""
Video Disease Detection Debug Trace Script
===========================================
Accepts a video path and traces the complete Model 1 + Model 2 V4 execution,
diagnosing why disease detection produces 'No disease detected' or misses disease.
"""

from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.config import (
    CROP_DISEASE_MAPPING,
    DEVICE,
    MODEL1_CHECKPOINT,
    MODEL1_CLASS_MAPPING,
    MODEL1_CONFIG,
    MODEL2_CHECKPOINT,
    MODEL2_CLASS_MAPPING,
)
from app.backend.services import (
    get_model1,
    get_model2,
    process_video_inference,
)
from model1_test_app.inference import load_model
from model1_test_app.video_inference import (
    TARGET_FRAMES_DEFAULT,
    extract_adaptive_video_frames,
    predict_video,
)
from models.model2_classifier_v4.predict import Model2DiseaseClassifierV4, format_disease_name_clean


def debug_video(video_path_str: str, csv_output_path: str = "reports/system_integration/video_disease_debug.csv"):
    video_path = Path(video_path_str).resolve()
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    print("=" * 50)
    print("VIDEO DISEASE DEBUG")
    print("=" * 50)
    print(f"Video:\n{video_path}\n")

    # Load models
    model1, idx_to_class1, _ = get_model1()
    m2_classifier: Model2DiseaseClassifierV4 = get_model2()

    # Step 1: Frame extraction & quality filtering
    extraction = extract_adaptive_video_frames(
        video_path=video_path,
        target_frames=TARGET_FRAMES_DEFAULT,
        min_target=16,
        quality_filter=True,
    )
    total_extracted = extraction["total_evaluated"]
    selected_frames = extraction["selected_frames"]
    usable_count = len(selected_frames)

    print(f"Frames extracted:\n{total_extracted}\n")
    print(f"Frames after quality filtering:\n{usable_count}\n")

    # Step 2: Run Model 1 Video Inference
    v_res = predict_video(
        video_path=video_path,
        model=model1,
        idx_to_class=idx_to_class1,
        device=DEVICE,
        target_frames=TARGET_FRAMES_DEFAULT,
        quality_filter=True,
        detect_disease=False,
    )

    m1_calls = v_res["frames_used"]
    final_pred = v_res["final_prediction"]
    majority_crop = final_pred.get("label", "Unknown")
    crop_conf = final_pred.get("confidence", 0.0)

    print(f"Model 1 calls:\n{m1_calls}\n")
    print(f"Majority crop:\n{majority_crop}")
    print(f"Crop confidence:\n{crop_conf:.4f} ({crop_conf*100:.1f}%)\n")

    # Step 3: Production Pipeline Simulation
    with open(video_path, "rb") as vf:
        video_bytes = vf.read()
    prod_res = process_video_inference(video_bytes, original_filename=video_path.name)
    prod_m2 = prod_res["model2"]

    print("=" * 50)
    print("ACTIVE PRODUCTION PIPELINE EXECUTION:")
    print("=" * 50)
    print(f"Production Model 2 Status: {prod_m2.get('status')}")
    print(f"Production Primary Disease: {prod_m2.get('primary_disease')}")
    print(f"Production Confidence: {prod_m2.get('confidence')}")
    print(f"Production Has Disease: {prod_m2.get('has_disease')}")
    print("=" * 50)

    # Step 4: Trace Model 2 V4 on EVERY valid frame
    frame_records = v_res["frame_records"]
    csv_rows = []

    print(f"\nModel 2 V4 calls (Exhaustive Per-Frame Analysis):")
    print(f"Total candidate frames to evaluate: {len(frame_records)}\n")

    for f in frame_records:
        frame_idx = f["frame_index"]
        frame_num = f["frame_number"]
        t_sec = f["timestamp_seconds"]
        f_crop = f["predicted_label"]
        f_crop_conf = f["confidence"]

        # Test both full frame thumbnail and tight ROI
        roi_img = f.get("roi_thumbnail") or f.get("thumbnail")
        if roi_img is None:
            continue

        # Raw Model 2 prediction (no crop gating)
        probs, raw_top = m2_classifier.predict_raw(roi_img)
        top1 = {"class_name": raw_top[0]["class_name"], "confidence": raw_top[0]["probability"]}
        top2 = {"class_name": raw_top[1]["class_name"], "confidence": raw_top[1]["probability"]} if len(raw_top) > 1 else {"class_name": "none", "confidence": 0.0}
        top3 = {"class_name": raw_top[2]["class_name"], "confidence": raw_top[2]["probability"]} if len(raw_top) > 2 else {"class_name": "none", "confidence": 0.0}

        # Crop-aware Model 2 prediction (gating by majority crop)
        crop_aware_m2 = m2_classifier.predict_crop_aware(
            image_input=roi_img,
            crop_name=majority_crop,
            crop_confidence=crop_conf,
        )

        is_compatible = "YES" if crop_aware_m2.get("top_compatible") else "NO"

        print(f"--------------------------------------------------")
        print(f"FRAME INDEX: {frame_idx} (Frame #{frame_num}, {t_sec:.2f}s)")
        print(f"CROP: {majority_crop} (Frame predicted: {f_crop})")
        print(f"CROP CONFIDENCE: {crop_conf:.4f}")
        print(f"\nRAW MODEL 2 TOP-1:")
        print(f"CLASS: {top1['class_name']}")
        print(f"CONFIDENCE: {top1['confidence']:.4f}")
        print(f"\nTOP-3:")
        print(f"1. {top1['class_name']} ({top1['confidence']:.4f})")
        print(f"2. {top2['class_name']} ({top2['confidence']:.4f})")
        print(f"3. {top3['class_name']} ({top3['confidence']:.4f})")
        print(f"\nCOMPATIBILITY: {is_compatible}")
        print(f"\nAFTER UNCERTAINTY GATE:")
        print(f"STATUS: {crop_aware_m2['status']}")
        print(f"DISEASE: {crop_aware_m2['disease']}")
        print(f"CONFIDENCE: {crop_aware_m2['disease_confidence']:.4f}")

        csv_rows.append({
            "video": video_path.name,
            "frame_index": frame_idx,
            "crop": majority_crop,
            "crop_confidence": round(crop_conf, 4),
            "raw_disease": top1["class_name"],
            "raw_disease_confidence": round(top1["confidence"], 4),
            "top2": top2["class_name"],
            "top2_confidence": round(top2["confidence"], 4),
            "top3": top3["class_name"],
            "top3_confidence": round(top3["confidence"], 4),
            "compatible": is_compatible,
            "uncertainty_status": crop_aware_m2["status"],
            "final_disease": crop_aware_m2["disease"],
            "final_confidence": round(crop_aware_m2["disease_confidence"], 4),
        })

    # Write CSV
    Path(csv_output_path).parent.mkdir(parents=True, exist_ok=True)
    if csv_rows:
        fieldnames = [
            "video",
            "frame_index",
            "crop",
            "crop_confidence",
            "raw_disease",
            "raw_disease_confidence",
            "top2",
            "top2_confidence",
            "top3",
            "top3_confidence",
            "compatible",
            "uncertainty_status",
            "final_disease",
            "final_confidence",
        ]
        with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"\nSaved CSV trace to: {csv_output_path}")

    return {
        "video": video_path.name,
        "frames_extracted": total_extracted,
        "usable_frames": usable_count,
        "majority_crop": majority_crop,
        "crop_confidence": crop_conf,
        "prod_m2": prod_m2,
        "frame_results": csv_rows,
    }


def main():
    parser = argparse.ArgumentParser(description="Debug Video Disease Detection Pipeline")
    parser.add_argument("video_path", nargs="?", default=None, help="Path to video file")
    args = parser.parse_args()

    target_video = args.video_path
    if not target_video:
        # Check if there is an existing test video in project
        candidates = [
            PROJECT_ROOT / "test_24f_tomato.mp4",
            PROJECT_ROOT / "test_plant_4s.mp4",
            PROJECT_ROOT / "temp_multimodal_uploads" / "smoke_test_video.mp4",
        ]
        for c in candidates:
            if c.exists():
                target_video = str(c)
                break

    if not target_video or not Path(target_video).exists():
        # Create a realistic test video from a known diseased leaf image
        print("No test video path supplied. Creating a realistic diseased tomato video for trace analysis...")
        tom_eb_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "early_blight"
        eb_imgs = list(tom_eb_dir.glob("*.jpg")) + list(tom_eb_dir.glob("*.png"))
        if not eb_imgs:
            eb_imgs = list((PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test").glob("**/*.jpg"))

        src_img_path = eb_imgs[0]
        src_cv = cv2.imread(str(src_img_path))
        src_cv = cv2.resize(src_cv, (640, 480))

        synthetic_vid = PROJECT_ROOT / "test_diseased_tomato_video.mp4"
        out = cv2.VideoWriter(str(synthetic_vid), cv2.VideoWriter_fourcc(*"mp4v"), 30.0, (640, 480))

        # 180 frames (6 seconds) with subtle camera pan and zoom
        for i in range(180):
            frame = src_cv.copy()
            dx = int(8 * np.sin(i / 10.0))
            dy = int(4 * np.cos(i / 10.0))
            scale = 1.0 + 0.05 * np.sin(i / 20.0)
            M = cv2.getRotationMatrix2D((320, 240), 0, scale)
            M[0, 2] += dx
            M[1, 2] += dy
            frame = cv2.warpAffine(frame, M, (640, 480))
            out.write(frame)
        out.release()
        target_video = str(synthetic_vid)

    debug_video(target_video)


if __name__ == "__main__":
    main()
