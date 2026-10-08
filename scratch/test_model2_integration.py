import io
import json
import os
import requests
from PIL import Image

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    resp = requests.get(f"{BASE_URL}/api/health")
    print("Health Status:", resp.status_code, resp.json())

def test_image_inference():
    val_dir = "data/processed/model2_dataset/images/val"
    val_imgs = [os.path.join(val_dir, f) for f in os.listdir(val_dir) if f.endswith(".jpg")]
    if not val_imgs:
        print("No validation images found.")
        return
    
    img_path = val_imgs[0]
    print(f"\nTesting image inference with: {img_path}")
    with open(img_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/api/chat",
            data={"text": "Diagnose this plant and detect any disease"},
            files={"image_file": ("test.jpg", f, "image/jpeg")},
        )
    print("Status Code:", resp.status_code)
    data = resp.json()
    print("Assistant Message:", data.get("message"))
    print("\nModel 1 Data:", json.dumps(data.get("model1"), indent=2))
    print("\nModel 2 Data (Detections Count):", len(data.get("model2", {}).get("detections", [])))
    print("Model 2 Summary:", json.dumps({k: v for k, v in data.get("model2", {}).items() if k != "annotated_preview_url"}, indent=2))
    if data.get("annotated_preview_url"):
        print("Annotated Preview URL prefix:", data.get("annotated_preview_url")[:50], "...")

if __name__ == "__main__":
    test_health()
    test_image_inference()
