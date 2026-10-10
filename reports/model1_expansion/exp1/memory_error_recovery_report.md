# EXP-1 MemoryError Recovery and Diagnosis Report

**Date:** October 10, 2026  
**Project:** `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`  
**Target:** EXP-1 — Two-Stage Transfer Learning (EfficientNet-B2, 46 classes)  
**Status:** Diagnosis Complete, Fix Implemented & Verified, Ready for Safe Restart

---

## 1. Executive Summary

During the initial run of EXP-1 training (`python scripts/train_model1_expanded_exp1.py --run`), the training process aborted during Stage 1 Epoch 1 with a Python host `MemoryError`. A subsequent unconstrained linear scan attempted in the previous session led to unresponsive session behavior. 

Following a system restart, a complete forensic diagnosis was conducted:
1. **No background Python processes are active.**
2. **All protected assets and EXP-0 baseline checkpoints remain completely intact and untouched.**
3. **The exact root cause was identified:** Several web-scraped dataset images possess extreme resolutions (up to 48.77 Megapixels, 8064×6048). Unbounded Pillow decoding (`raw.convert("RGB")`) allocated ~146 MB to ~300 MB of uncompressed bitmap buffers per large image into host RAM during batch iteration. Under Windows memory fragmentation and constrained available RAM (~1.6 GB free), a contiguous `malloc()` failed inside `PIL.Image.copy()`.
4. **Zero images are corrupt:** An incremental header and integrity scan of all 18,176 images across `train`, `val`, and `test` confirmed 0 corrupted files.
5. **Fix implemented:** Bounded-memory image decoding was implemented in `ExpandedPlantDataset.__getitem__` using Pillow's C libjpeg downsampling draft (`raw.draft("RGB", (448, 448))`), reducing per-image memory allocations by **98.5%** (from 146 MB to 2.2 MB) and yielding a **5.4× decoding speedup**.
6. **Verification passed:** A 100-batch (1,600 images) augmented DataLoader test executed cleanly at 78.9 images/second with stable memory and zero errors. Split counts match the authoritative manifest exactly (14,998 train, 1,592 val, 1,586 test).

---

## 2. Phase A — Recovery and Forensic Diagnosis

### 2.1 Process Status & System Resources
- **Active Python Processes:** None found.
- **Host RAM:** 15.34 GB visible (16,087,140 KB), ~1.63 GB free at startup.
- **GPU / VRAM:** NVIDIA GeForce RTX 3050 Laptop GPU (4,096 MiB VRAM), Driver 592.82, CUDA 13.1, 0 MiB allocated.
- **Root Cause Context:** The error was an operating system host RAM allocation failure (`MemoryError` in Python C runtime `malloc`), **not** a CUDA out-of-memory error.

### 2.2 Existing Checkpoints and Log State
- `models/model1_expanded/exp1/`: Empty (the crash occurred in Epoch 1 before any checkpoint was saved).
- `reports/model1_expansion/exp1/exp1_training.log`: Log terminated at Stage 1 Head Warmup initialization.
- `models/model1_expanded/best_model.pth` (EXP-0 baseline): Intact (MD5/weights untouched).
- `models/model1/best_model.pth` (Production Model 1): Intact and untouched.
- `models/model2_classifier_v4/` (Production Model 2): Intact and untouched.

### 2.3 Exact Failure Traceback
The failure occurred in `torch.utils.data.DataLoader` when fetching a batch during Stage 1 Epoch 1:

```text
Traceback (most recent call last):
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\scripts\train_model1_expanded_exp1.py", line 739, in <module>
    sys.exit(0 if run_exp1(evaluate_test=args.evaluate_test) else 1)
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\scripts\train_model1_expanded_exp1.py", line 472, in run_exp1
    run_stage("S1", STAGE1_EPOCHS, optimizer, scheduler, freeze_bn=True, patience=None, start_global=0)
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\scripts\train_model1_expanded_exp1.py", line 409, in run_stage
    train_loss, train_acc, train_macro, train_weighted = train_one_epoch(
        model, train_loader, criterion, optimizer_, scaler, device, stage_tag, freeze_bn)
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\scripts\train_model1_expanded_exp1.py", line 228, in train_one_epoch
    for images, targets, _ in train_loader:
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\venv\Lib\site-packages\torch\utils\data\dataloader.py", line 741, in __next__
    data = self._next_data()
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\venv\Lib\site-packages\torch\utils\data\dataloader.py", line 801, in _next_data
    data = self._dataset_fetcher.fetch(index)
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\venv\Lib\site-packages\torch\utils\data\_utils\fetch.py", line 54, in fetch
    data = [self.dataset[idx] for idx in possibly_batched_index]
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\scripts\train_model1_expanded_exp1.py", line 162, in __getitem__
    img = raw.convert("RGB")
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\venv\Lib\site-packages\PIL\Image.py", line 1081, in convert
    return self.copy()
  File "C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\venv\Lib\site-packages\PIL\Image.py", line 1365, in copy
    return self._new(self.im.copy())
MemoryError
```

### 2.4 Resume Feasibility
Because the failure occurred midway through Epoch 1, no intermediate weights or optimizer states were generated. Furthermore, per the EXP-1 experimental design, Stage 1 initializes from standard ImageNet-1K pretrained weights (`EfficientNet_B2_Weights.DEFAULT`) with a fresh 46-class linear head, deliberately avoiding resuming the single-stage Run-1 checkpoint to maintain controlled-variable isolation. Therefore, starting training freshly from Epoch 1 is the intended, safe, and correct protocol.

---

## 3. Phase B — Root Cause Resolution

### 3.1 Dataset Audit & Resolution Discovery
An incremental metadata and resolution audit across all 18,176 dataset files revealed:
- **Total files:** 18,176 (`.jpg`: 17,988, `.jpeg`: 142, `.png`: 46)
- **Corrupt images:** 0 (all file headers and data structures are valid)
- **Extreme resolutions:** 630 images exceed 10 Megapixels.
  - Largest image: `train/spinach/spinach_e73f7d48aa_spinach_leaves_diseased_005687.jpg` (8,064 × 6,048 = 48.77 MP)
  - Second largest: `train/wheat/wheat_bf38cac7f4_ps_wheat_powdery_mildew_Baidu_0279.jpg` (8,256 × 5,504 = 45.44 MP)

When Pillow reads an 8064×6048 image naively, it allocates 146 MB for the raw bitmap, duplicates it during `.convert("RGB")` (+146 MB), and retains it until downscaled to 224×224. In a batch of 16 images, several multi-megapixel images occurring in the same batch cause sudden memory spikes exceeding available heap memory.

### 3.2 Bounded-Memory Decoding Implementation
The `ExpandedPlantDataset.__getitem__` method in [train_model1_expanded_exp1.py](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/train_model1_expanded_exp1.py#L158-L168) was updated to use C-level downsampled decoding via libjpeg:

```python
    def __getitem__(self, idx: int):
        path, target = self.samples[idx]
        with Image.open(path) as raw:
            try:
                # Bounded memory decoding: downscale multi-megapixel JPEGs directly during C libjpeg decode
                raw.draft("RGB", (448, 448))
            except Exception:
                pass
            img = raw.convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target, path
```

### 3.3 Micro-Benchmark Verification
| Metric | Naive Decoding (Previous) | Bounded Draft Decoding (Current) | Improvement |
| :--- | :--- | :--- | :--- |
| **Spinach (48.7 MP) Memory** | ~146.3 MB | ~2.2 MB | **98.5% reduction** |
| **Spinach Decode Time** | 0.359 s | 0.066 s | **5.4× faster** |
| **Wheat (45.4 MP) Memory** | ~136.3 MB | ~2.1 MB | **98.5% reduction** |
| **Wheat Decode Time** | 0.416 s | 0.112 s | **3.7× faster** |
| **Output Tensor Shape** | `torch.Size([3, 224, 224])` | `torch.Size([3, 224, 224])` | Exact match |

---

## 4. Phase C — Safe Restart & Verification

### 4.1 DataLoader & Split Verification
A full DataLoader verification test was executed on the Windows host with `num_workers=0`:
- **Train split:** 14,998 images (Manifest: 14,998) — **PASS**
- **Val split:** 1,592 images (Manifest: 1,592) — **PASS**
- **Test split:** 1,586 images (Manifest: 1,586) — **PASS**
- **Batch Processing Rate:** 100 batches (1,600 images) processed in 20.27s (**78.9 images/sec**).
- **RAM Stability:** Available RAM remained completely stable with zero leakage.

### 4.2 Modernized API Call Cleanup
- Updated `torch.cuda.amp.autocast(...)` to modern `torch.amp.autocast("cuda", enabled=...)` in training, validation, and test evaluation loops to prevent deprecation warnings.

### 4.3 Protected Assets Confirmation
- `models/model1/best_model.pth`: Intact (`True`)
- `data/processed/model1_balanced/`: Intact (`True`)
- `models/model1_expanded/best_model.pth` (EXP-0): Intact (`True`)
- `models/model2_classifier_v4/`: Intact (`True`)
- `backups/model1_expansion_phase1_snapshot/`: Intact (`True`)

### 4.4 Proposed Training Command
The fix is completely self-contained within [scripts/train_model1_expanded_exp1.py](file:///C:/Users/vyasn/OneDrive/Desktop/Disease_prediction/scripts/train_model1_expanded_exp1.py). When ready, training can be started safely via:

```powershell
venv\Scripts\python.exe scripts/train_model1_expanded_exp1.py --run
```

To evaluate the immutable test set after training completes:
```powershell
venv\Scripts\python.exe scripts/train_model1_expanded_exp1.py --run --evaluate-test
```
