# Model 2 V2 Inference Contract & Healthy-Crop Standard

**Date:** 2026-10-07  
**Model:** EfficientNet-B2 Disease Classifier (117 Classes: Class 0 = shared `healthy`, Classes 1–116 = crop-specific diseases)  
**Checkpoint:** [`models/model2_classifier_v2/best_model.pth`](file:///C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\models\model2_classifier_v2\best_model.pth)  

---

## 1. Core Principles

1. **"Healthy" is a Status, NOT a Disease:**
   - When Model 1 identifies a crop (e.g., Tomato) and Model 2 predicts class 0 (`healthy`), the system explicitly reports that the crop is healthy.
   - The output contract sets `status: "healthy"` and `disease: null`.
   - The human-readable string outputs `Crop: Tomato\nStatus: Healthy` (and **never** `Disease: Healthy`).

2. **Universal Healthy Class Compatibility:**
   - The shared `healthy` class represents the absence of detectable disease lesions and is valid for all 39+ supported crops.

3. **Incompatible Prediction Protection:**
   - When Model 1 predicts a specific crop (e.g., `Tomato`) and Model 2 raw prediction strongly indicates an incompatible disease of another crop (e.g., `banana__panama_disease`), the system rejects the prediction and returns `status: "uncertain"` with `disease: null`.

4. **Calibrated Uncertainty Handling:**
   - Low-confidence predictions below decision thresholds are not forced into `diseased`; they return `status: "uncertain"` and `disease: null`.

---

## 2. Standardized JSON Output Contract

```json
{
  "crop": "tomato",
  "crop_confidence": 0.98,
  "status": "healthy",
  "disease": null,
  "disease_confidence": 0.994
}
```

### Field Definitions:

| Field | Type | Values / Description |
|---|---|---|
| `crop` | string | Normalized lowercase crop identifier (e.g., `"tomato"`, `"cucumber"`). |
| `crop_confidence` | float | Model 1 confidence score (0.0 to 1.0). |
| `status` | string | One of `"healthy"`, `"diseased"`, or `"uncertain"`. |
| `disease` | string \| null | Disease class slug (e.g., `"tomato__early_blight"`) when `status == "diseased"`; `null` when `status` is `"healthy"` or `"uncertain"`. |
| `disease_confidence` | float | Calibrated confidence score (0.0 to 1.0) from Model 2. |

---

## 3. Human-Readable Output Standard

### A. Healthy Case (e.g., Tomato + Healthy)
```
Crop: Tomato
Status: Healthy
```

### B. Diseased Case (e.g., Tomato + Tomato Early Blight)
```
Crop: Tomato
Disease: Early Blight
Status: Diseased
```

### C. Uncertain / Incompatible Case (e.g., Tomato + Banana Panama Disease)
```
Crop: Tomato
Status: Uncertain
```

---

## 4. Usage in Python

```python
from models.model2_classifier_v2.predict import Model2DiseaseClassifierV2

classifier = Model2DiseaseClassifierV2()

# Two-stage conditioned inference
result = classifier.predict_crop_aware(
    image_input="path/to/leaf.jpg",
    crop_name="Tomato",
    crop_confidence=0.96
)

print(result["status"])           # "healthy", "diseased", or "uncertain"
print(result["disease"])          # None or "tomato__early_blight"
print(result["human_readable"])   # Clean formatted output
```
