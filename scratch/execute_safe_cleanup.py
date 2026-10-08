import os
import sys
import shutil
import hashlib
from pathlib import Path

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

def format_size(size_bytes):
    if size_bytes >= 1024**3:
        return f"{size_bytes / (1024**3):.2f} GB"
    elif size_bytes >= 1024**2:
        return f"{size_bytes / (1024**2):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} B"

def perform_safe_deletion():
    print("==================================================", flush=True)
    print("EXECUTING SAFE CLEANUP (GREEN ITEMS ONLY)", flush=True)
    print("==================================================", flush=True)

    green_items = [
        {
            "rel_path": "models/model1_efficientnet_b2.pth",
            "type": "file",
            "reason": "Obsolete early experiment Model 1 checkpoint. Active is models/model1/best_model.pth."
        },
        {
            "rel_path": "reports/video_debug",
            "type": "dir",
            "reason": "Temporary frame crops and ROI debug dumps from video testing."
        },
        {
            "rel_path": "scratch/all_video_frames",
            "type": "dir",
            "reason": "Temporary frame extraction dump from sample video."
        },
        {
            "rel_path": "scratch/roi_visualizations",
            "type": "dir",
            "reason": "Temporary ROI debug visualizations."
        },
        {
            "rel_path": "scratch/video_test_frames",
            "type": "dir",
            "reason": "Temporary test frames."
        },
        {
            "rel_path": "data/external/cherry_tomato",
            "type": "dir",
            "reason": "Empty directory with 0 files."
        },
        {
            "rel_path": "data/external/dutch_rose",
            "type": "dir",
            "reason": "Empty directory with 0 files."
        },
        {
            "rel_path": "data/external/gypsophila",
            "type": "dir",
            "reason": "Empty directory with 0 files."
        },
        {
            "rel_path": "data/external/lilium",
            "type": "dir",
            "reason": "Empty directory with 0 files."
        },
        {
            "rel_path": "data/external/Original Image",
            "type": "dir",
            "reason": "Empty directory with 0 files."
        },
        {
            "rel_path": "requirements.txt",
            "type": "file",
            "reason": "Empty 0-byte file."
        }
    ]

    total_bytes_deleted = 0
    total_files_deleted = 0
    total_dirs_deleted = 0
    deletion_log = []

    for item in green_items:
        p = PROJECT_ROOT / item["rel_path"]
        if not p.exists():
            print(f"Skipping (does not exist): {item['rel_path']}", flush=True)
            continue

        if p.is_file():
            size = p.stat().st_size
            md5 = file_md5(p)
            try:
                p.unlink()
                total_bytes_deleted += size
                total_files_deleted += 1
                record = {
                    "path": item["rel_path"],
                    "size": format_size(size),
                    "size_bytes": size,
                    "type": "file",
                    "md5": md5,
                    "reason": item["reason"]
                }
                deletion_log.append(record)
                print(f"[DELETED FILE] {item['rel_path']:<35} : {format_size(size):>10} (MD5: {md5})", flush=True)
            except Exception as e:
                print(f"[ERROR DELETING FILE] {item['rel_path']}: {e}", flush=True)

        elif p.is_dir():
            dir_size = 0
            file_count = 0
            for root, dirs, files in os.walk(p):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        dir_size += os.path.getsize(fp)
                        file_count += 1
                    except OSError:
                        pass
            try:
                shutil.rmtree(p)
                total_bytes_deleted += dir_size
                total_files_deleted += file_count
                total_dirs_deleted += 1
                record = {
                    "path": item["rel_path"],
                    "size": format_size(dir_size),
                    "size_bytes": dir_size,
                    "type": "directory",
                    "files_count": file_count,
                    "reason": item["reason"]
                }
                deletion_log.append(record)
                print(f"[DELETED DIR ] {item['rel_path']:<35} : {format_size(dir_size):>10} ({file_count} files)", flush=True)
            except Exception as e:
                print(f"[ERROR DELETING DIR] {item['rel_path']}: {e}", flush=True)

    print("\n--------------------------------------------------", flush=True)
    print(f"TOTAL CLEANED: {format_size(total_bytes_deleted)} ({total_files_deleted} files, {total_dirs_deleted} dirs)", flush=True)
    print("--------------------------------------------------\n", flush=True)

    return total_bytes_deleted, total_files_deleted, total_dirs_deleted, deletion_log

if __name__ == "__main__":
    perform_safe_deletion()
