import torch

print("CUDA available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("GPU memory allocated:",
          torch.cuda.memory_allocated(0) / 1024**3, "GB")
    print("GPU memory reserved:",
          torch.cuda.memory_reserved(0) / 1024**3, "GB")
