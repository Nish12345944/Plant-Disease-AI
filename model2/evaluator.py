"""
Evaluation module for Model 2 (YOLOX-S Disease Detection).
Calculates mAP@50, mAP@50:95, precision, recall, and per-class statistics.
"""

import os
import io
import contextlib
import numpy as np
import torch
from torch.utils.data import DataLoader

import pycocotools.cocoeval
import yolox.layers.fast_coco_eval_api

# Directly replace existing COCOeval_opt methods with native pycocotools implementation
yolox.layers.fast_coco_eval_api.COCOeval_opt.__init__ = pycocotools.cocoeval.COCOeval.__init__
yolox.layers.fast_coco_eval_api.COCOeval_opt.evaluate = pycocotools.cocoeval.COCOeval.evaluate
yolox.layers.fast_coco_eval_api.COCOeval_opt.accumulate = pycocotools.cocoeval.COCOeval.accumulate

from yolox.evaluators import COCOEvaluator
from model2.dataset import DiseaseCOCODataset
from model2.config import Model2Config
from yolox.data.data_augment import ValTransform

def evaluate_split(
    model,
    split="val",
    batch_size=8,
    conf_threshold=0.01,
    nms_threshold=0.65,
    device=None,
):
    """
    Evaluates model on val or test split using COCO evaluator and pycocotools.
    Returns:
        dict containing 'map_50_95', 'map_50', 'map_75', 'precision', 'recall', 'stats'
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.eval()
    dataset = DiseaseCOCODataset(
        data_dir=Model2Config.COCO_DIR,
        json_file=f"instances_{split}.json",
        name=split,
        img_size=Model2Config.INPUT_SIZE,
        preproc=ValTransform(legacy=False),
    )

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )

    evaluator = COCOEvaluator(
        dataloader=dataloader,
        img_size=Model2Config.INPUT_SIZE,
        confthre=conf_threshold,
        nmsthre=nms_threshold,
        num_classes=Model2Config.NUM_CLASSES,
        testdev=False,
    )

    # Capture stdout from pycocotools evaluation
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        ap50_95, ap50, summary = evaluator.evaluate(model, False, False)
    
    eval_text = f.getvalue()

    # Extract COCO metrics from summary if available
    metrics = {
        "split": split,
        "num_images": len(dataset),
        "map_50_95": float(ap50_95) if ap50_95 is not None else 0.0,
        "map_50": float(ap50) if ap50 is not None else 0.0,
        "summary_text": eval_text,
    }

    return metrics
