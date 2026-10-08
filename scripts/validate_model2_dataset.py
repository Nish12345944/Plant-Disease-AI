"""Post-build validation for data/processed/model2_dataset (READ-ONLY).

Checks: label↔image pairing, split leakage (names + hashes), box validity,
duplicate filenames, contiguous class IDs, manifest consistency, PIL load.
"""
import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DST = ROOT / "data" / "processed" / "model2_dataset"
SPLITS = ("train", "val", "test")
FAILS = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        FAILS.append(name)


def sha(p, chunk=1048576):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def main():
    cm = json.load(open(DST / "class_mapping.json", encoding="utf-8"))
    n_cls = len(cm["classes"])
    ids = sorted(cm["class_to_idx"].values())
    check("class_ids_contiguous", ids == list(range(n_cls)),
          f"n={n_cls}")

    names_by_split, hashes_by_split, total_img, total_lbl = {}, {}, 0, 0
    bad_boxes = []
    for s in SPLITS:
        imgs = sorted((DST / "images" / s).glob("*"))
        lbls = sorted((DST / "labels" / s).glob("*.txt"))
        total_img += len(imgs)
        total_lbl += len(lbls)
        istems = {p.name for p in imgs}
        lstems = {p.stem for p in lbls}
        check(f"pair_{s}", len(istems) == len(lstems) and
              all(Path(n).stem in lstems for n in istems),
              f"img={len(istems)} lbl={len(lstems)}")
        for p in lbls:
            for ln in p.read_text(encoding="utf-8").splitlines():
                parts = ln.split()
                if len(parts) != 5:
                    bad_boxes.append((s, p.name, "bad_cols"))
                    continue
                cid = int(parts[0])
                x, y, w, h = map(float, parts[1:])
                if not (0 <= cid < n_cls and 0 < w <= 1 and 0 < h <= 1
                        and 0 <= x <= 1 and 0 <= y <= 1):
                    bad_boxes.append((s, p.name, ln))
        check(f"boxes_valid_{s}", not bad_boxes or
              all(b[0] != s for b in bad_boxes), f"bad={len(bad_boxes)}")
        dup = [n for n, c in Counter(p.name for p in imgs).items() if c > 1]
        check(f"no_dup_filenames_{s}", not dup, f"n={len(dup)}")
        names_by_split[s] = {p.name for p in imgs}
        hashes_by_split[s] = {sha(p): p.name for p in imgs}
        # PIL load sample
        try:
            from PIL import Image
            for p in imgs[:25]:
                with Image.open(p) as im:
                    im.verify()
            check(f"pil_load_{s}", True, f"sampled={min(25, len(imgs))}")
        except Exception as e:
            check(f"pil_load_{s}", False, str(e))

    for i, a in enumerate(SPLITS):
        for b in SPLITS[i + 1:]:
            ov = names_by_split[a] & names_by_split[b]
            check(f"no_split_overlap_name_{a}_{b}", not ov, f"n={len(ov)}")
            hv = set(hashes_by_split[a]) & set(hashes_by_split[b])
            check(f"no_split_leakage_hash_{a}_{b}", not hv, f"n={len(hv)}")

    # manifest consistency
    rows = list(csv.DictReader(open(DST / "manifest.csv", encoding="utf-8")))
    lbls_per_img = Counter(r["image"] for r in rows)
    man_names = set(lbls_per_img)
    disk_names = set().union(*names_by_split.values())
    check("manifest_names_match_disk", man_names == disk_names,
          f"manifest={len(man_names)} disk={len(disk_names)}")
    check("manifest_class_ids_valid",
          all(0 <= int(r["class_id"]) < n_cls for r in rows))
    # every manifest bbox matches label file line count
    mismatch = 0
    for name, n in lbls_per_img.items():
        s = name.split("_")[0]
        lp = DST / "labels" / s / (Path(name).stem + ".txt")
        if lp.exists():
            lines = [l for l in lp.read_text().splitlines() if l.strip()]
            # label file contains ALL boxes for that image
            if len(lines) != sum(
                    1 for r in rows if r["image"] == name):
                mismatch += 1
    check("label_line_counts_match_manifest", mismatch == 0,
          f"mismatch={mismatch}")

    check("no_forbidden_orphans_written",
          not (DST / "labels" / "train" / "orphan.txt").exists())

    summary = {"total_images": total_img, "total_labels": total_lbl,
               "manifest_rows": len(rows), "classes": n_cls,
               "failures": FAILS}
    print(json.dumps(summary, indent=2))
    print("VALIDATION:", "PASSED" if not FAILS else f"FAILED {FAILS}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
