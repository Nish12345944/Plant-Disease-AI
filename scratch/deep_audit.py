import os
import sys
import json
import hashlib
import re
from pathlib import Path
from collections import defaultdict

# Set stdout to utf-8 encoding safely
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DESKTOP_DIR = Path(r"c:\Users\vyasn\OneDrive\Desktop").resolve()

def get_dir_size_and_count(path):
    total_size = 0
    file_count = 0
    dir_count = 0
    try:
        for root, dirs, files in os.walk(path):
            dir_count += len(dirs)
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
                        file_count += 1
                except OSError:
                    pass
    except OSError:
        pass
    return total_size, file_count, dir_count

def format_size(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} B"

def file_hash(filepath, block_size=65536):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def run_deep_audit():
    print("==================================================")
    print("STARTING COMPLETE AUDIT FOR CLEANUP")
    print("==================================================")

    # 1. Total breakdown of data/ subdirectories
    print("\n--- 1. DATA DIRECTORY DETAILED AUDIT ---")
    data_dir = PROJECT_ROOT / "data"
    data_subdirs_stats = {}
    if data_dir.exists():
        for sub in sorted(data_dir.iterdir()):
            if sub.is_dir():
                s, fc, dc = get_dir_size_and_count(sub)
                data_subdirs_stats[sub.name] = {"size": s, "files": fc, "dirs": dc, "path": str(sub)}
                print(f"  data/{sub.name:<30} : {format_size(s):>10} ({fc} files, {dc} subdirs)")
                for subsub in sorted(sub.iterdir()):
                    if subsub.is_dir():
                        ss, sfc, sdc = get_dir_size_and_count(subsub)
                        print(f"    data/{sub.name}/{subsub.name:<25} : {format_size(ss):>10} ({sfc} files)")
                    else:
                        print(f"    data/{sub.name}/{subsub.name:<25} : {format_size(subsub.stat().st_size):>10}")
            else:
                print(f"  data/{sub.name:<30} : {format_size(sub.stat().st_size):>10}")

    # 2. Check other root directories
    print("\n--- 2. OTHER ROOT DIRECTORIES ---")
    other_dirs = ["models", "model1_test", "model1_test_app", "model2", "app", "audio", "audio_test_app", "video", "pipeline", "router", "scripts", "reports", "results", "scratch", "temp_multimodal_uploads", "test_multimodal_assets", "venv"]
    for od in other_dirs:
        p = PROJECT_ROOT / od
        if p.exists():
            s, fc, dc = get_dir_size_and_count(p)
            print(f"  {od:<30} : {format_size(s):>10} ({fc} files, {dc} dirs)")

    # 3. Root files
    print("\n--- 3. ROOT LEVEL FILES ---")
    for f in sorted(PROJECT_ROOT.iterdir()):
        if f.is_file():
            print(f"  {f.name:<30} : {format_size(f.stat().st_size):>10}")

    # 4. Desktop audit (parent directory)
    print("\n--- 4. DESKTOP AUDIT (PARENT DIR) ---")
    desktop_items = list(DESKTOP_DIR.iterdir())
    for item in sorted(desktop_items, key=lambda x: x.name.lower()):
        if item.name.lower() == "disease_prediction":
            continue
        try:
            name_clean = item.name.encode('ascii', errors='replace').decode('ascii')
            if item.is_dir():
                s, fc, dc = get_dir_size_and_count(item)
                print(f"  DESKTOP DIR  : {name_clean:<35} : {format_size(s):>10} ({fc} files)")
            else:
                print(f"  DESKTOP FILE : {name_clean:<35} : {format_size(item.stat().st_size):>10}")
        except Exception as e:
            print(f"  DESKTOP ERR  : {item} ({e})")

    # 5. Dependency / Reference scan across all scripts and codebase
    print("\n--- 5. SCRIPT & CODEBASE REFERENCE SCAN ---")
    code_extensions = {".py", ".json", ".js", ".jsx", ".ts", ".tsx", ".sh", ".bat", ".md", ".txt"}
    code_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if "venv" in root or "node_modules" in root or ".git" in root or ".gemini" in root:
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in code_extensions:
                code_files.append(Path(root) / f)

    # All dataset subdirectories
    all_dataset_dirs = []
    if data_dir.exists():
        for sub in data_dir.iterdir():
            if sub.is_dir():
                all_dataset_dirs.append(sub.name)
                for subsub in sub.iterdir():
                    if subsub.is_dir():
                        all_dataset_dirs.append(f"{sub.name}/{subsub.name}")
                        all_dataset_dirs.append(subsub.name)

    # Search each dataset dir name in code
    dir_references = defaultdict(list)
    for cf in code_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
            for d in all_dataset_dirs:
                if d in content:
                    dir_references[d].append(str(cf.relative_to(PROJECT_ROOT)))
        except Exception:
            pass

    for d in sorted(set(all_dataset_dirs)):
        refs = dir_references[d]
        print(f"  Dataset '{d}': {len(refs)} references in codebase")
        if refs:
            for r in refs[:5]:
                print(f"    -> {r}")
            if len(refs) > 5:
                print(f"    -> ... and {len(refs)-5} more")

    # 6. Check duplicates between model1_dataset, model1_balanced, plant_part_dataset, plant_part_dataset_split
    print("\n--- 6. DATASET REPRODUCIBILITY & REDUNDANCY ANALYSIS ---")
    # Let's inspect data/processed/
    processed_dir = data_dir / "processed"
    if processed_dir.exists():
        for psub in sorted(processed_dir.iterdir()):
            if psub.is_dir():
                print(f"\n  Inspecting data/processed/{psub.name}:")
                sub_items = list(psub.iterdir())
                print(f"    Sub-items ({len(sub_items)}): {[x.name for x in sub_items[:10]]}")

if __name__ == "__main__":
    run_deep_audit()
