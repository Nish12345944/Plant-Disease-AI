"""
Phase 1 Integration Test Suite: AgriculturalAssistant into /api/chat
====================================================================
Validates all 8 scenarios:
  A. Text-only factual question
  B. Text-only treatment question
  C. Image + diagnosis question
  D. Image + treatment question
  E. Healthy image (no false disease invented)
  F. Uncertain image (no false diagnosis forced)
  G. Audio + image integration
  H. Video + question integration
"""

from __future__ import annotations

import io
import sys
import wave
from pathlib import Path

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.main import app

client = TestClient(app)


def generate_synthetic_wav_bytes(duration_sec: float = 1.0, sample_rate: int = 16000) -> bytes:
    """Generate a clean synthetic sine wave in WAV format for audio endpoint testing."""
    num_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, num_samples, endpoint=False)
    audio = (0.2 * np.sin(2 * np.pi * 440 * t) * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    return buffer.getvalue()


def run_phase1_test_suite():
    print("=" * 80)
    print("PHASE 1 INTEGRATION TEST SUITE: /api/chat + AgriculturalAssistant")
    print("=" * 80)

    total_tests = 0
    passed_tests = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] {name}")
        else:
            print(f" [FAIL] {name}")
            if details:
                print(f"        Details: {details}")

    # -------------------------------------------------------------------------
    # Scenario A: Text-Only Factual Question
    # -------------------------------------------------------------------------
    print("\n--- Scenario A: Text-Only Factual Question ---")
    resp_a = client.post(
        "/api/chat",
        data={"text": "What are the symptoms of tomato early blight?", "session_id": "session_test_a"},
    )
    assert_test("A.1 HTTP Status 200", resp_a.status_code == 200, f"Status: {resp_a.status_code}")
    data_a = resp_a.json()
    assert_test(
        "A.2 AgriculturalAssistant grounded facts returned",
        "knowledge" in data_a
        and data_a["knowledge"] is not None
        and "concentric" in data_a["message"].lower()
        and data_a["knowledge"]["status"] in ("diseased", "general_info", "valid", "treatment"),
        f"Message: {data_a.get('message', '')[:100]}...",
    )
    assert_test(
        "A.3 Response contract preserved",
        all(k in data_a for k in ("id", "message", "query", "inputs", "router", "model1", "model2", "knowledge")),
    )

    # -------------------------------------------------------------------------
    # Scenario B: Text-Only Treatment Question
    # -------------------------------------------------------------------------
    print("\n--- Scenario B: Text-Only Treatment Question ---")
    resp_b = client.post(
        "/api/chat",
        data={"text": "How do I manage tomato early blight?", "session_id": "session_test_b"},
    )
    assert_test("B.1 HTTP Status 200", resp_b.status_code == 200)
    data_b = resp_b.json()
    assert_test(
        "B.2 Management facts & provenance present",
        "management" in data_b["message"].lower()
        and ("sanitation" in data_b["message"].lower() or "fungicide" in data_b["message"].lower() or "pruning" in data_b["message"].lower())
        and len(data_b.get("knowledge_sources", [])) > 0,
        f"Message: {data_b.get('message', '')[:120]}...",
    )

    # -------------------------------------------------------------------------
    # Scenario C: Image + Diagnosis Question
    # -------------------------------------------------------------------------
    print("\n--- Scenario C: Image + Diagnosis Question ---")
    # Find a real tomato early blight test image
    tomato_eb_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "early_blight"
    eb_images = list(tomato_eb_dir.glob("*.jpg")) + list(tomato_eb_dir.glob("*.png"))
    if not eb_images:
        # Fallback to any test image
        eb_images = list((PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test").glob("**/*.jpg"))

    test_eb_path = eb_images[0]
    with open(test_eb_path, "rb") as f:
        img_bytes = f.read()

    resp_c = client.post(
        "/api/chat",
        data={"text": "what is wrong with my plant?", "session_id": "session_test_c"},
        files={"image_file": ("tomato_eb.jpg", img_bytes, "image/jpeg")},
    )
    assert_test("C.1 HTTP Status 200", resp_c.status_code == 200)
    data_c = resp_c.json()
    assert_test(
        "C.2 Model 1 & Model 2 V4 diagnosis populated",
        data_c["model1"]["predicted_crop"].lower() == "tomato"
        and data_c["model2"]["has_disease"] is True
        and "early_blight" in data_c["model2"]["primary_disease_slug"],
        f"M1: {data_c['model1']['predicted_crop']}, M2: {data_c['model2'].get('primary_disease_slug')}",
    )
    assert_test(
        "C.3 AgriculturalAssistant incorporates visual diagnosis",
        "early blight" in data_c["message"].lower() or "tomato" in data_c["message"].lower(),
        f"Assistant message: {data_c.get('message', '')[:120]}...",
    )

    # -------------------------------------------------------------------------
    # Scenario D: Image + Treatment Question (Follow-up Turn)
    # -------------------------------------------------------------------------
    print("\n--- Scenario D: Image + Treatment Question ---")
    resp_d = client.post(
        "/api/chat",
        data={"text": "how do I treat it?", "session_id": "session_test_c"},
    )
    assert_test("D.1 HTTP Status 200", resp_d.status_code == 200)
    data_d = resp_d.json()
    assert_test(
        "D.2 Session dialogue resolves 'it' to Tomato Early Blight",
        data_d["knowledge"] is not None
        and data_d["knowledge"]["crop"] == "tomato"
        and "early_blight" in (data_d["knowledge"]["disease"] or "")
        and "management" in data_d["message"].lower(),
        f"Resolved Crop: {data_d['knowledge'].get('crop')}, Disease: {data_d['knowledge'].get('disease')}",
    )

    # -------------------------------------------------------------------------
    # Scenario E: Healthy Image (No False Disease Invented)
    # -------------------------------------------------------------------------
    print("\n--- Scenario E: Healthy Image ---")
    tomato_healthy_dir = PROJECT_ROOT / "data" / "processed" / "model2_v4" / "test" / "tomato" / "healthy"
    healthy_images = list(tomato_healthy_dir.glob("*.jpg")) + list(tomato_healthy_dir.glob("*.png"))
    test_healthy_path = healthy_images[0]
    with open(test_healthy_path, "rb") as f:
        healthy_img_bytes = f.read()

    resp_e = client.post(
        "/api/chat",
        data={"text": "Is my plant diseased?", "session_id": "session_test_e"},
        files={"image_file": ("tomato_healthy.jpg", healthy_img_bytes, "image/jpeg")},
    )
    assert_test("E.1 HTTP Status 200", resp_e.status_code == 200)
    data_e = resp_e.json()
    assert_test(
        "E.2 Model 2 outputs healthy contract status='healthy', disease=null",
        data_e["model2"]["status"] == "healthy"
        and data_e["model2"]["primary_disease_slug"] is None,
        f"M2 Status: {data_e['model2']['status']}, Slug: {data_e['model2']['primary_disease_slug']}",
    )
    assert_test(
        "E.3 AgriculturalAssistant does NOT invent disease",
        "healthy" in data_e["message"].lower()
        and ("no symptoms" in data_e["message"].lower() or "appears to be healthy" in data_e["message"].lower())
        and "chemical sprays are not needed" in data_e["message"].lower(),
        f"Assistant message: {data_e.get('message', '')[:120]}...",
    )

    # -------------------------------------------------------------------------
    # Scenario F: Uncertain / Non-Plant Image
    # -------------------------------------------------------------------------
    print("\n--- Scenario F: Uncertain Image ---")
    # Synthetic noise image
    noise_img = Image.fromarray(np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8))
    noise_buf = io.BytesIO()
    noise_img.save(noise_buf, format="JPEG")
    noise_bytes = noise_buf.getvalue()

    resp_f = client.post(
        "/api/chat",
        data={"text": "Diagnose this leaf", "session_id": "session_test_f"},
        files={"image_file": ("noise.jpg", noise_bytes, "image/jpeg")},
    )
    assert_test("F.1 HTTP Status 200", resp_f.status_code == 200)
    data_f = resp_f.json()
    assert_test(
        "F.2 Rejection or uncertain response triggered safely",
        data_f["model1"]["status"] in ("not_plant", "uncertain", "blurry", "valid")
        and ("uncertain" in data_f["message"].lower() or "incompatible" in data_f["message"].lower() or "clarification" in data_f["message"].lower() or "clear" in data_f["message"].lower()),
        f"Assistant message: {data_f.get('message', '')[:120]}...",
    )

    # -------------------------------------------------------------------------
    # Scenario G: Audio + Image Integration
    # -------------------------------------------------------------------------
    print("\n--- Scenario G: Audio + Image Integration ---")
    synthetic_wav = generate_synthetic_wav_bytes(duration_sec=0.5)
    resp_g = client.post(
        "/api/chat",
        data={"session_id": "session_test_g"},
        files={
            "audio_file": ("question.wav", synthetic_wav, "audio/wav"),
            "image_file": ("tomato_eb.jpg", img_bytes, "image/jpeg"),
        },
    )
    assert_test("G.1 HTTP Status 200", resp_g.status_code == 200)
    data_g = resp_g.json()
    assert_test(
        "G.2 Audio transcribed and visual inference executed together",
        data_g["inputs"]["audio"] is True
        and data_g["inputs"]["image"] is True
        and data_g["model1"] is not None
        and "tomato" in str(data_g["model1"].get("predicted_crop", "")).lower(),
        f"Inputs: {data_g['inputs']}, M1: {data_g['model1'].get('predicted_crop')}",
    )

    # -------------------------------------------------------------------------
    # Scenario H: Video + Question Integration
    # -------------------------------------------------------------------------
    print("\n--- Scenario H: Video + Question Integration ---")
    # Generate a small 16-frame synthetic MP4 in memory using cv2
    import cv2
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_vid:
        tmp_vid_path = tmp_vid.name

    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(tmp_vid_path, fourcc, 10.0, (256, 256))
        # Load tomato leaf image to write frames
        leaf_cv = cv2.imread(str(test_eb_path))
        leaf_cv = cv2.resize(leaf_cv, (256, 256))
        for _ in range(16):
            writer.write(leaf_cv)
        writer.release()

        with open(tmp_vid_path, "rb") as f:
            vid_bytes = f.read()

        resp_h = client.post(
            "/api/chat",
            data={"text": "What crop is this video showing?", "session_id": "session_test_h"},
            files={"video_file": ("test_vid.mp4", vid_bytes, "video/mp4")},
        )
        assert_test("H.1 HTTP Status 200", resp_h.status_code == 200)
        data_h = resp_h.json()
        assert_test(
            "H.2 Video frames evaluated and crop passed to assistant",
            data_h["inputs"]["video"] is True
            and data_h["video_inference"] is not None
            and data_h["video_inference"]["predicted_crop"].lower() == "tomato"
            and "tomato" in data_h["message"].lower(),
            f"Video predicted crop: {data_h.get('video_inference', {}).get('predicted_crop')}",
        )
    finally:
        if Path(tmp_vid_path).exists():
            try:
                Path(tmp_vid_path).unlink()
            except OSError:
                pass

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} TESTS PASSED ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 80)
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_phase1_test_suite()
    sys.exit(0 if success else 1)
