# Video Input Module Test & Validation Report

**Date:** 2026-10-06  
**Module:** `video/` (Plant Disease Detection Project)  
**Status:** VALIDATED & PASSING (10/10 automated tests passed)

---

## 1. Implementation Summary

A lightweight, modular, and memory-efficient video input and frame processing subsystem was developed for the plant disease detection pipeline. The module is strictly isolated to video ingest, validation, metadata extraction, sequential frame sampling, and statistical quality filtering without loading heavy machine learning models or loading full videos into RAM.

### Pipeline Flow
```text
VIDEO FILE (.mp4, .avi, .mov, .mkv, .webm, .m4v)
       ↓
[1. validate_video()]
    • File existence & read permissions
    • Supported extension whitelist
    • OpenCV VideoCapture stream integrity
    • First frame decodability check
       ↓
[2. get_video_metadata()]
    • Resolution (width x height), FPS, frame count, duration
    • FourCC codec decoding & fallback estimations
       ↓
[3. compute_sample_indices()]
    • Configurable rate (e.g. 1.0 FPS, 2.0 FPS)
    • Avoids duplicate frame indices
       ↓
[4. Sequential Frame Ingest & Quality Filter]
    • OpenCV cap.grab() for skipped frames (zero decode overhead)
    • OpenCV cap.read() only for target sample frames
    • FrameQualityFilter:
        - Mean intensity check (too_dark / too_bright)
        - Laplacian variance check (blurry)
        - Normalized composite quality score (0.0 - 1.0)
       ↓
[5. Temporary Storage & Cleanup]
    • JPEG write to temp_video_frames/session_<id>/
    • Automated cleanup utilities
       ↓
STRUCTURED RESULT (Ready for downstream Model 1 & Model 2 ingestion)
```

---

## 2. Files Created

| File | Purpose |
| :--- | :--- |
| `video/__init__.py` | Package initialisation exporting validation, metadata, sampling, and processing APIs |
| `video/frame_extractor.py` | Video validation, extension whitelisting, codec parsing, and metadata extraction |
| `video/processor.py` | Sequential frame sampler, OpenCV Laplacian/brightness quality filter, and session cleanup |
| `video/test_video.py` | CLI test interface with formatted terminal tables and visual preview output |
| `scripts/run_video_validation_suite.py` | Automated 10-point test runner validating all edge cases and formats |
| `reports/video_test_report.md` | Comprehensive validation and performance report |
| `reports/video_samples/` | Sample preview frames (`sample_01.jpg` .. `sample_10.jpg`) and `contact_sheet.jpg` |

No existing model checkpoints, datasets, audio modules, query router rules, or orchestrator code were modified.

---

## 3. Dependencies Used

All dependencies run 100% locally from `.\venv\`:
- **OpenCV (`cv2`)**: `5.0.0` (video streaming, decoding, Laplacian filter, image writes)
- **NumPy**: `2.5.3` (array statistics and fast mean/variance calculation)
- **Python Standard Library**: `pathlib`, `shutil`, `uuid`, `argparse`, `math`, `tempfile`

Zero cloud APIs, zero paid services, and zero heavy machine learning packages required at this ingest stage.

---

## 4. Test Results & Edge Cases Validated

The test suite in `scripts/run_video_validation_suite.py` was executed against synthetic video streams covering various FPS rates, durations, and artifact types.

```text
============================================================
VALIDATION SUITE RESULTS SUMMARY
============================================================
  [PASS] test_1_valid_mp4_metadata
  [PASS] test_2_multi_fps (15 FPS & 60 FPS)
  [PASS] test_3_non_existent
  [PASS] test_4_unsupported_ext
  [PASS] test_5_short_video (<1s)
  [PASS] test_6_empty_and_corrupt
  [PASS] test_7_quality_rejection
  [PASS] test_8_cleanup
  [PASS] test_9_sampling_1fps
  [PASS] test_10_sampling_2fps

TOTAL: 10/10 passed (100.0%)
```

### Detailed Test Outcomes:

1. **Metadata Extraction:**
   - Evaluated 5.0-second 30 FPS MP4 video (640x480).
   - Correctly extracted: `width=640`, `height=480`, `fps=30.0`, `frame_count=150`, `duration_seconds=5.0`, `codec='mp4v'`.
2. **Variable Frame Rates:**
   - 15 FPS AVI: `fps=15.0`, `frame_count=45`, `duration=3.0s`.
   - 60 FPS MP4: `fps=60.0`, `frame_count=120`, `duration=2.0s`.
3. **Invalid & Corrupt File Handling:**
   - Missing path: caught `InvalidVideoError: Video file does not exist`.
   - Unsupported extension (`.txt`): caught `InvalidVideoError: Unsupported video extension '.txt'`.
   - 0-byte file: caught `EmptyVideoError: Video file is empty (0 bytes)`.
   - Corrupted stream header: caught `InvalidVideoError: OpenCV could not open video file`.
4. **Short Video Support:**
   - 0.33-second video (10 frames): successfully sampled frame 0 without division-by-zero or empty-index errors.
5. **Quality Filter Rejection:**
   - Normal leaf frame (Frame 0): `quality_score = 0.77`, `status = ACCEPTED`
   - Dark frame (Frame 60, mean brightness 8.0 < 25.0): `status = REJECTED`, `reason = 'too_dark'`
   - Overexposed frame (Frame 90, mean brightness 248.0 > 235.0): `status = REJECTED`, `reason = 'too_bright'`
   - Blurry frame (Frame 120, Laplacian variance 1.54 < 50.0): `status = REJECTED`, `reason = 'blurry'`
6. **Sampling Accuracy:**
   - 1.0 FPS: exactly 5 frames sampled `[0, 30, 60, 90, 120]`.
   - 2.0 FPS: exactly 10 frames sampled `[0, 15, 30, 45, 60, 75, 90, 105, 120, 135]`.
7. **Storage & Cleanup:**
   - Temporary frames written to `temp_video_frames/session_<id>/` as standard JPEGs.
   - Calling `cleanup_frames()` completely removed the session folder and all files.

---

## 5. CLI Execution & Terminal Output

### Command:
```powershell
.\venv\Scripts\python.exe video/test_video.py temp_test_videos/sample_plant_30fps.mp4 --sample-fps 1.0
```

### Output:
```text
==================================================
VIDEO TEST
==================================================

File:
sample_plant_30fps.mp4

Resolution:
640 x 480

FPS:
30.0

Frames:
150

Duration:
5.0 sec

Sampling:
1.0 FPS

Sampled frames:
5

Accepted frames:
2

Rejected frames:
3

Temporary frame directory:
C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\temp_video_frames\session_3bdbd7e1

==================================================
Frame    Time       Quality      Status       Reason          
----------------------------------------------------------
0        0.00s      0.77         ACCEPTED     accepted        
30       1.00s      0.77         ACCEPTED     accepted        
60       2.00s      0.02         REJECTED     too_dark        
90       3.00s      0.02         REJECTED     too_bright      
120      4.00s      0.14         REJECTED     blurry          
==================================================

Visual preview: Saved 5 sample frames to: C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\video_samples
Contact sheet : C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\reports\video_samples\contact_sheet.jpg
```

---

## 6. Visual Preview Output

The test runner saved preview frames and an overview contact sheet under `reports/video_samples/`:
- `contact_sheet.jpg`: 2D montage grid of extracted frames with timestamps and indices.
- `sample_01_frame_000000.jpg` through `sample_05_frame_000120.jpg`.

---

## 7. Known Limitations & Future Integration Path

1. **Audio Streams**: Video audio tracks are deliberately untouched per requirements. When required later, audio can be extracted via PyAV/ffmpeg and fed to `audio/test_audio.py` (`faster-whisper`).
2. **Variable Frame Rate (VFR) Containers**: For VFR containers where metadata reports inaccurate FPS, the module automatically activates frame-probing fallbacks.
3. **Downstream Integration**: The resulting frame paths array in `process_video()`:
   ```json
   {
       "frame_index": 0,
       "timestamp_seconds": 0.0,
       "path": "temp_video_frames/session_xxx/frame_000000.jpg",
       "quality_score": 0.77,
       "accepted": true
   }
   ```
   can be passed directly to Model 1 (EfficientNet plant identification) and Model 2 (disease detection/bounding box localization) in future pipeline milestones.
