"""Build Model 2 YOLOX dataset from PlantSeg (READ-ONLY source).

Reads COCO JSONs + Metadata.csv, keeps only annotations whose image_id
exists in the SAME split file (orphans flagged, never merged across splits),
derives YOLO boxes from disease segmentation masks, copies images to
data/processed/model2_dataset/, writes labels/manifest/reports.

Source splits are REUSED as final splits (deterministic); SHA-256 hash check
detects physical duplicates across splits (leakage handling).
"""
from __future__ import annotations
import csv, hashlib, json, random, shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
SRC = ROOT / "data" / "external" / "plantseg" / "plantseg"
DST = ROOT / "data" / "processed" / "model2_dataset"
REP = ROOT / "reports"
SEED = 42
SPLITS = (("train", "annotation_train.json"),
          ("val", "annotation_val.json"),
          ("test", "annotation_test.json"))

DST_IMG = {s: DST / "images" / s for s, _ in SPLITS}
DST_LBL = {s: DST / "labels" / s for s, _ in SPLITS}


def sha256_file(p, chunk=1048576):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def seg_bbox(polys):
    xs, ys = [], []
    for poly in polys:
        if len(poly) < 6:
            return None
        xs.extend(poly[0::2])
        ys.extend(poly[1::2])
    if not xs:
        return None
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    return (x0, y0, x1 - x0, y1 - y0)


def id2img_fn(per_src, s, a):
    return per_src[s]["id2img"][a["image_id"]]["file_name"]


def bad(reason, split, img_id, a, fn, invalid_rows, bbox=None, dims=None):
    row = {"reason": reason, "source": f"{split}:{img_id}",
           "ann_id": a["id"], "file": fn}
    if bbox is not None:
        row["bbox"] = [round(float(v), 2) for v in bbox]
    if dims is not None:
        row["dims"] = dims
    invalid_rows.append(row)


def main():
    random.seed(SEED)
    meta = {}
    for r in csv.DictReader(open(SRC / "Metadata.csv", encoding="utf-8-sig")):
        meta[r["Name"]] = (r["Plant"], r["Disease"])
    print(f"Metadata rows: {len(meta)}", flush=True)

    for s in DST_IMG:
        DST_IMG[s].mkdir(parents=True, exist_ok=True)
        DST_LBL[s].mkdir(parents=True, exist_ok=True)

    per_src = {}
    for split, jf in SPLITS:
        d = json.load(open(SRC / jf, encoding="utf-8"))
        id2img = {i["id"]: i for i in d["images"]}
        valid, orphans = [], []
        for a in d["annotations"]:
            (valid if a["image_id"] in id2img else orphans).append(a)
        per_src[split] = {"json": d, "id2img": id2img,
                          "valid": valid, "orphans": orphans}
        print(f"{split}: images={len(id2img)} valid_anns={len(valid)} "
              f"orphans={len(orphans)}", flush=True)

    diseases = sorted({meta[id2img_fn(per_src, s, a)][1]
                       for s in per_src for a in per_src[s]["valid"]})
    cls = {name: i for i, name in enumerate(diseases)}
    crops = sorted({meta[id2img_fn(per_src, s, a)][0]
                    for s in per_src for a in per_src[s]["valid"]})
    print(f"Taxonomy: {len(crops)} crops, {len(diseases)} diseases",
          flush=True)
    with open(DST / "class_mapping.json", "w", encoding="utf-8") as f:
        json.dump({"classes": diseases, "class_to_idx": cls,
                   "crops": crops, "seed": SEED}, f, indent=2)

    manifest_rows, invalid_rows = [], []
    hash_to_locs = defaultdict(list)
    per_split_files = {s: set() for s, _ in SPLITS}

    for split, _ in SPLITS:
        id2img = per_src[split]["id2img"]
        by_img = defaultdict(list)
        for a in per_src[split]["valid"]:
            by_img[a["image_id"]].append(a)
        for img_id in sorted(by_img):
            info = id2img[img_id]
            fn = info["file_name"]
            W, H = info["width"], info["height"]
            src_img = SRC / "images" / split / fn
            if fn not in meta:
                invalid_rows.append({"reason": "missing_metadata",
                                     "split": split, "file": fn})
                continue
            if not src_img.exists():
                invalid_rows.append({"reason": "missing_image_file",
                                     "split": split, "file": fn})
                continue
            plant, disease = meta[fn]
            cid = cls[disease]
            dest_name = f"{split}_{fn}"
            yolo_lines = []
            for a in sorted(by_img[img_id], key=lambda x: x["id"]):
                segs = a.get("segmentation") or []
                bb = seg_bbox(segs)
                if bb is None:
                    bad("empty_or_degenerate_mask", split, img_id,
                        a, fn, invalid_rows)
                    continue
                x, y, w, h = bb
                if w <= 0 or h <= 0:
                    bad("non_positive_box", split, img_id,
                        a, fn, invalid_rows, [x, y, w, h])
                    continue
                if x < 0 or y < 0 or x + w > W + 1e-6 or y + h > H + 1e-6:
                    bad("box_out_of_bounds", split, img_id,
                        a, fn, invalid_rows, [x, y, w, h], [W, H])
                    continue
                xc, yc = (x + w / 2) / W, (y + h / 2) / H
                nw, nh = w / W, h / H
                if not (0 <= xc <= 1 and 0 <= yc <= 1
                        and 0 < nw <= 1 and 0 < nh <= 1):
                    bad("bad_normalized_box", split, img_id,
                        a, fn, invalid_rows)
                    continue
                yolo_lines.append(
                    f"{cid} {xc:.6f} {yc:.6f} {nw:.6f} {nh:.6f}")
                manifest_rows.append(
                    {"image": dest_name, "split": split, "crop": plant,
                     "disease": disease, "class_id": cid,
                     "source_split": split, "source_image_id": img_id,
                     "source_uid": f"{split}:{img_id}",
                     "source_annotation_id": a["id"],
                     "original_image_path": str(src_img),
                     "bbox_x": round(x, 2), "bbox_y": round(y, 2),
                     "bbox_width": round(w, 2), "bbox_height": round(h, 2),
                     "img_width": W, "img_height": H})
            if not yolo_lines:
                invalid_rows.append({"reason": "image_no_valid_boxes",
                                     "split": split, "file": fn})
                continue
            per_split_files[split].add(dest_name)
            dest_img = DST_IMG[split] / dest_name
            if not dest_img.exists():
                shutil.copy2(src_img, dest_img)
            with open(DST_LBL[split] / (Path(dest_name).stem + ".txt"),
                      "w", encoding="utf-8") as f:
                f.write("\n".join(yolo_lines) + "\n")
            try:
                hash_to_locs[sha256_file(dest_img)].append(dest_name)
            except OSError:
                invalid_rows.append({"reason": "hash_failed",
                                     "split": split, "file": dest_name})

    with open(DST / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        cols = ["image", "split", "crop", "disease", "class_id",
                "source_split", "source_image_id", "source_uid",
                "source_annotation_id", "original_image_path",
                "bbox_x", "bbox_y", "bbox_width", "bbox_height"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(manifest_rows)


    with open(DST / "excluded_annotations.json", "w",
              encoding="utf-8") as f:
        orph = [{"source_uid": f"{s}:{a['image_id']}",
                 "source_split": s, "ann_id": a["id"],
                 "category_id": a.get("category_id"),
                 "reason": "orphan_image_id_not_in_split_file"}
                for s in per_src for a in per_src[s]["orphans"]]
        json.dump({"orphan_annotations": orph,
                   "invalid_annotations": invalid_rows}, f, indent=2)

    leaks = {h: locs for h, locs in hash_to_locs.items()
             if len(set(locs)) > 1}
    cross = {h: locs for h, locs in leaks.items()
             if len({x.split("_")[0] for x in locs}) > 1}
    with open(DST / "hash_leakage.json", "w", encoding="utf-8") as f:
        json.dump({"duplicate_hashes": len(leaks),
                   "cross_split_hashes": len(cross),
                   "cross_split_files": sorted(
                       {x for locs in cross.values() for x in locs})}, f,
                  indent=2)
    print(f"WROTE files={sum(len(v) for v in per_split_files.values())} "
          f"anns={len(manifest_rows)}", flush=True)
    print(f"orphans={sum(len(per_src[s]['orphans']) for s in per_src)} "
          f"invalid={len(invalid_rows)} dup_hashes={len(leaks)} "
          f"cross_split={len(cross)}", flush=True)


if __name__ == "__main__":
    main()
