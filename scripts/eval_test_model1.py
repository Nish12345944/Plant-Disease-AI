"""Evaluate the trained Model 1 (EfficientNet-B2) best checkpoint on the unseen test set.

Generates:
- Test Accuracy
- Macro Precision
- Macro Recall
- Macro F1
- Weighted F1
- Top-3 Accuracy
- Per-class classification report
- Confusion matrix
"""

import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import efficientnet_b2

ROOT = Path(r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction")
DATASET_DIR = ROOT / "data" / "processed" / "model1_dataset"
MODELS_DIR = ROOT / "models" / "model1"
RESULTS_DIR = ROOT / "results" / "model1"

BEST_MODEL_PATH = MODELS_DIR / "best_model.pth"
CLASS_NAMES_PATH = MODELS_DIR / "class_names.json"
TEST_METRICS_PATH = RESULTS_DIR / "test_evaluation_report.json"
CONFUSION_MATRIX_PATH = RESULTS_DIR / "confusion_matrix.json"

IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_WORKERS = 2

class RobustImageFolder(datasets.ImageFolder):
    def __init__(self, root, fixed_classes, fixed_class_to_idx, transform=None):
        self.fixed_classes = fixed_classes
        self.fixed_class_to_idx = fixed_class_to_idx
        super().__init__(root, transform=transform, allow_empty=True)

    def find_classes(self, directory):
        return self.fixed_classes, self.fixed_class_to_idx

def run_evaluation():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("=" * 80)
    print("MODEL 1 BEST CHECKPOINT TEST SET EVALUATION")
    print(f"Device : {device} ({torch.cuda.get_device_name(0)})")
    print(f"Model  : {BEST_MODEL_PATH}")
    print("=" * 80)

    # 1. Load class names
    with open(CLASS_NAMES_PATH, encoding="utf-8") as f:
        meta = json.load(f)
        classes = meta["classes"]
        class_to_idx = meta["class_to_idx"]

    num_classes = len(classes)
    print(f"Total classes: {num_classes}")

    # 2. Test dataset and dataloader
    imagenet_mean = [0.485, 0.456, 0.406]
    imagenet_std = [0.229, 0.224, 0.225]

    eval_transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=imagenet_mean, std=imagenet_std),
    ])

    test_dir = DATASET_DIR / "test"
    test_dataset = RobustImageFolder(test_dir, classes, class_to_idx, transform=eval_transform)
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
    )
    print(f"Test samples: {len(test_dataset):,}")

    # 3. Model setup and checkpoint loading
    model = efficientnet_b2(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)

    print(f"Loading weights from {BEST_MODEL_PATH} (weights_only=False)...")
    checkpoint = torch.load(BEST_MODEL_PATH, map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    model.eval()

    best_epoch = checkpoint.get("epoch", "N/A")
    val_macro_f1 = checkpoint.get("val_macro_f1", "N/A")
    print(f"Loaded checkpoint saved from Epoch {best_epoch} (Val Macro F1: {val_macro_f1:.4f} if float else {val_macro_f1})")

    # 4. Evaluation Loop
    criterion = nn.CrossEntropyLoss()
    total_loss = 0.0
    all_preds = []
    all_targets = []
    all_probs = []

    print("\nRunning inference on test set with AMP...")
    t0 = time.time()
    with torch.no_grad():
        for images, targets in test_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)

            with torch.autocast("cuda", dtype=torch.float16):
                outputs = model(images)
                loss = criterion(outputs, targets)

            total_loss += loss.item() * targets.size(0)
            probs = torch.softmax(outputs, dim=1)
            preds = outputs.argmax(dim=1)

            all_probs.append(probs.cpu().numpy())
            all_preds.append(preds.cpu().numpy())
            all_targets.append(targets.cpu().numpy())

    infer_time = time.time() - t0
    all_preds = np.concatenate(all_preds)
    all_targets = np.concatenate(all_targets)
    all_probs = np.concatenate(all_probs)

    test_loss = total_loss / len(all_targets)
    test_acc = (all_preds == all_targets).mean()
    macro_prec = precision_score(all_targets, all_preds, average="macro", zero_division=0)
    macro_rec = recall_score(all_targets, all_preds, average="macro", zero_division=0)
    macro_f1 = f1_score(all_targets, all_preds, average="macro", zero_division=0)
    weighted_f1 = f1_score(all_targets, all_preds, average="weighted", zero_division=0)

    # Top-3 Accuracy
    top3_correct = 0
    for i, target in enumerate(all_targets):
        top3_indices = np.argsort(all_probs[i])[-3:]
        if target in top3_indices:
            top3_correct += 1
    top3_acc = top3_correct / len(all_targets)

    # Classification report
    unique_labels_present = sorted(list(set(all_targets) | set(all_preds)))
    target_names = [classes[idx] for idx in unique_labels_present]
    report_dict = classification_report(
        all_targets,
        all_preds,
        labels=unique_labels_present,
        target_names=target_names,
        output_dict=True,
        zero_division=0,
    )
    report_text = classification_report(
        all_targets,
        all_preds,
        labels=unique_labels_present,
        target_names=target_names,
        digits=4,
        zero_division=0,
    )

    # Confusion matrix
    cm = confusion_matrix(all_targets, all_preds, labels=list(range(num_classes)))
    cm_list = cm.tolist()

    # Save test metrics report
    test_results = {
        "best_epoch": int(best_epoch) if isinstance(best_epoch, (int, np.integer)) else best_epoch,
        "test_loss": float(round(test_loss, 4)),
        "test_accuracy": float(round(test_acc, 4)),
        "macro_precision": float(round(macro_prec, 4)),
        "macro_recall": float(round(macro_rec, 4)),
        "macro_f1": float(round(macro_f1, 4)),
        "weighted_f1": float(round(weighted_f1, 4)),
        "top3_accuracy": float(round(top3_acc, 4)),
        "inference_time_sec": float(round(infer_time, 2)),
        "total_test_samples": int(len(all_targets)),
        "per_class_report": report_dict,
    }

    with open(TEST_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)

    with open(CONFUSION_MATRIX_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "classes": classes,
            "confusion_matrix": cm_list,
        }, f, indent=2)

    print("\n" + "=" * 80)
    print("FINAL TEST METRICS SUMMARY")
    print("=" * 80)
    print(f"  Test Accuracy   : {test_acc * 100:.2f}% ({np.sum(all_preds == all_targets):,} / {len(all_targets):,})")
    print(f"  Macro Precision : {macro_prec:.4f}")
    print(f"  Macro Recall    : {macro_rec:.4f}")
    print(f"  Macro F1        : {macro_f1:.4f}")
    print(f"  Weighted F1     : {weighted_f1:.4f}")
    print(f"  Top-3 Accuracy  : {top3_acc * 100:.2f}%")
    print(f"  Test Loss       : {test_loss:.4f}")
    print(f"  Inference Time  : {infer_time:.2f} s ({infer_time / len(all_targets) * 1000:.2f} ms/image)")

    print("\n" + "=" * 80)
    print("PER-CLASS CLASSIFICATION REPORT")
    print("=" * 80)
    print(report_text)

    print("=" * 80)
    print(f"Saved Test Report to : {TEST_METRICS_PATH}")
    print(f"Saved Confusion Matrix : {CONFUSION_MATRIX_PATH}")
    print("=" * 80)
    sys.stdout.flush()

if __name__ == "__main__":
    run_evaluation()
