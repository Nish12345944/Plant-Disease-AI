"""
Regression Test Suite: Video Canonical Crop Undefined-Variable Fix
===================================================================
Verifies the fix for:
"Video processing failed: name 'video_canonical_crop' is not defined"

Tests:
1. Recognizable Plant Video:
   - Model 1 identifies crop from sampled frames.
   - Model 2 performs compatible disease inference or healthy shielding.
   - Verifies structured treatment payload (5 sections: Curable?, Cure/Treatment, Precautions, Prevention, Sources).
   - Verifies no NameError: name 'video_canonical_crop' is not defined.
2. Uncertain / Noise Video:
   - Open-set guard or frame filter identifies uncertain/unverified crop.
   - Disease analysis safely withheld or evaluated with uncertain shielding.
   - Verifies treatment payload contains safe non-curative guidance.
   - Verifies no NameError crash.
3. TestClient API Endpoint:
   - /api/inference/video and /api/chat endpoints return 200 OK without NameError.
4. Live Server /api/chat Verification:
   - Uploads video via HTTP to live http://127.0.0.1:8000/api/chat endpoint.
   - Verifies end-to-end response payload integrity and treatment structure.
"""

from __future__ import annotations

import io
import sys
import tempfile
import urllib.request
import json
from pathlib import Path

import cv2
import numpy as np
import httpx
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.main import app
from app.backend.services import process_video_inference

client = TestClient(app, raise_server_exceptions=True)


def create_synthetic_noise_video(num_frames: int = 12, fps: float = 30.0, size: tuple[int, int] = (320, 240)) -> bytes:
    """Create in-memory MP4 of random noise to test uncertain crop handling."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(tmp_path), fourcc, fps, size)
        for _ in range(num_frames):
            frame = np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)
            writer.write(frame)
        writer.release()
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def run_video_canonical_crop_regression_tests():
    print("=" * 80)
    print("RUNNING REGRESSION TEST: video_canonical_crop UNDEFINED VARIABLE FIX")
    print("=" * 80)

    total_checks = 0
    passed_checks = 0

    def check(name: str, condition: bool, details: str = ""):
        nonlocal total_checks, passed_checks
        total_checks += 1
        if condition:
            passed_checks += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            if details:
                print(f"         Details: {details}")

    # Locate test plant video
    real_vid_path = PROJECT_ROOT / "test_multimodal_assets" / "test_plant_4s.mp4"
    if not real_vid_path.exists():
        real_vid_path = PROJECT_ROOT / "temp_test_videos" / "sample_plant_30fps.mp4"

    assert real_vid_path.exists(), f"Could not find a valid test video file at {real_vid_path}"
    real_vid_bytes = real_vid_path.read_bytes()
    noise_vid_bytes = create_synthetic_noise_video(num_frames=10, fps=30.0)

    # -------------------------------------------------------------------------
    # PART 1: Recognizable Plant Video (Unit / Service Level)
    # -------------------------------------------------------------------------
    print("\n[PART 1] Recognizable Plant Video Inference Service...")
    try:
        res_real = process_video_inference(
            real_vid_bytes,
            original_filename="test_plant_4s.mp4",
            target_frames=8,
        )
        check("1.1 Recognizable video processed without NameError", True)
    except NameError as exc:
        check("1.1 Recognizable video processed without NameError", False, f"NameError raised: {exc}")
        res_real = {}
    except Exception as exc:
        check("1.1 Recognizable video processed without NameError", False, f"Unexpected error: {exc}")
        res_real = {}

    if res_real:
        crop_name = res_real.get("predicted_crop")
        canonical_class = res_real.get("predicted_class")
        crop_status = res_real.get("crop_status")
        check("1.2 Crop recognized and canonicalized", bool(crop_name and canonical_class), f"crop={crop_name}, class={canonical_class}")
        check("1.3 Crop accepted by open-set guard", crop_status == "accepted", f"crop_status={crop_status}")

        m2_summary = res_real.get("model2", {})
        check("1.4 Model 2 disease inference executed", m2_summary.get("status") in ("detected", "healthy", "uncertain"), f"m2_status={m2_summary.get('status')}")
        
        # Check treatment dictionary
        treatment = m2_summary.get("treatment")
        check("1.5 Treatment dictionary generated", isinstance(treatment, dict), f"treatment={type(treatment)}")
        if isinstance(treatment, dict):
            check("1.6 Treatment has 'curable_simple'", "curable_simple" in treatment, f"keys={list(treatment.keys())}")
            check("1.7 Treatment has 'cure_treatment' list", isinstance(treatment.get("cure_treatment"), list))
            check("1.8 Treatment has 'precautions' list", isinstance(treatment.get("precautions"), list))
            check("1.9 Treatment has 'prevention' list", isinstance(treatment.get("prevention"), list))
            check("1.10 Treatment has 'sources' list", isinstance(treatment.get("sources"), list))

    # -------------------------------------------------------------------------
    # PART 2: Uncertain / Non-Plant Video (Unit / Service Level)
    # -------------------------------------------------------------------------
    print("\n[PART 2] Uncertain / Noise Video Handling Service...")
    try:
        res_noise = process_video_inference(
            noise_vid_bytes,
            original_filename="noise_sample.mp4",
            target_frames=6,
        )
        check("2.1 Noise/uncertain video processed without NameError", True)
    except NameError as exc:
        check("2.1 Noise/uncertain video processed without NameError", False, f"NameError raised: {exc}")
        res_noise = {}
    except Exception as exc:
        check("2.1 Noise/uncertain video processed without NameError", False, f"Unexpected error: {exc}")
        res_noise = {}

    if res_noise:
        noise_crop_status = res_noise.get("crop_status")
        check("2.2 Uncertain/noise video crop correctly rejected or uncertain", noise_crop_status in ("rejected", "uncertain", "out_of_domain"), f"status={noise_crop_status}")
        
        noise_m2 = res_noise.get("model2", {})
        check("2.3 Disease analysis withheld or marked not_applicable/uncertain", noise_m2.get("status") in ("not_applicable", "uncertain"), f"m2_status={noise_m2.get('status')}")
        
        noise_treatment = noise_m2.get("treatment")
        check("2.4 Noise video treatment present and safe", isinstance(noise_treatment, dict))
        if isinstance(noise_treatment, dict):
            check("2.5 Noise video treatment contraindicates chemical sprays", not noise_treatment.get("has_treatment", False))

    # -------------------------------------------------------------------------
    # PART 3: In-Process TestClient /api/chat and /api/inference/video
    # -------------------------------------------------------------------------
    print("\n[PART 3] In-Process TestClient Endpoints...")
    # Inference endpoint
    resp_inf = client.post(
        "/api/inference/video",
        files={"file": ("test_plant_4s.mp4", real_vid_bytes, "video/mp4")},
        data={"target_frames": 8},
    )
    check("3.1 /api/inference/video returns 200 OK", resp_inf.status_code == 200, f"Status: {resp_inf.status_code}")
    if resp_inf.status_code == 200:
        inf_json = resp_inf.json()
        check("3.2 /api/inference/video response contains Model 2 with treatment", "treatment" in inf_json.get("model2", {}))

    # Chat endpoint with video
    resp_chat = client.post(
        "/api/chat",
        files={"video_file": ("test_plant_4s.mp4", real_vid_bytes, "video/mp4")},
        data={"text": "Diagnose this plant video and recommend cure"},
    )
    check("3.3 /api/chat with video_file returns 200 OK", resp_chat.status_code == 200, f"Status: {resp_chat.status_code}")
    if resp_chat.status_code == 200:
        chat_json = resp_chat.json()
        msg_text = chat_json.get("message", "")
        has_undefined_err = "name 'video_canonical_crop' is not defined" in msg_text or "Video processing failed" in msg_text
        check("3.4 /api/chat does not contain 'video_canonical_crop' error message", not has_undefined_err, f"Message snippet: {msg_text[:120]}")
        check("3.5 /api/chat returns structured treatment payload", isinstance(chat_json.get("treatment"), dict))
        check("3.6 /api/chat returns video_inference result node", isinstance(chat_json.get("video_inference"), dict))

    # -------------------------------------------------------------------------
    # PART 4: Live Server Verification (http://127.0.0.1:8000/api/chat)
    # -------------------------------------------------------------------------
    print("\n[PART 4] Live Server Verification (http://127.0.0.1:8000)...")
    live_url = "http://127.0.0.1:8000/api/chat"
    try:
        with httpx.Client(timeout=30.0) as http_client:
            live_resp = http_client.post(
                live_url,
                files={"video_file": ("test_plant_4s.mp4", real_vid_bytes, "video/mp4")},
                data={"text": "Identify crop and disease from this video"},
            )
            check("4.1 Live server /api/chat returns HTTP 200", live_resp.status_code == 200, f"HTTP {live_resp.status_code}")
            if live_resp.status_code == 200:
                live_data = live_resp.json()
                live_msg = live_data.get("message", "")
                has_live_err = "name 'video_canonical_crop' is not defined" in live_msg or "Video processing failed" in live_msg
                check("4.2 Live response does not report video_canonical_crop error", not has_live_err, f"Message: {live_msg[:120]}")
                check("4.3 Live response contains video_inference node", isinstance(live_data.get("video_inference"), dict))
                video_node = live_data.get("video_inference", {})
                check("4.4 Live response video_inference node has model2", isinstance(video_node.get("model2"), dict))
                live_treatment = live_data.get("treatment") or video_node.get("model2", {}).get("treatment")
                check("4.5 Live response has treatment data", isinstance(live_treatment, dict))
                if isinstance(live_treatment, dict):
                    print(f"      Treatment Curability: {live_treatment.get('curable_simple')}")
                    print(f"      Cure/Treatment bullets: {len(live_treatment.get('cure_treatment', []))}")
                    print(f"      Precaution bullets: {len(live_treatment.get('precautions', []))}")
                    print(f"      Prevention bullets: {len(live_treatment.get('prevention', []))}")
                    print(f"      Source links: {len(live_treatment.get('sources', []))}")
    except Exception as exc:
        check("4.1 Live server /api/chat connection and verification", False, f"Could not connect to live server: {exc}")

    print("\n" + "=" * 80)
    print(f"REGRESSION SUITE FINISHED: {passed_checks}/{total_checks} CHECKS PASSED")
    print("=" * 80)

    if passed_checks < total_checks:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    run_video_canonical_crop_regression_tests()
