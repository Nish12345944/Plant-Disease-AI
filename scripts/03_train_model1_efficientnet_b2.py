from pathlib import Path
import copy
import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, WeightedRandomSampler
from torchvision import datasets, transforms
from torchvision.models import EfficientNet_B2_Weights, efficientnet_b2


# ============================================================
# PATHS
# ============================================================

ROOT = Path(
    r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
)

DATASET_DIR = (
    ROOT
    / "data"
    / "final"
    / "model1_39"
)

MODEL_DIR = ROOT / "models"

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_PATH = (
    MODEL_DIR
    / "model1_efficientnet_b2.pth"
)


# ============================================================
# SETTINGS
# ============================================================

SEED = 42

torch.manual_seed(SEED)

# CPU currently
DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("=" * 50)
print("Device:", DEVICE)

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA:", torch.version.cuda)

print("=" * 50)

IMAGE_SIZE = 224

# CPU-friendly
BATCH_SIZE = 16

# The cleaned dataset is much harder than the old leaky one
# (no near-duplicate leakage, no PlantVillage-flooded tomato,
# no mislabelled fruit photos), so the model needs more epochs
# to converge. Early stopping below will end the run as soon as
# validation accuracy stops improving.
EPOCHS = 20

LEARNING_RATE = 1e-4

WEIGHT_DECAY = 1e-4

# Windows + CPU
NUM_WORKERS = 0

# Stop if validation accuracy does not improve
PATIENCE = 5


# ============================================================
# START
# ============================================================

print()
print("=" * 80)
print("MODEL 1 - EFFICIENTNET-B2")
print("=" * 80)

print()
print(f"Device       : {DEVICE}")
print(f"Dataset      : {DATASET_DIR}")
print(f"Image size   : {IMAGE_SIZE}")
print(f"Batch size   : {BATCH_SIZE}")
print(f"Epochs       : {EPOCHS}")
print(f"Learning rate: {LEARNING_RATE}")


# ============================================================
# CHECK DATASET
# ============================================================

train_dir = DATASET_DIR / "train"
val_dir = DATASET_DIR / "val"
test_dir = DATASET_DIR / "test"

for directory in [
    train_dir,
    val_dir,
    test_dir
]:

    if not directory.exists():

        raise FileNotFoundError(
            f"Dataset directory not found:\n"
            f"{directory}\n\n"
            f"Run 02_build_model1_39.py first."
        )


# ============================================================
# TRANSFORMS
# ============================================================

weights = EfficientNet_B2_Weights.DEFAULT

imagenet_mean = [
    0.485,
    0.456,
    0.406
]

imagenet_std = [
    0.229,
    0.224,
    0.225
]


# Training augmentation
train_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.RandomHorizontalFlip(
        p=0.5
    ),

    transforms.RandomRotation(
        degrees=10
    ),

    transforms.ColorJitter(
        brightness=0.15,
        contrast=0.15,
        saturation=0.15,
        hue=0.03
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=imagenet_mean,
        std=imagenet_std
    )
])


# Validation/test:
# NO random augmentation
eval_transform = transforms.Compose([

    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=imagenet_mean,
        std=imagenet_std
    )
])


# ============================================================
# DATASETS
# ============================================================

print()
print("=" * 80)
print("LOADING DATA")
print("=" * 80)

train_dataset = datasets.ImageFolder(
    root=train_dir,
    transform=train_transform
)

val_dataset = datasets.ImageFolder(
    root=val_dir,
    transform=eval_transform
)

test_dataset = datasets.ImageFolder(
    root=test_dir,
    transform=eval_transform
)


# ============================================================
# CLASS INFORMATION
# ============================================================

class_names = train_dataset.classes

num_classes = len(
    class_names
)

print()
print(
    f"Number of classes: {num_classes}"
)

print()

for index, class_name in enumerate(
    class_names
):

    print(
        f"{index:2d} -> {class_name}"
    )


print()
print(
    f"Train images: {len(train_dataset)}"
)

print(
    f"Validation images: {len(val_dataset)}"
)

print(
    f"Test images: {len(test_dataset)}"
)


# ============================================================
# CHECK CLASS MAPPING
# ============================================================

if (
    train_dataset.class_to_idx
    != val_dataset.class_to_idx
):

    raise RuntimeError(
        "Train and validation class mappings differ."
    )

if (
    train_dataset.class_to_idx
    != test_dataset.class_to_idx
):

    raise RuntimeError(
        "Train and test class mappings differ."
    )


# ============================================================
# CLASS COUNTS
# ============================================================

class_counts = [
    0
    for _ in range(num_classes)
]

for _, label in train_dataset.samples:

    class_counts[label] += 1


print()
print("=" * 80)
print("TRAINING CLASS COUNTS")
print("=" * 80)

for index, count in enumerate(
    class_counts
):

    print(
        f"{class_names[index]:<20} "
        f"{count:>5}"
    )


# ============================================================
# WEIGHTED SAMPLER
# ============================================================

# More weight to classes with fewer images.
#
# This is especially useful because your current dataset
# is highly imbalanced.

class_weights = [
    1.0 / max(count, 1)
    for count in class_counts
]

sample_weights = [
    class_weights[label]
    for _, label in train_dataset.samples
]

sample_weights = torch.DoubleTensor(
    sample_weights
)

sampler = WeightedRandomSampler(

    weights=sample_weights,

    num_samples=len(
        sample_weights
    ),

    replacement=True
)


# ============================================================
# DATALOADERS
# ============================================================

train_loader = DataLoader(

    train_dataset,

    batch_size=BATCH_SIZE,

    sampler=sampler,

    num_workers=NUM_WORKERS,

    pin_memory=False
)


val_loader = DataLoader(

    val_dataset,

    batch_size=BATCH_SIZE,

    shuffle=False,

    num_workers=NUM_WORKERS,

    pin_memory=False
)


test_loader = DataLoader(

    test_dataset,

    batch_size=BATCH_SIZE,

    shuffle=False,

    num_workers=NUM_WORKERS,

    pin_memory=False
)


# ============================================================
# MODEL
# ============================================================

print()
print("=" * 80)
print("LOADING EFFICIENTNET-B2")
print("=" * 80)

print(
    "Loading ImageNet pretrained weights..."
)

model = efficientnet_b2(
    weights=weights
)


# Replace final classifier
in_features = (
    model.classifier[1].in_features
)

model.classifier[1] = nn.Linear(
    in_features,
    num_classes
)

model = model.to(
    DEVICE
)


print(
    f"Classifier output: "
    f"{num_classes} classes"
)


# ============================================================
# LOSS
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# OPTIMIZER
# ============================================================

optimizer = torch.optim.AdamW(

    model.parameters(),

    lr=LEARNING_RATE,

    weight_decay=WEIGHT_DECAY
)


# ============================================================
# LR SCHEDULER
# ============================================================

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(

    optimizer,

    mode="max",

    factor=0.5,

    patience=1
)


# ============================================================
# TRAIN ONE EPOCH
# ============================================================

def train_one_epoch():

    model.train()

    total_loss = 0.0

    correct = 0

    total = 0

    for images, labels in train_loader:

        images = images.to(
            DEVICE
        )

        labels = labels.to(
            DEVICE
        )

        optimizer.zero_grad(
            set_to_none=True
        )

        outputs = model(
            images
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        total_loss += (
            loss.item()
            * images.size(0)
        )

        predictions = outputs.argmax(
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    average_loss = (
        total_loss / total
    )

    accuracy = (
        correct / total
    )

    return average_loss, accuracy


# ============================================================
# EVALUATION
# ============================================================

def evaluate(loader):

    model.eval()

    total_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(
                DEVICE
            )

            labels = labels.to(
                DEVICE
            )

            outputs = model(
                images
            )

            loss = criterion(
                outputs,
                labels
            )

            total_loss += (
                loss.item()
                * images.size(0)
            )

            predictions = outputs.argmax(
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)

    average_loss = (
        total_loss / total
    )

    accuracy = (
        correct / total
    )

    return average_loss, accuracy


# ============================================================
# TRAINING
# ============================================================

print()
print("=" * 80)
print("STARTING TRAINING")
print("=" * 80)

best_val_accuracy = 0.0

best_epoch = 0

best_state = None

epochs_without_improvement = 0


for epoch in range(
    1,
    EPOCHS + 1
):

    start_time = time.time()

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    train_loss, train_accuracy = (
        train_one_epoch()
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    val_loss, val_accuracy = (
        evaluate(
            val_loader
        )
    )

    # --------------------------------------------------------
    # Scheduler
    # --------------------------------------------------------

    scheduler.step(
        val_accuracy
    )

    elapsed = (
        time.time()
        - start_time
    )

    current_lr = (
        optimizer.param_groups[0]["lr"]
    )

    # --------------------------------------------------------
    # Print
    # --------------------------------------------------------

    print()
    print(
        "-" * 80
    )

    print(
        f"Epoch {epoch}/{EPOCHS}"
    )

    print(
        f"Train Loss     : "
        f"{train_loss:.4f}"
    )

    print(
        f"Train Accuracy : "
        f"{train_accuracy * 100:.2f}%"
    )

    print(
        f"Val Loss       : "
        f"{val_loss:.4f}"
    )

    print(
        f"Val Accuracy   : "
        f"{val_accuracy * 100:.2f}%"
    )

    print(
        f"Learning Rate  : "
        f"{current_lr:.7f}"
    )

    print(
        f"Time           : "
        f"{elapsed:.1f}s"
    )

    # --------------------------------------------------------
    # Save best
    # --------------------------------------------------------

    if val_accuracy > best_val_accuracy:

        best_val_accuracy = (
            val_accuracy
        )

        best_epoch = epoch

        best_state = copy.deepcopy(
            model.state_dict()
        )

        torch.save(

            {
                "model_state_dict":
                    best_state,

                "class_names":
                    class_names,

                "class_to_idx":
                    train_dataset.class_to_idx,

                "num_classes":
                    num_classes,

                "architecture":
                    "efficientnet_b2",

                "image_size":
                    IMAGE_SIZE,

                "best_val_accuracy":
                    best_val_accuracy,

                "epoch":
                    best_epoch,
            },

            MODEL_PATH
        )

        print()
        print(
            ">>> BEST MODEL SAVED"
        )

        print(
            f">>> Validation Accuracy: "
            f"{best_val_accuracy * 100:.2f}%"
        )

        epochs_without_improvement = 0

    else:

        epochs_without_improvement += 1

        print(
            f">>> No improvement "
            f"({epochs_without_improvement}/"
            f"{PATIENCE})"
        )

    # --------------------------------------------------------
    # Early stopping
    # --------------------------------------------------------

    if (
        epochs_without_improvement
        >= PATIENCE
    ):

        print()
        print(
            "Early stopping triggered."
        )

        break


# ============================================================
# RESTORE BEST MODEL
# ============================================================

if best_state is not None:

    model.load_state_dict(
        best_state
    )


# ============================================================
# FINAL TEST
# ============================================================

print()
print("=" * 80)
print("FINAL TEST")
print("=" * 80)

test_loss, test_accuracy = (
    evaluate(
        test_loader
    )
)

print()
print(
    f"Test Loss     : "
    f"{test_loss:.4f}"
)

print(
    f"Test Accuracy : "
    f"{test_accuracy * 100:.2f}%"
)

print()
print(
    f"Best Val Acc  : "
    f"{best_val_accuracy * 100:.2f}%"
)

print(
    f"Best Epoch    : "
    f"{best_epoch}"
)


# ============================================================
# FINAL SAVE
# ============================================================

torch.save(

    {
        "model_state_dict":
            model.state_dict(),

        "class_names":
            class_names,

        "class_to_idx":
            train_dataset.class_to_idx,

        "num_classes":
            num_classes,

        "architecture":
            "efficientnet_b2",

        "image_size":
            IMAGE_SIZE,

        "test_accuracy":
            test_accuracy,

        "best_val_accuracy":
            best_val_accuracy,
    },

    MODEL_PATH
)


# ============================================================
# DONE
# ============================================================

print()
print("=" * 80)
print("TRAINING COMPLETE")
print("=" * 80)

print()
print(
    "Model saved to:"
)

print(
    MODEL_PATH
)

print()
print(
    "This is the current baseline Model 1."
)

print(
    "It will need retraining after adding "
    "the remaining 18 crop classes."
)