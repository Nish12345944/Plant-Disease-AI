# Model 2 Retraining V2 (144 Classes) — Preflight Report

- **Dataset:** `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_retraining_v2`
- **Manifest:** `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\processed\model2_retraining_v2_manifest.csv`
- **Total Images:** 35,441 (Train: 30,088, Val: 3,049, Test: 2,304)
- **Total Classes:** 144
- **Execution Device:** cuda (NVIDIA GeForce RTX 3050 Laptop GPU)
- **Initialization Checkpoint:** `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\models\model2_retraining_v1\best_model.pth`
- **Batch Size / Accumulation:** Batch Size 4, Grad Accum 8 (Effective Batch Size = 32)
- **Stage 1 (Head Warmup):** 4 epochs @ LR=0.001 (Backbone frozen)
- **Stage 2 (Fine-Tuning):** 16 epochs @ LR=0.0001 -> 1e-06 (Cosine Annealing)
- **Early Stopping Patience:** 6 epochs on Validation Macro F1
- **Status:** **ALL PREFLIGHT CHECKS PASSED — READY FOR EXECUTION**
