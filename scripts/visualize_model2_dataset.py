"""Visualize random Model 2 validation samples with disease boxes.

Saves annotated PNGs to reports/model2_samples/. READ-ONLY w.r.t. dataset.
Usage: python scripts/visualize_model2_dataset.py [n_samples]
"""
import json, random, sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DST = ROOT / "data" / "processed" / "model2_dataset"
OUT = ROOT / "reports" / "model2_samples"
SEED = 42


def main(n=8):
    random.seed(SEED)
    cm = json.load(open(DST / "class_mapping.json", encoding="utf-8"))
    classes = cm["classes"]
    val_dir = DST / "images" / "val"
    imgs = sorted(val_dir.glob("*"))
    if not imgs:
        print("no val images")
        return 1
    pick = random.sample(imgs, min(n, len(imgs)))
    OUT.mkdir(parents=True, exist_ok=True)
    for p in pick:
        lbl = DST / "labels" / "val" / (p.stem + ".txt")
        if not lbl.exists():
            continue
        im = Image.open(p).convert("RGB")
        dr = ImageDraw.Draw(im)
        W, H = im.size
        for ln in lbl.read_text(encoding="utf-8").splitlines():
            cid, xc, yc, w, h = ln.split()
            cid, xc, yc, w, h = int(cid), *map(float, (xc, yc, w, h))
            x0, y0 = (xc - w / 2) * W, (yc - h / 2) * H
            x1, y1 = (xc + w / 2) * W, (yc + h / 2) * H
            dr.rectangle([x0, y0, x1, y1], outline="red", width=3)
            name = classes[cid]
            dr.rectangle([x0, max(0, y0 - 14), x0 + 7 * len(name) + 6,
                          y0], fill="red")
            dr.text((x0 + 3, max(0, y0 - 13)), name, fill="white")
        im.save(OUT / f"val_{p.stem}.png")
        print(f"saved val_{p.stem}.png")
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 8))
