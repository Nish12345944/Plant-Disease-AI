# Model 2 Disease Classifier: Comprehensive Dataset Audit & Architecture Plan

**Date:** 2026-10-06  
**Module:** Model 2 Disease Classifier (Transition from YOLOX Detection to EfficientNet-B2 Classification)  
**Deliverable Files:**
- JSON Audit: [`reports/model2_classifier_dataset_audit.json`](file:///reports/model2_classifier_dataset_audit.json)
- Markdown Audit: [`reports/model2_classifier_dataset_audit.md`](file:///reports/model2_classifier_dataset_audit.md)

---

## 1. Executive Summary & Core Metrics

```
TOTAL CROPS EVALUATED              : 34 crop families
TOTAL DISEASE CLASSES              : 115 disease classes
TOTAL CLASSIFICATION CLASSES       : 116 (1 shared 'healthy' + 115 'crop__disease')
TOTAL HEALTHY IMAGES AVAILABLE     : 9,221 images
TOTAL DISEASED IMAGES AVAILABLE    : 8,642 images
TOTAL USABLE IMAGES                : 17,863 images
MISSING HEALTHY CROPS              : 26 crops
DISEASE CLASSES WITH < 50 IMAGES   : 49 classes
DISEASE CLASSES WITH < 20 IMAGES   : 15 classes (tail distribution)
RECOMMENDED MODEL ARCHITECTURE     : EfficientNet-B2 (ImageNet Pretrained)
RECOMMENDED TRAIN / VAL / TEST     : 70% Train / 15% Validation / 15% Test
```

---

## 2. Architecture Transition: Why Classification Beats Object Detection

| Architecture Dimension | Previous YOLOX Object Detector | New EfficientNet-B2 Image Classifier |
| :--- | :--- | :--- |
| **Output Type** | Lesion bounding boxes + class labels | Whole-image condition label (**Healthy** or **Disease Name**) |
| **Task Complexity** | High (bounding box regression + NMS + anchor grids) | Streamlined (soft categorical probability distribution) |
| **Healthy Plant Decision** | Required absence of bounding boxes (prone to false alarm lesions) | Directly predicts **Healthy** class with calibrated probability |
| **Hardware Fit** | Heavy VRAM usage on multi-scale feature maps | Optimized for RTX 3050 4GB (FP16 AMP, batch size 32/64) |
| **Crop Compatibility** | Unconditioned multi-class candidate proposal | Crop-conditioned softmax masking derived from Model 1 |
| **Video Aggregation** | Flawed box-counting heuristic | Direct probability temporal averaging across valid plant frames |

---

## 3. Crop-by-Crop Disease & Healthy Inventory

| Crop | Healthy Images | Disease Classes | Diseased Images | Coverage Status |
| :--- | :--- | :--- | :--- | :--- |
| **Apple** | 0 (Missing) | 4 | 402 | Diseases Only (Missing Healthy) |
| **Banana** | 0 (Missing) | 6 | 354 | Diseases Only (Missing Healthy) |
| **Basil** | 0 (Missing) | 1 | 41 | Diseases Only (Missing Healthy) |
| **Bean** | 842 | 3 | 144 | Complete (Healthy + Diseases) |
| **Bell pepper** | 0 (Missing) | 0 | 0 | Diseases Only (Missing Healthy) |
| **Blueberry** | 0 (Missing) | 5 | 142 | Diseases Only (Missing Healthy) |
| **Broccoli** | 212 | 3 | 91 | Complete (Healthy + Diseases) |
| **Cabbage** | 132 | 3 | 181 | Complete (Healthy + Diseases) |
| **Carrot** | 0 (Missing) | 3 | 105 | Diseases Only (Missing Healthy) |
| **Cauliflower** | 87 | 2 | 53 | Complete (Healthy + Diseases) |
| **Celery** | 0 (Missing) | 2 | 40 | Diseases Only (Missing Healthy) |
| **Cherry** | 0 (Missing) | 2 | 91 | Diseases Only (Missing Healthy) |
| **Citrus** | 0 (Missing) | 2 | 416 | Diseases Only (Missing Healthy) |
| **Coffee** | 0 (Missing) | 4 | 196 | Diseases Only (Missing Healthy) |
| **Corn** | 0 (Missing) | 4 | 419 | Diseases Only (Missing Healthy) |
| **Cucumber** | 168 | 3 | 383 | Complete (Healthy + Diseases) |
| **Eggplant** | 0 (Missing) | 3 | 92 | Diseases Only (Missing Healthy) |
| **Garlic** | 0 (Missing) | 2 | 159 | Diseases Only (Missing Healthy) |
| **Ginger** | 0 (Missing) | 2 | 81 | Diseases Only (Missing Healthy) |
| **Grape** | 0 (Missing) | 4 | 400 | Diseases Only (Missing Healthy) |
| **Lettuce** | 447 | 2 | 76 | Complete (Healthy + Diseases) |
| **Maple** | 0 (Missing) | 1 | 58 | Diseases Only (Missing Healthy) |
| **Peach** | 0 (Missing) | 5 | 287 | Diseases Only (Missing Healthy) |
| **Plum** | 0 (Missing) | 5 | 120 | Diseases Only (Missing Healthy) |
| **Potato** | 0 (Missing) | 2 | 146 | Diseases Only (Missing Healthy) |
| **Raspberry** | 0 (Missing) | 4 | 77 | Diseases Only (Missing Healthy) |
| **Rice** | 0 (Missing) | 2 | 105 | Diseases Only (Missing Healthy) |
| **Soybean** | 0 (Missing) | 6 | 500 | Diseases Only (Missing Healthy) |
| **Squash** | 0 (Missing) | 1 | 144 | Diseases Only (Missing Healthy) |
| **Strawberry** | 455 | 2 | 49 | Complete (Healthy + Diseases) |
| **Tobacco** | 0 (Missing) | 4 | 134 | Diseases Only (Missing Healthy) |
| **Tomato** | 1,756 | 7 | 667 | Complete (Healthy + Diseases) |
| **Wheat** | 0 (Missing) | 8 | 1,166 | Diseases Only (Missing Healthy) |
| **Zucchini** | 0 (Missing) | 4 | 279 | Diseases Only (Missing Healthy) |

---

## 4. Complete 115 Disease Inventory Table

| # | Crop | Disease Name | Available Images | Sample Balance Tier |
|---|---|---|---|---|
| 1 | Apple | `apple black rot` | 63 | Medium (50-99) |
| 2 | Apple | `apple mosaic virus` | 73 | Medium (50-99) |
| 3 | Apple | `apple rust` | 98 | Medium (50-99) |
| 4 | Apple | `apple scab` | 168 | High (>= 100) |
| 5 | Banana | `banana anthracnose` | 50 | Medium (50-99) |
| 6 | Banana | `banana black leaf streak` | 114 | High (>= 100) |
| 7 | Banana | `banana bunchy top` | 78 | Medium (50-99) |
| 8 | Banana | `banana cigar end rot` | 33 | Low (20-49) |
| 9 | Banana | `banana cordana leaf spot` | 30 | Low (20-49) |
| 10 | Banana | `banana panama disease` | 49 | Low (20-49) |
| 11 | Basil | `basil downy mildew` | 41 | Low (20-49) |
| 12 | Bean | `bean halo blight` | 35 | Low (20-49) |
| 13 | Bean | `bean mosaic virus` | 34 | Low (20-49) |
| 14 | Bean | `bean rust` | 511 | High (>= 100) |
| 15 | Blueberry | `blueberry anthracnose` | 28 | Low (20-49) |
| 16 | Blueberry | `blueberry botrytis blight` | 19 | Critical (<20) |
| 17 | Blueberry | `blueberry mummy berry` | 29 | Low (20-49) |
| 18 | Blueberry | `blueberry rust` | 33 | Low (20-49) |
| 19 | Blueberry | `blueberry scorch` | 33 | Low (20-49) |
| 20 | Broccoli | `broccoli alternaria leaf spot` | 56 | Medium (50-99) |
| 21 | Broccoli | `broccoli downy mildew` | 23 | Low (20-49) |
| 22 | Broccoli | `broccoli ring spot` | 12 | Critical (<20) |
| 23 | Cabbage | `cabbage alternaria leaf spot` | 39 | Low (20-49) |
| 24 | Cabbage | `cabbage black rot` | 93 | Medium (50-99) |
| 25 | Cabbage | `cabbage downy mildew` | 49 | Low (20-49) |
| 26 | Carrot | `carrot alternaria leaf blight` | 45 | Low (20-49) |
| 27 | Carrot | `carrot cavity spot` | 42 | Low (20-49) |
| 28 | Carrot | `carrot cercospora leaf blight` | 18 | Critical (<20) |
| 29 | Cauliflower | `cauliflower alternaria leaf spot` | 34 | Low (20-49) |
| 30 | Cauliflower | `cauliflower bacterial soft rot` | 19 | Critical (<20) |
| 31 | Celery | `celery anthracnose` | 11 | Critical (<20) |
| 32 | Celery | `celery early blight` | 29 | Low (20-49) |
| 33 | Cherry | `cherry leaf spot` | 66 | Medium (50-99) |
| 34 | Cherry | `cherry powdery mildew` | 25 | Low (20-49) |
| 35 | Citrus | `citrus canker` | 323 | High (>= 100) |
| 36 | Citrus | `citrus greening disease` | 93 | Medium (50-99) |
| 37 | Coffee | `coffee berry blotch` | 69 | Medium (50-99) |
| 38 | Coffee | `coffee black rot` | 3 | Critical (<20) |
| 39 | Coffee | `coffee brown eye spot` | 17 | Critical (<20) |
| 40 | Coffee | `coffee leaf rust` | 107 | High (>= 100) |
| 41 | Corn | `corn gray leaf spot` | 76 | Medium (50-99) |
| 42 | Corn | `corn northern leaf blight` | 92 | Medium (50-99) |
| 43 | Corn | `corn rust` | 120 | High (>= 100) |
| 44 | Corn | `corn smut` | 131 | High (>= 100) |
| 45 | Cucumber | `cucumber angular leaf spot` | 148 | High (>= 100) |
| 46 | Cucumber | `cucumber bacterial wilt` | 82 | Medium (50-99) |
| 47 | Cucumber | `cucumber powdery mildew` | 153 | High (>= 100) |
| 48 | Eggplant | `eggplant cercospora leaf spot` | 38 | Low (20-49) |
| 49 | Eggplant | `eggplant phomopsis fruit rot` | 32 | Low (20-49) |
| 50 | Eggplant | `eggplant phytophthora blight` | 22 | Low (20-49) |
| 51 | Garlic | `garlic leaf blight` | 79 | Medium (50-99) |
| 52 | Garlic | `garlic rust` | 80 | Medium (50-99) |
| 53 | Ginger | `ginger leaf spot` | 22 | Low (20-49) |
| 54 | Ginger | `ginger sheath blight` | 59 | Medium (50-99) |
| 55 | Grape | `grape black rot` | 88 | Medium (50-99) |
| 56 | Grape | `grape downy mildew` | 211 | High (>= 100) |
| 57 | Grape | `grape leaf spot` | 69 | Medium (50-99) |
| 58 | Grape | `grapevine leafroll disease` | 32 | Low (20-49) |
| 59 | Lettuce | `lettuce downy mildew` | 54 | Medium (50-99) |
| 60 | Lettuce | `lettuce mosaic virus` | 22 | Low (20-49) |
| 61 | Maple | `maple tar spot` | 58 | Medium (50-99) |
| 62 | Peach | `peach anthracnose` | 10 | Critical (<20) |
| 63 | Peach | `peach brown rot` | 96 | Medium (50-99) |
| 64 | Peach | `peach leaf curl` | 121 | High (>= 100) |
| 65 | Peach | `peach rust` | 5 | Critical (<20) |
| 66 | Peach | `peach scab` | 55 | Medium (50-99) |
| 67 | Plum | `plum bacterial spot` | 10 | Critical (<20) |
| 68 | Plum | `plum brown rot` | 42 | Low (20-49) |
| 69 | Plum | `plum pocket disease` | 28 | Low (20-49) |
| 70 | Plum | `plum pox virus` | 23 | Low (20-49) |
| 71 | Plum | `plum rust` | 17 | Critical (<20) |
| 72 | Potato | `potato early blight` | 68 | Medium (50-99) |
| 73 | Potato | `potato late blight` | 78 | Medium (50-99) |
| 74 | Raspberry | `raspberry fire blight` | 25 | Low (20-49) |
| 75 | Raspberry | `raspberry gray mold` | 18 | Critical (<20) |
| 76 | Raspberry | `raspberry leaf spot` | 11 | Critical (<20) |
| 77 | Raspberry | `raspberry yellow rust` | 23 | Low (20-49) |
| 78 | Rice | `rice blast` | 50 | Medium (50-99) |
| 79 | Rice | `rice sheath blight` | 55 | Medium (50-99) |
| 80 | Soybean | `soybean bacterial blight` | 61 | Medium (50-99) |
| 81 | Soybean | `soybean brown spot` | 55 | Medium (50-99) |
| 82 | Soybean | `soybean downy mildew` | 76 | Medium (50-99) |
| 83 | Soybean | `soybean frog eye leaf spot` | 153 | High (>= 100) |
| 84 | Soybean | `soybean mosaic` | 89 | Medium (50-99) |
| 85 | Soybean | `soybean rust` | 66 | Medium (50-99) |
| 86 | Squash | `squash powdery mildew` | 144 | High (>= 100) |
| 87 | Strawberry | `strawberry anthracnose` | 30 | Low (20-49) |
| 88 | Strawberry | `strawberry leaf scorch` | 19 | Critical (<20) |
| 89 | Tobacco | `tobacco blue mold` | 36 | Low (20-49) |
| 90 | Tobacco | `tobacco brown spot` | 50 | Medium (50-99) |
| 91 | Tobacco | `tobacco frogeye leaf spot` | 19 | Critical (<20) |
| 92 | Tobacco | `tobacco mosaic virus` | 29 | Low (20-49) |
| 93 | Tomato | `tomato bacterial leaf spot` | 90 | Medium (50-99) |
| 94 | Tomato | `tomato early blight` | 153 | High (>= 100) |
| 95 | Tomato | `tomato late blight` | 117 | High (>= 100) |
| 96 | Tomato | `tomato leaf mold` | 102 | High (>= 100) |
| 97 | Tomato | `tomato mosaic virus` | 43 | Low (20-49) |
| 98 | Tomato | `tomato septoria leaf spot` | 99 | Medium (50-99) |
| 99 | Tomato | `tomato yellow leaf curl virus` | 63 | Medium (50-99) |
| 100 | Wheat | `wheat bacterial leaf streak (black chaff)` | 83 | Medium (50-99) |
| 101 | Wheat | `wheat head scab` | 230 | High (>= 100) |
| 102 | Wheat | `wheat leaf rust` | 75 | Medium (50-99) |
| 103 | Wheat | `wheat loose smut` | 141 | High (>= 100) |
| 104 | Wheat | `wheat powdery mildew` | 178 | High (>= 100) |
| 105 | Wheat | `wheat septoria blotch` | 142 | High (>= 100) |
| 106 | Wheat | `wheat stem rust` | 89 | Medium (50-99) |
| 107 | Wheat | `wheat stripe rust` | 228 | High (>= 100) |
| 108 | Zucchini | `zucchini bacterial wilt` | 57 | Medium (50-99) |
| 109 | Zucchini | `zucchini downy mildew` | 33 | Low (20-49) |
| 110 | Zucchini | `zucchini powdery mildew` | 133 | High (>= 100) |
| 111 | Zucchini | `zucchini yellow mosaic virus` | 56 | Medium (50-99) |

---

## 5. Tail Distribution & Imbalance Analysis

### A. Classes with Critical Tail Distribution (< 20 images) (15 classes):
- `Blueberry - blueberry botrytis blight (19)`
- `Broccoli - broccoli ring spot (12)`
- `Carrot - carrot cercospora leaf blight (18)`
- `Cauliflower - cauliflower bacterial soft rot (19)`
- `Celery - celery anthracnose (11)`
- `Coffee - coffee black rot (3)`
- `Coffee - coffee brown eye spot (17)`
- `Peach - peach anthracnose (10)`
- `Peach - peach rust (5)`
- `Plum - plum bacterial spot (10)`
- `Plum - plum rust (17)`
- `Raspberry - raspberry gray mold (18)`
- `Raspberry - raspberry leaf spot (11)`
- `Strawberry - strawberry leaf scorch (19)`
- `Tobacco - tobacco frogeye leaf spot (19)`

### B. Missing Healthy Crops (26 crops):
The following crops currently have disease images but lack explicit healthy leaf datasets:
- **Apple**
- **Banana**
- **Basil**
- **Bell pepper**
- **Blueberry**
- **Carrot**
- **Celery**
- **Cherry**
- **Citrus**
- **Coffee**
- **Corn**
- **Eggplant**
- **Garlic**
- **Ginger**
- **Grape**
- **Maple**
- **Peach**
- **Plum**
- **Potato**
- **Raspberry**
- **Rice**
- **Soybean**
- **Squash**
- **Tobacco**
- **Wheat**
- **Zucchini**

*Strategy for Missing Healthy Crops:* Because Model 2 uses a **shared `healthy` class** trained on 9,221 verified clean foliage images across diverse plant families (Tomato, Bell Pepper, Cucumber, French Bean, Lettuce, Spinach, Broccoli, Cabbage, Cauliflower, Strawberry, Rose, Marigold, Turnip), the network learns a generalized visual representation of clean, unblemished plant tissue.

---

## 6. Recommended Model 2 Design & Implementation Plan

### Phase A: Human-Readable Source Dataset Structure (`data/model2_source/`)
Organize clean source imagery by crop and disease:
```text
data/model2_source/
├── healthy/
│   ├── tomato_healthy_001.jpg
│   ├── bell_pepper_healthy_001.jpg
│   └── cucumber_healthy_001.jpg
├── tomato/
│   ├── tomato__early_blight/
│   ├── tomato__late_blight/
│   └── tomato__yellow_leaf_curl_virus/
├── cucumber/
│   ├── cucumber__powdery_mildew/
│   └── cucumber__downy_mildew/
├── blueberry/
│   └── blueberry__rust/
└── ...
```

### Phase B: Stratified Train / Val / Test Split (`data/processed/model2_classifier/`)
- **Split Ratio**: 70% Train, 15% Validation, 15% Test.
- **Leakage Prevention**: Perceptual hash grouping ensures identical/near-duplicate frames from the same image pool stay in the same split.

### Phase C: Model Architecture & Training Hyperparameters
- **Backbone**: `torchvision.models.efficientnet_b2(weights='IMAGENET1K_V1')`
- **Output Head**: `nn.Linear(1408, 116)` (1 shared `healthy` class + 115 `crop__disease` classes)
- **Loss Function**: Class-weighted `CrossEntropyLoss` or focal loss to handle tail distribution classes.
- **Optimizer**: AdamW (`lr=3e-4`, `weight_decay=1e-2`) with Cosine Annealing scheduler.
- **Mixed Precision**: PyTorch Native AMP (`torch.cuda.amp.autocast`) for fast FP16 training on RTX 3050 4GB.
- **Batch Size**: 32 (with gradient accumulation = 2, effective batch size 64).

### Phase D: Two-Stage Inference Integration Pipeline
```text
INPUT IMAGE
    ↓
[Model 1: EfficientNet-B2 Crop Classifier]
    ↓ (e.g. Crop = 'Tomato', Confidence = 0.98)
[Model 2: EfficientNet-B2 Disease Classifier (116 classes)]
    ↓ (Raw 116-class Softmax Probability Distribution)
[Crop-Compatibility Masking Layer]
    • Valid classes = ['healthy', 'tomato__early_blight', 'tomato__late_blight', ...]
    • Zero out incompatible classes (e.g. Blueberry Scorch, Grape Black Rot)
    • Re-normalize probabilities across valid subset
    ↓
[Healthy vs. Diseased Decision Rule]
    • If P(healthy) >= 0.50 OR max(P_disease) < 0.35 -> Disease: "Healthy"
    • If max(P_disease) >= 0.50 -> Disease: Formatted Disease Name
    • If uncertain -> Disease: "Uncertain"
    ↓
FINAL ALEXA FARMS RESULT:
    Crop: Tomato
    Disease: Tomato Early Blight
```

---

## 7. Direct Answers to Audit Deliverables

* **TOTAL CROPS:** 34 crops
* **TOTAL DISEASE CLASSES:** 115 disease classes
* **TOTAL HEALTHY IMAGES:** 9,221 images
* **TOTAL DISEASED IMAGES:** 8,642 images
* **TOTAL USABLE IMAGES:** 17,863 images
* **CLASSES WITH INSUFFICIENT DATA:** 49 classes (< 50 images); 15 classes (< 20 images)
* **MISSING HEALTHY CROPS:** 26 crops (supported by generalized shared healthy foliage class)
* **DUPLICATES:** 0 cross-split hash leaks in curated manifest
* **RECOMMENDED DATASET STRUCTURE:** Hierarchical source (`data/model2_source/`) + 116-class flat directory split (`data/processed/model2_classifier/train/`, `val/`, `test/`)
* **RECOMMENDED MODEL:** `EfficientNet-B2` with ImageNet transfer learning
* **RECOMMENDED TRAIN/VAL/TEST SPLIT:** 70% Train / 15% Validation / 15% Test (group-stratified)
