# Production Baseline Manifest — Version 4.0 Freeze

**Baseline Release Date:** 2026-10-08  
**Status:** PRODUCTION FROZEN BASELINE (V4)  

## 1. Model Artifacts & Configurations

- **Model 1 Checkpoint:** `models/model1/best_model.pth`  
- **Model 1 Class Mapping:** `models/model1/class_mapping.json` (22 classes)  
- **Model 1 Config:** `models/model1/config.json` (Architecture: EfficientNet-B2, Input: 260x260)  

- **Model 2 V4 Checkpoint:** `models/model2_classifier_v4/best_model.pth`  
- **Model 2 V4 Class Mapping:** `models/model2_classifier_v4/class_mapping.json` (117 classes: 0=healthy, 1..116 diseases)  
- **Model 2 V4 Config:** `models/model2_classifier_v4/config.json` (Architecture: EfficientNet-B2, Input: 260x260)  

## 2. Active Application Stack

- **Active Backend:** FastAPI (`app/backend/main.py` + `app/backend/services.py`)  
- **Active Frontend:** Vanilla HTML5/CSS3/JS Web UI (`app/frontend/index.html` + `app/frontend/app.js`)  
- **Video Inference Implementation:** Multi-frame uniform sampling + temporal aggregation (`app/backend/services.py:process_video_inference`)  
- **Knowledge Engine:** Deterministic rule & catalog-based retrieval (`knowledge/database.py` + `knowledge/assistant.py`)  
- **Query Router:** Deterministic fuzzy & phonetic intent classifier (`router/intent_classifier.py`)  
- **Audio / STT Engine:** Faster-Whisper Small (`Systran/faster-whisper-small` via `audio/transcriber.py`)  

## 3. Production Thresholds & Invariants

- **Model 2 Uncertainty Confidence Threshold:** `0.40`
- **Model 2 Uncertainty Margin Threshold:** `0.05`
- **Video Frame Extraction Range:** `16 to 24 frames`
- **Video Disease Aggregation Rule:** Temporal consensus across valid frames with confidence weighting
- **Crop-Disease Compatibility Gate:** Strict masking via `data/processed/model2_organized_crop_disease_mapping.json`
- **LLM Dependency:** CONFIRMED ABSENT (100% deterministic & offline verifiable)

## 4. Dataset Baselines

- **V4 Immutable Test Split:** 2,304 images (`data/processed/model2_v4/model2_v4_manifest.csv`)
- **Locked External Benchmark:** 178 eligible images (`data/external/end_to_end_test/manifest.csv`)

## 5. Test Suite Verification Summary

- **Total Regression Verification Tests:** 24
- **Passed:** 24 (100.0%)
- **Failed:** 0
- **Regression Status:** ALL TESTS PASSED
