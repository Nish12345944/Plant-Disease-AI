from pathlib import Path
import pyarrow.parquet as pq
from PIL import Image
import io

# CHANGE ONLY THIS if your parquet filename is different
PARQUET_FILE = Path(
    r"data\external\model2_supplementary\zucchini__downy_mildew\train-00002-of-00005.parquet"
)

OUTPUT_DIR = Path(
    r"data\external\model2_supplementary\zucchini__downy_mildew"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("PARQUET IMAGE EXTRACTION")
print("=" * 70)

print(f"\nReading: {PARQUET_FILE}")

pf = pq.ParquetFile(PARQUET_FILE)

print(f"Rows: {pf.metadata.num_rows}")
print(f"Columns: {pf.schema.names}")

# Read metadata first
table = pq.read_table(PARQUET_FILE)

print("\nColumn types:")
for name, column in zip(table.column_names, table.columns):
    print(f"  {name}: {column.type}")

# Find likely image column
image_column = None

for name in table.column_names:
    if name.lower() in ["image", "images", "img"]:
        image_column = name
        break

if image_column is None:
    print("\nERROR: Could not automatically find image column.")
    print("Available columns:", table.column_names)
    raise SystemExit(1)

print(f"\nUsing image column: {image_column}")

images = table[image_column]

count = 0

for i in range(len(images)):
    item = images[i].as_py()

    try:
        # Hugging Face Image feature usually stores:
        # {"bytes": ..., "path": ...}
        if isinstance(item, dict):
            image_bytes = item.get("bytes")

            if image_bytes is None:
                print(f"Skipping {i}: no image bytes")
                continue

        elif isinstance(item, bytes):
            image_bytes = item

        else:
            print(f"Skipping {i}: unsupported type {type(item)}")
            continue

        image = Image.open(io.BytesIO(image_bytes))
        image.load()

        output_file = OUTPUT_DIR / f"zucchini_downy_mildew_{i:05d}.jpg"

        # Convert to RGB for consistent JPEG output
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(output_file, "JPEG", quality=95)

        count += 1

        if count % 25 == 0:
            print(f"Extracted {count} images...")

    except Exception as e:
        print(f"Skipping row {i}: {e}")

print("\n" + "=" * 70)
print(f"DONE — extracted {count} images")
print(f"Output: {OUTPUT_DIR}")
print("=" * 70)