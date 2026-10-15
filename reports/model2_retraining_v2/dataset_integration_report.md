# Model 2 Retraining V2 — Dataset Integration Report

**Date:** 2026-10-12  
**Dataset Source:** `data/external/model2_new_data/`  
**Target Dataset Version:** `model2_retraining_v2`  
**Baseline Model:** Model 2 Retraining V1 (143 Classes, EfficientNet-B2)  

---

## 1. Executive Summary

A comprehensive, multi-phase audit of the new raw image collection in `data/external/model2_new_data/` was conducted to prepare an isolated, reproducible dataset version (`model2_retraining_v2`) for future training experiments.

| Metric | Count | Details |
| :--- | :--- | :--- |
| **Total Raw Files Scanned** | **3,581** | Across 17 leaf directories |
| **Valid & Readable Images** | **3,581** (100%) | 3,577 `.jpg`, 2 `.webp`, 2 `.png`; 0 corrupt files |
| **Unique SHA-256 Hashes** | **3,216** | 365 exact duplicate copies within source data |
| **Exact V1 Train Duplicates** | **323** | 323 of 324 images in `Blueberry Fruit healthy` already exist in V1 Train |
| **Exact V1 Val Duplicates** | **0** | Clean; zero exact validation leaks |
| **Exact Protected Test Duplicates** | **0** | Clean; zero exact test leaks |
| **Protected Test Near-Duplicates (pHash $\le$ 4)** | **48** | Quarantined to prevent benchmark contamination |
| **Cross-Folder Label Collisions** | **213** | 107 distinct SHAs appearing across conflicting label folders |
| **Accepted Clean Images (Existing Classes)** | **2,273** | High-confidence additions to 12 existing V1 classes |
| **Images Pending Review (New/Ambiguous)** | **567** | Tomato Anthracnose (336) & Tomato Fusarium Wilt (231) |

---

## 2. Source Inventory & Data Quality

All 3,581 files across 17 leaf directories were individually verified using PIL and SHA-256 hashing:

| Leaf Directory | Total Files | Valid | Corrupt | Extensions | Unique SHAs | Internal Redundancy |
| :--- | :---: | :---: | :---: | :--- | :---: | :---: |
| `banana cigar end rot` | 204 | 204 | 0 | .jpg:204 | 196 | 8 |
| `Blueberry Fruit healthy` | 324 | 324 | 0 | .jpg:324 | 324 | 0 |
| `broccoli/broccoli alternaria leaf spot` | 272 | 272 | 0 | .jpg:272 | 245 | 27 |
| `broccoli/broccoli downy mildew` | 232 | 232 | 0 | .jpg:232 | 209 | 23 |
| `broccoli/broccoli healthy` | 158 | 158 | 0 | .jpg:158 | 148 | 10 |
| `broccoli/broccoli ring spot` | 205 | 205 | 0 | .jpg:205 | 185 | 20 |
| `celery anthracnose` | 98 | 98 | 0 | .jpg:98 | 98 | 0 |
| `eggplant/eggplant phomopsis blight` | 35 | 35 | 0 | .jpg:35 | 35 | 0 |
| `eggplant/eggplant phytophthora spot` | 234 | 234 | 0 | .jpg:234 | 234 | 0 |
| `eggplant/eggplant_phomopsis` | 88 | 88 | 0 | .jpg:88 | 79 | 9 |
| `lettuce/lettuce downy mildew` | 149 | 149 | 0 | .jpg:149 | 144 | 5 |
| `lettuce/lettuce mosaic virus` | 113 | 113 | 0 | .jpg:113 | 113 | 0 |
| `tomato/early blight of tomato fruit` | 358 | 358 | 0 | .jpg:358 | 309 | 49 |
| `tomato/Late blight of tomato fruit` | 310 | 310 | 0 | .jpg:308, .webp:2 | 258 | 52 |
| `tomato/tomato fruit Anthracnose` | 336 | 336 | 0 | .jpg:334, .png:2 | 272 | 64 |
| `tomato/tomato fruit fusarium wilt` | 231 | 231 | 0 | .jpg:231 | 188 | 43 |
| `tomato/tomato yellow curl virus` | 234 | 234 | 0 | .jpg:234 | 189 | 45 |
| **Total** | **3,581** | **3,581** | **0** | — | **3,216** | **365** |

---

## 3. Taxonomy Reconciliation & Label Analysis

### 3.1 Mapping to Existing Model 2 V1 Classes

1. **`banana cigar end rot` &rarr; `banana__cigar_end_rot` (Class ID 8)**  
   *Musicillium theobromae* causes classic necrotic tip rot on banana fingers. Directly aligns with existing class 8.  
   - Action: `ADD_TO_EXISTING_CLASS`. (196 unique images).

2. **`Blueberry Fruit healthy` &rarr; `healthy` (Class ID 0)**  
   Model 2 maintains a single, unified healthy class (`healthy`, Class ID 0) for all crop foliage and fruit.  
   - 323 of 324 images are exact SHA-256 duplicates of existing `train/blueberry/healthy/` images.  
   - Action: 323 images excluded as historical duplicates; 1 unique image accepted into `healthy`.

3. **`broccoli/broccoli healthy` &rarr; `healthy` (Class ID 0)**  
   Clean non-conflicting images mapped to shared `healthy` (Class ID 0). 1 image colliding with ring spot excluded.

4. **Broccoli Disease Folders (`alternaria leaf spot`, `downy mildew`, `ring spot`)**  
   - Mapped to `broccoli__alternaria_leaf_spot` (Class ID 28), `broccoli__downy_mildew` (Class ID 29), and `broccoli__ring_spot` (Class ID 30).  
   - Web scraping noise caused significant cross-folder duplicate collisions (e.g., 26 duplicate images shared between alternaria and ring spot, 19 between alternaria and downy mildew). All 72 colliding images excluded to ensure label purity.

5. **`celery anthracnose` &rarr; `celery__anthracnose` (Class ID 42)**  
   Clean folder of 98 images with zero collisions. Directly reinforces existing class 42.

6. **Eggplant Folders (`phomopsis blight`, `eggplant_phomopsis`, `phytophthora spot`)**  
   - `eggplant phomopsis blight` and `eggplant_phomopsis` represent the same organism (*Phomopsis vexans*), sharing 18 identical images. Both map to `eggplant__phomopsis_fruit_rot` (Class ID 62).  
   - `eggplant phytophthora spot` maps to `eggplant__phytophthora_blight` (Class ID 63). 11 images colliding across phomopsis and phytophthora excluded.

7. **Lettuce Folders (`downy mildew`, `mosaic virus`)**  
   - `lettuce downy mildew` maps to `lettuce__downy_mildew` (Class ID 75). (14 images colliding with broccoli downy mildew excluded).  
   - `lettuce mosaic virus` maps to `lettuce__mosaic_virus` (Class ID 76). (113 clean images).

8. **Tomato Folders (`early blight`, `late blight`, `yellow curl virus`)**  
   - In Model 2 taxonomy, pathological agents are classified canonically regardless of plant organ (*Alternaria solani* causes collar rot, foliage blight, and concentric sunken fruit rot; *Phytophthora infestans* attacks both green fruit and leaves).  
   - Fruit early blight maps to `tomato__early_blight` (Class ID 125).  
   - Fruit late blight maps to `tomato__late_blight` (Class ID 126).  
   - Yellow curl virus maps to `tomato__yellow_leaf_curl_virus` (Class ID 130).

---

### 3.2 Candidate New Classes & Ambiguities Requiring Review

#### A. `tomato/tomato fruit Anthracnose` (336 Images) &mdash; CANDIDATE NEW CLASS
- **Pathology:** *Colletotrichum coccodes* (Tomato Anthracnose) causes circular, sunken, water-soaked ring lesions on ripe tomato fruit.  
- **Taxonomy Status:** Absent from the 143-class V1 taxonomy.  
- **Impact:** Adding this class expands Model 2 to **144 classes**. Requires adding `tomato__anthracnose` to `class_mapping.json` (Class ID 143) and `crop_disease_mapping.json`.  
- **Recommendation:** High agronomic value. Accept as Class 143 upon human approval.

#### B. `tomato/tomato fruit fusarium wilt` (231 Images) &mdash; AGRONOMIC CONFLICT
- **Pathology:** *Fusarium oxysporum f. sp. lycopersici* is a vascular root/stem wilt causing unilateral foliar chlorosis, stunting, and vascular browning. It does **not** cause primary fruit spot lesions.  
- **Inspection Findings:** The scraped images show necrotic fruit spots colliding with Late Blight (4 images), Anthracnose (4 images), and Leaf Curl Virus (1 image).  
- **Recommendation:** **QUARANTINE / EXCLUDE**. Scraped query is scientifically mismatched with the symptoms depicted.

---

## 4. Protected Test Set Protection

The 2,304-image historical test set (`data/processed/model2_retraining_v1/test/`) is strictly protected:
- **Exact SHA-256 Matches:** **0** (no exact duplicates in the new data).
- **Perceptual Near-Duplicates (pHash Hamming Distance $\le$ 4):** **48 images** in the new collection closely resemble or represent resized/re-encoded versions of protected test images.
- **Action Taken:** All 48 near-duplicate images are **strictly excluded** from the new training and validation pools to preserve evaluation validity.

---

## 5. Summary of Accepted Clean Additions

If approved, the 2,273 accepted clean images will augment existing V1 classes as follows:

| Canonical Class | Class ID | Existing V1 Train | Existing V1 Val | New Accepted | Proposed Total Pool |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `healthy` | 0 | 1,440 | 180 | +148 | 1,768 |
| `banana__cigar_end_rot` | 8 | 100 | 15 | +196 | 311 |
| `broccoli__alternaria_leaf_spot` | 28 | 101 | 15 | +188 | 304 |
| `broccoli__downy_mildew` | 29 | 102 | 15 | +168 | 285 |
| `broccoli__ring_spot` | 30 | 100 | 15 | +150 | 265 |
| `celery__anthracnose` | 42 | 100 | 15 | +98 | 213 |
| `eggplant__phomopsis_fruit_rot` | 62 | 100 | 15 | +86 | 201 |
| `eggplant__phytophthora_blight` | 63 | 100 | 15 | +217 | 332 |
| `lettuce__downy_mildew` | 75 | 102 | 15 | +130 | 247 |
| `lettuce__mosaic_virus` | 76 | 101 | 15 | +113 | 229 |
| `tomato__early_blight` | 125 | 370 | 46 | +300 | 716 |
| `tomato__late_blight` | 126 | 374 | 47 | +289 | 710 |
| `tomato__yellow_leaf_curl_virus` | 130 | 400 | 50 | +190 | 640 |
| **Total** | — | — | — | **+2,273** | — |
