import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()

def file_md5(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def run_reference_audit():
    print("--- SCANNING CODEBASE REFERENCES ---", flush=True)
    scan_dirs = ["app", "audio", "audio_test_app", "model1_test", "model1_test_app", "model2", "models", "pipeline", "router", "scripts", "video"]
    
    code_files = []
    for sd in scan_dirs:
        p = PROJECT_ROOT / sd
        if p.exists():
            for root, dirs, files in os.walk(p):
                if any(skip in root for skip in ["node_modules", ".git", "__pycache__"]):
                    continue
                for f in files:
                    ext = os.path.splitext(f)[1].lower()
                    if ext in [".py", ".json", ".js", ".jsx", ".ts", ".tsx", ".sh", ".bat", ".md", ".txt"]:
                        code_files.append(Path(root) / f)

    for rf in [PROJECT_ROOT / "legacy_flask_app.py", PROJECT_ROOT / "project_workflow.txt", PROJECT_ROOT / "gpu.py"]:
        if rf.exists():
            code_files.append(rf)

    print(f"Total source/script files scanned: {len(code_files)}", flush=True)

    targets = [
        "model1_balanced",
        "model1_dataset",
        "plant_part_dataset_split",
        "plant_part_dataset",
        "model2_dataset",
        "model2_yolox",
        "data/downloads",
        "data/external",
        "data/raw",
        "model1_efficientnet_b2.pth",
        "best_model.pth",
        "last_model.pth",
        "yolox_s.pth",
        "legacy_flask_app",
        "audio_test_app",
        "model1_test",
        "temp_multimodal_uploads",
        "test_multimodal_assets",
        "video_debug",
    ]

    target_refs = defaultdict(list)
    for cf in code_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
            for t in targets:
                if t in content:
                    rel_p = str(cf.relative_to(PROJECT_ROOT))
                    target_refs[t].append(rel_p)
        except Exception as e:
            pass

    print("\n--- REFERENCE RESULTS ---", flush=True)
    for t in targets:
        refs = target_refs[t]
        print(f"\nTarget '{t}': ({len(refs)} references)", flush=True)
        for r in refs:
            print(f"  - {r}", flush=True)

    print("\n--- MODEL WEIGHTS HASH COMPARISON ---", flush=True)
    m1_best = PROJECT_ROOT / "models" / "model1" / "best_model.pth"
    m1_root = PROJECT_ROOT / "models" / "model1_efficientnet_b2.pth"
    if m1_best.exists() and m1_root.exists():
        h1 = file_md5(m1_best)
        h2 = file_md5(m1_root)
        print(f"models/model1/best_model.pth MD5 : {h1}", flush=True)
        print(f"models/model1_efficientnet_b2.pth MD5: {h2}", flush=True)
        print(f"Are they EXACT IDENTICAL DUPLICATES? -> {h1 == h2}", flush=True)

    # Check empty directories in data/external
    print("\n--- EMPTY DIRECTORIES IN data/external ---", flush=True)
    ext_dir = PROJECT_ROOT / "data" / "external"
    if ext_dir.exists():
        for sub in sorted(ext_dir.iterdir()):
            if sub.is_dir():
                items = list(sub.iterdir())
                if len(items) == 0:
                    print(f"EMPTY DIR: data/external/{sub.name}", flush=True)

    # Save detailed reference json
    with open(PROJECT_ROOT / "scratch" / "reference_audit.json", "w", encoding="utf-8") as f:
        json.dump({k: v for k, v in target_refs.items()}, f, indent=2)

    print("\nREFERENCE AUDIT SAVED to scratch/reference_audit.json", flush=True)

if __name__ == "__main__":
    run_reference_audit()
