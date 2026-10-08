"""Generate model2_dataset_build_report.md + summary JSON from build outputs."""
import csv, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DST = ROOT / "data" / "processed" / "model2_dataset"
REP = ROOT / "reports"

rows = list(csv.DictReader(open(DST / "manifest.csv", encoding="utf-8")))
cm = json.load(open(DST / "class_mapping.json", encoding="utf-8"))
exc = json.load(open(DST / "excluded_annotations.json", encoding="utf-8"))
lk = json.load(open(DST / "hash_leakage.json", encoding="utf-8"))

imgs_split = {s: len(list((DST / "images" / s).iterdir()))
              for s in ("train", "val", "test")}
anns_split = Counter(r["split"] for r in rows)
img_all = {r["image"] for r in rows}
per_crop_img = defaultdict(set)
per_dis_ann = Counter()
per_dis_img = defaultdict(set)
for r in rows:
    per_crop_img[r["crop"]].add(r["image"])
    per_dis_ann[r["disease"]] += 1
    per_dis_img[r["disease"]].add(r["image"])

orphans = len(exc["orphan_annotations"])
invalid = exc["invalid_annotations"]
removed_leak = lk["remediation"]["files_removed"]

summary = {
    "source": "PlantSeg (COCO masks + Metadata.csv)",
    "source_images": 7774,
    "source_annotations": 77394,
    "usable_images": len(img_all),
    "usable_annotations": len(rows),
    "excluded": {
        "orphan_annotations": orphans,
        "invalid_annotations": len(invalid),
        "images_removed_for_leakage": removed_leak,
        "images_without_valid_boxes": sum(
            1 for x in invalid if x["reason"] == "image_no_valid_boxes"),
        "boxes_out_of_bounds": sum(
            1 for x in invalid if x["reason"] == "box_out_of_bounds"),
    },
    "crops": len(cm["crops"]),
    "diseases": len(cm["classes"]),
    "images_per_split": imgs_split,
    "annotations_per_split": dict(anns_split),
    "hash_leakage": {
        "cross_split_hashes_before": lk["cross_split_hashes"],
        "files_removed": removed_leak,
        "cross_split_after": lk["post_fix_cross_split_hashes"],
        "same_split_duplicate_groups_retained":
            lk["post_fix_same_split_duplicate_groups"],
    },
}
json.dump(summary, open(REP / "model2_dataset_build_summary.json", "w"),
          indent=2)

dis_sorted = sorted(per_dis_ann.items(), key=lambda x: x[1])
crop_sorted = sorted(((c, len(s)) for c, s in per_crop_img.items()),
                     key=lambda x: -x[1])
md = ["# Model 2 Dataset Build Report (PlantSeg → YOLOX)\n\n",
      "**Date:** 2026-10-05 · **Source:** `data/external/plantseg/` "
      "(READ-ONLY, unmodified) · **Output:** "
      "`data/processed/model2_dataset/`\n\n",
      "## 1. Headline numbers\n\n| Metric | Value |\n|---|---|\n",
      "| Source images | 7774 |\n| Source annotations | 77394 |\n",
      f"| **Usable images** | **{len(img_all)}** |\n",
      f"| **Usable annotations (boxes)** | **{len(rows)}** |\n",
      f"| Crops | {len(cm['crops'])} |\n",
      f"| Diseases (classes) | {len(cm['classes'])} |\n",
      f"| train images / boxes | {imgs_split['train']} / {anns_split['train']} |\n",
      f"| val images / boxes | {imgs_split['val']} / {anns_split['val']} |\n",
      f"| test images / boxes | {imgs_split['test']} / {anns_split['test']} |\n\n",
      "## 2. Excluded / invalid (never silently discarded)\n\n",
      f"- Orphan annotations (image_id not in same split file): **{orphans}** "
      f"→ `excluded_annotations.json`\n",
      f"- Invalid annotation/box rows: **{len(invalid)}**\n",
      f"- Images removed for cross-split hash leakage: **{removed_leak}** "
      f"(policy keep train > val > test) → `hash_leakage.json`\n",
      f"- Cross-split leakage after fix: **{lk['post_fix_cross_split_hashes']}**"
      f"; same-split duplicate groups retained: "
      f"{lk['post_fix_same_split_duplicate_groups']}\n\n",
      "### Invalid annotation reasons\n\n| Reason | Count |\n|---|---|\n"]
for k, v in Counter(x["reason"] for x in invalid).most_common():
    md.append(f"| {k} | {v} |\n")
md += ["\n## 3. Images per crop (top 20)\n\n| Crop | Images |\n|---|---|\n"]
for c, n in crop_sorted[:20]:
    md.append(f"| {c} | {n} |\n")
md += [f"\n(all {len(crop_sorted)} crops in summary JSON)\n",
       "\n## 4. Annotations per disease — smallest 15 / largest 15\n\n",
       "| Disease | Annotations | Images |\n|---|---|---|\n"]
for d, n in dis_sorted[:15]:
    md.append(f"| {d} | {n} | {len(per_dis_img[d])} |\n")
md.append("| ... | ... | ... |\n")
for d, n in dis_sorted[-15:]:
    md.append(f"| {d} | {n} | {len(per_dis_img[d])} |\n")
md += ["\n## 5. Class mapping\n\n",
       f"`class_mapping.json`: {len(cm['classes'])} contiguous IDs "
       f"0..{len(cm['classes']) - 1} (sorted, seed {cm['seed']}).\n",
       "\n## 6. Dataset structure\n\n```\nmodel2_dataset/\n",
       "├── images/{train,val,test}/  (<split>_<orig>.jpg)\n",
       "├── labels/{train,val,test}/  (YOLO: cls xc yc w h normalized)\n",
       "├── class_mapping.json\n",
       "├── manifest.csv  (provenance: source_uid, annotation_id, bbox)\n",
       "├── excluded_annotations.json\n└── hash_leakage.json\n```\n",
       "\n## 7. Limitations\n\n",
       "- Boxes derived from disease-region polygons (mask ratios 4e-5..1).\n",
       "- 21,580 source anns are orphans (IDs restart per split file) — "
       "flagged, never merged across splits.\n",
       "- Source splits reused as final splits (deterministic, seed 42).\n",
       "- Same-split byte-duplicate groups retained (flagged, no leakage).\n",
       "\n## 8. Verdict\n\n",
       f"PlantSeg **supports** the YOLOX disease-localization dataset: "
       f"{len(img_all)} images / {len(rows)} boxes / {len(cm['classes'])} "
       f"classes built and validated.\n"]
open(REP / "model2_dataset_build_report.md", "w",
     encoding="utf-8").write("".join(md))
print("images:", len(img_all), "anns:", len(rows),
      "diseases:", len(cm["classes"]), "splits:", summary["images_per_split"])
