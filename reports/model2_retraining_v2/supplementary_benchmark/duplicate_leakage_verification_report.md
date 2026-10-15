# Model 2 V2 Supplementary Benchmark - Duplicate & Leakage Verification Report

## 1. Multi-Stage Leakage Defense Protocol

To protect the scientific validity of the supplementary evaluation, every image was subjected to a four-stage screening pipeline:

1. **SHA-256 Exact Train Collision Check**: Checked against all 30,088 training hashes.
2. **SHA-256 Exact Validation Collision Check**: Checked against all 3,049 validation hashes.
3. **SHA-256 Exact Test Collision Check**: Checked against all 2,304 immutable test hashes.
4. **Perceptual Hash (pHash) Distance Screening**: Computed 64-bit DCT perceptual hash against all 2,304 test images. Any candidate with distance $\le 4$ was rejected.

## 2. Leakage Verification Results

| Leakage Check | Candidates Audited | Detected Collisions | Action Taken | Post-Audit Status |
|---|---|---|---|---|
| Training Set Leakage | 123 | 52 | Quarantined / Excluded | **ZERO LEAKAGE (0)** |
| Validation Set Leakage | 123 | 9 | Quarantined / Excluded | **ZERO LEAKAGE (0)** |
| Immutable Test Leakage (SHA-256) | 123 | 0 | None Detected | **ZERO LEAKAGE (0)** |
| Test Set Perceptual Near-Duplicates | 123 | 2 (`imgi_106`, `imgi_70`) | Quarantined / Excluded | **ZERO LEAKAGE (0)** |
| Cross-Disease Label Collisions | 123 | 11 (Phytophthora) | Quarantined / Excluded | **ZERO CONFLICTS (0)** |

## 3. Eligible Image Integrity Certificate

All 24 images admitted to `data/processed/model2_v2_supplementary_benchmark/images/eggplant/phomopsis_fruit_rot/`:
- Have unique SHA-256 hashes not present anywhere in the training, validation, or test splits.
- Have test pHash distances between 14 and 20 (well above the near-duplicate threshold of 4).
- Are authentic, uncompressed photographic images of phomopsis fruit rot symptoms on eggplant.