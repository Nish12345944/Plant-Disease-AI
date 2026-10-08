from flask import Flask, request, render_template_string
from PIL import Image
import io
import json
import base64
from pathlib import Path

import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models import efficientnet_b2

app = Flask(__name__)

# ============================================================
# LOAD MODEL 1 (EFFICIENTNET-B2)
# ============================================================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = Path("models/model1/best_model.pth")
CLASS_NAMES_PATH = Path("models/model1/class_names.json")

with open(CLASS_NAMES_PATH, encoding="utf-8") as f:
    CLASSES = json.load(f)["classes"]

model = efficientnet_b2(weights=None)
in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, len(CLASSES))

checkpoint = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
model.load_state_dict(checkpoint["model_state_dict"])
model = model.to(DEVICE)
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    ),
])

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Plant Model Tester</title>
    <style>
        body {
            font-family: Arial;
            text-align: center;
            margin-top: 80px;
        }

        .box {
            width: 500px;
            margin: auto;
            padding: 40px;
            border: 1px solid #ddd;
            border-radius: 15px;
        }

        img {
            max-width: 400px;
            max-height: 400px;
            margin: 20px;
        }

        button {
            padding: 12px 25px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>🌱 Plant Model Tester</h1>

    <form method="POST" enctype="multipart/form-data">

        <input type="file"
               name="image"
               accept="image/*, .webp, .wps, .png, .jpg, .jpeg, image/webp"
               required>

        <br><br>

        <button type="submit">Predict</button>

    </form>

    {% if error %}
        <p style="color: #e53e3e; font-weight: bold; margin-top: 15px;">{{ error }}</p>
    {% endif %}

    {% if image %}
        <img src="data:image/jpeg;base64,{{ image }}">
    {% endif %}

    {% if prediction %}
        <h2>Prediction: {{ prediction }}</h2>
        <h3>Confidence: {{ confidence }}%</h3>
    {% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    image_data = None
    prediction = None
    confidence = None
    error = None

    if request.method == "POST":

        if "image" not in request.files or not request.files["image"].filename:
            return render_template_string(HTML)

        file = request.files["image"]

        try:
            image = Image.open(file.stream if hasattr(file, "stream") else file)
            if getattr(image, "is_animated", False):
                image.seek(0)
            image = image.convert("RGB")

            # Model prediction
            tensor = transform(image).unsqueeze(0).to(DEVICE)
            with torch.no_grad():
                outputs = model(tensor)
                probs = torch.softmax(outputs, dim=1)[0]
                top_prob, top_idx = torch.max(probs, dim=0)

            predicted_class = CLASSES[top_idx.item()]
            prediction = predicted_class.replace("_", " ").title()
            confidence = f"{top_prob.item() * 100:.2f}"

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")

            image_data = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

        except Exception as e:
            error = f"Error processing image: {e}"

    return render_template_string(
        HTML,
        image=image_data,
        prediction=prediction,
        confidence=confidence,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )