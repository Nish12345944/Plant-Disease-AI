# Carrot Dataset Audit — `products_sam.v15i.yolov8`

**Scope:** inspection and label verification only. No source files were renamed, moved, deleted, or modified. No model was trained and no production file was changed.


## Headline finding

The folder is named `carrot`, but `data.yaml` identifies the source as Roboflow project **`products_sam`** (workspace `diploma-wdwcx`, v15) — a **generic produce/fruit DEFECT segmentation dataset**. Its 26 classes are mostly physical/quality defects (`bruise`, `poke`, `scratch`, `cut`, `crack`, `print`, `squeeze`, `color`, `contamination`, `defect`) plus disease names from multiple crops (`esca`=grapevine, `mold-bread`=bread). 
**None of the 26 classes belong to the carrot Model 2 taxonomy** (``alternaria_leaf_blight`, `cavity_spot`, `cercospora_leaf_blight``). Crop identity is NOT verified from source metadata, so no image was assigned a `carrot__*` label or added to the candidate set.


## 1. Directory & format

- **Format:** YOLOv8 **segmentation** (`class_id x1 y1 x2 y2 ...` polygon), NOT bounding-box. Coordinates are normalized polygon vertices in [0,1].
- **Config splits:** `train`, `valid`, `test`. **On disk only `train` and `test` exist; NO `valid`/`val` folder** → `has_valid_split: false`.
- **`nc`:** 26. Class names read from `data.yaml` `names:` (never inferred from IDs).


## 2. Image & annotation counts

| Split | Images | Label files |
|---|---:|---:|
| train | 1,171 | 1,171 |
| test | 223 | 223 |
| **Total** | **1,394** | **1,394** |

- **Valid, non-empty, correctly-matched annotations:** 1,394 / 1,394 (100%).
- Multi-class images: 0. Missing labels: 0. Empty: 0. Invalid IDs: 0. Malformed: 0. Invalid coords: 0.
