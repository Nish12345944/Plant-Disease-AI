"""Fix cross-split hash leakage in data/processed/model2_dataset (dataset only).

Policy: for byte-identical images in >1 split, KEEP the copy in the split with
highest priority (train > val > test); delete image+label from lower-priority
splits; drop their manifest rows; record every removal in
hash_leakage.json (remediation section). Same-split duplicates are flagged
but retained (no leakage). Original PlantSeg source is untouched.
"""
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path

DST = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
           r"\data\processed\model2_dataset")
SPLITS = ("train", "val", "test")
PRIO = {s: i for i, s in enumerate(SPLITS)}


def sha(p, chunk=1048576):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def main():
    groups = defaultdict(list)
    for s in SPLITS:
        for p in sorted((DST / "images" / s).iterdir()):
            if p.is_file():
                groups[sha(p)].append((s, p.name))

    removed, kept_same_split = [], []
    for h, locs in groups.items():
        if len(locs) < 2:
            continue
        by_split = defaultdict(list)
        for s, n in locs:
            by_split[s].append(n)
        if len(by_split) == 1:
            kept_same_split.append(sorted(locs))
            continue
        keeper = min(by_split, key=lambda s: PRIO[s])
        for s, names in by_split.items():
            if s == keeper:
                continue
            for n in names:
                (DST / "images" / s / n).unlink()
                (DST / "labels" / s / (Path(n).stem + ".txt")).unlink()
                removed.append({"image": n, "split": s, "kept_in": keeper,
                                "sha256": h})

    # rewrite manifest without removed images
    rows = list(csv.DictReader(open(DST / "manifest.csv", encoding="utf-8")))
    gone = {r["image"] for r in removed}
    kept = [r for r in rows if r["image"] not in gone]
    with open(DST / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(kept)

    # re-verify
    recheck = defaultdict(list)
    for s in SPLITS:
        for p in sorted((DST / "images" / s).iterdir()):
            if p.is_file():
                recheck[sha(p)].append(f"{s}/{p.name}")
    cross_now = {h: v for h, v in recheck.items()
                 if len({x.split("/")[0] for x in v}) > 1}
    same_now = {h: v for h, v in recheck.items()
                if len({x.split("/")[0] for x in v}) == 1 and len(v) > 1}

    out = json.load(open(DST / "hash_leakage.json", encoding="utf-8"))
    out["remediation"] = {
        "policy": "keep train > val > test; remove lower-priority copies",
        "files_removed": len(removed),
        "manifest_rows_removed": len(rows) - len(kept),
        "removed": removed,
        "same_split_duplicates_retained": sorted(
            [sorted(v) for v in same_now.values()]),
    }
    out["post_fix_cross_split_hashes"] = len(cross_now)
    out["post_fix_same_split_duplicate_groups"] = len(same_now)
    json.dump(out, open(DST / "hash_leakage.json", "w"), indent=2)
    print(f"removed={len(removed)} rows_dropped={len(rows) - len(kept)} "
          f"cross_split_remaining={len(cross_now)} "
          f"same_split_dup_groups={len(same_now)}")


if __name__ == "__main__":
    main()
