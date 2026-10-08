"""READ-ONLY Model 2 dataset audit. Never writes to data/external/."""
from __future__ import annotations
import json, os, re
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
EXT = ROOT / "data" / "external"
OUT = ROOT / "reports" / "model2_dataset_audit.json"

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
HEALTHY_KEYS = ("healthy", "health", "_h", "no_disease", "normal", "good")
DISEASE_KEYS = ("disease", "diseased", "blight", "mildew", "rust", "spot",
                "lesion", "wilt", "rot", "virus", "fungus", "fungal",
                "bacteria", "anthracnose", "mosaic", "canker", "scab")


def is_image(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMG_EXTS


def fast_count_images(d):
    """Fast image count via os.scandir recursion (no rglob overhead)."""
    n = 0
    try:
        with os.scandir(d) as it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):
                        n += fast_count_images(e.path)
                    elif e.is_file(follow_symlinks=False) and \
                            os.path.splitext(e.name)[1].lower() in IMG_EXTS:
                        n += 1
                except OSError:
                    continue
    except OSError:
        pass
    return n


def fast_list(d, want_images=True, cap=4000):
    """Collect up to cap image paths (or .txt labels) via scandir."""
    out, trunc = [], False
    stack = [str(d)]
    ext = IMG_EXTS if want_images else {".txt"}
    while stack:
        cur = stack.pop()
        try:
            with os.scandir(cur) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        elif e.is_file(follow_symlinks=False) and \
                                os.path.splitext(e.name)[1].lower() in ext:
                            out.append(Path(e.path))
                            if len(out) >= cap:
                                return out, True
                    except OSError:
                        continue
        except OSError:
            continue
    return out, trunc


def all_images(d, cap=4000):
    if not Path(d).exists():
        return [], False
    return fast_list(d, True, cap)


def read_text_safe(p: Path, limit=200000):
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read(limit)
    except OSError:
        return ""


def _pv(val):
    v = val.strip().strip("'\"")
    if v.startswith("["):
        return [x.strip(" '\"") for x in v.strip("[]").split(",") if x.strip()]
    return v


def parse_yaml_simple(text):
    out = {}
    names = []
    in_names = False
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("-") and in_names:
            names.append(s[1:].strip(" '\""))
            continue
        if ":" in line and not line.startswith((" ", "\t")):
            k, v = line.split(":", 1)
            k = k.strip()
            in_names = (k == "names" and not v.strip())
            if v.strip():
                out[k] = _pv(v)
    if names:
        out["names"] = names
    return out

def check_image_open(p):
    try:
        if p.stat().st_size == 0:
            return False, "zero_byte"
    except OSError:
        return False, "stat_error"
    try:
        with open(p, "rb") as f:
            head = f.read(32)
        if len(head) < 8:
            return False, "too_small"
        is_jpg = head[:2] == b"\xff\xd8"
        is_png = head[:8] == b"\x89PNG\r\n\x1a\n"
        if p.suffix.lower() in (".jpg", ".jpeg") and not is_jpg:
            return False, "bad_header"
        if p.suffix.lower() == ".png" and not is_png:
            return False, "bad_header"
        return True, ""
    except OSError:
        return False, "stat_error"


def analyze_yolo_labels(label_files, cap=1500):
    n_empty = 0
    box_rows = 0
    per_file_boxes, classes_seen = [], set()
    multi_class_files = 0
    seg_like = 0
    bad_lines = 0
    files = label_files[:cap]
    for lf in files:
        txt = read_text_safe(lf).strip()
        if not txt:
            n_empty += 1
            per_file_boxes.append(0)
            continue
        boxes, cls = 0, set()
        for line in txt.splitlines():
            parts = line.split()
            if len(parts) < 5:
                bad_lines += 1
                continue
            try:
                c = int(float(parts[0]))
                cls.add(c)
                vals = [float(v) for v in parts[1:]]
            except ValueError:
                bad_lines += 1
                continue
            if len(vals) > 4:
                seg_like += 1
            elif not all(0.0 <= v <= 1.0 for v in vals[:4]):
                bad_lines += 1
                continue
            boxes += 1
        box_rows += boxes
        per_file_boxes.append(boxes)
        classes_seen |= cls
        if len(cls) > 1:
            multi_class_files += 1
    n_files = len(label_files)
    return dict(label_files=n_files, label_files_analyzed=len(files),
                empty=n_empty, box_rows=box_rows,
                avg_boxes=round(box_rows / max(len(files), 1), 2),
                max_boxes=max(per_file_boxes) if per_file_boxes else 0,
                classes_seen=sorted(classes_seen),
                multi_class_files=multi_class_files,
                seg_like_rows=seg_like, bad_lines=bad_lines)


def sample_multi_object(label_files, k=200):
    """Fraction of sampled label files with >1 box (multi-object proxy)."""
    if not label_files:
        return None
    multi = tot = 0
    for lf in label_files[:k]:
        txt = read_text_safe(lf, 5000).strip()
        if not txt:
            continue
        n = sum(1 for ln in txt.splitlines() if len(ln.split()) >= 5)
        tot += 1
        if n > 1:
            multi += 1
    return round(multi / tot, 3) if tot else 0.0


def audit_yolo_dataset(d):
    """Roboflow-style YOLO dataset: data.yaml + train/valid/test images/labels."""
    info = {"kind": "yolo_roboflow", "splits": {}}
    yamls = list(d.glob("*.yaml")) + list(d.glob("*.yml"))
    info["yaml"] = yamls[0].name if yamls else None
    info["class_names"] = []
    if yamls:
        parsed = parse_yaml_simple(read_text_safe(yamls[0]))
        names = parsed.get("names", [])
        info["class_names"] = names if isinstance(names, list) else [names]
        info["nc"] = parsed.get("nc", len(info["class_names"]))
    imgs, labels, paired, missing, empty = [], [], 0, 0, 0
    for split in ("train", "valid", "test", "val"):
        sd = Path(d) / split
        if not sd.exists():
            continue
        for sub in ("images", "labels"):
            sdir = sd / sub
            if not sdir.exists():
                continue
            got, _t = fast_list(sdir, sub == "images", 25000)
            (imgs if sub == "images" else labels).extend(got)
        info["splits"][split] = True
    for extra in ("images", "labels"):
        ed = Path(d) / extra
        if ed.exists() and not info["splits"]:
            got, _t = fast_list(ed, extra == "images", 25000)
            (imgs if extra == "images" else labels).extend(got)
    img_stems = {p.stem for p in imgs}
    lab_stems = {p.stem for p in labels}
    paired = len(img_stems & lab_stems)
    missing = len(img_stems - lab_stems)
    empty = sum(1 for lf in labels if lf.stat().st_size == 0)
    info.update(images=len(imgs), labels=len(labels), paired=paired,
                images_missing_labels=missing, empty_labels=empty)
    info["yolo_stats"] = analyze_yolo_labels(labels)
    info["multi_object_frac"] = sample_multi_object(labels)
    return info, imgs


def audit_folder_classes(d):
    classes = {}
    for sub in sorted(p for p in Path(d).iterdir() if p.is_dir()):
        if sub.name.lower() in ("labels", "annotations", "masks"):
            continue
        classes[sub.name] = fast_count_images(sub)
        if classes[sub.name] == 0:
            del classes[sub.name]
    return classes


def audit_one(d):
    """Full read-only audit of one dataset folder."""
    rec = {"dataset": d.name, "exists": d.exists(), "empty": False}
    if not d.exists() or not any(d.iterdir()):
        rec.update(empty=True, annotation="none", images=0)
        return rec, []
    yamls = list(d.glob("data.yaml")) + list(d.glob("*.yaml"))
    has_split = any((d / s).exists() for s in ("train", "valid", "test", "val"))
    has_img_label = False
    for s in ("train", "valid", "test", "val"):
        if (d / s / "images").exists() or (d / s / "labels").exists():
            has_img_label = True
            break
    plantseg_jsons = list(d.rglob("annotation_*.json"))
    if (yamls and has_img_label) or has_img_label:
        det, imgs = audit_yolo_dataset(d)
        rec.update(det, annotation="yolo_boxes")
        rec["annotation_format"] = "YOLO"
        if det["yolo_stats"].get("seg_like_rows"):
            rec["annotation"] = "yolo_segmentation?"
    elif plantseg_jsons or (d / "plantseg").exists():
        rec.update(audit_plantseg(d), annotation="coco_masks",
                   annotation_format="COCO(RLE)+masks")
        imgs, _trunc = all_images(d / "plantseg" / "images")
        if not imgs:
            imgs, _trunc = all_images(d)
    else:
        classes = audit_folder_classes(d)
        total = sum(classes.values())
        imgs, trunc = ([], False) if total > 4000 else all_images(d)
        rec["annotation"] = "classification-only"
        rec["annotation_format"] = "none"
        rec["classes"] = classes
        rec["images"] = total
        if trunc:
            rec["image_list_truncated"] = True
        if not classes:
            rec["annotation"] = "none"
    if "images_total" not in rec:
        if "imgs" in dir() and isinstance(imgs, list) and imgs:
            pass
        else:
            imgs = []
        rec["images_total"] = len(imgs) if imgs else rec.get("images", 0)
    # health split + corrupt sample + single/multi proxy
    h, dis, unk = 0, 0, 0
    for im in imgs:
        s = str(im).lower()
        if any(k in s for k in HEALTHY_KEYS):
            h += 1
        elif any(k in s for k in DISEASE_KEYS):
            dis += 1
        else:
            unk += 1
    rec["healthy_images"] = h
    rec["diseased_name_images"] = dis
    rec["unlabelled_name_images"] = unk
    sample = imgs[:min(60, len(imgs))]
    bad = {}
    for im in sample:
        ok, reason = check_image_open(im)
        if not ok:
            bad[reason] = bad.get(reason, 0) + 1
    rec["corrupt_sample_checked"] = len(sample)
    rec["corrupt_sample_issues"] = bad
    return rec, imgs


def audit_plantseg(d: Path):
    """PlantSeg: COCO JSONs + images + mask annotations folders."""
    base = d / "plantseg" if (d / "plantseg").exists() else d
    out = {"splits": {}}
    for jf in sorted(base.glob("annotation_*.json")):
        try:
            with open(jf, encoding="utf-8") as f:
                js = json.load(f)
            imgs = js.get("images", [])
            anns = js.get("annotations", [])
            cats = [c.get("name") for c in js.get("categories", [])]
            out["splits"][jf.stem] = {"images": len(imgs),
                                      "annotations": len(anns),
                                      "categories": cats}
        except Exception as e:
            out["splits"][jf.stem] = {"error": str(e)[:120]}
    mask_dirs = [p for p in (base / "annotations").rglob("*") if p.is_dir()] \
        if (base / "annotations").exists() else []
    out["mask_files"] = sum(1 for m in (base / "annotations").rglob("*")
                            if m.is_file() and m.suffix.lower() in IMG_EXTS)
    return out


def main():
    import sys
    only = sys.argv[1:] or None
    datasets = sorted(p for p in EXT.iterdir())
    report = {"datasets": [], "totals": {}}
    all_counts = Counter()
    for d in datasets:
        if not d.is_dir():
            continue
        if only and d.name not in only:
            continue
        print(f"Auditing {d.name} ...", flush=True)
        rec, _ = audit_one(d)
        report["datasets"].append(rec)
        all_counts["datasets"] += 1
        all_counts["images"] += rec.get("images_total", 0)
    report["totals"] = dict(all_counts)
    mode = "a" if only else "w"
    if only:
        import json as _j
        try:
            with open(OUT, encoding="utf-8") as f:
                prev = _j.load(f)
            prev["datasets"] = [x for x in prev["datasets"]
                                if x["dataset"] not in {r["dataset"] for r in report["datasets"]}]
            prev["datasets"].extend(report["datasets"])
            with open(OUT, "w", encoding="utf-8") as f:
                _j.dump(prev, f, indent=2)
        except (OSError, ValueError):
            with open(OUT, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
    else:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    print(f"Wrote {OUT} ({len(report['datasets'])} datasets)")


if __name__ == "__main__":
    main()
