# Project Cleanup & Storage Audit Report

**Date:** 2026-10-06  
**Target Root:** `C:\Users\vyasn\OneDrive\Desktop\Disease_prediction`  
**Parent Inspected:** `C:\Users\vyasn\OneDrive\Desktop`  
**Audit Type:** Complete Read-Only Dependency & Disk Storage Audit

---

## 1. Executive Summary

A comprehensive, read-only dependency and storage audit was executed across the entire `Disease_prediction` workspace and its parent directory (`Desktop`). Every file, dataset directory, model checkpoint, manifest, script, and cache directory was evaluated against the active runtime application (**Alexa Farms** / FastAPI + React), standalone inference modules (**Model 1** EfficientNet-B2, **Model 2** YOLOX-S), and historical training reproducibility pipelines.

### Overall Disk Usage Breakdown
| Category | Disk Space | Files Count | Active Role / Status | Safety Classification |
| :--- | :--- | :--- | :--- | :--- |
| **`data/processed/model1_balanced/`** | 2.81 GB | 16,537 files | **Active Model 1 Production Dataset** (22 classes balanced) | **RED (PROTECTED)** |
| **`data/processed/model2_dataset/`** | 976.91 MB | 15,266 files | **Active Model 2 Disease Dataset** (YOLOX annotations + splits) | **RED (PROTECTED)** |
| **`data/processed/model2_yolox/`** | 9.06 MB | 5 files | **Active Model 2 COCO format annotations** | **RED (PROTECTED)** |
| **`models/model1/`** | 119.05 MB | 6 files | **Active Model 1 Checkpoints & Configs** (`best_model.pth`, etc.) | **RED (PROTECTED)** |
| **`models/model2/`** | 69.03 MB | 5 files | **Active Model 2 Checkpoints & Configs** (`best_model.pth`, etc.) | **RED (PROTECTED)** |
| **`models/pretrained/`** | 68.75 MB | 1 file | **Pretrained YOLOX-S Backbone** (`yolox_s.pth`) | **RED (PROTECTED)** |
| **`app/`** | 86.99 MB | 6,627 files | **Alexa Farms Application** (FastAPI backend + React frontend) | **RED (PROTECTED)** |
| **`audio/`, `video/`, `router/`, `pipeline/`** | ~114 KB | 24 files | **Core Multimodal & Processing Modules** | **RED (PROTECTED)** |
| **`venv/`** | 5.53 GB | 43,976 files | **Active Python Virtual Environment** | **RED (PROTECTED)** |
| **`data/processed/model1_dataset/`** | 12.77 GB | 52,263 files | Interim raw 22-crop dataset (source for balanced dataset) | **YELLOW (NEEDS REVIEW)** |
| **`data/processed/plant_part_dataset/`** | 16.85 GB | 110,574 files | Interim pre-filtered dataset from earlier ETL script | **YELLOW (NEEDS REVIEW)** |
| **`data/processed/plant_part_dataset_split/`** | 8.01 GB | 92,085 files | Interim train/val split of plant parts | **YELLOW (NEEDS REVIEW)** |
| **`data/external/`** | 18.68 GB | 154,894 files | Raw scraped image repository across 30 crops | **YELLOW (NEEDS REVIEW)** |
| **`data/downloads/`** | 1002.91 MB | 9,496 files | Raw downloaded archives (beans, flowers-102) | **YELLOW (NEEDS REVIEW)** |
| **`models/model1_efficientnet_b2.pth`** | 29.93 MB | 1 file | Obsolete early experiment Model 1 checkpoint | **GREEN (SAFE TO DELETE)** |
| **`reports/video_debug/`** | 20.19 MB | 136 files | Temporary frame crops and ROI debug dumps | **GREEN (SAFE TO DELETE)** |
| **`scratch/all_video_frames/`** | 5.15 MB | 24 files | Temporary frame dumps from sample video analysis | **GREEN (SAFE TO DELETE)** |
| **`scratch/roi_visualizations/`** | 1.41 MB | 6 files | Temporary ROI debug visualizations | **GREEN (SAFE TO DELETE)** |
| **`scratch/video_test_frames/`** | 1.30 MB | 6 files | Temporary video test frames | **GREEN (SAFE TO DELETE)** |
| **Empty folders in `data/external/`** | 0 B | 0 files | 5 empty folders (`cherry_tomato`, `dutch_rose`, `gypsophila`, `lilium`, `Original Image`) | **GREEN (SAFE TO DELETE)** |
| **`requirements.txt` (root)** | 0 B | 1 file | Empty 0-byte file | **GREEN (SAFE TO DELETE)** |

---

## 2. Parent Directory Audit (`C:\Users\vyasn\OneDrive\Desktop`)

A full recursive check of the desktop folder was performed.
- **Finding**: There are **zero** duplicate project copies, orphaned datasets, or stray Roboflow downloads from `Disease_prediction` on the Desktop.
- All other desktop items belong to independent personal, coursework, and separate project workspaces (`data science`, `DSA`, `FAST-API`, `GenAI`, `MLP`, `querymind-ai`, `samprakshi`, `tabdu`, `mongosh`).
- **Safety Directive**: **ZERO modifications or deletions will be performed on the parent Desktop directory.**

---

## 3. Detailed Safety Classification

### GREEN — 100% Safe to Delete
These items have been proven obsolete, temporary, or redundant with zero references in runtime, evaluation, or production configuration:
1. `models/model1_efficientnet_b2.pth` (29.93 MB): Obsolete early checkpoint with MD5 hash `ef6d20...` (active is `models/model1/best_model.pth` with MD5 `2c986d...`).
2. `reports/video_debug/` (20.19 MB, 136 files): Frame crops dumped during previous video diagnostic sessions.
3. `scratch/all_video_frames/` (5.15 MB, 24 files): Temporary frame extraction dump.
4. `scratch/roi_visualizations/` (1.41 MB, 6 files): Temporary ROI crops.
5. `scratch/video_test_frames/` (1.30 MB, 6 files): Temporary test frames.
6. Empty folders in `data/external/`:
   - `data/external/cherry_tomato` (0 B)
   - `data/external/dutch_rose` (0 B)
   - `data/external/gypsophila` (0 B)
   - `data/external/lilium` (0 B)
   - `data/external/Original Image` (0 B)
7. `requirements.txt` (0 B empty file in root).

### YELLOW — Possibly Safe / Ambiguous (Requires Manual Confirmation)
These datasets consume significant disk space (~58.3 GB). They are not used by the live runtime application, but represent historical ETL stages or raw data pools:
1. `data/processed/plant_part_dataset/` (16.85 GB) & `data/processed/plant_part_dataset_split/` (8.01 GB): Created during plant-parts preprocessing.
2. `data/processed/model1_dataset/` (12.77 GB): Raw 22-class unbalanced dataset.
3. `data/external/` (18.68 GB): Original raw web-scraped images across 30 crops.
4. `data/downloads/` (1002.91 MB): Raw downloaded image archives.
5. `legacy_flask_app.py` (4.07 KB): Legacy Flask demo.

*Per safety requirements, YELLOW items will NOT be deleted automatically.*

### RED — DO NOT DELETE (Protected Active Assets)
1. **Model 1 Production Checkpoint & Config**:
   - `models/model1/best_model.pth`
   - `models/model1/config.json`
   - `models/model1/class_mapping.json`
   - `models/model1/class_names.json`
   - `models/model1/last_model.pth`
2. **Model 1 Active Dataset**:
   - `data/processed/model1_balanced/`
   - `data/processed/model1_balanced_manifest.csv`
   - `data/processed/model1_balanced_summary.json`
   - `data/processed/model1_balanced_report.md`
3. **Model 2 Production Checkpoint & Config**:
   - `models/model2/best_model.pth`
   - `models/model2/config.json`
   - `models/model2/class_mapping.json`
   - `models/model2/last_model.pth`
   - `models/model2/training_summary.json`
   - `models/pretrained/yolox_s.pth`
4. **Model 2 Active Dataset**:
   - `data/processed/model2_dataset/`
   - `data/processed/model2_yolox/`
5. **Application & Service Code**:
   - `app/` (FastAPI backend + React frontend)
   - `audio/`, `audio_test_app/`
   - `video/`
   - `router/`
   - `pipeline/`
   - `model1_test_app/`
   - `model2/`
   - `scripts/`
   - `venv/`
   - `test_multimodal_assets/`

---

## 4. Execution & Validation Plan
1. Delete only **GREEN** items.
2. Verify all 13 health checks (Model 1, Model 2, FastAPI backend, Router, Audio, Video, Image/Video inference).
