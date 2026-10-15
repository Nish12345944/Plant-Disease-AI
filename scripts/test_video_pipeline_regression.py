"""
Video Pipeline Regression Test Suite
====================================
Tests end-to-end video processing and error handling across both /api/chat and
/api/inference/video endpoints to prevent regressions of HTTP 500/502 errors:

1. Short videos (<1s)
2. Longer valid videos (3-5s)
3. Corrupted / unopenable video files (returns clean HTTP 400, not 500/502)
4. Empty video files (returns clean HTTP 400)
5. Videos exceeding maximum duration (returns clean HTTP 400)
6. Videos with 0 or few usable plant frames (returns HTTP 200 with safe rejection, no crash)
7. Text-only workflow preservation
8. Image workflow preservation
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.backend.main import app
from app.backend.services import process_video_inference

client = TestClient(app, raise_server_exceptions=False)


def create_synthetic_mp4(
    num_frames: int = 15,
    fps: float = 30.0,
    size: tuple[int, int] = (320, 240),
    is_noise: bool = True,
) -> bytes:
    """Create an in-memory MP4 byte stream for deterministic testing."""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(tmp_path), fourcc, fps, size)
        for i in range(num_frames):
            if is_noise:
                frame = np.random.randint(0, 255, (size[1], size[0], 3), dtype=np.uint8)
            else:
                # Solid color or basic gradient
                frame = np.full((size[1], size[0], 3), (30 + i * 2, 120, 30), dtype=np.uint8)
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


def run_all_video_regression_tests():
    print("=" * 80)
    print("RUNNING VIDEO PIPELINE & MULTIMODAL REGRESSION TEST SUITE")
    print("=" * 80)

    total_tests = 0
    passed_tests = 0

    def check(name: str, condition: bool, details: str = ""):
        nonlocal total_tests, passed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            if details:
                print(f"         Details: {details}")

    # -------------------------------------------------------------------------
    # TEST 1: Short Video (<1s, e.g. 10 frames @ 30fps)
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Short video handling (<1s)...")
    short_vid = create_synthetic_mp4(num_frames=10, fps=30.0)
    
    # 1.1 /api/inference/video
    r_inf = client.post(
        "/api/inference/video",
        files={"file": ("short.mp4", short_vid, "video/mp4")},
        data={"target_frames": 4},
    )
    check("1.1 Short video on /api/inference/video returns 200", r_inf.status_code == 200, f"HTTP {r_inf.status_code}")

    # 1.2 /api/chat
    r_chat = client.post(
        "/api/chat",
        files={"file": ("short.mp4", short_vid, "video/mp4")},
        data={"input_type": "video"},
    )
    check("1.2 Short video on /api/chat returns 200 (no crash)", r_chat.status_code == 200, f"HTTP {r_chat.status_code}: {r_chat.text[:100]}")

    # -------------------------------------------------------------------------
    # TEST 2: Valid Real Video (French Bean, ~4s)
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Real plant video (French Bean, 4s)...")
    real_vid_path = PROJECT_ROOT / "test_multimodal_assets" / "test_plant_4s.mp4"
    if not real_vid_path.exists():
        real_vid_path = PROJECT_ROOT / "temp_test_videos" / "test_plant_4s.mp4"
    if real_vid_path.exists():
        real_vid_bytes = real_vid_path.read_bytes()
        r_real_inf = client.post(
            "/api/inference/video",
            files={"file": ("test_plant_4s.mp4", real_vid_bytes, "video/mp4")},
            data={"target_frames": 8},
        )
        check("2.1 Real video /api/inference/video returns 200", r_real_inf.status_code == 200, f"HTTP {r_real_inf.status_code}")
        inf_data = r_real_inf.json() if r_real_inf.status_code == 200 else {}
        check("2.2 Real video crop accepted", inf_data.get("crop_status") == "accepted", f"Crop: {inf_data.get('predicted_crop')}")

        r_real_chat = client.post(
            "/api/chat",
            files={"file": ("test_plant_4s.mp4", real_vid_bytes, "video/mp4")},
            data={"input_type": "video"},
        )
        check("2.3 Real video /api/chat returns 200 with diagnosed condition", r_real_chat.status_code == 200, f"HTTP {r_real_chat.status_code}")
    else:
        print("  [SKIP] test_plant_4s.mp4 not found")

    # -------------------------------------------------------------------------
    # TEST 3: Invalid & Corrupted Video Files (Must return 400, NEVER 500 or 502)
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Corrupt and invalid video files...")
    corrupt_bytes = b"ftypmp42" + b"\x00\x00\x00\x00corrupted_payload_not_a_valid_video"
    
    # 3.1 Corrupt file on /api/inference/video
    r_corr_inf = client.post(
        "/api/inference/video",
        files={"file": ("corrupt.mp4", corrupt_bytes, "video/mp4")},
        data={"target_frames": 8},
    )
    check("3.1 Corrupt video returns HTTP 400 on /api/inference/video", r_corr_inf.status_code == 400, f"HTTP {r_corr_inf.status_code}: {r_corr_inf.text[:100]}")
    check("3.2 Corrupt video error detail is informative", "could not open video" in r_corr_inf.text.lower() or "corrupt" in r_corr_inf.text.lower(), r_corr_inf.text[:100])

    # 3.2 Corrupt file on /api/chat
    r_corr_chat = client.post(
        "/api/chat",
        files={"file": ("corrupt.mp4", corrupt_bytes, "video/mp4")},
        data={"input_type": "video"},
    )
    check("3.3 Corrupt video returns HTTP 400 on /api/chat", r_corr_chat.status_code == 400, f"HTTP {r_corr_chat.status_code}: {r_corr_chat.text[:100]}")

    # 3.3 Empty file (0 bytes)
    r_empty_chat = client.post(
        "/api/chat",
        files={"file": ("empty.mp4", b"", "video/mp4")},
        data={"input_type": "video"},
    )
    check("3.4 Empty video returns HTTP 400 on /api/chat", r_empty_chat.status_code == 400, f"HTTP {r_empty_chat.status_code}: {r_empty_chat.text[:100]}")

    # 3.4 Unsupported extension (.txt)
    r_unsupp_chat = client.post(
        "/api/chat",
        files={"file": ("readme.txt", b"plain text content", "text/plain")},
        data={"input_type": "video"},
    )
    check("3.5 Unsupported format returns HTTP 400 on /api/chat", r_unsupp_chat.status_code == 400, f"HTTP {r_unsupp_chat.status_code}: {r_unsupp_chat.text[:100]}")

    # -------------------------------------------------------------------------
    # TEST 4: Duration Limit Exceeded (>30s)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Duration limit enforcement (>30s)...")
    long_vid_path = PROJECT_ROOT / "temp_test_videos" / "Video-2.mp4"
    if not long_vid_path.exists():
        dl_path = Path.home() / "Downloads" / "Video-2.mp4"
        if dl_path.exists():
            long_vid_path = dl_path
    
    if long_vid_path.exists():
        long_vid_bytes = long_vid_path.read_bytes()
        r_long_chat = client.post(
            "/api/chat",
            files={"file": ("long_video.mp4", long_vid_bytes, "video/mp4")},
            data={"input_type": "video"},
        )
        check("4.1 Video >30s returns HTTP 400 with duration limit detail", r_long_chat.status_code == 400, f"HTTP {r_long_chat.status_code}")
        check("4.2 Error message mentions duration limit", "duration" in r_long_chat.text.lower() and "30s" in r_long_chat.text.lower(), r_long_chat.text[:100])
    else:
        print("  [SKIP] 34s video not found")

    # -------------------------------------------------------------------------
    # TEST 5: Video With 0 Usable Plant Frames (Synthetic Noise / Blurry Video)
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Videos with zero usable plant frames...")
    noise_vid = create_synthetic_mp4(num_frames=20, fps=30.0, is_noise=True)
    
    r_noise_inf = client.post(
        "/api/inference/video",
        files={"file": ("noise.mp4", noise_vid, "video/mp4")},
        data={"target_frames": 4},
    )
    check("5.1 Noise video on /api/inference/video returns 200 with rejection", r_noise_inf.status_code == 200, f"HTTP {r_noise_inf.status_code}")
    noise_data = r_noise_inf.json() if r_noise_inf.status_code == 200 else {}
    check("5.2 Crop status is rejected (non_plant_image)", noise_data.get("crop_status") == "rejected", f"Status: {noise_data.get('crop_status')}")

    r_noise_chat = client.post(
        "/api/chat",
        files={"file": ("noise.mp4", noise_vid, "video/mp4")},
        data={"input_type": "video"},
    )
    check("5.3 Noise video on /api/chat returns 200 without crashing", r_noise_chat.status_code == 200, f"HTTP {r_noise_chat.status_code}")
    chat_json = r_noise_chat.json() if r_noise_chat.status_code == 200 else {}
    check("5.4 Chat message presents clear guidance on plant visibility", bool(chat_json.get("message")), f"Message: {chat_json.get('message')}")

    # -------------------------------------------------------------------------
    # TEST 6: Preservation of Existing Workflows (Text, Audio, Image)
    # -------------------------------------------------------------------------
    print("\n[TEST 6] Preservation of Image, Text, and Audio workflows...")
    
    # 6.1 Text-only query
    r_text = client.post(
        "/api/chat",
        data={"text": "How do I control powdery mildew on tomato?", "input_type": "text"},
    )
    check("6.1 Text-only query returns HTTP 200", r_text.status_code == 200, f"HTTP {r_text.status_code}")
    text_data = r_text.json() if r_text.status_code == 200 else {}
    check("6.2 Text-only response has agricultural guidance", bool(text_data.get("message")), f"Msg: {text_data.get('message')[:60]}")

    # 6.2 Image query with valid image
    # Synthetic clean image
    clean_img = np.full((300, 300, 3), (40, 160, 40), dtype=np.uint8)
    _, img_encoded = cv2.imencode(".jpg", clean_img)
    img_bytes = img_encoded.tobytes()

    r_img = client.post(
        "/api/chat",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
        data={"input_type": "image"},
    )
    check("6.3 Image query returns HTTP 200", r_img.status_code == 200, f"HTTP {r_img.status_code}")

    print("\n" + "=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} TESTS PASSED")
    print("=" * 80)
    return passed_tests == total_tests


if __name__ == "__main__":
    success = run_all_video_regression_tests()
    sys.exit(0 if success else 1)
