import os
import sys
import json
import hashlib
from pathlib import Path
from collections import defaultdict

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(r"c:\Users\vyasn\OneDrive\Desktop\Disease_prediction").resolve()
DESKTOP_DIR = Path(r"c:\Users\vyasn\OneDrive\Desktop").resolve()

def format_size(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} B"

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

def run_fast_audit():
    print("--- 1. AUDITING PROJECT ROOT TOP-LEVEL ITEMS ---", flush=True)
    root_stats = {}
    for item in sorted(PROJECT_ROOT.iterdir()):
        if item.is_dir():
            s, fc, dc = get_dir_size_and_count(item)
            root_stats[item.name] = {"type": "dir", "size": s, "size_str": format_size(s), "files": fc, "dirs": dc}
            print(f"DIR  {item.name:<30} : {format_size(s):>10} ({fc} files, {dc} dirs)", flush=True)
        else:
            s = item.stat().st_size
            root_stats[item.name] = {"type": "file", "size": s, "size_str": format_size(s), "files": 1, "dirs": 0}
            print(f"FILE {item.name:<30} : {format_size(s):>10}", flush=True)

    print("\n--- 2. AUDITING data/ DIRECTORY DETAILED ---", flush=True)
    data_stats = {}
    data_dir = PROJECT_ROOT / "data"
    for sub in sorted(data_dir.iterdir()):
        if sub.is_dir():
            s, fc, dc = get_dir_size_and_count(sub)
            data_stats[sub.name] = {"size": s, "size_str": format_size(s), "files": fc, "dirs": dc, "subdirs": {}}
            print(f"  data/{sub.name:<30} : {format_size(s):>10} ({fc} files, {dc} subdirs)", flush=True)
            for subsub in sorted(sub.iterdir()):
                if subsub.is_dir():
                    ss, sfc, sdc = get_dir_size_and_count(subsub)
                    data_stats[sub.name]["subdirs"][subsub.name] = {"size": ss, "size_str": format_size(ss), "files": sfc}
                    print(f"    data/{sub.name}/{subsub.name:<25} : {format_size(ss):>10} ({sfc} files)", flush=True)
                else:
                    data_stats[sub.name]["subdirs"][subsub.name] = {"size": subsub.stat().st_size, "size_str": format_size(subsub.stat().st_size), "files": 1}
                    print(f"    data/{sub.name}/{subsub.name:<25} : {format_size(subsub.stat().st_size):>10}", flush=True)
        else:
            data_stats[sub.name] = {"size": sub.stat().st_size, "size_str": format_size(sub.stat().st_size), "files": 1}
            print(f"  data/{sub.name:<30} : {format_size(sub.stat().st_size):>10}", flush=True)

    print("\n--- 3. AUDITING models/ DIRECTORY ---", flush=True)
    models_dir = PROJECT_ROOT / "models"
    for item in sorted(models_dir.iterdir()):
        if item.is_dir():
            s, fc, _ = get_dir_size_and_count(item)
            print(f"  models/{item.name:<25} : {format_size(s):>10} ({fc} files)", flush=True)
            for sub in sorted(item.iterdir()):
                print(f"    models/{item.name}/{sub.name:<20} : {format_size(sub.stat().st_size):>10}", flush=True)
        else:
            print(f"  models/{item.name:<25} : {format_size(item.stat().st_size):>10}", flush=True)

    print("\n--- 4. DESKTOP DIRECTORY ITEMS (SHALLOW) ---", flush=True)
    for item in sorted(DESKTOP_DIR.iterdir()):
        if item.name.lower() == "disease_prediction":
            continue
        try:
            name_clean = item.name.encode('ascii', errors='replace').decode('ascii')
            if item.is_dir():
                print(f"  DESKTOP DIR  : {name_clean:<35}", flush=True)
            else:
                print(f"  DESKTOP FILE : {name_clean:<35} : {format_size(item.stat().st_size):>10}", flush=True)
        except Exception:
            pass

    print("\n--- 5. SCANNING CODEBASE REFERENCES ---", flush=True)
    code_extensions = {".py", ".json", ".js", ".jsx", ".ts", ".tsx", ".sh", ".bat", ".md", ".txt"}
    code_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if any(skip in root for skip in ["venv", "node_modules", ".git", ".gemini"]):
            continue
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in code_extensions:
                code_files.append(Path(root) / f)

    targets = [
        "model1_balanced", "model1_dataset", "plant_part_dataset", "plant_part_dataset_split",
        "model2_dataset", "model2_yolox", "data/external", "data/raw", "best_model.pth",
        "last_model.pth", "model1_efficientnet_b2.pth", "yolox_s.pth", "legacy_flask_app",
        "audio_test_app", "model1_test", "reports/model2", "reports/video_debug"
    ]

    references = defaultdict(list)
    for cf in code_files:
        try:
            content = cf.read_text(encoding="utf-8", errors="ignore")
            for t in targets:
                if t in content:
                    rel_p = str(cf.relative_to(PROJECT_ROOT))
                    references[t].append(rel_p)
        except Exception:
            pass

    for t, refs in references.items():
        print(f"  Target '{t}': referenced in {len(refs)} files", flush=True)
        for r in refs[:6]:
            print(f"    - {r}", flush=True)
        if len(refs) > 6:
            print(f"    - ... and {len(refs)-6} more", flush=True)

    # Save full audit dictionary
    full_audit = {
        "root_stats": root_stats,
        "data_stats": data_stats,
        "references": {k: v for k, v in references.items()},
    }
    with open(PROJECT_ROOT / "scratch" / "fast_audit_result.json", "w", encoding="utf-8") as f:
        json.dump(full_audit, f, indent=2)

    print("\nFAST AUDIT COMPLETED. Saved scratch/fast_audit_result.json", flush=True)

if __name__ == "__main__":
    run_fast_audit()
