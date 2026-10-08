# Model 1 Plant & Crop Identification Testing Application

A local browser-based testing application for the trained Model 1 plant/crop classification model (EfficientNet-B2). Supports single-image inference and multi-frame video inference with automated quality filtering and probability aggregation.

---

## 1. Purpose

The application is an isolated testing interface for Model 1. It answers the question:
> **"What plant/crop is this?"**

It strictly identifies crops and plants across 22 verified target classes without running disease detection (Model 2), object localization (YOLOX), or RAG/LLM pipelines.

---

## 2. Architecture

```text
                               [ USER INPUT ]
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
                 [ IMAGE ]                       [ VIDEO ]
                     │                               │
                     │                               ▼
                     │                 [ Uniform Frame Extraction ]
                     │                 • 16–24 frames sampled across 0% to 100%
                     │                 • OpenCV quality filter (dark/blur/bright)
                     │                 • Adaptive replenishment if frames rejected
                     │                               │
                     │                               ▼
                     │                    [ 16–24 Selected Frames ]
                     │                               │
                     └───────────────┬───────────────┘
                                     ▼
                    [ Exact ImageNet Preprocessing ]
                    • Resize: (224, 224)
                    • Normalize: Mean=[0.485, 0.456, 0.406], Std=[0.229, 0.224, 0.225]
                                     │
                                     ▼
                      [ Model 1: EfficientNet-B2 ]
                      • Loaded once: models/model1/best_model.pth
                      • Dynamic classes: models/model1/class_mapping.json
                      • Accelerated on CUDA (RTX 3050 Laptop GPU)
                                     │
                                     ▼
                      [ Model 1 on EVERY Selected Frame ]
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
              [ Single Image ]               [ Video Aggregation ]
              • Top-1 prediction             • Mean probability across all selected frames
              • Top-3 confidence bars        • 100% of analyzed frames shown in UI grid
                                             • Detailed frame-level metrics table
```

---

## 3. Model & Classes

- **Architecture:** EfficientNet-B2 (PyTorch torchvision)
- **Checkpoint:** `models/model1/best_model.pth`
- **Configuration:** `models/model1/config.json`
- **Class Mapping:** `models/model1/class_mapping.json` (dynamically loaded)
- **Target Classes (22):**
  anthurium, blueberry, broccoli, capsicum, carnation, cherry_tomato, chrysanthemum, cucumber, french_bean, geranium, gerbera, gypsophila, lettuce, lilium, marigold, melon, orchid, rose, spinach, strawberry, tomato, zucchini.

---

## 4. Supported Inputs

- **Images:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`
- **Videos:** `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.m4v`

---

## 5. How Image Inference Works

1. Image is loaded via PIL and converted to RGB.
2. The exact validation transform is applied:
   - Resize to $(224, 224)$
   - Convert to Tensor ($[0.0, 1.0]$)
   - Normalize with standard ImageNet statistics
3. Tensor is passed through EfficientNet-B2 in `eval()` mode with `torch.no_grad()`.
4. Softmax calculates probability distribution across all 22 classes.
5. Returns Top-1 prediction with confidence percentage and Top-3 ranked classes.

---

## 6. How Video Inference Works

1. **Ingest & Validation:** The video is validated using `video.frame_extractor.validate_video()` ensuring format and header integrity.
2. **16–24 Uniform Temporal Sampling:** Rather than taking only the first few frames or a fixed 10 frames, candidate frames are sampled uniformly across the entire duration (from 0% to 100%).
3. **Quality Filtering & Adaptive Replenishment:**
   - Filters out dark ($\text{mean} < 20.0$), overexposed ($\text{mean} > 240.0$), and blurry ($\text{var} < 15.0$) frames.
   - If candidate frames are rejected, the algorithm automatically probes intermediate video segments to replenish the candidate pool until the target (default: 24 frames) is achieved.
   - If a video genuinely contains fewer usable frames (e.g. short clips), it utilizes all available usable frames with a notice.
4. **Model 1 on EVERY Selected Frame:** Every single selected frame is passed through Model 1 to obtain its own crop prediction, confidence, and full 22-class probability distribution.
5. **Prediction Aggregation:**
   - Calculates the average probability for each class across all selected frames:
     $$\bar{P}_c = \frac{1}{N} \sum_{i=1}^N P_i(c)$$
   - The class with the highest average probability becomes the final video prediction.
6. **Complete Frame Review:** The UI displays **100% of the frames used for inference** in a 4-column responsive grid with individual timestamps, predictions, and confidence percentages (no 10-frame limit).

---

## 7. How to Run

From the project root:

```powershell
.\venv\Scripts\python.exe -m streamlit run model1_test_app/app.py
```

Open `http://localhost:8501` in your browser.

---

## 8. Known Limitations

- **Plant Identification Only:** Does not detect diseases, spots, or pests (Model 2 handles disease detection).
- **Audio Ignored:** Video audio tracks are ignored per specifications.
