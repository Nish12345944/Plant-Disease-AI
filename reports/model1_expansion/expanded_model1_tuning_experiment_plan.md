# EXPANDED MODEL 1 — CONTROLLED TUNING EXPERIMENT PLAN

**Phase:** Error Analysis & Tuning Preparation  
**Target Architecture:** EfficientNet-B2 (PyTorch, CUDA, AMP FP16)  
**Hardware Profile:** RTX 3050 Laptop GPU (4 GB VRAM safe batch size: 16)  
**Status:** PROPOSED EXPERIMENT MATRIX (No training executed in this phase)  

---

## 1. Experimentation Philosophy & Controls

To guarantee scientific rigor and avoid confounding variables:
1. **Single Variable Isolation:** Exactly one major design factor is modified per experiment run.
2. **Immutable Test Set:** The 1,580-image test set remains strictly quarantined and will never be evaluated until the best checkpoint of a candidate run is selected.
3. **Primary Selection Metric:** **Validation Macro F1** (evaluated across all active classes using label-constrained scikit-learn).
4. **Secondary Metrics:** Validation Accuracy, Test Top-1, Test Top-3, Weighted F1, and per-class F1 on weak classes (`cherry`, `cauliflower`, `basil`, `ginger`, `raspberry`).
5. **Deterministic Seed:** All runs initialized with `seed = 42`.

---

## 2. Proposed Experiment Matrix

| Run ID | Experiment Name | Core Hypothesis / Factor Changed | Configuration Details | Expected Benefit | Potential Risk | Acceptance Criterion |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXP-0** | **Baseline Reproduction & Metric Correction** | Establish verified, corrected baseline without dual-weighting skew | Single-stage AdamW (`lr=3e-4`), 10 epochs, Cosine Annealing, corrected label-constrained metric calculation | Eliminates evaluation slicing artifact; reproduces 90.38% Top-1 cleanly | None | Top-1 $\ge 90.0\%$, Val Macro F1 $\ge 86.0\%$ |
| **EXP-1** | **Two-Stage Transfer Learning** | Pretrained ImageNet features are distorted by full-backbone gradient updates from the random linear head | **Stage 1 (Warmup):** Freeze backbone, train 46-class linear head for 4 epochs (`lr=1e-3`).<br>**Stage 2 (Fine-tune):** Unfreeze full backbone, train 10 epochs with lower learning rate (`lr=7e-5`, Cosine Annealing to `1e-6`). | Prevents catastrophic forgetting of low-level edge/texture features; stabilizes minority crop logits | Slower training (14 total epochs vs 10) | Validation Macro F1 $\ge 88.0\%$ (+1.4% over baseline) |
| **EXP-2** | **Decoupled Imbalance Strategy (Eliminate Double Penalty)** | Simultaneously using `WeightedRandomSampler` AND weighted loss squares penalty ratios, destabilizing AdamW | Keep standard shuffle DataLoader; use **Class-Balanced Loss** ($w_c \propto \frac{1 - \beta}{1 - \beta^{N_c}}$ with $\beta=0.999$, clamped $[0.5, 3.0]$) OR smoothed loss weights alone without sampler | Prevents oversampling artifacts on small classes; produces smoother loss surface | Minority classes with <50 samples may need slightly higher epochs | Per-class F1 on `cauliflower` $>60\%$, `ginger` $>70\%$ |
| **EXP-3** | **Extended Schedule with Learning Rate Warmup** | 10 epochs was under-converged (val loss 0.3791 still dropping at epoch 10) | 15 total epochs; 1 epoch linear warmup to `2e-4`, followed by cosine decay to `5e-7`. Early stopping patience = 4 | Allows fine-grained decision boundaries (e.g. *Brassica oleracea* separation) to fully converge | Overfitting on majority classes (mitigated by AdamW weight decay `1e-4`) | Val loss $<0.340$, Val Macro F1 $\ge 88.5\%$ |
| **EXP-4** | **Targeted Foliage Augmentations (Identity-Preserving)** | Single-leaf images suffer from background/lesion bias | Add `RandomAffine(degrees=15, translate=(0.08, 0.08), scale=(0.92, 1.08))` and gentle `RandomErasing(p=0.2, scale=(0.02, 0.15))` | Forces network to learn leaf shape/venation rather than localized spot patches | Excessive distortion could confuse serrated margins | Top-3 Accuracy $\ge 98.0\%$, `cherry` F1 $>50\%$ |

---

## 3. Detailed Experiment Configurations

### 3.1 EXP-1: Two-Stage Transfer Learning Protocol
- **Stage 1 (Head Warmup):**
  - Freeze all EfficientNet-B2 convolutional feature extractors:
    ```python
    for param in model.features.parameters():
        param.requires_grad = False
    ```
  - Train only `model.classifier`:
    - Optimizer: `AdamW(model.classifier.parameters(), lr=1e-3, weight_decay=1e-4)`
    - Duration: 4 epochs
    - Objective: Adapt the 46 randomly initialized linear head weights without propagating noisy gradients into pretrained convolutional weights.
- **Stage 2 (Full Backbone Fine-Tuning):**
  - Unfreeze all parameters:
    ```python
    for param in model.parameters():
        param.requires_grad = True
    ```
  - Optimizer: `AdamW(model.parameters(), lr=7e-5, weight_decay=1e-4)`
  - Scheduler: `CosineAnnealingLR(T_max=10, eta_min=1e-6)`
  - Duration: 10 epochs

### 3.2 EXP-2: Imbalance Strategy Simplification
- **Observation:** In Run 1, both `WeightedRandomSampler` ($p_i \propto N_c^{-0.20}$) and `CrossEntropyLoss` ($w_c \propto N_c^{-0.35}$) were applied at the same time. The cumulative weight ratio reached $\approx N_c^{-0.55}$, which effectively doubled the gradient amplification for minority classes and induced volatility.
- **Proposed Solution:**
  - Standard shuffling DataLoader (`shuffle=True`, no random sampler).
  - Class-Balanced Softmax Loss using Cui et al. effective number of samples formulation:
    $$E_{n_c} = \frac{1 - \beta^{n_c}}{1 - \beta}, \quad w_c = \frac{1}{E_{n_c}}$$
    With $\beta = 0.999$, normalized to mean 1.0 across active classes and clamped between $[0.4, 2.8]$.
  - Zero loss weight ($0.0$) explicitly assigned to empty/gap classes (`cherry_tomato`, `gypsophila`).

### 3.3 EXP-4: Conservative Augmentation Specification
To avoid distorting botanically critical diagnostic traits (e.g. leaf margins, venation patterns):
- **Permitted:**
  - `RandomHorizontalFlip(p=0.5)`
  - `RandomRotation(degrees=15)`
  - `RandomAffine(degrees=10, translate=(0.05, 0.05), scale=(0.95, 1.05))`
  - `ColorJitter(brightness=0.10, contrast=0.10, saturation=0.10, hue=0.02)`
  - `RandomErasing(p=0.15, scale=(0.02, 0.12), value="random")`
- **Prohibited:**
  - Aggressive Shearing ($>15^\circ$) — alters leaf shape geometry.
  - Large Hue Shifts ($>0.05$) — alters natural leaf chlorosis and anthocyanin signatures.
  - MixUp / CutMix — creates synthetic hybrid plants, strictly violating production requirements.

---

## 4. Evaluation & Gating Criteria

For any tuned checkpoint to be considered a **Promotion Candidate**:
1. **Overall Top-1 Accuracy:** $\ge 92.0\%$ (vs 90.38% baseline).
2. **Overall Top-3 Accuracy:** $\ge 98.0\%$ (vs 97.34% baseline).
3. **Overall Macro F1:** $\ge 87.0\%$ (vs 83.81% baseline).
4. **Original 22-Class Top-1:** $\ge 95.0\%$ (maintaining production parity).
5. **New 24-Class Top-1:** $\ge 88.0\%$ (vs 84.02% baseline).
6. **No Critical Crop Regressions:** Zero regressions on core food crops (`tomato`, `potato`, `wheat`, `rice`, `corn`, `soybean`).
7. **Audit & Safety:** Must pass 100% of SHA-256 integrity and leakage checks.
