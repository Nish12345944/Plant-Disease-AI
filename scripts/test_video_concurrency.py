"""Test video inference endpoint responsiveness with concurrent /health checks."""

from __future__ import annotations

import threading
import time
from pathlib import Path
import requests

BASE_URL = "http://127.0.0.1:8000"

def measure_health_check() -> float:
    t0 = time.perf_counter()
    resp = requests.get(f"{BASE_URL}/health", timeout=5.0)
    return (time.perf_counter() - t0) * 1000

def run_health_monitor(stop_event: threading.Event, latencies: list[float]):
    while not stop_event.is_set():
        try:
            lat = measure_health_check()
            latencies.append(lat)
        except Exception:
            latencies.append(9999.0)
        time.sleep(0.1)

def main():
    vid_path = Path("test_24f_tomato.mp4")
    if not vid_path.exists():
        print("Video file not found.")
        return

    vid_bytes = vid_path.read_bytes()
    print(f"Testing /api/inference/video ({len(vid_bytes)/1024/1024:.2f} MB)...")

    stop_event = threading.Event()
    latencies: list[float] = []
    t_mon = threading.Thread(target=run_health_monitor, args=(stop_event, latencies))
    t_mon.start()

    t0 = time.perf_counter()
    resp = requests.post(
        f"{BASE_URL}/api/inference/video",
        files={"file": ("video.mp4", vid_bytes, "video/mp4")},
        data={"target_frames": "6"},
        timeout=120.0,
    )
    duration = (time.perf_counter() - t0) * 1000
    stop_event.set()
    t_mon.join()

    print(f"Video endpoint returned HTTP {resp.status_code} in {duration:.1f}ms")
    if latencies:
        print(f"Probed /health {len(latencies)} times during video inference.")
        print(f"/health stats: avg={sum(latencies)/len(latencies):.2f}ms, min={min(latencies):.2f}ms, max={max(latencies):.2f}ms")
        assert max(latencies) < 500.0, f"Health check blocked during video! max={max(latencies)}ms"
    print("Video concurrency test passed!")

if __name__ == "__main__":
    main()
