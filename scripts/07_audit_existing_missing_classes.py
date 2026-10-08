from pathlib import Path
import yaml
from collections import defaultdict

ROOT = Path("data/external")

TARGETS = {
    "kale",
    "parsley",
    "dill",
    "chives",
    "oregano",
    "thyme",
    "rosemary",
    "gerbera",
    "carnation",
    "dutch_rose",
    "lilium",
    "orchid",
    "chrysanthemum",
}

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

ALIASES = {
    "coriander": "coriander",
    "corriander": "coriander",
    "lily": "lilium",
    "chrysanthemum": "chrysanthemum",
}

def norm(x):
    x = x.strip().lower()
    x = x.replace("_", " ").replace("-", " ")
    x = " ".join(x.split())
    return ALIASES.get(x, x)

results = defaultdict(set)

for yaml_path in ROOT.rglob("data.yaml"):
    try:
        data = yaml.safe_load(
            yaml_path.read_text(encoding="utf-8", errors="ignore")
        )
    except Exception:
        continue

    if not isinstance(data, dict) or "names" not in data:
        continue

    names = data["names"]

    if isinstance(names, dict):
        names = [names[k] for k in sorted(names)]

    names = [norm(str(x)) for x in names]

    target_ids = {
        i: name for i, name in enumerate(names)
        if name in TARGETS
    }

    if not target_ids:
        continue

    dataset_root = yaml_path.parent

    print(f"\n{'='*70}")
    print(dataset_root.relative_to(ROOT))
    print("TARGET CLASSES:", list(target_ids.values()))

    for split in ["train", "valid", "val", "test"]:
        label_dir = dataset_root / split / "labels"
        image_dir = dataset_root / split / "images"

        if not label_dir.exists():
            continue

        for label_file in label_dir.glob("*.txt"):
            try:
                lines = [
                    x.strip()
                    for x in label_file.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).splitlines()
                    if x.strip()
                ]

                class_ids = []
                for line in lines:
                    parts = line.split()
                    if parts:
                        class_ids.append(int(parts[0]))

                recognized = {
                    target_ids[c]
                    for c in class_ids
                    if c in target_ids
                }

                # Only accept images where all annotated objects
                # belong to ONE target class.
                if len(recognized) == 1:
                    cls = next(iter(recognized))

                    for ext in IMAGE_EXTS:
                        img = image_dir / (label_file.stem + ext)
                        if img.exists():
                            results[cls].add(str(img.resolve()))
                            break

            except Exception:
                pass

print("\n\nFINAL UNIQUE IMAGE COUNTS")
print("=" * 70)

for cls in sorted(TARGETS):
    print(f"{cls:20s} {len(results[cls]):5d}")

print("\n\nSOURCE BREAKDOWN")
print("=" * 70)

for cls in sorted(TARGETS):
    print(f"\n{cls}:")
    sources = defaultdict(int)

    for img in results[cls]:
        p = Path(img)
        # Find which external dataset it belongs to
        try:
            rel = p.relative_to(ROOT.resolve())
            source = rel.parts[0]
        except Exception:
            source = "unknown"
        sources[source] += 1

    for source, count in sorted(sources.items()):
        print(f"  {source:40s} {count}")