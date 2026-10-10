# EXPANDED MODEL 1 — TRAINING CONFIGURATION & PIPELINE CODE REVIEW

**Phase:** Error Analysis & Tuning Preparation  
**Target File Reviewed:** `scripts/train_model1_expanded.py`  
**Checkpoint Analyzed:** `models/model1_expanded/best_model.pth`  
**Configuration Audited:** 46-Class EfficientNet-B2 Pipeline  

---

## 1. Technical Audit Summary

| Component | Code Implementation | Audit Finding | Status |
| :--- | :--- | :--- | :---: |
| **ImageNet Normalization** | `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]` | Exact match with torchvision `EfficientNet_B2_Weights.DEFAULT` pretrained specification. Channels ordered correctly (RGB). | **VERIFIED (CORRECT)** |
| **Train vs Eval Transforms** | Train uses RandomHorizontalFlip, RandomRotation(15), ColorJitter; Eval uses deterministic Resize & Normalize | Correct separation. Evaluation transforms are strictly deterministic without stochastic corruption. | **VERIFIED (CORRECT)** |
| **Augmentation Identity Preservation** | Rotations $\le 15^\circ$, ColorJitter (0.15, 0.15, 0.15, 0.03) | Preserves botanical leaf geometry, serration, and chlorophyll chromaticity. Zero synthetic artifacts or cross-crop mixing. | **VERIFIED (CORRECT)** |
| **Loss Weights & Sampler Interaction** | `WeightedRandomSampler` ($p_i \propto N_c^{-0.20}$) + `CrossEntropyLoss` ($w_c \propto N_c^{-0.35}$) | **Dual-weighting interaction detected.** Both mechanisms apply inverse-frequency adjustments simultaneously, resulting in a compound ratio $\approx N_c^{-0.55}$. | **REQUIRES DECOUPLING** |
| **Checkpoint Restoration & Mapping** | Checkpoint saves `class_to_idx`, `sorted_classes`, `architecture`, `mean`, `std` | Complete metadata bundle saved. Restores flawlessly on CPU and CUDA. | **VERIFIED (CORRECT)** |
| **Epoch Sufficiency** | 10 epochs with Cosine Annealing | Val loss decreased from 0.5979 (Epoch 1) to 0.3791 (Epoch 10). The curve was still downward-sloping, indicating under-convergence on fine-grained distinctions. | **INSUFFICIENT (NEEDS 14-15 EPOCHS)** |
| **Early Stopping Schedule** | Patience = 3 epochs | Did not trigger (Epoch 10 was the best checkpoint). A longer schedule of 14–15 epochs with patience = 4 is justified. | **JUSTIFIED FOR EXTENSION** |
| **Metric Subset Calculation** | Sliced array `f1_score()` without `labels` parameter | **Slicing bug detected.** Misclassified predictions formed phantom classes with support 0, falsely depressing reported subset Macro F1. | **REQUIRES FIX IN SCRIPT** |

---

## 2. Deep Component Analysis

### 2.1 Normalization & Input Tensor Preprocessing
- **Code:**
  ```python
  transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
  ```
- **Validation:** Both training and evaluation pipelines load images via PIL `Image.open().convert("RGB")`. Tensor values are scaled to $[0.0, 1.0]$ by `ToTensor()` prior to normalization. Preprocessing perfectly matches torchvision's pretrained EfficientNet-B2 standard.

### 2.2 Transform Differentiation & Augmentation Integrity
- **Train Transform:**
  ```python
  transforms.Compose([
      transforms.Resize((224, 224)),
      transforms.RandomHorizontalFlip(p=0.5),
      transforms.RandomRotation(degrees=15),
      transforms.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.03),
      transforms.ToTensor(),
      transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])
  ```
- **Eval Transform:**
  ```python
  transforms.Compose([
      transforms.Resize((224, 224)),
      transforms.ToTensor(),
      transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
  ])
  ```
- **Assessment:**
  - The evaluation pipeline is 100% deterministic.
  - The training augmentations are conservative and biologically appropriate. The slight hue jitter ($\pm 0.03$) mimics natural sunlight variations without altering diseased vs healthy tissue distinction.
  - Crop identity is strictly preserved.

### 2.3 Sampler and Loss Weighting Compound Interaction
- **Code in First-Run Script:**
  ```python
  # 1. Loss weights
  raw_loss_weights[c_idx] = float(np.clip((median_cnt / max(cnt, 2)) ** 0.35, 0.3, 3.5))
  criterion = nn.CrossEntropyLoss(weight=class_weights_tensor)

  # 2. Sampler weights
  raw_sample_weights[c_idx] = float(np.clip((median_cnt / max(cnt, 2)) ** 0.20, 0.4, 2.5))
  sampler = WeightedRandomSampler(sample_weights, num_samples=len(train_dataset), replacement=True)
  ```
- **Critique:**
  - When a minority class is oversampled by the sampler *and* simultaneously upweighted in the loss function, its effective gradient contribution is scaled by:
    $$\Delta \theta \propto \frac{1}{N_c^{0.20}} \times \frac{1}{N_c^{0.35}} = \frac{1}{N_c^{0.55}}$$
  - For small classes, this creates excessive gradient magnitude that can destabilize AdamW second-moment tracking and cause the network to overfit to idiosyncratic backgrounds of minority samples.
- **Recommendation:** Decouple these mechanisms. Use standard shuffling in the DataLoader, and rely solely on a well-calibrated loss function (e.g. Cui et al. Class-Balanced Loss or smoothed clamped CrossEntropyLoss).

### 2.4 Training Duration & Convergence Analysis
- **Empirical Epoch Trajectory:**
  - Epoch 1: Train Loss `1.2622` | Val Loss `0.5979` | Val Macro F1 `75.04%`
  - Epoch 3: Train Loss `0.3827` | Val Loss `0.4531` | Val Macro F1 `82.94%`
  - Epoch 6: Train Loss `0.1402` | Val Loss `0.4104` | Val Macro F1 `84.59%`
  - Epoch 8: Train Loss `0.0695` | Val Loss `0.3906` | Val Macro F1 `86.12%`
  - Epoch 10: Train Loss `0.0485` | Val Loss `0.3791` | Val Macro F1 `86.63%`
- **Assessment:**
  - Notice that between Epoch 8 and Epoch 10, Validation Loss dropped from `0.3906` to `0.3791`, and Validation Macro F1 rose from `86.12%` to `86.63%`.
  - The model was still learning and had **not reached a plateau**.
  - 10 epochs was an arbitrary constraint adopted from the smaller 22-class model. A 46-class problem with complex visual confounders (*Brassica oleracea*, *Rosaceae*, monocots) requires 14–15 epochs for complete convergence.

### 2.5 Checkpoint Restoration and Serialization Integrity
- **Code:**
  ```python
  torch.save({
      "epoch": epoch,
      "model_state_dict": model.state_dict(),
      "val_macro_f1": val_macro_f1,
      "val_accuracy": val_accuracy,
      "class_to_idx": class_to_idx,
      "sorted_classes": sorted_classes,
      "architecture": "efficientnet_b2",
      "image_size": IMAGE_SIZE,
      "mean": IMAGENET_MEAN,
      "std": IMAGENET_STD,
  }, BEST_MODEL_PATH)
  ```
- **Validation:**
  - Serialized dictionary contains full architecture and normalization metadata.
  - Checkpoint was successfully restored and validated during our deep evaluation test. No missing keys or mismatched dimensions.

---

## 3. Recommended Code Adjustments for Future Tuning

When the project proceeds to the tuning execution phase, the training script should incorporate:
1. **Explicit Label Constraint in Subset Metrics:**
   ```python
   # Corrected subset metric calculation:
   orig_macro_f1 = f1_score(orig_targets, orig_preds, labels=orig_indices, average="macro", zero_division=0)
   new_macro_f1 = f1_score(new_targets, new_preds, labels=new_indices, average="macro", zero_division=0)
   ```
2. **Two-Stage Backbone Warmup:**
   ```python
   # Stage 1: Freeze backbone
   for param in model.features.parameters():
       param.requires_grad = False
   ```
3. **Decoupled Sampling:** Replace `WeightedRandomSampler` with standard shuffle `DataLoader(shuffle=True)` and single smoothed loss weighting.
4. **Schedule Extension:** Set `EPOCHS = 14` with `PATIENCE = 4`.
