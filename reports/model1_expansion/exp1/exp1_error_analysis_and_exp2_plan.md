# EXP-1 Forensic Error Analysis & Controlled EXP-2 Plan

**Date:** October 10, 2026  
**Project Root:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
**Target Model:** Expanded Model 1 (46-Class Plant Identification Classifier)  
**Evaluated Artifact:** [`models/model1_expanded/exp1/best_model_exp1.pth`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1_expanded/exp1/best_model_exp1.pth) (Global Epoch 14, Stage 2 Epoch 10)  
**Test Set Evidence:** [`reports/model1_expansion/exp1/exp1_test_evaluation_report.md`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_test_evaluation_report.md) (1,586 test images, 163 misclassifications, 10.28% error rate)  

---

## 1. Executive Summary & Core Diagnostic Findings

The EXP-1 Two-Stage Transfer Learning experiment achieved **89.72% Top-1 Test Accuracy**, **96.97% Top-3 Accuracy**, and an active-class **Macro F1 of 84.71%** (a **+0.90% overall Macro F1 gain** and a **+3.62% gain on the Original-22 crop taxonomy** to **96.13%** compared to EXP-0).

A detailed forensic analysis of all 163 test misclassifications ([`exp1_misclassifications.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_misclassifications.csv)) revealed three distinct failure modes:

1. **Botanical Family Morphological Clusters (62.6% of errors, 102/163):** Visual confusion between closely related species within the same botanical family (*Rosaceae* stone/pome fruits, *Brassicaceae* crucifers, *Fabaceae* legumes, and *Poaceae* monocots).
2. **Plant Part & Organ Ambiguity (19.0% of errors, 31/163):** Fruit vs. fruit and flower vs. flower confusions (e.g., dark blueberry clusters confused with dark grapes or plums; chrysanthemum flowers confused with gerberas).
3. **Severe Minority Sample Imbalance & Overconfidence (18.4% of errors, 30/163):** Extreme variance and collapsed precision on classes with very small evaluation support (e.g., basil, celery, ginger, cherry).

---

## 2. Weakest Performing Active Classes

The following 9 active classes exhibited the lowest test F1 scores ($F_1 < 75.0\%$):

| Class Name | Subset | Test Support | Precision | Recall | Test F1 | Training Support | Primary Error Mechanism |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **ginger** | NEW_24 | 9 | 40.00% | 44.44% | **42.11%** | 354 | Monocot strap-leaf similarity (confused with garlic & rice) |
| **cherry** | NEW_24 | 14 | 55.56% | 35.71% | **43.48%** | 111 | Rosaceae foliage similarity (confused with plum, peach, apple) |
| **basil** | NEW_24 | 6 | 35.71% | 83.33% | **50.00%** | 568 | Broadleaf mildew false positives (4 zucchini & 1 cherry falsely predicted as basil) |
| **cauliflower** | NEW_24 | 10 | 55.56% | 50.00% | **52.63%** | 425 | *Brassica oleracea* vegetative leaf confusion with broccoli |
| **garlic** | NEW_24 | 20 | 63.64% | 70.00% | **66.67%** | 158 | Monocot parallel venation confusion with wheat |
| **plum** | NEW_24 | 22 | 77.78% | 63.64% | **70.00%** | 299 | Rosaceae leaf spot confusion with cherry & apple |
| **rice** | NEW_24 | 16 | 73.33% | 68.75% | **70.97%** | 123 | Gramineae leaf streak confusion with wheat |
| **celery** | NEW_24 | 6 | 62.50% | 83.33% | **71.43%** | 53 | Low training support; compound leaf serration overlap |
| **eggplant** | NEW_24 | 14 | 71.43% | 71.43% | **71.43%** | 394 | Solanaceae broadleaf overlap with bellpepper/potato |

---

## 3. Systematic Grouping of Failure Modes

### 3.1 Failure Mode A: Botanical Family Foliage Similarity

```
[Family Clusters]
├── Rosaceae (Pome & Stone Fruits)
│   ├── peach -> apple (5 errors)
│   ├── plum -> cherry (3 errors)
│   ├── plum -> apple (2 errors)
│   └── cherry -> rose (2 errors)
├── Brassicaceae (Cruciferous Crops - Brassica oleracea)
│   ├── cabbage -> broccoli (4 errors)
│   ├── cauliflower -> broccoli (3 errors)
│   └── broccoli -> cabbage (2 errors)
├── Fabaceae (Legumes)
│   ├── french_bean -> soybean (4 errors)
│   └── soybean -> french_bean (1 error)
└── Poaceae & Monocots (Cereals & Alliums)
    ├── wheat -> corn (4 errors)
    ├── wheat -> garlic (4 errors)
    ├── garlic -> wheat (3 errors)
    └── ginger -> rice (2 errors)
```

**Forensic Evidence:**
- In *Brassicaceae*, cabbage, broccoli, and cauliflower share identical genetic origins (*Brassica oleracea*). When images display early-stage seedling leaves or isolated diseased leaf patches without heads or inflorescences, 2D CNN features at 224×224 resolution cannot reliably differentiate the species.
- In *Rosaceae*, peach, apple, plum, and cherry share serrated margin leaf shapes with brown spot / rust fungal lesions.

### 3.2 Failure Mode B: Plant Part & Organ Ambiguity (Fruit / Berry vs. Leaf)
- **Blueberry $\rightarrow$ Plum / Grape:** Multiple blueberry images showing ripe dark blue/purple berries were classified as plum (`blueberry_1de5f8467c_blueberry_fruit_diseased_014151.jpg`, 98.6% confidence) or grape (`blueberry_26b5b9c370_blueberry_fruit_diseased_014368.jpg`, 94.1% confidence; `blueberry_ec6bd77493_blueberry_fruit_diseased_014281.jpg`, 97.9% confidence).
- **Chrysanthemum $\rightarrow$ Gerbera:** Composite flower head images (`chrysanthemum_6976d3df1b...jpg`, 99.8% confidence) confused with Gerbera daisies.
- **Root Cause:** Model 1 is trained on whole-image representations that encompass leaves, stems, flowers, and fruits without explicit organ-mask conditioning.

### 3.3 Failure Mode C: Low-Support Evaluation Variance & False Positive Sink
- **Basil False Positive Sink:** While basil recall is high (83.33%, 5/6 correct), its precision dropped to 35.71% because 9 other crops (including 4 zucchini, 1 cherry, 1 citrus, 1 apple, 1 lettuce, 1 tomato) were falsely predicted as basil.
- **Cause:** Basil has 568 training images with extensive web-scraped color/lighting diversity, causing the classifier head to develop a broad decision region for textured green leaves.

---

## 4. Source-Domain & Training Composition Inspection

Analyzing the provenance manifest (`data/processed/model1_expanded_manifest.csv`) for the weakest classes without test-set contamination:

| Class | Total Disk | Train | Val | Test | Dominant Source | Source Distribution Notes |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **cherry** | 139 | 111 | 14 | 14 | `web_scraped_verified` (59%) | Severe shortage; high field noise in web scrapes |
| **celery** | 65 | 53 | 6 | 6 | `web_scraped_verified` (63%) | Severe data deficit (<100 total images) |
| **rice** | 155 | 123 | 16 | 16 | `internal_ingested` (56%) | Mixed field lighting and narrow viewing angles |
| **garlic** | 198 | 158 | 20 | 20 | `internal_ingested` (72%) | Moderate deficit; monocot leaf streaks dominate |
| **ginger** | 372 | 354 | 9 | 9 | `roboflow_verified` (76%) | Heavy synthetic/studio background bias in source |
| **gypsophila** | 0 | 0 | 0 | 0 | None (Halted in Phase 3B) | **100% Zero-Data Gap Class** |
| **cherry_tomato**| 0 | 0 | 0 | 0 | None (Taxonomy gap) | **100% Zero-Data Gap Class** |

---

## 5. Ranked Remediation Plan

### Tier 1: High-Priority Dataset Ingestion & Curation (No Code Changes)
1. **Acquire and Ingest Curated `cherry` Images (+250 to +300 real images):** Cherry is currently the weakest tree fruit class ($F_1 = 43.48\%$) due to having only 111 training images.
2. **Targeted Acquisition for Minority Deficit Classes:**
   - `celery`: Expand from 53 $\rightarrow \ge 250$ images.
   - `carnation`: Expand from 41 $\rightarrow \ge 200$ images.
   - `lilium`: Expand from 37 $\rightarrow \ge 200$ images.
3. **Curate Single-Species `gypsophila`:** Extract verified single-species Gypsophila samples from verified botanical repositories to eliminate the 0-support gap.

### Tier 2: Taxonomic Disambiguation & Hard-Negative Balancing
1. **Brassica Disambiguation:** Introduce higher resolution inputs (256×256 or 288×288) or texture-preserving augmentations to capture fine vein structure differences between cabbage, broccoli, and cauliflower.
2. **Rosaceae Disambiguation:** Balance loss weights and sample frequencies for peach, plum, cherry, and apple to avoid dominant-class attractor bias.
3. **Monocot Disambiguation:** Regulate wheat, corn, garlic, and ginger feature embeddings via contrastive or multi-crop consistency regularization.

### Tier 3: Model Architecture & Optimization Enhancements (EXP-2)
1. **Label Smoothing Regularization:** Implement `label_smoothing=0.08` in `CrossEntropyLoss` to eliminate the 31 overconfident ($>90\%$ confidence) misclassifications.
2. **Native EfficientNet-B2 Resolution (288×288):** Upscale input resolution from 224×224 to EfficientNet-B2's native 288×288 resolution (GPU-safe on RTX 3050 with batch size 16).
3. **Cosine Warmup with Higher Backbone Learning Rate:** Extend Stage 2 to 12 epochs with a 1-epoch linear warmup before cosine decay.

---

## 6. Recommended Controlled EXP-2 Design

### 6.1 Controlled Factor Isolation vs. EXP-1
| Experimental Factor | EXP-0 Baseline | EXP-1 (Completed) | Proposed EXP-2 | Rationale |
| :--- | :---: | :---: | :---: | :--- |
| **Schedule** | Single-Stage (14 ep) | Two-Stage (4 ep S1 + 10 ep S2) | Two-Stage (4 ep S1 + 12 ep S2) | Retain two-stage isolation; extend fine-tuning |
| **Input Resolution** | 224 × 224 | 224 × 224 | **288 × 288** | Native EfficientNet-B2 resolution for vein detail |
| **Loss Function** | Class-Weighted CE | Class-Weighted CE | **Class-Weighted CE + Label Smoothing (0.08)** | Suppresses overconfident cross-family errors |
| **Optimizer** | AdamW (`lr=3e-4`) | S1: `1e-3`, S2: `7e-5 → 1e-6` | S1: `1e-3`, S2: `8e-5 → 5e-7` | Optimized learning rate trajectory |
| **Batch Size** | 16 | 16 | **16** | RTX 3050 4 GB VRAM verified safe |
| **Image Decoding** | Naive Pillow | Bounded Draft (448×448) | **Bounded Draft (576×576)** | Bounded memory with native 288×288 support |

### 6.2 Strict Safety Invariants for EXP-2
- **Isolated Output Paths:**
  - Model Checkpoints: `models/model1_expanded/exp2/best_model_exp2.pth`
  - Reports & Metrics: `reports/model1_expansion/exp2/`
- **Protected Assets Locked:**
  - `models/model1/best_model.pth` (Production locked)
  - `models/model1_expanded/best_model.pth` (EXP-0 baseline locked)
  - `models/model1_expanded/exp1/` (EXP-1 artifacts locked)
  - `models/model2_classifier_v4/` (Production Model 2 locked)
  - `data/processed/model1_balanced/` (Production dataset locked)
- **Validation-Only Model Selection:** Early stopping and best checkpoint selection strictly driven by validation Active Macro F1.
- **Immutable Test Split:** The 1,586 test images remain untouched and evaluated only after EXP-2 training finishes.

---

## 7. Machine-Readable Artifact References

- Test Evaluation Report: [`reports/model1_expansion/exp1/exp1_test_evaluation_report.md`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_test_evaluation_report.md)
- Per-Class Metrics CSV: [`reports/model1_expansion/exp1/exp1_per_class_metrics.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_per_class_metrics.csv)
- Full Misclassifications Catalog: [`reports/model1_expansion/exp1/exp1_misclassifications.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_misclassifications.csv)
- Confusion Matrix: [`reports/model1_expansion/exp1/exp1_confusion_matrix.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp1/exp1_confusion_matrix.json)
- Training Summary: [`models/model1_expanded/exp1/training_summary_exp1.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model1_expanded/exp1/training_summary_exp1.json)
