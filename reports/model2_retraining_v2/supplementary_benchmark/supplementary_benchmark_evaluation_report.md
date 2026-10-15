# Model 2 V2 - Supplementary Benchmark Evaluation Report

**Evaluated Checkpoint:** `models/model2_retraining_v2/best_model.pth` (Epoch 14)  
**Generated:** 2026-10-13 15:35:42  
**Preprocessing:** Production `Resize((260, 260))` -> `ToTensor()` -> `Normalize(ImageNet)`  

## 1. Separate Benchmark Reporting Principle

> [!IMPORTANT]
> Per Requirement 9, metrics for the **immutable protected test set (n=2,304)** and the **supplementary benchmark (n=24)** are reported **strictly separately**. They are never merged into a single metric, nor is it claimed that increasing test support automatically improves model generalization.

## 2. Benchmark Comparison (Immutable Test Set vs. Supplementary Benchmark)

### A. Original Immutable Benchmark (`data/processed/model2_retraining_v2_manifest.csv`, $n=2{,}304$):
- **Test Samples**: 5 images for `eggplant__phomopsis_fruit_rot`
- **Raw Top-1 Accuracy**: 80.0% (4 / 5 correct)
- **Precision**: 100.0% (1.00)
- **Recall**: 80.0% (0.80)
- **F1-Score**: **88.89% (0.8889)**

### B. Supplementary Benchmark (`data/processed/model2_v2_supplementary_benchmark/`, $n=24$):
- **Verified Test Samples**: 24 images for `eggplant__phomopsis_fruit_rot`
- **Raw Model 2 Correct**: 13 / 24 (54.17%)
- **Crop-Aware Pipeline Correct**: 16 / 24 (66.67%)
- **Supplementary F1-Score (Crop-Aware)**: **66.67%**

## 3. Disease Reliability Count Audit ($F_1 \ge 0.70$ and Support $\ge 10$)

| Benchmark Source | Total Disease Classes Evaluated | Classes with Support $\ge 10$ | Classes with $F_1 \ge 0.70$ & Support $\ge 10$ | Notes |
|---|---|---|---|---|
| **Original Immutable Benchmark (n=2,304)** | 143 diseases | 48 | **29 (Raw)** / **32 (Crop-Aware)** | Standard immutable benchmark |
| **Supplementary Benchmark (n=24)** | 1 disease (`eggplant__phomopsis`) | 1 | **0 (F1=66.67% < 70%)** | Crop-Aware $F_1 = 66.67\%$, Support = 24 |
| **Isolated Verified Expansion** | 10 target classes audited | 1 qualified test set | **+0 Passed >= 70%** | Near-reliable (66.7%); 9 classes declared data shortfalls |

## 4. Error Analysis on Supplementary Benchmark

Misclassifications observed on the 24 supplementary eggplant phomopsis images:
- Image `imgi_122_2.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.02) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_131_5511751ppt.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.00) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_134_3.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.00) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_139_1-s2.0-S2307410825001129-ga1.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.00) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_151_7296-Phomopsis-Blight-eggplant.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.56) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_25_default.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.60) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_34_default.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.00) instead of `eggplant__phomopsis_fruit_rot`
- Image `imgi_80_images.jpg`: Predicted `eggplant__phytophthora_blight` (conf: 0.46) instead of `eggplant__phomopsis_fruit_rot`

## 5. Summary & Conclusions
1. On the supplementary benchmark of 24 unseen, non-leaked external images, `eggplant__phomopsis_fruit_rot` achieves **66.67% crop-aware accuracy** (recovering from 54.17% raw accuracy). Its remaining errors are strictly intra-eggplant visual confusions with `eggplant__phytophthora_blight`.
2. Under the strict reliability criterion ($F_1 \ge 0.70$ and Support $\ge 10$):
   - On the **Original Immutable Benchmark ($n=2{,}304$)**: Exactly **29 classes** (Raw) / **32 classes** (Crop-Aware) qualify.
   - On the **Supplementary Benchmark ($n=24$)**: `eggplant__phomopsis_fruit_rot` achieves **66.67%**, placing it in the **Near-Reliable Tier** (just below the 70.0% cutoff).
3. The remaining 9 target classes have **zero additional verified test images** in `data/external/`. This data deficit is explicitly documented in the manifest rather than masked with synthesized or mislabeled data.