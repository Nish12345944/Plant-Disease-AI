"""Clean and reorganise every plant/crop/flower dataset in data/external.

The sources under ``data/external`` are wildly inconsistent: some carry
train/val/test splits, some nest part folders several levels deep, some
put the images straight inside the plant folder and some are YOLO
detection exports.  This script merges all of them into one clean,
part-centric dataset::

    data/processed/plant_part_dataset/<plant>/<plant>_<part>/<image>

It also:

  * recursively discovers every image regardless of nesting depth
  * prefers real metadata (folder names, YOLO class names, YAML files,
    plantseg file names) over guessing (see ``plant_part_rules``)
  * drops unreadable / corrupt / tiny images
  * removes exact duplicates (sha256) and near duplicates (dHash)
  * never mixes plants or parts, and never touches the sources
  * writes a detailed audit (CSV + JSON) and a counts report

Usage
-----
    python scripts/11_clean_organize_plant_parts.py
    python scripts/11_clean_organize_plant_parts.py --limit 500
    python scripts/11_clean_organize_plant_parts.py --force
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import shutil
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from plant_part_rules import (  # noqa: E402
    IGNORE_DIRS,
    IMAGE_EXTENSIONS,
    PLANTSEG_DATASETS,
    Decision,
    normalize,
    resolve_by_path,
    resolve_plantseg,
    resolve_yolo_class,
)

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DEFAULT_EXTERNAL = ROOT / "data" / "external"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "plant_part_dataset"
DEFAULT_REPORTS = ROOT / "reports"


# ======================================================================
# Arguments
# ======================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge data/external into a clean plant-part dataset."
    )
    parser.add_argument("--external", type=Path, default=DEFAULT_EXTERNAL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument(
        "--near-dup-threshold", type=int, default=5,
        help="Max dHash Hamming distance treated as a near duplicate.",
    )
    parser.add_argument(
        "--min-size", type=int, default=32,
        help="Images whose shorter side is below this are dropped.",
    )
    parser.add_argument(
        "--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1),
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Only inspect the first N images (debug / smoke test).",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Delete the output folder first if it already exists.",
    )
    return parser.parse_args()


# ======================================================================
# YOLO dataset discovery
# ======================================================================

def parse_yolo_names(yaml_path: Path):
    """Return the ``names`` list from a YOLO data.yaml (no PyYAML needed)."""
    try:
        text = yaml_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("names:"):
            payload = stripped[len("names:"):].strip()
            if payload.startswith("["):
                try:
                    return list(ast.literal_eval(payload))
                except (ValueError, SyntaxError):
                    return None
    return None


def discover_yolo_datasets(external: Path):
    """Map ``dataset_key -> {class_id: class_name}``."""
    found = {}
    for top in sorted(p for p in external.iterdir() if p.is_dir()):
        for yaml_path in top.glob("*.yaml"):
            names = parse_yolo_names(yaml_path)
            if names:
                found[normalize(top.name)] = {
                    i: str(name) for i, name in enumerate(names)
                }
                break
    return found


def yolo_label_path(image_path: Path) -> Path:
    """Map ``.../images/x.jpg`` to ``.../labels/x.txt``."""
    parts = list(image_path.parts)
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == "images":
            parts[i] = "labels"
            return Path(*parts).with_suffix(".txt")
    return image_path.with_suffix(".txt")



# ======================================================================
# YOLO decision
# ======================================================================

def resolve_yolo_image(dataset, label_file: Path, class_names):
    if not label_file.exists():
        return Decision(source="yolo_label", reason="missing_annotation")

    try:
        text = label_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return Decision(source="yolo_label", reason="unreadable_annotation")

    class_ids = []
    for line in text.splitlines():
        tokens = line.split()
        if not tokens:
            continue
        try:
            class_ids.append(int(float(tokens[0])))
        except ValueError:
            continue

    if not class_ids:
        return Decision(source="yolo_label", reason="empty_annotation")

    resolved = set()
    exclusions = []
    for class_id in sorted(set(class_ids)):
        name = class_names.get(class_id)
        if name is None:
            exclusions.append(f"unknown_class_id:{class_id}")
            continue
        plant, part, reason = resolve_yolo_class(dataset, name)
        if reason:
            exclusions.append(reason)
        else:
            resolved.add((plant, part))

    if not resolved:
        reason = exclusions[0] if exclusions else "no_annotation"
        return Decision(source="yolo_label", reason=reason)

    if len(resolved) == 1:
        plant, part = next(iter(resolved))
        return Decision(plant=plant, part=part, source="yolo_label")

    plants = {p for p, _ in resolved}
    if len(plants) > 1:
        return Decision(
            source="yolo_label",
            reason=f"multi_plant_annotation({len(plants)})",
        )
    return Decision(
        source="yolo_label",
        reason=f"multi_part_annotation({len(resolved)})",
    )


# ======================================================================
# Candidate discovery + resolution
# ======================================================================

def scan_candidates(external: Path, limit: int = 0):
    records = []
    for dirpath, dirnames, filenames in os.walk(external):
        dirnames[:] = [d for d in dirnames if d.lower() not in IGNORE_DIRS]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in IMAGE_EXTENSIONS:
                continue
            abs_path = Path(dirpath) / filename
            rel_parts = abs_path.relative_to(external).parts
            records.append((abs_path, rel_parts))
            if limit and len(records) >= limit:
                return records
    return records


def resolve_all(records, yolo_datasets, plantseg_datasets):
    results = []
    for abs_path, rel_parts in records:
        dataset = normalize(rel_parts[0])
        if dataset in yolo_datasets:
            decision = resolve_yolo_image(
                dataset, yolo_label_path(abs_path), yolo_datasets[dataset]
            )
        elif dataset in plantseg_datasets:
            decision = resolve_plantseg(abs_path.stem)
        else:
            decision = resolve_by_path(list(rel_parts))
        results.append(decision)
    return results


# ======================================================================
# Image inspection (validation + fingerprints) - runs in worker processes
# ======================================================================

def dhash64(gray_image) -> int:
    """64-bit difference hash of a PIL image."""
    small = gray_image.resize((9, 8), Image.BILINEAR)
    pixels = list(small.getdata())
    bits = 0
    for row in range(8):
        for col in range(8):
            offset = row * 9 + col
            if pixels[offset] > pixels[offset + 1]:
                bits |= 1 << (row * 8 + col)
    return bits


def inspect_image(path_str: str, min_size: int):
    """Return a dict describing one image (never raises)."""
    path = Path(path_str)
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        sha = digest.hexdigest()
    except OSError as exc:
        return {"path": path_str, "ok": False,
                "error": f"unreadable_file:{exc.__class__.__name__}"}

    try:
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            if width < min_size or height < min_size:
                return {"path": path_str, "ok": False, "sha": sha,
                        "error": f"image_too_small:{width}x{height}"}
            grey = image.convert("L")
            dhash = dhash64(grey)
    except Exception as exc:  # noqa: BLE001 - PIL raises many types
        return {"path": path_str, "ok": False, "sha": sha,
                "error": f"corrupt_image:{exc.__class__.__name__}"}

    return {"path": path_str, "ok": True, "sha": sha, "dhash": dhash,
            "width": width, "height": height}


# ======================================================================
# Duplicate detection
# ======================================================================

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, item):
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != root:
            self.parent[item], item = root, self.parent[item]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def near_dup_groups(hashes, threshold):
    """Group indices whose 64-bit hashes are within *threshold* bits.

    Uses 8 x 8-bit blocks: any pair at distance <= 7 shares a block, so
    the pigeonhole principle guarantees no pair is missed.
    """
    buckets = defaultdict(list)
    for index, value in enumerate(hashes):
        for shift in range(0, 64, 8):
            buckets[(shift, (value >> shift) & 0xFF)].append(index)

    union = UnionFind(len(hashes))
    for members in buckets.values():
        if len(members) < 2:
            continue
        first = members[0]
        for other in members[1:]:
            if hamming(hashes[first], hashes[other]) <= threshold:
                union.union(first, other)

    groups = defaultdict(list)
    for index in range(len(hashes)):
        groups[union.find(index)].append(index)
    return groups


def place_file(src: Path, dst: Path):
    """Put *src* at *dst* without losing the run if one file misbehaves.

    Tries a hard link first (same volume, no extra disk space), then a
    plain copy.  Returns ``None`` on success or a short error string.
    """
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return f"mkdir_failed:{type(exc).__name__}"

    if dst.exists():
        return None

    try:
        os.link(src, dst)
        return None
    except OSError:
        pass

    for _ in range(2):
        try:
            shutil.copy2(src, dst)
            return None
        except FileNotFoundError:
            if not src.exists():
                return "source_missing_during_copy"
            if dst.exists():
                dst.unlink()
        except OSError as exc:
            return f"copy_failed:{type(exc).__name__}"
    return "copy_failed:source_unreadable"


# ======================================================================
# Reports
# ======================================================================

AUDIT_FIELDS = [
    "source_file", "detected_plant", "detected_part", "output_path",
    "duplicate_status", "invalid_status", "reason", "decision_source",
]


def finish(args, output, reports, started, **stats):
    audit_rows = stats["audit_rows"]
    audit_rows.sort(key=lambda row: (row["source_file"], row["reason"]))

    audit_csv = reports / "plant_part_dataset_audit.csv"
    with open(audit_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        writer.writerows(audit_rows)

    ambiguous_csv = reports / "plant_part_dataset_ambiguous.csv"
    with open(ambiguous_csv, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=AUDIT_FIELDS)
        writer.writeheader()
        for row in audit_rows:
            if row["invalid_status"] == "ambiguous":
                writer.writerow(row)

    manifest_path = reports / "plant_part_dataset_manifest.json"
    manifest_path.write_text(
        json.dumps(stats["manifest"], indent=1), encoding="utf-8"
    )

    per_class = {
        f"{plant}/{plant}_{part}": count
        for (plant, part), count in sorted(stats["per_class"].items())
    }
    per_plant = dict(sorted(stats["plant_counts"].items()))
    per_part = dict(sorted(stats["part_counts"].items()))

    assumption_counts = Counter()
    for row in audit_rows:
        if row["duplicate_status"] == "kept" and "(assumed)" in row["decision_source"]:
            assumption_counts[f"{row['detected_plant']}_{row['detected_part']}"] += 1
    assumption_counts = dict(assumption_counts.most_common())

    valid_before = (
        stats["final_count"] + stats.get("copy_failures", 0)
        + stats["near_dups"] + stats["exact_dups"] + stats["cross_dups"]
    )

    summary = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source_root": str(args.external),
        "output_root": str(output),
        "parameters": {
            "near_dup_threshold": args.near_dup_threshold,
            "min_size": args.min_size,
            "limit": args.limit,
        },
        "totals": {
            "source_images": stats["total_source"],
            "resolved": valid_before + 0,
            "ambiguous": stats["ambiguous"],
            "valid_images": valid_before,
            "corrupted_images": stats["corrupt"],
            "exact_duplicates_removed": stats["exact_dups"],
            "cross_class_duplicates_removed": stats["cross_dups"],
            "near_duplicates_removed": stats["near_dups"],
            "copy_failures": stats.get("copy_failures", 0),
            "final_images": stats["final_count"],
            "near_dup_groups": stats["group_count"],
        },
        "exclusion_reasons": dict(stats["reason_counts"].most_common()),
        "invalid_reasons": dict(stats["invalid_reasons"].most_common()),
        "copy_failure_reasons": dict(
            stats.get("copy_failure_reasons", Counter()).most_common()),
        "counts_per_plant": per_plant,
        "counts_per_part": per_part,
        "counts_per_plant_part": per_class,
        "counts_per_plant_part_assumption": assumption_counts,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    summary_path = reports / "plant_part_dataset_summary.json"
    summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8")

    # --------------------------------------------------------------- print
    line = "=" * 78
    print()
    print(line)
    print("FINAL SUMMARY")
    print(line)
    print(f"  total source images      : {human(stats['total_source'])}")
    print(f"  ambiguous (excluded)     : {human(stats['ambiguous'])}")
    print(f"  valid images             : {human(valid_before)}")
    print(f"  corrupted/invalid images : {human(stats['corrupt'])}")
    print(f"  exact duplicates removed : {human(stats['exact_dups'])}")
    print(f"  cross-class dups removed : {human(stats['cross_dups'])}")
    print(f"  near duplicates removed  : {human(stats['near_dups'])}")
    copy_failures = stats.get("copy_failures", 0)
    if copy_failures:
        print(f"  copy failures            : {human(copy_failures)}")
        for reason, count in stats["copy_failure_reasons"].most_common(5):
            print(f"      {reason}: {human(count)}")
    print(f"  FINAL IMAGE COUNT        : {human(stats['final_count'])}")

    print()
    print("COUNTS PER PLANT")
    for plant, count in sorted(per_plant.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {plant:<22} {human(count):>8}")

    print()
    print("COUNTS PER PLANT-PART")
    for name, count in sorted(per_class.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {name:<38} {human(count):>8}")

    print()
    print("COUNTS PER PART")
    for part, count in sorted(per_part.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {part:<22} {human(count):>8}")

    print()
    print("ARTEFACTS")
    print(f"  dataset      : {output}")
    print(f"  audit csv    : {audit_csv}")
    print(f"  ambiguous csv: {ambiguous_csv}")
    print(f"  manifest json: {manifest_path}")
    print(f"  summary json : {summary_path}")
    print(f"  elapsed      : {summary['elapsed_seconds']}s")
    print(line)
    return 0


# ======================================================================
# Main
# ======================================================================

def human(n):
    return f"{n:,}"



def main():
    args = parse_args()
    started = time.time()

    external = args.external
    output = args.output
    reports = args.reports
    reports.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("PLANT-PART DATASET CLEANUP")
    print("=" * 78)
    print(f"source      : {external}")
    print(f"output      : {output}")
    print(f"reports     : {reports}")
    print(f"workers     : {args.workers}")
    print(f"near-dup    : hamming <= {args.near_dup_threshold}")
    print()

    if output.exists():
        if not args.force:
            print(f"ERROR: {output} already exists. Re-run with --force.")
            return 1
        print(f"Removing existing output: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------- scan
    print("Scanning sources ...")
    yolo_datasets = discover_yolo_datasets(external)
    print(f"  YOLO datasets with data.yaml: {len(yolo_datasets)}")
    for key, names in sorted(yolo_datasets.items()):
        print(f"    {key}  ({len(names)} classes)")

    records = scan_candidates(external, args.limit)
    print(f"  candidate images: {human(len(records))}")

    # ------------------------------------------------------------ resolve
    print("Resolving plant / part from metadata ...")
    decisions = resolve_all(records, yolo_datasets, PLANTSEG_DATASETS)

    audit_rows = []
    accepted = []
    reason_counts = Counter()
    unknown_plant_counts = Counter()

    for (abs_path, rel_parts), decision in zip(records, decisions):
        rel_str = "/".join(rel_parts)
        if decision.ok:
            accepted.append({
                "abs_path": abs_path,
                "rel": rel_str,
                "plant": decision.plant,
                "part": decision.part,
                "source": decision.source,
            })
        else:
            reason_counts[decision.reason] += 1
            if decision.plant:
                unknown_plant_counts[decision.plant] += 1
            audit_rows.append({
                "source_file": rel_str,
                "detected_plant": decision.plant or "",
                "detected_part": decision.part or "",
                "output_path": "",
                "duplicate_status": "",
                "invalid_status": "ambiguous",
                "reason": decision.reason,
                "decision_source": decision.source,
            })

    print(f"  resolved : {human(len(accepted))}")
    print(f"  ambiguous: {human(sum(reason_counts.values()))}")
    for reason, count in reason_counts.most_common():
        print(f"    {reason}: {human(count)}")

    # ------------------------------------------------------------ inspect
    print()
    print(f"Inspecting {human(len(accepted))} images (validating + hashing) ...")
    inspect_fn = partial(inspect_image, min_size=args.min_size)
    inspect_paths = [str(item["abs_path"]) for item in accepted]

    inspections = []
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for index, result in enumerate(
            pool.map(inspect_fn, inspect_paths, chunksize=32)
        ):
            inspections.append(result)
            if index and index % 10000 == 0:
                print(f"    inspected {human(index)} ...")

    valid = []
    corrupt = 0
    invalid_reasons = Counter()
    for item, result in zip(accepted, inspections):
        if result["ok"]:
            item["sha"] = result["sha"]
            item["dhash"] = result["dhash"]
            item["width"] = result["width"]
            item["height"] = result["height"]
            valid.append(item)
        else:
            corrupt += 1
            invalid_reasons[result["error"]] += 1
            audit_rows.append({
                "source_file": item["rel"],
                "detected_plant": item["plant"],
                "detected_part": item["part"],
                "output_path": "",
                "duplicate_status": "",
                "invalid_status": "corrupt_or_invalid",
                "reason": result["error"],
                "decision_source": item["source"],
            })

    print(f"  valid   : {human(len(valid))}")
    print(f"  invalid : {human(corrupt)}")
    for reason, count in invalid_reasons.most_common():
        print(f"    {reason}: {human(count)}")

    # -------------------------------------------------------------- dedup
    print()
    print("Deduplicating ...")
    valid.sort(key=lambda item: (item["plant"], item["part"], item["rel"]))

    seen_sha = {}
    kept = []
    exact_dups = 0
    cross_dups = 0

    for item in valid:
        first = seen_sha.get(item["sha"])
        if first is None:
            seen_sha[item["sha"]] = item
            kept.append(item)
            continue
        same_class = (first["plant"], first["part"]) == (
            item["plant"], item["part"])
        status = "exact_duplicate" if same_class else "duplicate_cross_class"
        if same_class:
            exact_dups += 1
        else:
            cross_dups += 1
        audit_rows.append({
            "source_file": item["rel"],
            "detected_plant": item["plant"],
            "detected_part": item["part"],
            "output_path": "",
            "duplicate_status": status,
            "invalid_status": "",
            "reason": f"{status}:{first['rel']}",
            "decision_source": item["source"],
        })

    by_class = defaultdict(list)
    for item in kept:
        by_class[(item["plant"], item["part"])].append(item)

    near_dups = 0
    final = []
    group_count = 0
    for (plant, part), items in sorted(by_class.items()):
        hashes = [item["dhash"] for item in items]
        groups = near_dup_groups(hashes, args.near_dup_threshold)
        for root in sorted(groups):
            members = sorted(groups[root])
            group_id = f"{plant}_{part}_g{group_count:06d}"
            group_count += 1
            representative = items[members[0]]
            for position, offset in enumerate(members):
                item = items[offset]
                item["group_id"] = group_id
                if position == 0:
                    final.append(item)
                    continue
                near_dups += 1
                audit_rows.append({
                    "source_file": item["rel"],
                    "detected_plant": item["plant"],
                    "detected_part": item["part"],
                    "output_path": "",
                    "duplicate_status": "near_duplicate",
                    "invalid_status": "",
                    "reason": f"near_duplicate:{representative['rel']}",
                    "decision_source": item["source"],
                })

    print(f"  exact duplicates removed : {human(exact_dups)}")
    print(f"  cross-class duplicates   : {human(cross_dups)}")
    print(f"  near duplicates removed  : {human(near_dups)}")

    # --------------------------------------------------------------- copy
    print()
    print(f"Copying {human(len(final))} images ...")
    final.sort(key=lambda item: (item["plant"], item["part"], item["rel"]))

    per_class_seq = Counter()
    plant_counts = Counter()
    part_counts = Counter()
    manifest = []
    copy_failures = 0
    copy_failure_reasons = Counter()

    for item in final:
        plant, part = item["plant"], item["part"]
        per_class_seq[(plant, part)] += 1
        plant_counts[plant] += 1
        part_counts[part] += 1

        ext = item["abs_path"].suffix.lower()
        dest_dir = output / plant / f"{plant}_{part}"
        dest = dest_dir / f"{plant}_{part}_{per_class_seq[(plant, part)]:06d}{ext}"

        failure = place_file(item["abs_path"], dest)
        if failure:
            copy_failures += 1
            copy_failure_reasons[failure] += 1
            per_class_seq[(plant, part)] -= 1
            plant_counts[plant] -= 1
            part_counts[part] -= 1
            audit_rows.append({
                "source_file": item["rel"],
                "detected_plant": plant,
                "detected_part": part,
                "output_path": "",
                "duplicate_status": "",
                "invalid_status": "copy_failed",
                "reason": failure,
                "decision_source": item["source"],
            })
            continue

        rel_out = str(dest.relative_to(output))
        item["output_path"] = rel_out
        audit_rows.append({
            "source_file": item["rel"],
            "detected_plant": plant,
            "detected_part": part,
            "output_path": rel_out,
            "duplicate_status": "kept",
            "invalid_status": "",
            "reason": "",
            "decision_source": item["source"],
        })
        manifest.append({
            "output_path": rel_out,
            "plant": plant,
            "part": part,
            "group_id": item["group_id"],
            "source_file": item["rel"],
            "sha256": item["sha"],
            "dhash": item["dhash"],
            "width": item["width"],
            "height": item["height"],
        })

    # ------------------------------------------------------------ reports
    return finish(
        args, output, reports, started, total_source=len(records),
        ambiguous=sum(reason_counts.values()), reason_counts=reason_counts,
        corrupt=corrupt, invalid_reasons=invalid_reasons,
        exact_dups=exact_dups, cross_dups=cross_dups, near_dups=near_dups,
        final_count=len(final) - copy_failures,
        plant_counts=plant_counts,
        part_counts=part_counts, per_class=per_class_seq,
        manifest=manifest, audit_rows=audit_rows,
        group_count=group_count, unknown_plant_counts=unknown_plant_counts,
        copy_failures=copy_failures,
        copy_failure_reasons=copy_failure_reasons,
    )


if __name__ == "__main__":
    sys.exit(main())

