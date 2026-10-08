"""
Standalone Training Pipeline for Model 2 (Plant Disease Detection & Localization using YOLOX-S).
"""

import os
import sys
import time
import json
import argparse
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.amp import autocast, GradScaler

import pycocotools.cocoeval
import yolox.layers.fast_coco_eval_api

# Directly replace existing COCOeval_opt methods with native pycocotools implementation
yolox.layers.fast_coco_eval_api.COCOeval_opt.__init__ = pycocotools.cocoeval.COCOeval.__init__
yolox.layers.fast_coco_eval_api.COCOeval_opt.evaluate = pycocotools.cocoeval.COCOeval.evaluate
yolox.layers.fast_coco_eval_api.COCOeval_opt.accumulate = pycocotools.cocoeval.COCOeval.accumulate

from yolox.exp import Exp
from yolox.utils import ModelEMA, postprocess
from yolox.data.data_augment import TrainTransform, ValTransform

# Add workspace to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model2.dataset import DiseaseCOCODataset
from model2.config import Model2Config
from model2.evaluator import evaluate_split

def setup_directories():
    os.makedirs(Model2Config.OUTPUT_MODEL_DIR, exist_ok=True)
    os.makedirs(Model2Config.REPORT_DIR, exist_ok=True)
    os.makedirs(Model2Config.PREDICTIONS_DIR, exist_ok=True)

def load_pretrained_yolox_s(model, pretrained_path):
    if not os.path.exists(pretrained_path):
        print(f"[Warning] Pretrained weights {pretrained_path} not found. Training from scratch.", flush=True)
        return model
    
    print(f"[Trainer] Loading pretrained weights from {pretrained_path}...", flush=True)
    ckpt = torch.load(pretrained_path, map_location="cpu")
    state_dict = ckpt["model"] if "model" in ckpt else ckpt
    model_dict = model.state_dict()
    
    matched = {}
    mismatched = []
    for k, v in state_dict.items():
        if k in model_dict and model_dict[k].shape == v.shape:
            matched[k] = v
        else:
            mismatched.append(k)
            
    model_dict.update(matched)
    model.load_state_dict(model_dict)
    print(f"[Trainer] Successfully transferred {len(matched)} layers. Initialized {len(mismatched)} new/modified layers.", flush=True)
    return model

def get_lr_scheduler(optimizer, total_iters, warmup_iters, lr_init, min_lr_ratio=0.05):
    """Cosine learning rate scheduler with warmup."""
    def lr_lambda(step):
        if step < warmup_iters:
            # Linear warmup
            return max(1e-4, (step + 1) / max(1, warmup_iters))
        else:
            # Cosine decay
            progress = (step - warmup_iters) / max(1, (total_iters - warmup_iters))
            cosine_factor = 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))
            return min_lr_ratio + (1.0 - min_lr_ratio) * cosine_factor
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

def train(
    epochs=Model2Config.MAX_EPOCH,
    batch_size=Model2Config.BATCH_SIZE,
    accumulate_batches=Model2Config.ACCUMULATE_GRAD_BATCHES,
    lr=Model2Config.LR,
    eval_interval=2,
    use_amp=Model2Config.AMP,
    resume=True,
):
    setup_directories()
    
    # Save config and class mapping to output directory
    class_mapping = Model2Config.load_class_mapping()
    with open(Model2Config.SAVED_CLASS_MAPPING_PATH, "w", encoding="utf-8") as f:
        json.dump(class_mapping, f, indent=2)
    with open(Model2Config.SAVED_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(Model2Config.to_dict(), f, indent=2)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"============================================================", flush=True)
    print(f" STARTING MODEL 2 TRAINING (YOLOX-S)", flush=True)
    print(f" Device: {device} | CUDA Available: {torch.cuda.is_available()}", flush=True)
    if torch.cuda.is_available():
        print(f" GPU: {torch.cuda.get_device_name(0)}", flush=True)
        print(f" VRAM: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB", flush=True)
    print(f" Total Classes: {Model2Config.NUM_CLASSES}", flush=True)
    print(f" Input Resolution: {Model2Config.INPUT_SIZE}", flush=True)
    print(f" Batch Size: {batch_size} (Effective Batch Size: {batch_size * accumulate_batches})", flush=True)
    print(f" Total Epochs: {epochs}", flush=True)
    print(f" Mixed Precision (AMP): {use_amp}", flush=True)
    print(f"============================================================", flush=True)

    # 1. Build Model
    exp = Exp()
    exp.num_classes = Model2Config.NUM_CLASSES
    exp.depth = Model2Config.DEPTH
    exp.width = Model2Config.WIDTH
    model = exp.get_model()

    start_epoch = 1
    history = {
        "epoch": [],
        "train_total_loss": [],
        "train_iou_loss": [],
        "train_conf_loss": [],
        "train_cls_loss": [],
        "val_map_50": [],
        "val_map_50_95": [],
        "lr": [],
    }

    if resume and os.path.exists(Model2Config.LAST_MODEL_PATH):
        print(f"[Trainer] Resuming from checkpoint: {Model2Config.LAST_MODEL_PATH}...", flush=True)
        ckpt = torch.load(Model2Config.LAST_MODEL_PATH, map_location="cpu")
        state_dict = ckpt["model"] if "model" in ckpt else ckpt
        model.load_state_dict(state_dict)
        if "epoch" in ckpt:
            start_epoch = ckpt["epoch"] + 1
        if "history" in ckpt:
            history = ckpt["history"]
        print(f"[Trainer] Successfully resumed at Epoch {start_epoch}.", flush=True)
    else:
        model = load_pretrained_yolox_s(model, Model2Config.PRETRAINED_WEIGHTS)

    model.to(device)

    # Model EMA for stable convergence
    ema_model = ModelEMA(model, 0.9998)
    ema_model.updates = 0

    # 2. Datasets & DataLoaders
    train_dataset = DiseaseCOCODataset(
        data_dir=Model2Config.COCO_DIR,
        json_file="instances_train.json",
        name="train",
        img_size=Model2Config.INPUT_SIZE,
        preproc=TrainTransform(max_labels=100, flip_prob=0.5, hsv_prob=0.5),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=0,  # 0 workers for Windows stability
        pin_memory=True if torch.cuda.is_available() else False,
        drop_last=True,
    )

    # 3. Optimizer & Scheduler
    optimizer = torch.optim.SGD(
        model.parameters(),
        lr=lr,
        momentum=Model2Config.MOMENTUM,
        weight_decay=Model2Config.WEIGHT_DECAY,
        nesterov=True,
    )
    
    steps_per_epoch = len(train_loader) // accumulate_batches
    total_optimizer_steps = epochs * steps_per_epoch
    warmup_steps = Model2Config.WARMUP_EPOCHS * steps_per_epoch
    scheduler = get_lr_scheduler(optimizer, total_optimizer_steps, warmup_steps, lr)
    scaler = GradScaler("cuda", enabled=use_amp and torch.cuda.is_available())

    # Training Tracking History
    history = {
        "epoch": [],
        "train_total_loss": [],
        "train_iou_loss": [],
        "train_conf_loss": [],
        "train_cls_loss": [],
        "val_map_50": [],
        "val_map_50_95": [],
        "lr": [],
    }

    best_val_map = -1.0
    start_time = time.time()

    for epoch in range(start_epoch, epochs + 1):
        model.train()
        epoch_start_time = time.time()
        
        running_total_loss = 0.0
        running_iou_loss = 0.0
        running_conf_loss = 0.0
        running_cls_loss = 0.0
        batches_processed = 0

        optimizer.zero_grad()

        for batch_idx, (imgs, targets, info_imgs, ids) in enumerate(train_loader):
            imgs = imgs.to(device, non_blocking=True).float()
            targets = targets.to(device, non_blocking=True).float()

            with autocast("cuda", enabled=use_amp and torch.cuda.is_available()):
                outputs = model(imgs, targets)
                total_loss = outputs["total_loss"]
                loss_scaled = total_loss / accumulate_batches

            scaler.scale(loss_scaled).backward()

            if (batch_idx + 1) % accumulate_batches == 0 or (batch_idx + 1) == len(train_loader):
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=10.0)
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                scheduler.step()
                ema_model.update(model)

            # Record stats
            running_total_loss += total_loss.item()
            running_iou_loss += outputs["iou_loss"].item()
            running_conf_loss += outputs["conf_loss"].item()
            running_cls_loss += outputs["cls_loss"].item()
            batches_processed += 1

            if (batch_idx + 1) % 100 == 0 or (batch_idx + 1) == len(train_loader):
                current_lr = optimizer.param_groups[0]["lr"]
                print(
                    f"Epoch [{epoch:02d}/{epochs:02d}] Batch [{batch_idx+1:04d}/{len(train_loader):04d}] "
                    f"Loss: {total_loss.item():.4f} (IoU: {outputs['iou_loss'].item():.4f}, "
                    f"Obj: {outputs['conf_loss'].item():.4f}, Cls: {outputs['cls_loss'].item():.4f}) "
                    f"LR: {current_lr:.6f}",
                    flush=True
                )

        # Epoch loss averages
        avg_total_loss = running_total_loss / max(1, batches_processed)
        avg_iou_loss = running_iou_loss / max(1, batches_processed)
        avg_conf_loss = running_conf_loss / max(1, batches_processed)
        avg_cls_loss = running_cls_loss / max(1, batches_processed)
        current_lr = optimizer.param_groups[0]["lr"]
        epoch_time = time.time() - epoch_start_time

        print(
            f"--- Epoch {epoch}/{epochs} Complete ({epoch_time:.1f}s) --- "
            f"Avg Loss: {avg_total_loss:.4f} | IoU: {avg_iou_loss:.4f} | "
            f"Obj: {avg_conf_loss:.4f} | Cls: {avg_cls_loss:.4f}",
            flush=True
        )

        history["epoch"].append(epoch)
        history["train_total_loss"].append(avg_total_loss)
        history["train_iou_loss"].append(avg_iou_loss)
        history["train_conf_loss"].append(avg_conf_loss)
        history["train_cls_loss"].append(avg_cls_loss)
        history["lr"].append(current_lr)

        # Validation Evaluation
        val_map_50 = 0.0
        val_map_50_95 = 0.0
        if epoch % eval_interval == 0 or epoch == epochs:
            print(f"[Trainer] Evaluating validation set at epoch {epoch}...", flush=True)
            val_metrics = evaluate_split(ema_model.ema, split="val", batch_size=Model2Config.VAL_BATCH_SIZE, device=device)
            val_map_50 = val_metrics["map_50"]
            val_map_50_95 = val_metrics["map_50_95"]
            print(f"[Validation @ Epoch {epoch}] mAP@50: {val_map_50:.4f} | mAP@50:95: {val_map_50_95:.4f}", flush=True)

            # Best model tracking
            if val_map_50_95 > best_val_map:
                best_val_map = val_map_50_95
                print(f"[*] New best validation mAP@50:95: {best_val_map:.4f}! Saving {Model2Config.BEST_MODEL_PATH}...", flush=True)
                torch.save({"model": ema_model.ema.state_dict(), "epoch": epoch, "val_map_50_95": best_val_map}, Model2Config.BEST_MODEL_PATH)

        history["val_map_50"].append(val_map_50)
        history["val_map_50_95"].append(val_map_50_95)

        # Save last checkpoint
        torch.save({"model": ema_model.ema.state_dict(), "epoch": epoch, "history": history}, Model2Config.LAST_MODEL_PATH)
        if not os.path.exists(Model2Config.BEST_MODEL_PATH):
            torch.save({"model": ema_model.ema.state_dict(), "epoch": epoch, "val_map_50_95": best_val_map}, Model2Config.BEST_MODEL_PATH)

        # Update training curves and summary every epoch
        plot_training_curves(history, Model2Config.TRAINING_CURVES_PATH)
        save_training_summary(history, best_val_map, time.time() - start_time, epoch, epochs)

    print(f"\n============================================================", flush=True)
    print(f" TRAINING COMPLETE in {(time.time() - start_time) / 60:.2f} minutes", flush=True)
    print(f" Best Validation mAP@50:95: {best_val_map:.4f}", flush=True)
    print(f" Best Checkpoint: {Model2Config.BEST_MODEL_PATH}", flush=True)
    print(f"============================================================", flush=True)
    return history

def plot_training_curves(history, save_path):
    plt.figure(figsize=(14, 10))
    epochs = history["epoch"]

    # 1. Total Loss
    plt.subplot(2, 2, 1)
    plt.plot(epochs, history["train_total_loss"], "r-o", label="Total Loss", linewidth=2)
    plt.title("Training Total Loss", fontsize=12)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    # 2. Loss Components
    plt.subplot(2, 2, 2)
    plt.plot(epochs, history["train_iou_loss"], "b-", label="IoU Loss")
    plt.plot(epochs, history["train_conf_loss"], "g-", label="Objectness Loss")
    plt.plot(epochs, history["train_cls_loss"], "m-", label="Classification Loss")
    plt.title("Loss Components", fontsize=12)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    # 3. Validation mAP
    plt.subplot(2, 2, 3)
    val_epochs = [e for e, m in zip(epochs, history["val_map_50"]) if m > 0]
    val_map50 = [m for m in history["val_map_50"] if m > 0]
    val_map50_95 = [m for m in history["val_map_50_95"] if m > 0]
    if val_map50:
        plt.plot(val_epochs, val_map50, "g-o", label="Val mAP@50", linewidth=2)
        plt.plot(val_epochs, val_map50_95, "b-s", label="Val mAP@50:95", linewidth=2)
    plt.title("Validation mAP Progression", fontsize=12)
    plt.xlabel("Epoch")
    plt.ylabel("mAP")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    # 4. Learning Rate Schedule
    plt.subplot(2, 2, 4)
    plt.plot(epochs, history["lr"], "k-", label="Learning Rate")
    plt.title("Learning Rate Schedule", fontsize=12)
    plt.xlabel("Epoch")
    plt.ylabel("LR")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()

def save_training_summary(history, best_val_map, elapsed_seconds, current_epoch, total_epochs):
    summary = {
        "model": "YOLOX-S",
        "num_classes": Model2Config.NUM_CLASSES,
        "input_resolution": list(Model2Config.INPUT_SIZE),
        "epochs_completed": current_epoch,
        "total_target_epochs": total_epochs,
        "elapsed_time_seconds": round(elapsed_seconds, 2),
        "elapsed_time_minutes": round(elapsed_seconds / 60.0, 2),
        "final_train_loss": round(history["train_total_loss"][-1], 4) if history["train_total_loss"] else None,
        "best_val_map_50_95": round(best_val_map, 4),
        "history": history,
    }
    with open(Model2Config.TRAINING_SUMMARY_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Model 2 YOLOX-S")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Per-GPU batch size")
    parser.add_argument("--accumulate", type=int, default=2, help="Gradient accumulation steps")
    parser.add_argument("--lr", type=float, default=0.002, help="Learning rate")
    parser.add_argument("--eval_interval", type=int, default=2, help="Validation evaluation interval (epochs)")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume from last checkpoint")
    args = parser.parse_args()

    train(
        epochs=args.epochs,
        batch_size=args.batch_size,
        accumulate_batches=args.accumulate,
        lr=args.lr,
        eval_interval=args.eval_interval,
        resume=not args.no_resume,
    )
