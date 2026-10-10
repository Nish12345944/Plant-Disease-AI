# Model 1 Expanded EXP-2 — Phase 2: Targeted Data Acquisition Report

**Report Date:** October 10, 2026  
**Project Root:** [`C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction)  
**Authoritative Manifest:** [`data/processed/model1_expanded_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/processed/model1_expanded_manifest.csv) (18,176 records)  
**Staging Directory:** [`data/external/model1_exp2/raw_acquisitions/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions)  
**Candidate Manifest:** [`reports/model1_expansion/exp2/exp2_acquisition_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp2/exp2_acquisition_manifest.csv)  
**Status:** **PHASE 2 ACQUISITION COMPLETE & VERIFIED** — All 5 deficit targets exceeded with 100% real, botanically-verified, deduplicated images.

---

## 1. Executive Summary & Acquisition Scorecard

In accordance with the EXP-2 Data Gap Audit ([`reports/model1_expansion/exp2/exp2_dataset_gap_audit.md`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp2/exp2_dataset_gap_audit.md)), Phase 2 targeted the acquisition of genuine, botanically-verified physical photographs for the 5 priority bottleneck classes.

A total of **1,090 unique, clean, high-resolution candidate images** were successfully acquired, verified, and staged under `data/external/model1_exp2/raw_acquisitions/`. Every class target has been met and exceeded.

### Acquisition Summary Table

| Priority Class | Pre-Acquisition Train | Audit Target Minimum | Real Images Acquired & Staged | Surplus Over Target | Post-Acquisition Projected Train | Verified Usable Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **cherry** | 111 | +239 | **260** | **+21** | 371 | **TARGET MET (108.8%)** |
| **celery** | 53 | +197 | **220** | **+23** | 273 | **TARGET MET (111.7%)** |
| **carnation** | 41 | +159 | **190** | **+31** | 231 | **TARGET MET (119.5%)** |
| **lilium** | 37 | +163 | **190** | **+27** | 227 | **TARGET MET (116.6%)** |
| **gypsophila** | 0 | +200 | **230** | **+30** | 230 | **TARGET MET (115.0%)** |
| **TOTAL** | **242** | **+958** | **1,090** | **+132** | **1,332** | **ALL TARGETS EXCEEDED** |

> [!IMPORTANT]
> **Strict Non-Augmentation Confirmation:** Zero synthetic augmentations (no rotations, flips, blurs, or color shifts) were generated. Every single one of the 1,090 staged files represents a distinct, genuine biological photograph verified by SHA-256 and perceptual hashing.

---

## 2. In-Depth Per-Class Provenance & Botanical Verification

### 2.1 Cherry (`cherry`) — Prunus avium & Prunus cerasus
- **Target Shortage:** +239 images $\rightarrow$ **Acquired: 260 verified images**.
- **Taxonomic Focus:** Sweet Cherry (*Prunus avium*, Taxon ID 61964) and Sour Cherry (*Prunus cerasus*, Taxon ID 68763).
- **Botanical Verification:** Research-grade community botanist consensus. Focuses on tree foliage, leaf margins, and orchard branch contexts to eliminate the previous tight-crop background bias that caused cross-talk with Peach, Plum, and Apple.
- **Resolution Range:** 225×500 to 500×500 RGB.
- **Staging Location:** [`data/external/model1_exp2/raw_acquisitions/cherry/inaturalist_research/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions/cherry/inaturalist_research)

### 2.2 Celery (`celery`) — Apium graveolens
- **Target Shortage:** +197 images $\rightarrow$ **Acquired: 220 verified images**.
- **Taxonomic Focus:** Cultivated and wild celery (*Apium graveolens*, Taxon ID 58788).
- **Botanical Verification:** Research-grade observations capturing compound leaves, serrated margins, and vegetative stalks.
- **Resolution Range:** 225×500 to 500×500 RGB.
- **Staging Location:** [`data/external/model1_exp2/raw_acquisitions/celery/inaturalist_research/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions/celery/inaturalist_research)

### 2.3 Carnation (`carnation`) — Dianthus caryophyllus & Dianthus barbatus
- **Target Shortage:** +159 images $\rightarrow$ **Acquired: 190 verified images**.
- **Taxonomic Focus:** Carnation / Clove Pink (*Dianthus caryophyllus*, Taxon ID 83063 / 1249905) and Sweet William (*Dianthus barbatus*, Taxon ID 60874).
- **Botanical Verification:** Resolves the previous single-source vulnerability (which had only 41 training images). Includes varied greenhouse, cut-flower, and garden specimens with characteristic fringed petal margins and glaucous linear foliage.
- **Resolution Range:** 225×500 to 500×500 RGB.
- **Staging Location:** [`data/external/model1_exp2/raw_acquisitions/carnation/inaturalist_research/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions/carnation/inaturalist_research)

### 2.4 Lilium (`lilium`) — True Lilies (Genus Lilium)
- **Target Shortage:** +163 images $\rightarrow$ **Acquired: 190 verified images**.
- **Taxonomic Focus:** True lilies (*Lilium* genus, Taxon ID 48928), including *Lilium lancifolium* (tiger lily), *Lilium candidum* (Madonna lily), *Lilium regale*, and *Lilium longiflorum* (Easter lily).
- **Botanical Verification:** True lilies verified with six tepals and lanceolate alternate leaves, strictly distinguishing them from daylilies (*Hemerocallis*) and water lilies (*Nymphaea*).
- **Resolution Range:** 225×500 to 500×500 RGB.
- **Staging Location:** [`data/external/model1_exp2/raw_acquisitions/lilium/inaturalist_research/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions/lilium/inaturalist_research)

### 2.5 Gypsophila (`gypsophila`) — Baby's Breath (Genus Gypsophila)
- **Target Shortage:** +200 images $\rightarrow$ **Acquired: 230 verified images**.
- **Taxonomic Focus:** Single-species *Gypsophila paniculata* (Taxon ID 77322) and *Gypsophila elegans* (Taxon ID 163456).
- **Botanical Verification:** Establishes the **P0 founding dataset** for Gypsophila, completely eliminating the 0-sample gap. All specimens are single-species verified panicles with diffuse white/pinkish inflorescences, completely avoiding the multi-species Daisy/Hydrangea contamination from the rejected Roboflow set.
- **Resolution Range:** 225×500 to 500×500 RGB.
- **Staging Location:** [`data/external/model1_exp2/raw_acquisitions/gypsophila/inaturalist_research/`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/raw_acquisitions/gypsophila/inaturalist_research)

---

## 3. License Distribution & Compliance

All 1,090 images were acquired under explicit open-access and creative commons licenses:

| License | Image Count | Percentage | Commercial / Academic Status |
| :--- | :---: | :---: | :--- |
| **CC BY-NC 4.0** | 919 | 84.31% | Attribution Non-Commercial (Permitted for research & evaluation) |
| **CC BY 4.0** | 102 | 9.36% | Attribution Open Access |
| **CC0 (Public Domain)** | 35 | 3.21% | Public Domain Dedication |
| **CC BY-NC-SA 4.0** | 15 | 1.38% | Non-Commercial Share-Alike |
| **CC BY-SA 4.0** | 11 | 1.01% | Attribution Share-Alike |
| **CC BY-NC-ND 4.0** | 6 | 0.55% | Non-Commercial No-Derivatives |
| **CC BY-ND 4.0** | 2 | 0.18% | Attribution No-Derivatives |
| **TOTAL** | **1,090** | **100.0%** | **Fully Audited & Documented** |

---

## 4. Deduplication & Contamination Screening Audit

The acquisition script ([`scripts/acquire_model1_exp2_data.py`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/acquire_model1_exp2_data.py)) executed a multi-tier deduplication and validation pipeline:

### 4.1 Filter & Rejection Statistics (74 Rejected)
- **Exact SHA-256 Overlaps with Existing 18,176 Images:** 0 admitted (any existing hash match immediately dropped).
- **Intra-Batch Near-Duplicates (pHash $d_H \le 4$):** 48 candidate photos rejected as burst shots or minor crops of identical specimens.
- **Low Resolution ($< 224\times 224$):** 16 photos rejected.
- **Network / Corrupted Byte Streams:** 10 downloads discarded.

All 74 rejected candidates and reasons are logged in [`data/external/model1_exp2/manifests/exp2_rejected_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/manifests/exp2_rejected_manifest.csv).

### 4.2 Cross-Split Zero Leakage Confirmation
- **Protected Test Set (1,586 Images):** Unmodified and completely isolated. 0 hash or perceptual overlap exists between the 1,090 staged images and the test set.

---

## 5. Machine-Readable Deliverables Catalog

1. **Accepted Candidates Manifest:**
   - [`reports/model1_expansion/exp2/exp2_acquisition_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model1_expansion/exp2/exp2_acquisition_manifest.csv) (1,090 rows)
   - Columns: `canonical_crop`, `filename`, `staged_relpath`, `source_dataset`, `source_url`, `observation_id`, `photo_id`, `original_label`, `license`, `sha256`, `phash`, `width`, `height`, `quality_status`, `duplicate_status`, `acceptance_reason`, `retrieval_date`.
2. **Rejected Candidates Manifest:**
   - [`data/external/model1_exp2/manifests/exp2_rejected_manifest.csv`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/manifests/exp2_rejected_manifest.csv) (74 rows)
3. **Acquisition Summary JSON:**
   - [`data/external/model1_exp2/manifests/exp2_acquisition_summary.json`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/data/external/model1_exp2/manifests/exp2_acquisition_summary.json)
4. **Acquisition Pipeline Script:**
   - [`scripts/acquire_model1_exp2_data.py`](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/acquire_model1_exp2_data.py)

---

## 6. Safety Verification: Protected Assets Status

The following protected assets were audited post-acquisition and verified 100% untouched:

- `models/model1/best_model.pth` — **UNTOUCHED**
- `data/processed/model1_balanced/` — **UNTOUCHED**
- `models/model1_expanded/best_model.pth` — **UNTOUCHED**
- `models/model1_expanded/exp1/` — **UNTOUCHED**
- `models/model2_classifier_v4/` — **UNTOUCHED**
- `backups/model1_expansion_phase1_snapshot/` — **UNTOUCHED**
- `data/processed/model1_expanded_manifest.csv` (18,176 records) — **UNTOUCHED**
- `data/processed/model1_expanded/test/` (1,586 protected test images) — **UNTOUCHED**
- No model training or evaluation was performed.

---

## 7. Next Actions for EXP-2 Phase 3 (Ingestion & Dataset Integration)

With 1,090 verified candidate images staged under `data/external/model1_exp2/raw_acquisitions/`:
1. Execute Phase 3 ingestion planning to integrate the staged images into `data/processed/model1_expanded/` train and validation splits (allocating ~85% to train and ~15% to validation, with 0 changes to the test set).
2. Update the authoritative manifest with new SHA-256 provenance records.
3. Validate complete dataset integrity before launching Model 1 Expanded EXP-2 training.
