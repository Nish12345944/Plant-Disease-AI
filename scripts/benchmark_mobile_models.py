"""
Benchmark Script: Mobile ONNX vs PyTorch Latency, Size, and Throughput
======================================================================
Measures file sizes, CPU latency, Desktop GPU latency (warmup + 50 iterations),
median, average, p95, min, max, and throughput.
"""

import os
import sys
import time
import json
from pathlib import Path
import numpy as np
import torch
import onnxruntime as ort

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



def benchmark_pytorch(model: torch.nn.Module, input_tensor: torch.Tensor, device_str: str, num_iters: int = 50, warmup: int = 10):
    device = torch.device(device_str)
    model = model.to(device)
    model.eval()
    inp = input_tensor.to(device)

    # Warmup
    with torch.no_grad():
        for _ in range(warmup):
            _ = model(inp)
            if device.type == "cuda":
                torch.cuda.synchronize()

    times = []
    with torch.no_grad():
        for _ in range(num_iters):
            if device.type == "cuda":
                torch.cuda.synchronize()
            t0 = time.perf_counter()
            _ = model(inp)
            if device.type == "cuda":
                torch.cuda.synchronize()
            t1 = time.perf_counter()
            times.append((t1 - t0) * 1000.0)  # ms

    return {
        "avg_ms": float(np.mean(times)),
        "median_ms": float(np.median(times)),
        "p95_ms": float(np.percentile(times, 95)),
        "min_ms": float(np.min(times)),
        "max_ms": float(np.max(times)),
        "throughput_fps": float(1000.0 / np.mean(times)),
    }


def benchmark_onnx(onnx_path: Path, input_np: np.ndarray, provider: str, num_iters: int = 50, warmup: int = 10):
    opts = ort.SessionOptions()
    opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess = ort.InferenceSession(str(onnx_path), opts, providers=[provider])
    input_name = sess.get_inputs()[0].name

    # Warmup
    for _ in range(warmup):
        _ = sess.run(None, {input_name: input_np})

    times = []
    for _ in range(num_iters):
        t0 = time.perf_counter()
        _ = sess.run(None, {input_name: input_np})
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0)

    return {
        "avg_ms": float(np.mean(times)),
        "median_ms": float(np.median(times)),
        "p95_ms": float(np.percentile(times, 95)),
        "min_ms": float(np.min(times)),
        "max_ms": float(np.max(times)),
        "throughput_fps": float(1000.0 / np.mean(times)),
    }


def run_benchmarks():
    print("=" * 80)
    print("STARTING MOBILE MODEL BENCHMARK SUITE")
    print("=" * 80)

    from scripts.validate_onnx_models import load_pytorch_model1, load_pytorch_model2

    # Check CUDA availability for Desktop benchmarks
    cuda_available = torch.cuda.is_available()
    cuda_provider = "CUDAExecutionProvider" if cuda_available and "CUDAExecutionProvider" in ort.get_available_providers() else None

    print(f"Hardware Info:")
    print(f"  CPU Threads : {os.cpu_count()}")
    print(f"  CUDA GPU    : {torch.cuda.get_device_name(0) if cuda_available else 'None'}")
    print(f"  ORT Providers: {ort.get_available_providers()}")

    bench_results = {}

    # -------------------------------------------------------------------------
    # 1. Model 1 Benchmarking
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("BENCHMARKING MODEL 1 (Crop Classifier, 22 Classes, Input: 224x224)")
    print("-" * 80)
    
    m1_py, _ = load_pytorch_model1()
    m1_t = torch.randn(1, 3, 224, 224, dtype=torch.float32)
    m1_np = m1_t.numpy()
    m1_mobile_dir = PROJECT_ROOT / "models" / "model1" / "mobile"

    m1_files = {
        "PyTorch FP32": PROJECT_ROOT / "models" / "model1" / "best_model.pth",
        "ONNX FP32": m1_mobile_dir / "model1_fp32.onnx",
        "ONNX FP16": m1_mobile_dir / "model1_fp16.onnx",
        "ONNX INT8": m1_mobile_dir / "model1_int8.onnx",
    }

    m1_data = {}
    for name, path in m1_files.items():
        size_mb = path.stat().st_size / (1024 * 1024)
        if name == "PyTorch FP32":
            cpu_bench = benchmark_pytorch(m1_py, m1_t, "cpu")
            gpu_bench = benchmark_pytorch(m1_py, m1_t, "cuda") if cuda_available else None
        else:
            cpu_bench = benchmark_onnx(path, m1_np, "CPUExecutionProvider")
            gpu_bench = benchmark_onnx(path, m1_np, "CUDAExecutionProvider") if cuda_provider else None

        m1_data[name] = {
            "size_mb": round(size_mb, 2),
            "cpu": cpu_bench,
            "gpu": gpu_bench,
        }
        print(f"[{name:<12}] Size: {size_mb:6.2f} MB | CPU Avg: {cpu_bench['avg_ms']:6.2f} ms | P95: {cpu_bench['p95_ms']:6.2f} ms | FPS: {cpu_bench['throughput_fps']:5.1f}")
        if gpu_bench:
            print(f"              Desktop GPU Avg: {gpu_bench['avg_ms']:6.2f} ms | P95: {gpu_bench['p95_ms']:6.2f} ms | FPS: {gpu_bench['throughput_fps']:5.1f}")

    bench_results["model1"] = m1_data

    # -------------------------------------------------------------------------
    # 2. Model 2 V2 Benchmarking
    # -------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("BENCHMARKING MODEL 2 V2 (Disease Classifier, 117 Classes, Input: 260x260)")
    print("-" * 80)

    m2_py, _ = load_pytorch_model2()
    m2_t = torch.randn(1, 3, 260, 260, dtype=torch.float32)
    m2_np = m2_t.numpy()
    m2_mobile_dir = PROJECT_ROOT / "models" / "model2_classifier_v2" / "mobile"

    m2_files = {
        "PyTorch FP32": PROJECT_ROOT / "models" / "model2_classifier_v2" / "best_model.pth",
        "ONNX FP32": m2_mobile_dir / "model2_fp32.onnx",
        "ONNX FP16": m2_mobile_dir / "model2_fp16.onnx",
        "ONNX INT8": m2_mobile_dir / "model2_int8.onnx",
    }

    m2_data = {}
    for name, path in m2_files.items():
        size_mb = path.stat().st_size / (1024 * 1024)
        if name == "PyTorch FP32":
            cpu_bench = benchmark_pytorch(m2_py, m2_t, "cpu")
            gpu_bench = benchmark_pytorch(m2_py, m2_t, "cuda") if cuda_available else None
        else:
            cpu_bench = benchmark_onnx(path, m2_np, "CPUExecutionProvider")
            gpu_bench = benchmark_onnx(path, m2_np, "CUDAExecutionProvider") if cuda_provider else None

        m2_data[name] = {
            "size_mb": round(size_mb, 2),
            "cpu": cpu_bench,
            "gpu": gpu_bench,
        }
        print(f"[{name:<12}] Size: {size_mb:6.2f} MB | CPU Avg: {cpu_bench['avg_ms']:6.2f} ms | P95: {cpu_bench['p95_ms']:6.2f} ms | FPS: {cpu_bench['throughput_fps']:5.1f}")
        if gpu_bench:
            print(f"              Desktop GPU Avg: {gpu_bench['avg_ms']:6.2f} ms | P95: {gpu_bench['p95_ms']:6.2f} ms | FPS: {gpu_bench['throughput_fps']:5.1f}")

    bench_results["model2_v2"] = m2_data

    # Save benchmark JSON report
    report_path = PROJECT_ROOT / "reports" / "onnx_benchmark_results.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(bench_results, f, indent=2)
    print(f"\n[OK] Saved Benchmark Data to: {report_path}")

    return bench_results


if __name__ == "__main__":
    run_benchmarks()
