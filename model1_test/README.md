# Model 1 - Plant/Crop Classifier Testing Interface

A simple, local Streamlit image-upload testing interface for the trained **Model 1 (EfficientNet-B2)** 22-class plant and crop classifier.

---

## Features
- **Local & Offline:** Uses local PyTorch checkpoint [`models/model1/best_model.pth`](../models/model1/best_model.pth) with zero external APIs.
- **Hardware Acceleration:** Auto-detects NVIDIA CUDA GPU if present; falls back to CPU cleanly.
- **Top-1 & Top-3 Predictions:** Outputs primary predicted plant/crop, confidence percentage, and ranked top 3 classes.
- **Supported Formats:** JPG, JPEG, PNG, WEBP, BMP.
- **Cached Weights:** Instant inference after initial model load via Streamlit resource caching.

---

## How to Run

1. Open PowerShell or Terminal in the project root:
   ```powershell
   cd C:\Users\vyasn\OneDrive\Desktop\Disease_prediction
   ```

2. Activate the virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Launch the Streamlit application:
   ```powershell
   python -m streamlit run model1_test/app.py
   ```
   *(or `.\venv\Scripts\streamlit run model1_test/app.py`)*

4. Open your web browser at:
   ```
   http://localhost:8501
   ```

---

## Model & Architecture Specs
- **Model Checkpoint:** `models/model1/best_model.pth`
- **Class Mapping:** `models/model1/class_mapping.json` (22 target taxonomy classes)
- **Input Dimensions:** 224 x 224 RGB
- **Normalization:** ImageNet mean `[0.485, 0.456, 0.406]` and std `[0.229, 0.224, 0.225]`
- **Framework:** PyTorch (`torch`, `torchvision`)
