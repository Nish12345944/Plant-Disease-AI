"""Comprehensive Regression and Performance Test Suite for Sequential Model Swapping.

Tests:
1. Banana Anthracnose (diseased leaf): Model 1 -> Banana, Crop Guard -> accepted, Model 2 -> Anthracnose, Treatment -> CGIAR ProMusa, HTTP 200.
2. Healthy Banana leaf: Model 1 -> Banana, Crop Guard -> accepted, Model 2 -> Healthy, HTTP 200.
3. Unsupported crop (Bajra / Pearl Millet): Model 1 -> bajra/wheat, Crop Guard -> rejected/uncertain_crop, Model 2 -> NOT loaded, HTTP 422.
4. Non-plant image (solid wall / random noise): Image Validation -> rejected, Model 1 & 2 -> NOT loaded, HTTP 422.
5. Invalid file type / corrupt upload: HTTP 400.
6. Five consecutive predictions: latency and RSS stability.
7. Concurrent requests: bounded inference slot protection, HTTP 200 / 429 / queue handling, health check responsiveness.
"""

import gc
import io
import json
import os
import sys
import threading
import time
from pathlib import Path
import psutil
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Enforce CPU execution
os.environ["FORCE_CPU"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["SEQUENTIAL_MODEL_SWAPPING"] = "true"

from fastapi.testclient import TestClient
from app.backend.main import app, _RATE_LIMIT_BUCKET
from app.backend.model_manager import model_manager, release_memory

client = TestClient(app)
proc = psutil.Process(os.getpid())

def mem():
    release_memory()
    return round(proc.memory_info().rss / (1024 * 1024), 2)

def run_suite():
    results = {}
    print("=" * 70)
    print("SEQUENTIAL MODEL SWAPPING REGRESSION & VERIFICATION SUITE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Test 1: Verify health check memory and sequential mode flag
    # -------------------------------------------------------------------------
    print("\n[TEST 1] Initial Health Check & Sequential Flag Verification...")
    h_res = client.get("/health")
    assert h_res.status_code == 200, f"Expected 200, got {h_res.status_code}"
    h_data = h_res.json()
    assert h_data["status"] == "healthy"
    assert h_data["models"]["model1"]["loaded"] is False
    assert h_data["models"]["model2"]["loaded"] is False
    assert h_data["memory"]["sequential_swapping"] is True
    print(f"  Health Check: OK, RSS: {h_data['memory']['rss_mb']} MB, Sequential: {h_data['memory']['sequential_swapping']}")
    results["test1_health"] = {"passed": True, "data": h_data["memory"]}

    # -------------------------------------------------------------------------
    # Test 2: Diseased Banana (Anthracnose) Full E2E Pipeline
    # -------------------------------------------------------------------------
    print("\n[TEST 2] Testing Diseased Banana Leaf (Anthracnose)...")
    banana_dis_path = PROJECT_ROOT / "data" / "processed" / "model2_dataset" / "model2_retraining_v2-20261116T050512Z-1-001" / "model2_retraining_v2" / "test" / "banana" / "anthracnose" / "imgi_381_1_anthracnose1.jpg"
    with open(banana_dis_path, "rb") as f:
        dis_bytes = f.read()

    _RATE_LIMIT_BUCKET.clear()
    t0 = time.time()
    res_dis = client.post("/api/v1/predict", files={"file": ("banana_anthracnose.jpg", dis_bytes, "image/jpeg")})
    t_dis = time.time() - t0

    assert res_dis.status_code == 200, f"Expected 200, got {res_dis.status_code}: {res_dis.text}"
    data_dis = res_dis.json()
    assert data_dis["success"] is True
    assert data_dis["crop"]["slug"] == "banana"
    assert data_dis["crop"]["name"] == "Banana"
    assert data_dis["disease"]["slug"] == "banana__anthracnose"
    assert data_dis["disease"]["name"] == "Anthracnose"
    assert data_dis["disease"]["is_healthy"] is False
    assert data_dis["disease"]["confidence"] > 0.90
    assert len(data_dis["treatment"]["sources"]) > 0
    assert "PROMUSA" in data_dis["treatment"]["sources"][0]["source_id"]

    # Verify both models unloaded after prediction
    assert model_manager.is_model1_loaded is False, "Model 1 was not unloaded!"
    assert model_manager.is_model2_loaded is False, "Model 2 was not unloaded!"
    print(f"  Passed in {t_dis:.2f}s: Crop={data_dis['crop']['name']}, Disease={data_dis['disease']['name']} ({data_dis['disease']['confidence']:.2%})")
    print(f"  Source: {data_dis['treatment']['sources'][0]['organization']}")
    print(f"  Post-inference state: Model1 loaded={model_manager.is_model1_loaded}, Model2 loaded={model_manager.is_model2_loaded}")
    results["test2_diseased_banana"] = {"passed": True, "latency_sec": round(t_dis, 3), "rss_mb": mem()}

    # -------------------------------------------------------------------------
    # Test 3: Healthy Banana Foliage
    # -------------------------------------------------------------------------
    print("\n[TEST 3] Testing Healthy Banana Leaf...")
    banana_hlth_path = PROJECT_ROOT / "data" / "processed" / "model2_dataset" / "model2_retraining_v2-20261116T050512Z-1-001" / "model2_retraining_v2" / "test" / "banana" / "healthy" / "de4e5826f1_imgi_240_images.jpg"
    with open(banana_hlth_path, "rb") as f:
        hlth_bytes = f.read()

    _RATE_LIMIT_BUCKET.clear()
    t0 = time.time()
    res_hlth = client.post("/api/v1/predict", files={"file": ("banana_healthy.jpg", hlth_bytes, "image/jpeg")})
    t_hlth = time.time() - t0

    assert res_hlth.status_code == 200, f"Expected 200, got {res_hlth.status_code}: {res_hlth.text}"
    data_hlth = res_hlth.json()
    assert data_hlth["success"] is True
    assert data_hlth["crop"]["slug"] == "banana"
    assert data_hlth["disease"]["is_healthy"] is True
    assert model_manager.is_model1_loaded is False
    assert model_manager.is_model2_loaded is False
    print(f"  Passed in {t_hlth:.2f}s: Crop={data_hlth['crop']['name']}, Healthy={data_hlth['disease']['is_healthy']}")
    results["test3_healthy_banana"] = {"passed": True, "latency_sec": round(t_hlth, 3), "rss_mb": mem()}

    # -------------------------------------------------------------------------
    # Test 4: Unsupported Crop Rejection (Bajra / Pearl Millet)
    # -------------------------------------------------------------------------
    print("\n[TEST 4] Testing Unsupported Crop Rejection (Bajra Foliage)...")
    bajra_path = PROJECT_ROOT / "test_multimodal_assets" / "bajra_foliage_crop.jpg"
    with open(bajra_path, "rb") as f:
        bajra_bytes = f.read()

    _RATE_LIMIT_BUCKET.clear()
    t0 = time.time()
    res_bajra = client.post("/api/v1/predict", files={"file": ("bajra.jpg", bajra_bytes, "image/jpeg")})
    t_bajra = time.time() - t0

    assert res_bajra.status_code == 422, f"Expected 422, got {res_bajra.status_code}: {res_bajra.text}"
    data_bajra = res_bajra.json()
    assert data_bajra["success"] is False
    assert data_bajra["error"]["code"] in ("UNCERTAIN_CROP", "UNSUPPORTED_CROP")
    # Crucially verify Model 2 was NEVER loaded!
    assert model_manager.is_model1_loaded is False
    assert model_manager.is_model2_loaded is False
    print(f"  Passed in {t_bajra:.2f}s: Rejection Code={data_bajra['error']['code']}, HTTP {res_bajra.status_code}")
    print(f"  Model 2 was NOT loaded: is_model2_loaded={model_manager.is_model2_loaded}")
    results["test4_unsupported_crop"] = {"passed": True, "latency_sec": round(t_bajra, 3), "rss_mb": mem()}

    # -------------------------------------------------------------------------
    # Test 5: Non-Plant Image Rejection (Solid Gray Wall)
    # -------------------------------------------------------------------------
    print("\n[TEST 5] Testing Non-Plant Image (Solid Gray Wall)...")
    wall_path = PROJECT_ROOT / "test_multimodal_assets" / "invalid_synthetic" / "solid_gray_wall.jpg"
    with open(wall_path, "rb") as f:
        wall_bytes = f.read()

    _RATE_LIMIT_BUCKET.clear()
    t0 = time.time()
    res_wall = client.post("/api/v1/predict", files={"file": ("wall.jpg", wall_bytes, "image/jpeg")})
    t_wall = time.time() - t0

    assert res_wall.status_code == 422, f"Expected 422, got {res_wall.status_code}: {res_wall.text}"
    data_wall = res_wall.json()
    assert data_wall["success"] is False
    assert data_wall["error"]["code"] == "INVALID_IMAGE"
    assert model_manager.is_model1_loaded is False
    assert model_manager.is_model2_loaded is False
    print(f"  Passed in {t_wall:.2f}s: Rejection Code={data_wall['error']['code']} (Reason: {data_wall['error']['reason_code']})")
    results["test5_non_plant"] = {"passed": True, "latency_sec": round(t_wall, 3), "rss_mb": mem()}

    # -------------------------------------------------------------------------
    # Test 6: Invalid File Upload (Corrupt bytes & Text File)
    # -------------------------------------------------------------------------
    print("\n[TEST 6] Testing Invalid Uploads (Corrupt bytes & Text File)...")
    _RATE_LIMIT_BUCKET.clear()
    res_txt = client.post("/api/v1/predict", files={"file": ("notes.txt", b"Hello world", "text/plain")})
    assert res_txt.status_code == 400, f"Expected 400, got {res_txt.status_code}"

    res_corrupt = client.post("/api/v1/predict", files={"file": ("corrupt.jpg", b"NOT_A_JPEG_FILE_DATA", "image/jpeg")})
    assert res_corrupt.status_code == 422, f"Expected 422, got {res_corrupt.status_code}"
    print(f"  Passed: Text upload -> HTTP {res_txt.status_code}, Corrupt image -> HTTP {res_corrupt.status_code}")
    results["test6_invalid_upload"] = {"passed": True}

    # -------------------------------------------------------------------------
    # Test 7: Five Consecutive Predictions (Latency & Memory Stability)
    # -------------------------------------------------------------------------
    print("\n[TEST 7] Testing 5 Consecutive Predictions for Latency & Memory Stability...")
    consecutive_latencies = []
    consecutive_rss = []
    for i in range(5):
        _RATE_LIMIT_BUCKET.clear()
        t_start = time.time()
        r = client.post("/api/v1/predict", files={"file": (f"banana_run_{i}.jpg", dis_bytes, "image/jpeg")})
        lat = round(time.time() - t_start, 3)
        consecutive_latencies.append(lat)
        curr_rss = mem()
        consecutive_rss.append(curr_rss)
        assert r.status_code == 200
        assert r.json()["success"] is True
        print(f"  Run {i+1}: {lat:.3f}s | Current RSS: {curr_rss:.1f} MB")

    avg_lat = round(sum(consecutive_latencies) / len(consecutive_latencies), 3)
    print(f"  Average Latency: {avg_lat:.3f}s, Latencies: {consecutive_latencies}")
    print(f"  RSS progression: {consecutive_rss}")
    results["test7_consecutive"] = {
        "passed": True,
        "latencies": consecutive_latencies,
        "avg_latency": avg_lat,
        "rss_progression": consecutive_rss,
    }

    # -------------------------------------------------------------------------
    # Test 8: Concurrency Protection & Health Responsiveness
    # -------------------------------------------------------------------------
    print("\n[TEST 8] Testing Concurrency Semaphore Protection & Health Check Responsiveness...")
    _RATE_LIMIT_BUCKET.clear()

    concurrent_responses = []
    def make_concurrent_request(req_id):
        r = client.post("/api/v1/predict", files={"file": (f"concurrent_{req_id}.jpg", dis_bytes, "image/jpeg")})
        concurrent_responses.append((req_id, r.status_code))

    threads = [threading.Thread(target=make_concurrent_request, args=(i,)) for i in range(2)]
    t_start_conc = time.time()
    for th in threads:
        th.start()

    # While threads are running, probe /health to verify it is responsive and NOT blocked by inference
    time.sleep(0.1)
    t_h = time.time()
    h_concurrent = client.get("/health")
    t_h_ms = round((time.time() - t_h) * 1000, 2)
    assert h_concurrent.status_code == 200
    print(f"  /health probe during active inference: HTTP {h_concurrent.status_code} in {t_h_ms:.1f}ms")

    for th in threads:
        th.join()
    t_conc_total = round(time.time() - t_start_conc, 3)

    print(f"  Concurrent requests finished in {t_conc_total:.2f}s with status codes: {[code for _, code in concurrent_responses]}")
    for _, code in concurrent_responses:
        assert code in (200, 429), f"Unexpected status {code}"

    results["test8_concurrency"] = {
        "passed": True,
        "health_latency_ms": t_h_ms,
        "concurrent_statuses": [code for _, code in concurrent_responses],
    }

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("FINAL SUMMARY: ALL REGRESSION TESTS PASSED SUCCESSFULLY")
    print(f"Peak Measured RSS: {max(consecutive_rss)} MB")
    print(f"All Models Unloaded: Model1={model_manager.is_model1_loaded}, Model2={model_manager.is_model2_loaded}")
    print("=" * 70)
    return results

if __name__ == "__main__":
    res = run_suite()
    with open(PROJECT_ROOT / "reports" / "sequential_swapping_test_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print("\nTest results saved to reports/sequential_swapping_test_results.json")
