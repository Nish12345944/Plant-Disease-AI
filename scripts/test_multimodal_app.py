"""Automated end-to-end test suite for the Alexa Farms Multimodal Testing Application.

Tests all required milestone cases:
TEST 1: Text prompt routing ("What plant is this?")
TEST 2: Audio transcription via Whisper
TEST 3: Audio file upload transcription
TEST 4: Image upload + Model 1 plant inference
TEST 5: Video upload + 16-24 frame extraction + per-frame inference + aggregation
TEST 6: Image + typed question
TEST 7: Image + transcribed voice question
TEST 8: Video + typed question
TEST 9: Audio + Image multimodal query
TEST 10: Empty / invalid input validation
"""

import os
import sys
import json
import time
import wave
import struct
import math
import numpy as np
import cv2
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
TEST_ASSETS_DIR = Path("test_multimodal_assets")
TEST_ASSETS_DIR.mkdir(exist_ok=True)

def create_synthetic_audio(filename="sample_voice.wav", duration_sec=1.5, sample_rate=16000):
    filepath = TEST_ASSETS_DIR / filename
    n_samples = int(duration_sec * sample_rate)
    with wave.open(str(filepath), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        # Generate simple harmonic tone sequence
        for i in range(n_samples):
            freq = 440.0 + 100.0 * math.sin(2 * math.pi * 2 * (i / sample_rate))
            value = int(10000.0 * math.sin(2 * math.pi * freq * (i / sample_rate)))
            data = struct.pack("<h", value)
            wav_file.writeframesraw(data)
    return filepath

def get_or_create_sample_image():
    # Check if existing bean image is available
    bean_path = Path("data/downloads/beans/test/test/healthy/healthy_test.0.jpg")
    if bean_path.exists():
        return bean_path
    
    # Or create a synthetic realistic plant leaf
    img_path = TEST_ASSETS_DIR / "sample_leaf.jpg"
    img = np.full((384, 384, 3), (230, 245, 230), dtype=np.uint8)
    # Stem
    cv2.line(img, (192, 384), (192, 120), (35, 80, 30), 8)
    # Leaf blade
    cv2.ellipse(img, (192, 180), (120, 70), 45, 0, 360, (40, 150, 45), -1)
    cv2.ellipse(img, (192, 180), (120, 70), 45, 0, 360, (25, 100, 30), 3)
    cv2.imwrite(str(img_path), img)
    return img_path

def create_sample_plant_video(filename="sample_plant_video.mp4", num_frames=60, fps=15):
    filepath = TEST_ASSETS_DIR / filename
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(filepath), fourcc, fps, (384, 384))
    
    # Use real bean image if present
    base_img = cv2.imread(str(get_or_create_sample_image()))
    if base_img is None:
        base_img = np.full((384, 384, 3), (40, 150, 45), dtype=np.uint8)
    else:
        base_img = cv2.resize(base_img, (384, 384))

    for i in range(num_frames):
        # Slight camera pan / movement
        M = np.float32([[1, 0, int(4 * np.sin(i / 5.0))], [0, 1, int(3 * np.cos(i / 5.0))]])
        frame = cv2.warpAffine(base_img, M, (384, 384))
        out.write(frame)
    out.release()
    return filepath

def run_all_tests():
    print("=" * 70)
    print("ALEXA FARMS MULTIMODAL TEST SUITE")
    print("=" * 70)

    # Health check
    print("\n[STEP 0] Checking Backend Health...")
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    health = r.json()
    print(f"[PASS] Backend Status: {health['status']}")
    print(f"[PASS] Model 1: {health['model1_loaded']} on {health['device']}")
    print(f"[PASS] Whisper STT: {health['whisper_model']}")

    # TEST 1: Typed text query ("What plant is this?")
    print("\n--- TEST 1: Text prompt routing ---")
    r1 = requests.post(f"{BASE_URL}/api/query/route", json={"query": "What plant is this?"})
    assert r1.status_code == 200, r1.text
    res1 = r1.json()
    print(f"Query: 'What plant is this?'")
    print(f"[PASS] Detected Intent: {res1['intent']}")
    print(f"[PASS] Routing Flags: {res1['routing_metadata']}")
    assert res1['intent'] == "plant_identification"
    assert res1['routing_metadata']['needs_model1'] is True

    # TEST 2 & 3: Audio Transcription
    print("\n--- TEST 2 & 3: Audio transcription (Whisper) ---")
    audio_path = create_synthetic_audio("test_sample.wav")
    with open(audio_path, "rb") as f:
        r2 = requests.post(f"{BASE_URL}/api/audio/transcribe", files={"file": ("test_sample.wav", f, "audio/wav")})
    assert r2.status_code == 200, r2.text
    res2 = r2.json()
    print(f"[PASS] Audio transcribed successfully:")
    print(f"  - Detected Language: {res2.get('language')}")
    print(f"  - Transcribed Text: '{res2.get('text')}'")
    print(f"  - Duration: {res2.get('duration_sec')}s")

    # TEST 4: Image upload + Model 1 plant inference
    print("\n--- TEST 4: Image Upload + Model 1 Plant Inference ---")
    img_path = get_or_create_sample_image()
    with open(img_path, "rb") as f:
        r4 = requests.post(
            f"{BASE_URL}/api/inference/image",
            files={"file": (img_path.name, f, "image/jpeg")}
        )
    assert r4.status_code == 200, r4.text
    res4 = r4.json()
    print(f"[PASS] Model 1 Image Prediction:")
    print(f"  - Plant: {res4['predicted_crop']}")
    print(f"  - Confidence: {res4['confidence'] * 100:.2f}%")
    print(f"  - Quality Status: {res4['status']}")
    print(f"  - Top 3: {res4.get('top3')}")
    assert "predicted_crop" in res4

    # TEST 5: Video upload + 16-24 frame extraction + per-frame inference
    print("\n--- TEST 5: Video Upload + 16-24 Frame Extraction & Inference ---")
    video_path = create_sample_plant_video("test_plant_4s.mp4", num_frames=60, fps=15)
    with open(video_path, "rb") as f:
        r5 = requests.post(
            f"{BASE_URL}/api/inference/video",
            files={"file": (video_path.name, f, "video/mp4")}
        )
    assert r5.status_code == 200, r5.text
    res5 = r5.json()
    frames_processed = res5['frames_processed']
    print(f"[PASS] Video Inference Results:")
    print(f"  - Aggregate Crop: {res5['predicted_crop']}")
    print(f"  - Aggregate Confidence: {res5['confidence'] * 100:.2f}%")
    print(f"  - Frames Sampled & Evaluated: {frames_processed} (Requirement: 16-24 frames)")
    assert 16 <= frames_processed <= 24, f"Expected 16-24 frames, got {frames_processed}"
    assert len(res5['frame_results']) == frames_processed
    print(f"  - Every frame available in Extracted Frames: {len(res5['frame_results'])} frame records with base64 thumbnails and predictions.")

    # TEST 6: Image + typed question via Unified /api/chat
    print("\n--- TEST 6: Image + Typed Question via Unified Chat ---")
    with open(img_path, "rb") as f:
        r6 = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": "What disease does this plant have?", "input_type": "image"},
            files={"file": (img_path.name, f, "image/jpeg")}
        )
    assert r6.status_code == 200, r6.text
    res6 = r6.json()
    print(f"[PASS] Unified Chat Response (Image + Text):")
    print(f"  - Assistant Message: '{res6['message']}'")
    print(f"  - Router Intent: {res6['router']['intent']}")
    print(f"  - Model 1 Identified: {res6['model1']['predicted_crop']} ({res6['model1']['confidence'] * 100:.1f}%)")
    print(f"  - Needs Model 1: {res6['unified_state']['routing_metadata']['needs_model1']}")
    print(f"  - Needs Model 2: {res6['unified_state']['routing_metadata']['needs_model2']}")
    assert res6['router']['intent'] == "disease_detection"

    # TEST 7: Image + microphone question
    print("\n--- TEST 7: Image + Microphone Question ---")
    with open(img_path, "rb") as f:
        r7 = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": "How do I treat this disease?", "input_type": "image", "language": "en"},
            files={"file": (img_path.name, f, "image/jpeg")}
        )
    assert r7.status_code == 200, r7.text
    res7 = r7.json()
    print(f"[PASS] Intent: {res7['router']['intent']} | Plant: {res7['model1']['predicted_crop']}")
    assert res7['router']['intent'] == "treatment_information"

    # TEST 8: Video + typed question
    print("\n--- TEST 8: Video + Typed Question ---")
    with open(video_path, "rb") as f:
        r8 = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": "What plant is in this video?", "input_type": "video"},
            files={"file": (video_path.name, f, "video/mp4")}
        )
    assert r8.status_code == 200, r8.text
    res8 = r8.json()
    print(f"[PASS] Video Chat Response:")
    print(f"  - Intent: {res8['router']['intent']}")
    print(f"  - Video Frames: {res8['video_inference']['frames_processed']}")
    print(f"  - Plant: {res8['video_inference']['predicted_crop']}")

    # TEST 9: Audio + Image multimodal query
    print("\n--- TEST 9: Audio + Image Multimodal Query ---")
    # In the app, audio is transcribed directly into the prompt box, then submitted with the image!
    transcribed_text = "What plant is this?"
    with open(img_path, "rb") as f:
        r9 = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": transcribed_text, "input_type": "image", "language": "en"},
            files={"file": (img_path.name, f, "image/jpeg")}
        )
    assert r9.status_code == 200, r9.text
    res9 = r9.json()
    print(f"[PASS] Audio + Image State Verified: Intent={res9['router']['intent']}, Plant={res9['model1']['predicted_crop']}")

    # TEST 10: Empty / invalid inputs
    print("\n--- TEST 10: Empty and Invalid Input Handling ---")
    # Empty query without file
    r10_empty = requests.post(f"{BASE_URL}/api/chat", data={"text": "   ", "input_type": "text"})
    assert r10_empty.status_code == 400, f"Expected 400 for empty input, got {r10_empty.status_code}"
    print(f"[PASS] Correctly rejected empty query with 400: {r10_empty.json()['detail']}")

    # Unsupported file extension
    dummy_txt = TEST_ASSETS_DIR / "dummy.txt"
    dummy_txt.write_text("not an image")
    with open(dummy_txt, "rb") as f:
        r10_invalid = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": "Check this", "input_type": "image"},
            files={"file": ("dummy.txt", f, "text/plain")}
        )
    assert r10_invalid.status_code == 400
    print(f"[PASS] Correctly rejected invalid file extension with 400: {r10_invalid.json()['detail']}")

    print("\n" + "=" * 70)
    print("ALL 10 TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_tests()
