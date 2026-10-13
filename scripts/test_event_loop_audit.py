"""Test script for FastAPI event-loop responsiveness and bounded concurrency audit."""

from __future__ import annotations

import io
import math
import struct
import threading
import time
import wave
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_synthetic_wav(duration_sec: float = 2.0, freq: float = 440.0) -> bytes:
    """Generate a clean 16kHz mono WAV audio file in-memory."""
    sample_rate = 16000
    num_samples = int(sample_rate * duration_sec)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        for i in range(num_samples):
            # 440 Hz sine wave
            val = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * freq * i / sample_rate))
            wf.writeframes(struct.pack("<h", val))
    return buf.getvalue()


def measure_health_check() -> float:
    """Ping /health and measure response latency in milliseconds."""
    t0 = time.perf_counter()
    resp = requests.get(f"{BASE_URL}/health", timeout=5.0)
    latency_ms = (time.perf_counter() - t0) * 1000
    if resp.status_code != 200:
        raise RuntimeError(f"/health returned HTTP {resp.status_code}")
    return latency_ms


def run_health_monitor(stop_event: threading.Event, latencies: list[float], interval_sec: float = 0.05):
    """Repeatedly ping /health until stopped, recording latency for each ping."""
    while not stop_event.is_set():
        try:
            lat = measure_health_check()
            latencies.append(lat)
        except Exception as exc:
            latencies.append(9999.0)  # Record failure
        time.sleep(interval_sec)


def main():
    print("=" * 70)
    print("FASTAPI EVENT LOOP RESPONSIVENESS & CONCURRENCY BENCHMARK")
    print("=" * 70)

    # 1. Baseline latency
    baseline_lats = [measure_health_check() for _ in range(10)]
    avg_base = sum(baseline_lats) / len(baseline_lats)
    print(f"[1/5] Baseline /health Latency: {avg_base:.2f}ms (min={min(baseline_lats):.2f}ms, max={max(baseline_lats):.2f}ms)")

    # Media fixtures
    wav_bytes = generate_synthetic_wav(duration_sec=2.0)
    img_path = Path("data/downloads/beans/test/test/angular_leaf_spot/angular_leaf_spot_test.0.jpg")
    img_bytes = img_path.read_bytes() if img_path.exists() else None
    vid_path = Path("test_24f_tomato.mp4")
    vid_bytes = vid_path.read_bytes() if vid_path.exists() else None

    # 2. Audio Transcription + Health Monitor
    print("\n[2/5] Testing /api/audio/transcribe with concurrent /health probes...")
    stop_audio = threading.Event()
    audio_lats: list[float] = []
    t_mon = threading.Thread(target=run_health_monitor, args=(stop_audio, audio_lats, 0.05))
    t_mon.start()

    t_start = time.perf_counter()
    resp_audio = requests.post(
        f"{BASE_URL}/api/audio/transcribe",
        files={"file": ("test.wav", wav_bytes, "audio/wav")},
        timeout=30.0,
    )
    t_audio_dur = (time.perf_counter() - t_start) * 1000
    stop_audio.set()
    t_mon.join()

    print(f"  -> Audio finished in {t_audio_dur:.1f}ms (status={resp_audio.status_code})")
    if audio_lats:
        print(f"  -> Concurrently probed /health {len(audio_lats)} times.")
        print(f"  -> /health latencies during Whisper: avg={sum(audio_lats)/len(audio_lats):.2f}ms, min={min(audio_lats):.2f}ms, max={max(audio_lats):.2f}ms")
        assert max(audio_lats) < 500.0, f"Health check blocked during audio! max={max(audio_lats)}ms"
    else:
        print("  -> Warning: No health probes captured during audio.")

    # 3. Image Inference + Health Monitor
    if img_bytes:
        print("\n[3/5] Testing /api/inference/image with concurrent /health probes...")
        stop_img = threading.Event()
        img_lats: list[float] = []
        t_mon = threading.Thread(target=run_health_monitor, args=(stop_img, img_lats, 0.05))
        t_mon.start()

        t_start = time.perf_counter()
        resp_img = requests.post(
            f"{BASE_URL}/api/inference/image",
            files={"file": ("plant.jpg", img_bytes, "image/jpeg")},
            timeout=30.0,
        )
        t_img_dur = (time.perf_counter() - t_start) * 1000
        stop_img.set()
        t_mon.join()

        print(f"  -> Image inference finished in {t_img_dur:.1f}ms (status={resp_img.status_code})")
        if img_lats:
            print(f"  -> Concurrently probed /health {len(img_lats)} times.")
            print(f"  -> /health latencies during Image Inference: avg={sum(img_lats)/len(img_lats):.2f}ms, min={min(img_lats):.2f}ms, max={max(img_lats):.2f}ms")
            assert max(img_lats) < 500.0, f"Health check blocked during image inference! max={max(img_lats)}ms"

    # 4. Multimodal Chat Endpoint + Health Monitor
    print("\n[4/5] Testing /api/chat (multimodal query) with concurrent /health probes...")
    stop_chat = threading.Event()
    chat_lats: list[float] = []
    t_mon = threading.Thread(target=run_health_monitor, args=(stop_chat, chat_lats, 0.05))
    t_mon.start()

    t_start = time.perf_counter()
    files_payload = {}
    if img_bytes:
        files_payload["image_file"] = ("leaf.jpg", img_bytes, "image/jpeg")
    files_payload["audio_file"] = ("question.wav", wav_bytes, "audio/wav")

    resp_chat = requests.post(
        f"{BASE_URL}/api/chat",
        data={"text": "How do I treat this disease?"},
        files=files_payload,
        timeout=30.0,
    )
    t_chat_dur = (time.perf_counter() - t_start) * 1000
    stop_chat.set()
    t_mon.join()

    print(f"  -> Chat response in {t_chat_dur:.1f}ms (status={resp_chat.status_code})")
    if chat_lats:
        print(f"  -> Concurrently probed /health {len(chat_lats)} times.")
        print(f"  -> /health latencies during Chat: avg={sum(chat_lats)/len(chat_lats):.2f}ms, min={min(chat_lats):.2f}ms, max={max(chat_lats):.2f}ms")
        assert max(chat_lats) < 500.0, f"Health check blocked during chat! max={max(chat_lats)}ms"

    # 5. Combined Stress Test: Multiple Concurrent Media Inferences + Health Check
    print("\n[5/5] Full Concurrency Test: Audio + Image + Chat executing simultaneously...")
    stop_stress = threading.Event()
    stress_lats: list[float] = []
    t_mon = threading.Thread(target=run_health_monitor, args=(stop_stress, stress_lats, 0.05))
    t_mon.start()

    results = {}
    def call_audio():
        r = requests.post(f"{BASE_URL}/api/audio/transcribe", files={"file": ("t.wav", wav_bytes, "audio/wav")})
        results["audio"] = r.status_code

    def call_image():
        r = requests.post(f"{BASE_URL}/api/inference/image", files={"file": ("p.jpg", img_bytes, "image/jpeg")})
        results["image"] = r.status_code

    def call_chat():
        r = requests.post(f"{BASE_URL}/api/chat", data={"text": "Diagnose my crop"})
        results["chat"] = r.status_code

    th1 = threading.Thread(target=call_audio)
    th2 = threading.Thread(target=call_image)
    th3 = threading.Thread(target=call_chat)

    t0_stress = time.perf_counter()
    th1.start()
    th2.start()
    th3.start()
    th1.join()
    th2.join()
    th3.join()
    t_total_stress = (time.perf_counter() - t0_stress) * 1000
    stop_stress.set()
    t_mon.join()

    print(f"  -> Concurrent batch finished in {t_total_stress:.1f}ms: results={results}")
    if stress_lats:
        print(f"  -> Concurrently probed /health {len(stress_lats)} times.")
        print(f"  -> /health latencies under full concurrent load: avg={sum(stress_lats)/len(stress_lats):.2f}ms, min={min(stress_lats):.2f}ms, max={max(stress_lats):.2f}ms")
        assert max(stress_lats) < 500.0, f"Health check blocked during stress test! max={max(stress_lats)}ms"

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED: Event loop remained completely non-blocking!")
    print("=" * 70)


if __name__ == "__main__":
    main()
