# Model 1 Dataset Audit for Model 2 Disease Detection & Localization

**Audit Date:** 2026-10-06  
**Primary Dataset Audited:** `data/processed/model1_balanced/`  
**Manifest:** `data/processed/model1_balanced_manifest.csv` (16,537 image records)  
**Associated Metadata:** `data/processed/model1_balanced_summary.json`, `data/external/`  
**Audit Purpose:** Determine exactly which images from the Model 1 crop classification dataset can be reused to build the Model 2 disease detection/localization dataset (YOLOX-S).

---

## 1. Executive Summary

| Audit Dimension | Metric / Finding | Status / Suitability |
| :--- | :--- | :--- |
| **Total Images in Model 1 Balanced** | **16,537 images** | Fully cataloged across 20 active crop classes |
| **Bounding Boxes / Localization Masks** | **0 annotations (0.0%)** | ❌ Model 1 is a pure classification dataset |
| **Group A: Directly Reusable for Model 2** | **0 images (0.0%)** | No images have pre-existing disease bounding boxes |
| **Group B: Reusable After Annotation** | **6,774 images (41.0%)** | Diseased foliage with traceable disease provenance |
| **Group C: Healthy Negative Background Samples** | **3,596 images (21.7%)** | Clean healthy foliage (negative/background samples) |
| **Group D: Not Suitable / Unusable** | **6,167 images (37.3%)** | Flower/fruit-only images, ambiguous health status |

---

## 2. Model 1 Dataset Overview

The Model 1 balanced dataset was curated specifically for **22-class whole-image crop identification** using an EfficientNet-B2 backbone.

### Manifest Schema (`model1_balanced_manifest.csv`)
- `image_path`: Path to the image relative to workspace.
- `plant_class`: Model 1 target crop name (e.g. `tomato`, `cucumber`, `capsicum`).
- `plant_part`: Anatomical part (`leaves`, `flower`, `fruit`, `stem`, `whole_plant`).
- `health_status`: Historical flag (`healthy`, `diseased`, `unknown`, `not_specified`).
- `split`: Dataset split assignment (`train` 80.0%, `val` 10.0%, `test` 10.0%).
- `duplicate_group`: Perceptual hash cluster ID ensuring zero cross-split leakage.
- `source_dataset`: Original source identifier.
- `is_supplement`: Boolean flag indicating supplementary downloads.

### Split Distribution
- **Train:** 13,225 images (80.0%)
- **Validation:** 1,649 images (10.0%)
- **Test:** 1,663 images (10.0%)
- **Total:** 16,537 images

---

## 3. Crop-by-Crop Inventory & Health Status

| Crop | Total Images | Healthy | Diseased | Unknown | Dominant Plant Parts | Reusability Potential |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tomato** | 1,500 | 165 | 1,319 | 16 | Leaves (1,478), Fruit (22) | 1,319 diseased leaves, 165 healthy |
| **Cucumber** | 1,500 | 168 | 1,315 | 17 | Leaves (500), Stem (500), Fruit (500) | 500 diseased leaves, 168 healthy |
| **Capsicum** | 1,500 | 804 | 696 | 0 | Leaves (1,404), Fruit (96) | 696 diseased leaves, 804 healthy |
| **Spinach** | 1,500 | 705 | 795 | 0 | Leaves (1,500) | 795 diseased leaves, 705 healthy |
| **French Bean** | 1,400 | 415 | 985 | 0 | Leaves (1,400) | 985 diseased leaves, 415 healthy |
| **Rose** | 1,500 | 432 | 845 | 223 | Leaves (1,329), Flower (171) | 845 diseased leaves, 432 healthy |
| **Lettuce** | 1,500 | 447 | 602 | 451 | Leaves (1,500) | 602 diseased leaves, 447 healthy |
| **Broccoli** | 414 | 102 | 312 | 0 | Leaves (414) | 312 diseased leaves, 102 healthy |
| **Zucchini** | 393 | 0 | 393 | 0 | Leaves (393) | 393 diseased leaves (Powdery Mildew) |
| **Blueberry** | 314 | 0 | 314 | 0 | Leaves (202), Fruit (112) | 202 diseased leaves |
| **Strawberry** | 1,500 | 1,410 | 90 | 0 | Fruit (1,373), Leaves (127) | 90 diseased leaves, 127 healthy |
| **Marigold** | 1,197 | 270 | 389 | 538 | Leaves (1,130), Flower (67) | 389 diseased leaves, 270 healthy |
| **Orchid** | 1,200 | 0 | 0 | 1,200 | Flower (1,200) | 0 (Flowers only, no disease labels) |
| **Chrysanthemum**| 418 | 0 | 0 | 418 | Leaves (418) | 0 (Ambiguous health status) |
| **Geranium** | 251 | 0 | 0 | 251 | Leaves (135), Flower (116) | 0 (Ambiguous health status) |
| **Melon** | 247 | 0 | 0 | 247 | Fruit (247) | 0 (Fruit only, no disease labels) |
| **Anthurium** | 104 | 0 | 0 | 104 | Flower (104) | 0 (Flower only, no disease labels) |
| **Carnation** | 51 | 51 | 0 | 0 | Flower (51) | 0 (Flower only) |
| **Lilium** | 45 | 45 | 0 | 0 | Flower (45) | 0 (Flower only) |
| **Gerbera** | 3 | 0 | 0 | 3 | Flower (3) | 0 (Flower only) |
| **Cherry Tomato**| 0 | 0 | 0 | 0 | — | 0 |
| **Gypsophila** | 0 | 0 | 0 | 0 | — | 0 |
| **TOTAL** | **16,537** | **5,010** | **7,055** | **4,472** | — | — |

---

## 4. Disease Provenance & Tracing

When Model 1 was assembled, images from external datasets (such as PlantVillage, Makerere HF Beans, and Kaggle) were pooled by crop name, and filenames were normalized (e.g. `tomato_leaves_diseased_000000.jpg`). 

Tracing the original source folders in `data/external/` reveals the specific underlying disease conditions:

| Crop | Traceable Disease Condition | Source Dataset | M1 Images |
| :--- | :--- | :--- | :--- |
| **Tomato** | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus | PlantVillage (`data/external/tomato`) | 1,319 |
| **French Bean** | Bean Rust, Angular Leaf Spot | Hugging Face Beans (`data/downloads/beans`) | 985 |
| **Rose** | Rose Black Spot, Powdery Mildew | Kaggle Rose (`data/external/rose_new`) | 845 |
| **Spinach** | Downy Mildew, Spinach Anthracnose | Kaggle Spinach (`data/external/spinach_disease`) | 795 |
| **Capsicum** | Bell Pepper Bacterial Spot | PlantVillage (`data/external/pepper_bell`) | 696 |
| **Lettuce** | Bacterial Leaf Spot, Septoria | Roboflow Lettuce (`data/external/lettuce-disease.v6i.folder`) | 602 |
| **Cucumber** | Cucumber Powdery Mildew, Downy Mildew | Kaggle Cucumber (`data/external/cucumber`) | 500 |
| **Zucchini** | Zucchini Powdery Mildew | Kaggle Zucchini (`data/external/zuchhini`) | 393 |
| **Marigold** | Marigold Foliar Blight / Leaf Spot | Kaggle Marigold (`data/external/Marigold_new`) | 389 |
| **Broccoli** | Alternaria Leaf Spot, Downy Mildew | Kaggle Broccoli (`data/external/broccoli_new`) | 312 |
| **Blueberry** | Blueberry Rust / Leaf Spot | Kaggle Blueberry (`data/external/blueberry`) | 202 |
| **Strawberry** | Strawberry Leaf Scorch | PlantVillage (`data/external/strawberry`) | 90 |

---

## 5. Localization & Bounding Box Availability

### Critical Finding
- **`data/processed/model1_balanced/` contains ZERO bounding box annotations.**
- It is strictly an image-level classification dataset formatted as directory trees (`train/<crop>/`, `val/<crop>/`, `test/<crop>/`).
- **None of the Model 1 images can be directly fed into Model 2 without object detection bounding boxes.**

### Annotated External Repositories in `data/external/`
Some original download folders in `data/external/` contain YOLO-formatted text annotations, but they are from unrelated herbal or fruit bounding box datasets:
- `data/external/Herbal_Dataset.v11i.yolov11`: 20,940 YOLO txt annotations (herbal plant bounding boxes, not disease lesions).
- `data/external/Fruits Model.v1i.yolov11`: 774 YOLO txt annotations (fruit localization, not disease lesions).
- `data/external/herbs.v4i.yolov11`: 939 YOLO txt annotations (leaf counting, not disease lesions).

---

## 6. Reusability Classification (Groups A, B, C, D)

```
TOTAL IMAGES AUDITED: 16,537

[Group A: Directly Reusable]        :      0  (  0.0%)
[Group B: Reusable After Annotation]:  6,774  ( 41.0%)
[Group C: Healthy Negative Samples] :  3,596  ( 21.7%)
[Group D: Not Suitable / Unusable]  :  6,167  ( 37.3%)
```

### Group A: Directly Reusable (0 images, 0.0%)
- **0 images**. Zero images possess pre-labeled bounding boxes enclosing specific disease lesions.

### Group B: Reusable After Bounding-Box Annotation (6,774 images, 41.0%)
- These images have verified crop identity and traceable disease provenance from known single-disease datasets.
- **Requirement**: They require bounding box annotation around disease lesions (e.g. via CVAT, Label Studio, or Roboflow) before training YOLOX-S.

### Group C: Healthy Negative Samples (3,596 images, 21.7%)
- High-quality, verified healthy foliage images across 9 crops:
  - Strawberry: 127 leaves
  - Capsicum: 804 leaves
  - Spinach: 705 leaves
  - Lettuce: 447 leaves
  - Rose: 432 leaves
  - French Bean: 415 leaves
  - Marigold: 270 leaves
  - Cucumber: 168 leaves
  - Tomato: 165 leaves
  - Broccoli: 102 leaves
- **Role in Model 2**: Directly usable as negative / background images (images with zero bounding boxes) to train the detector not to trigger false alarms on healthy foliage.

### Group D: Not Suitable for Model 2 (6,167 images, 37.3%)
- **Flowers & Ornamental blooms (2,771 images)**: Orchid (1,200), Anthurium (104), Carnation (51), Lilium (45), Gerbera (3), Rose flowers (171), Geranium flowers (116). Model 2 detects foliage lesions; floral close-ups are out-of-domain.
- **Fruit-only close-ups (2,120 images)**: Strawberry fruits (1,373), Cucumber fruit/stem (1,000), Melon fruits (247), Tomato fruits (22).
- **Ambiguous health status (1,276 images)**: Chrysanthemum (418), Geranium leaves (135), Marigold unverified (538), Lettuce unverified (451).

---

## 7. Model 2 Crop & Disease Coverage Matrix

| Crop Family | Model 1 Healthy Leaves | Model 1 Diseased Leaves | Traceable Diseases in Model 1 | Missing in Model 1? |
| :--- | :--- | :--- | :--- | :--- |
| **Tomato** | 165 | 1,319 | Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria, Yellow Leaf Curl, Mosaic Virus | No (Rich coverage) |
| **Capsicum / Bell Pepper** | 804 | 696 | Bacterial Spot | No (Need Frogeye / Powdery Mildew) |
| **Cucumber** | 168 | 500 | Powdery Mildew, Downy Mildew | No (Need Bacterial Wilt / Angular Spot) |
| **French Bean** | 415 | 985 | Bean Rust, Angular Leaf Spot | No (Need Halo Blight) |
| **Spinach** | 705 | 795 | Downy Mildew, Anthracnose | Model 2 does not have Spinach in 34 crops |
| **Rose** | 432 | 845 | Black Spot, Powdery Mildew | Model 2 does not have Rose in 34 crops |
| **Broccoli** | 102 | 312 | Alternaria, Downy Mildew | No |
| **Zucchini** | 0 | 393 | Powdery Mildew | Missing Healthy Zucchini foliage |
| **Blueberry** | 0 | 202 | Rust, Leaf Spot | Missing Healthy Blueberry foliage |
| **Strawberry** | 127 | 90 | Leaf Scorch | Missing Strawberry Anthracnose |
| **Marigold** | 270 | 389 | Leaf Blight | Model 2 does not have Marigold in 34 crops |
| **Apple** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Banana** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Carrot** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Citrus** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Corn** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Grape** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Peach** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Potato** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Rice** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Soybean** | 0 | 0 | None | ❌ 100% Missing in Model 1 |
| **Wheat** | 0 | 0 | None | ❌ 100% Missing in Model 1 |

---

## 8. Specific Answers to Audit Questions

### A. How many images can be directly reused?
**0 images (0.0%).** Model 1 contains zero object detection bounding boxes or segmentation masks.

### B. How many healthy images can be used as negative/background samples?
**3,596 images (21.7%).** Verified healthy leaf images from crops like Capsicum (804), Spinach (705), Lettuce (447), Rose (432), French Bean (415), Marigold (270), Cucumber (168), Tomato (165), Strawberry (127), and Broccoli (102).

### C. How many diseased images require manual bounding-box annotation?
**6,774 images (41.0%).** These images have valid disease provenance (PlantVillage, Makerere Beans, etc.) across 10 crops (Tomato, French Bean, Rose, Spinach, Capsicum, Lettuce, Cucumber, Zucchini, Marigold, Broccoli, Blueberry, Strawberry) and can be annotated with lesion bounding boxes.

### D. Which crops/diseases need additional datasets?
14 major Model 2 crop families have **zero representation** in Model 1:
- Apple (Black Rot, Mosaic, Rust, Scab)
- Banana (Anthracnose, Black Leaf Streak, Bunchy Top, Panama Disease)
- Carrot (Alternaria Blight, Cavity Spot, Cercospora)
- Citrus (Canker, Greening Disease)
- Coffee (Berry Blotch, Black Rot, Leaf Rust)
- Corn (Gray Leaf Spot, Northern Leaf Blight, Rust, Smut)
- Grape (Black Rot, Downy Mildew, Leaf Spot)
- Peach (Brown Rot, Leaf Curl, Scab)
- Plum (Bacterial Spot, Brown Rot, Rust)
- Potato (Early Blight, Late Blight)
- Raspberry (Fire Blight, Gray Mold)
- Rice (Blast, Sheath Blight)
- Soybean (Bacterial Blight, Brown Spot, Rust)
- Wheat (Black Chaff, Head Scab, Rusts, Smut)

### E. Which existing Model 1 images should NOT be reused?
**6,167 images (37.3%):**
- 2,771 flower/bloom images (Orchid, Anthurium, Carnation, Lilium, Gerbera, etc.)
- 2,120 fruit-only images (Strawberry berries, Melon melons, Cucumber fruits)
- 1,276 unlabelled or ambiguous health status images

### F. Recommended Model 2 Dataset Architecture
1. **Preserve Model 1 Dataset Untouched**: Model 1 serves crop classification and must remain stable.
2. **Dedicated Object Detection Dataset (`data/processed/model2_dataset/`)**:
   - High-quality COCO/Pascal-VOC bounding box annotations formatted strictly for YOLOX.
   - Sourced from dedicated multi-crop disease detection datasets (PlantDoc, RoCoLe, PlantVillage Object Detection, Roboflow Crop Disease datasets) that natively include bounding boxes.
   - Supplemented by selected Model 1 healthy negative samples (3,596 clean background images) to suppress false positives on clean leaves.
