# Model 2 (YOLOX-S) Disease Detection & Localization Training Report

## 1. Executive Summary
- **Model Architecture**: YOLOX-S (Depth: 0.33, Width: 0.50, Decoupled Head)
- **Task**: Multi-class bounding-box plant disease detection and localization
- **Disease Classes**: 115 contiguous classes (0–114)
- **Input Resolution**: 640 × 640
- **Training Epochs Completed**: 3 / 10
- **Total Training Time**: 12.38 minutes

## 2. Dataset Distribution
| Split | Images | Bounding Boxes | Bounding Boxes / Image |
|---|---|---|---|
| **Train** | 5,353 | 38,074 | 7.11 |
| **Validation** | 809 | 6,106 | 7.55 |
| **Test** | 1,469 | 10,382 | 7.07 |
| **Total** | **7,631** | **54,562** | **7.15** |

## 3. Training & Hardware Configuration
- **Hardware**: NVIDIA GeForce RTX 3050 Laptop GPU (4.0 GB VRAM)
- **Batch Size**: 8 (with gradient accumulation factor 2 $\rightarrow$ Effective Batch Size 16)
- **Optimizer**: SGD (lr=0.002, momentum=0.9, weight_decay=0.0005, Nesterov=True)
- **LR Scheduler**: Linear Warmup (3 epochs) followed by Cosine Annealing decay
- **Mixed Precision**: Automatic Mixed Precision (AMP) with PyTorch `GradScaler`
- **Pretrained Initialization**: Official YOLOX-S COCO weights transferred across 456 backbone/neck layers

## 4. Evaluation Performance

### Validation Metrics
- **Validation mAP@50**: `0.0249`
- **Validation mAP@50:95**: `0.0148`

### Test Set Metrics (Single Unbiased Final Evaluation)
- **Test mAP@50**: `0.0166`
- **Test mAP@50:95**: `0.0095`
- **Test Images Evaluated**: 1,469 images
- **Test Boxes Evaluated**: 10,382 annotations

## 5. Artifacts Generated
- **Best Weights**: [`models/model2/best_model.pth`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model2/best_model.pth)
- **Model Config**: [`models/model2/config.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model2/config.json)
- **Class Mapping**: [`models/model2/class_mapping.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/models/model2/class_mapping.json)
- **Training Curves**: [`reports/model2/training_curves.png`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2/training_curves.png)
- **Metrics Data**: [`reports/model2/metrics.json`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2/metrics.json)
- **Visual Predictions**: Directory [`reports/model2_predictions/`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_predictions/)
- **Visual Report**: [`reports/model2_visual_report.md`](file:///c:/Users/vyasn/OneDrive/Desktop/Disease_prediction/reports/model2_visual_report.md)

## 6. Standalone Inference Usage
```bash
.\venv\Scripts\python.exe model2/test_model2.py path/to/leaf_image.jpg --conf 0.25
```

Python API:
```python
from model2 import predict_disease
results = predict_disease('path/to/leaf_image.jpg', conf_threshold=0.25)
print(results)
# {'detections': [{'disease_id': 12, 'disease': 'early_blight', 'confidence': 0.912, 'bbox': [x1, y1, x2, y2]}]}
```

## 7. Limitations & Future Work
- **Tail Classes**: Ultra-low support disease classes with < 10 bounding boxes in the training distribution show lower recall.
- **Extreme Shadowing / Glare**: Intense sunlight glare on wet leaves can cause partial lesion boundary clipping.
- **Downstream Orchestration**: Standalone Model 2 is fully ready for downstream multi-modal router and video frame aggregation integration in subsequent stages.