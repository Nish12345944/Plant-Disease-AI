"""Extract images from the spinach parquet file into the same folder.

Reads data/processed/spinach/train-00000-of-00001.parquet (HuggingFace-style
schema: image.path, image.bytes, label) and writes each image's raw bytes to
data/processed/spinach/<image.path>. Duplicates are skipped.
"""

from __future__ import annotations

import collections
import sys
from pathlib import Path

import pyarrow.parquet as pq

BASE_DIR = Path(__file__).resolve().parents[1]
SPINACH_DIR = BASE_DIR / "data" / "processed" / "spinach"
PARQUET_FILE = SPINACH_DIR / "train-00000-of-00001.parquet"


def main() -> int:
    if not PARQUET_FILE.is_file():
        print(f"ERROR: parquet file not found: {PARQUET_FILE}")
        return 1

    table = pq.read_table(PARQUET_FILE, columns=["image", "label"])
    image_col = table.column("image").combine_chunks()
    paths = image_col.field("path")
    bytes_col = image_col.field("bytes")
    labels = table.column("label").combine_chunks()

    written = 0
    skipped_existing = 0
    skipped_missing = 0
    errors: list[str] = []
    label_counts: collections.Counter = collections.Counter()

    for i in range(len(table)):
        rel_path = paths[i].as_py()
        data = bytes_col[i].as_py()
        label = labels[i].as_py()

        if not rel_path or data is None:
            skipped_missing += 1
            continue

        # Keep everything inside the spinach folder; flatten any directory
        # components from the original path to avoid nested output dirs.
        out_name = Path(rel_path.replace("\\", "/")).name
        out_path = SPINACH_DIR / out_name

        if out_path.exists():
            skipped_existing += 1
            continue

        try:
            out_path.write_bytes(data)
        except OSError as exc:
            errors.append(f"{rel_path}: {exc}")
            continue

        written += 1
        label_counts[label] += 1
        if written % 500 == 0:
            print(f"  ...{written} images written")

    print(f"Rows processed : {len(table)}")
    print(f"Written        : {written} -> {SPINACH_DIR}")
    print(f"Already existed: {skipped_existing}")
    print(f"Empty/missing  : {skipped_missing}")
    if errors:
        print(f"Errors         : {len(errors)}")
        for msg in errors[:10]:
            print(f"  {msg}")
    print(f"Labels written : {dict(sorted(label_counts.items(), key=lambda kv: str(kv[0])))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
