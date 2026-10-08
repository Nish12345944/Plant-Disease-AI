"""
Dataset loader for Model 2 (Plant Disease Detection & Localization) using YOLOX.
Uses non-destructive COCO format annotations while referencing the original image files.
"""

import os
import cv2
import numpy as np
import torch
from yolox.data.datasets import COCODataset
from yolox.data.data_augment import TrainTransform, ValTransform

class DiseaseCOCODataset(COCODataset):
    def __init__(
        self,
        data_dir="data/processed/model2_yolox",
        json_file="instances_train.json",
        name="train",
        img_size=(640, 640),
        preproc=None,
        cache=False,
    ):
        super().__init__(
            data_dir=data_dir,
            json_file=json_file,
            name=name,
            img_size=img_size,
            preproc=preproc,
            cache=cache,
        )
        self.split_name = name

    def load_resized_img(self, index):
        img_info = self.coco.loadImgs(self.ids[index])[0]
        if "file_path" in img_info and os.path.exists(img_info["file_path"]):
            img_path = img_info["file_path"]
        else:
            img_path = os.path.join("data/processed/model2_dataset", "images", self.split_name, img_info["file_name"])
        
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Could not load image: {img_path}")
        
        r = min(self.img_size[0] / img.shape[0], self.img_size[1] / img.shape[1])
        resized_img = cv2.resize(
            img,
            (int(img.shape[1] * r), int(img.shape[0] * r)),
            interpolation=cv2.INTER_LINEAR,
        ).astype(np.uint8)
        return resized_img

    def load_image(self, index):
        img_info = self.coco.loadImgs(self.ids[index])[0]
        if "file_path" in img_info and os.path.exists(img_info["file_path"]):
            img_path = img_info["file_path"]
        else:
            img_path = os.path.join("data/processed/model2_dataset", "images", self.split_name, img_info["file_name"])
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Could not load image: {img_path}")
        return img


def get_disease_dataset(split="train", img_size=(640, 640), is_train=True):
    """
    Returns DiseaseCOCODataset instance with appropriate preproc transform.
    """
    json_file = f"instances_{split}.json"
    if is_train:
        # Conservative augmentations preserving lesion shape/texture
        preproc = TrainTransform(
            max_labels=100,
            flip_prob=0.5,
            hsv_prob=0.5
        )
    else:
        preproc = ValTransform(legacy=False)
    
    return DiseaseCOCODataset(
        data_dir="data/processed/model2_yolox",
        json_file=json_file,
        name=split,
        img_size=img_size,
        preproc=preproc,
    )
