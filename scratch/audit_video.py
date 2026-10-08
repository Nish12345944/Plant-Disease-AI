import os
import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
import cv2
import numpy as np
import torch
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from model1_test_app.inference import load_model, format_class_name, get_eval_transform
from model1_test_app.plant_detector import assess_plant_presence_and_quality, extract_tight_plant_rois
from model1_test_app.video_inference import extract_adaptive_video_frames, predict_video
from model2.test_model2 import load_model2, predict_disease, get_class_mapping

def run_audit(video_path):
    print("=" * 60)
    print("DIAGNOSTIC AUDIT ON VIDEO:", video_path)
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Device:", device)

    m1_ckpt = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
    m1_map = PROJECT_ROOT / "models" / "model1" / "class_mapping.json"
    m1_cfg = PROJECT_ROOT / "models" / "model1" / "config.json"
    m1_model, idx_to_class, class_to_idx, _, _ = load_model(m1_ckpt, m1_map, m1_cfg, device=device)

    m2_ckpt = PROJECT_ROOT / "models" / "model2" / "best_model.pth"
    m2_model, _ = load_model2(str(m2_ckpt), device=device)
    m2_class_mapping = get_class_mapping()

    extraction = extract_adaptive_video_frames(video_path, target_frames=24, min_target=16, quality_filter=True)
    metadata = extraction["metadata"]
    selected_frames = extraction["selected_frames"]
    rejected_frames = extraction["rejected_frames"]

    print(f"Video metadata: {metadata['width']}x{metadata['height']}, {metadata['fps']} fps, {metadata['frame_count']} total frames, duration: {metadata['duration_seconds']}s")
    print(f"Sampled frames: {len(selected_frames)}, Rejected by initial quality filter: {len(rejected_frames)}")

    transform = get_eval_transform()
    frame_analyses = []
    thresholds = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]

    for seq_num, f_data in enumerate(selected_frames, start=1):
        idx = f_data["frame_index"]
        t_sec = f_data["timestamp_seconds"]
        frame_bgr = f_data.get("frame_bgr")
        frame_img = f_data["frame_image"]

        assessment = assess_plant_presence_and_quality(frame_bgr if frame_bgr is not None else frame_img)
        f_status = assessment["status"]
        candidate_rois = assessment.get("rois", [])

        if f_status == "blurry" or f_status == "unknown" or not candidate_rois:
            frame_analyses.append({
                "seq_num": seq_num,
                "frame_idx": idx,
                "timestamp": t_sec,
                "status": f_status,
                "reason": assessment.get("reason"),
                "crop": "None",
                "crop_conf": 0.0,
                "m2_detections_roi": {th: [] for th in thresholds},
                "m2_detections_full": {th: [] for th in thresholds},
            })
            continue

        # Evaluate candidate plant ROIs with Model 1
        roi_results = []
        for r_idx, roi_dict in enumerate(candidate_rois):
            roi_pil = roi_dict["roi_pil"]
            tensor = transform(roi_pil).unsqueeze(0).to(device)
            with torch.no_grad():
                logits = m1_model(tensor)
                probs = torch.softmax(logits, dim=1)[0].cpu().numpy()
            top_idx = int(np.argmax(probs))
            top_cls_name = idx_to_class[top_idx]
            top_conf = float(probs[top_idx])
            roi_results.append({
                "roi_index": r_idx,
                "box": roi_dict["box"],
                "probs": probs,
                "top_idx": top_idx,
                "top_class": top_cls_name,
                "top_conf": top_conf,
                "roi_pil": roi_pil,
            })

        best_roi = max(roi_results, key=lambda r: r["top_conf"])
        best_crop = best_roi["top_class"]
        best_crop_conf = best_roi["top_conf"]
        best_roi_pil = best_roi["roi_pil"]

        # Run Model 2 at various thresholds on ROI
        m2_dets_roi = {}
        m2_dets_full = {}
        for th in thresholds:
            res_roi = predict_disease(best_roi_pil, conf_threshold=th, model_path=str(m2_ckpt))
            m2_dets_roi[th] = res_roi.get("detections", [])
            # Also test on FULL frame for comparison
            res_full = predict_disease(frame_img, conf_threshold=th, model_path=str(m2_ckpt))
            m2_dets_full[th] = res_full.get("detections", [])

        frame_analyses.append({
            "seq_num": seq_num,
            "frame_idx": idx,
            "timestamp": t_sec,
            "status": "valid",
            "reason": "Plant ROI detected",
            "crop": best_crop,
            "crop_conf": best_crop_conf,
            "m2_detections_roi": m2_dets_roi,
            "m2_detections_full": m2_dets_full,
        })

    # Print Detailed Findings
    print("\n" + "=" * 60)
    print("FRAME-BY-FRAME RESULTS TABLE (Model 2 on ROI at conf_threshold=0.20)")
    print(f"{'#':<3} {'Idx':<5} {'Time':<6} {'Status':<7} {'Model 1 Crop':<12} {'M1 Conf':<8} {'Model 2 Detections (Disease & Conf)'}")
    print("-" * 80)

    crop_counts = Counter()
    disease_frames_map = defaultdict(list)
    disease_conf_map = defaultdict(list)

    for fa in frame_analyses:
        seq = fa["seq_num"]
        idx = fa["frame_idx"]
        t = f"{fa['timestamp']:.2f}s"
        st = fa["status"]
        crop = fa["crop"]
        c_conf = f"{fa['crop_conf']*100:.1f}%" if fa['crop_conf'] > 0 else "-"
        dets_20 = fa["m2_detections_roi"][0.20]
        
        if st == "valid":
            crop_counts[crop] += 1

        det_str = ", ".join([f"{d['disease']} ({d['confidence']:.2f})" for d in dets_20]) if dets_20 else "None (Healthy/No Lesion)"
        print(f"{seq:<3} {idx:<5} {t:<6} {st:<7} {crop:<12} {c_conf:<8} {det_str}")

        for d in dets_20:
            d_name = d["disease"]
            disease_frames_map[d_name].append(seq)
            disease_conf_map[d_name].append(d["confidence"])

    print("\n" + "=" * 60)
    print("MODEL 1 CROP DISTRIBUTION ACROSS VALID FRAMES:")
    valid_frames_count = sum(1 for fa in frame_analyses if fa["status"] == "valid")
    print(f"Total evaluated frames: {len(frame_analyses)}, Valid plant frames: {valid_frames_count}")
    for crop, count in crop_counts.items():
        print(f"  - {crop}: {count}/{valid_frames_count} ({count/valid_frames_count*100:.1f}%)")

    print("\n" + "=" * 60)
    print("MODEL 2 DISEASE PREDICTIONS SUMMARY (conf_threshold = 0.20 on ROI):")
    print(f"Unique disease classes predicted: {len(disease_frames_map)}")
    for d_name, frames in sorted(disease_frames_map.items(), key=lambda x: len(x[1]), reverse=True):
        confs = disease_conf_map[d_name]
        mean_c = np.mean(confs)
        max_c = np.max(confs)
        print(f"  Disease: '{d_name}'")
        print(f"    - Frames ({len(frames)}/{valid_frames_count}): {frames} ({len(frames)/valid_frames_count*100:.1f}%)")
        print(f"    - Mean conf: {mean_c:.3f}, Max conf: {max_c:.3f}")
        associated_crop = d_name.split()[0] if " " in d_name else d_name.split("_")[0]
        m1_top_crop = crop_counts.most_common(1)[0][0] if crop_counts else "unknown"
        print(f"    - Implied crop from disease name: '{associated_crop}' vs Model 1 predicted crop: '{m1_top_crop}'")

    print("\n" + "=" * 60)
    print("THRESHOLD SENSITIVITY ANALYSIS (Model 2 detections count on ROI across all frames):")
    for th in thresholds:
        all_dets = []
        for fa in frame_analyses:
            all_dets.extend(fa["m2_detections_roi"][th])
        d_counts = Counter(d["disease"] for d in all_dets)
        print(f"  Threshold {th:.2f}: {len(all_dets)} total detections across {len(d_counts)} unique classes -> {dict(d_counts)}")

    print("\n" + "=" * 60)
    print("THRESHOLD SENSITIVITY ANALYSIS (Model 2 detections count on FULL FRAME across all frames):")
    for th in thresholds:
        all_dets = []
        for fa in frame_analyses:
            all_dets.extend(fa["m2_detections_full"][th])
        d_counts = Counter(d["disease"] for d in all_dets)
        print(f"  Threshold {th:.2f}: {len(all_dets)} total detections across {len(d_counts)} unique classes -> {dict(d_counts)}")

if __name__ == "__main__":
    vid = r"C:\Users\vyasn\Downloads\gemini_generated_video_17a86e10.mp4"
    run_audit(vid)
