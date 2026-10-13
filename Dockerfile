# ==============================================================================
# Multi-Stage Monolith Dockerfile: Plant Disease AI (Render Free Plan)
# Bundles React 18 / Vite Frontend + FastAPI Backend in a Single Service
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build Frontend Assets
# ------------------------------------------------------------------------------
FROM node:20-slim AS frontend-builder
WORKDIR /build/frontend

# Install dependencies
COPY app/frontend/package*.json ./
RUN npm ci

# Build static bundle to dist/
COPY app/frontend/ ./
RUN npm run build

# ------------------------------------------------------------------------------
# Stage 2: Python Runtime Environment
# ------------------------------------------------------------------------------
FROM python:3.10-slim AS runtime

# Install system libraries needed by OpenCV headless & curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies using CPU-optimized PyTorch
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code, models, knowledge base, router, and audio/video modules
COPY app/ ./app/
COPY knowledge/ ./knowledge/
COPY router/ ./router/
COPY model1_test_app/ ./model1_test_app/
COPY models/ ./models/
COPY audio/ ./audio/
COPY video/ ./video/
RUN mkdir -p data/processed temp_multimodal_uploads

# Copy compiled frontend from Stage 1 into app/frontend/dist
COPY --from=frontend-builder /build/frontend/dist ./app/frontend/dist

# Environment settings for Render Free
ENV PYTHONUNBUFFERED=1 \
    PORT=10000 \
    EAGER_LOAD_MODELS=false \
    WHISPER_MODEL_SIZE=tiny \
    MODEL1_CHECKPOINT=models/model1_expanded/best_model.pth \
    MODEL1_CLASS_MAPPING=models/model1_expanded/class_mapping.json \
    MODEL1_CONFIG=models/model1_expanded/config.json \
    MODEL2_CHECKPOINT=models/model2_retraining_v2/best_model.pth \
    MODEL2_CLASS_MAPPING=models/model2_retraining_v2/class_mapping.json \
    MODEL2_CONFIG=models/model2_retraining_v2/config.json \
    CROP_DISEASE_MAPPING=models/model2_retraining_v2/crop_disease_mapping.json

EXPOSE 10000

# Start command
CMD ["sh", "-c", "uvicorn app.backend.main:app --host 0.0.0.0 --port ${PORT:-10000} --workers 1 --timeout-keep-alive 75"]
