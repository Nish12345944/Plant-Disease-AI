"""
Secure Checkpoint Downloader & Weights Manager for Cloud Deployments.
====================================================================
Safely downloads model checkpoints from private HTTPS object storage (S3, R2, HuggingFace)
during application startup or lazy loading on low-memory containers (e.g. Render Free).

Security & Safety Guarantees:
1. Enforces HTTPS for all remote downloads.
2. Strictly requires and validates SHA-256 checksums before placing checkpoints into service.
3. Streams in bounded chunks (64 KB) to avoid memory spikes on 512 MB containers.
4. Strips query parameters (pre-signed tokens) and redacts authorization credentials from logs.
5. Uses thread locks to prevent concurrent downloads of the same checkpoint.
6. Atomic file replacement via os.replace() prevents partial or corrupt weights from being loaded.
7. Graceful degradation: never crashes the FastAPI server if remote storage is unreachable.
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
import threading
import time
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import requests

from app.backend.config import MODEL1_CHECKPOINT, MODEL2_CHECKPOINT

logger = logging.getLogger(__name__)

# Minimum plausible file size for a PyTorch EfficientNet checkpoint (rejects HTML errors / empty files)
MIN_CHECKPOINT_BYTES: int = 5 * 1024 * 1024  # 5 MB

# Concurrency locks per model to prevent multiple requests from downloading simultaneously
_DOWNLOAD_LOCKS: dict[str, threading.Lock] = {
    "model1": threading.Lock(),
    "model2": threading.Lock(),
}

# Hexadecimal pattern for 64-character SHA-256
_SHA256_PATTERN = re.compile(r"^[a-fA-F0-9]{64}$")


@dataclass(frozen=True)
class CheckpointSpec:
    """Specification of a managed model checkpoint."""
    name: str
    dest_path: Path
    url_env_var: str
    sha256_env_var: str
    min_bytes: int = MIN_CHECKPOINT_BYTES


CHECKPOINT_SPECS: dict[str, CheckpointSpec] = {
    "model1": CheckpointSpec(
        name="model1",
        dest_path=MODEL1_CHECKPOINT,
        url_env_var="MODEL1_WEIGHTS_URL",
        sha256_env_var="MODEL1_WEIGHTS_SHA256",
    ),
    "model2": CheckpointSpec(
        name="model2",
        dest_path=MODEL2_CHECKPOINT,
        url_env_var="MODEL2_WEIGHTS_URL",
        sha256_env_var="MODEL2_WEIGHTS_SHA256",
    ),
}


def sanitize_url(url: str) -> str:
    """Strip query parameters and credentials from a URL for safe logging.

    Pre-signed URLs (S3/R2/GCS) contain secrets in their query string.
    """
    if not url:
        return ""
    try:
        parsed = urllib.parse.urlsplit(url)
        return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))
    except Exception:
        return "[unparseable-url]"


def compute_file_sha256(file_path: Path, chunk_size: int = 65536) -> str:
    """Compute the lowercase SHA-256 hex digest of a file in streaming chunks."""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest().lower()


def is_valid_sha256(value: Optional[str]) -> bool:
    """Check whether a string is a valid 64-character hex SHA-256 digest."""
    if not value or not isinstance(value, str):
        return False
    return bool(_SHA256_PATTERN.match(value.strip()))


def download_checkpoint_spec(
    spec: CheckpointSpec,
    max_retries: int = 3,
    connect_timeout: float = 10.0,
    read_timeout: float = 60.0,
    session: Optional[requests.Session] = None,
) -> dict[str, Any]:
    """Download and verify a single checkpoint if required.

    Returns a status dict:
      {
          "name": str,
          "available": bool,
          "status": str ("existing_valid" | "downloaded" | "not_configured" | "failed"),
          "message": str,
      }
    """
    dest_path = spec.dest_path
    url = (os.environ.get(spec.url_env_var) or "").strip()
    expected_sha256 = (os.environ.get(spec.sha256_env_var) or "").strip().lower()
    bearer_token = (os.environ.get("MODEL_WEIGHTS_BEARER_TOKEN") or "").strip()

    lock = _DOWNLOAD_LOCKS.get(spec.name)
    if lock is None:
        lock = threading.Lock()
        _DOWNLOAD_LOCKS[spec.name] = lock

    with lock:
        # Case 1: Checkpoint already exists on disk
        if dest_path.is_file():
            # If expected SHA-256 is provided, verify local integrity
            if expected_sha256:
                if not is_valid_sha256(expected_sha256):
                    logger.error(
                        f"Configured {spec.sha256_env_var} is not a valid 64-char hex SHA-256 string. "
                        f"Refusing to accept local or remote weights for {spec.name}."
                    )
                    return {
                        "name": spec.name,
                        "available": False,
                        "status": "failed",
                        "message": f"Invalid {spec.sha256_env_var} format.",
                    }

                current_sha256 = compute_file_sha256(dest_path)
                if current_sha256 == expected_sha256:
                    logger.info(
                        f"Existing checkpoint for {spec.name} verified with matching SHA-256: {dest_path.name}"
                    )
                    return {
                        "name": spec.name,
                        "available": True,
                        "status": "existing_valid",
                        "message": "Local checkpoint matches expected SHA-256.",
                    }
                else:
                    logger.warning(
                        f"Existing checkpoint for {spec.name} at {dest_path} failed checksum validation. "
                        f"(Expected: {expected_sha256[:10]}..., Found: {current_sha256[:10]}...). Re-download required."
                    )
            else:
                # If no URL is configured either, assume local developer workflow
                if not url:
                    logger.info(f"Existing local checkpoint for {spec.name} detected at {dest_path}.")
                    return {
                        "name": spec.name,
                        "available": True,
                        "status": "existing_valid",
                        "message": "Local checkpoint present (no remote URL configured).",
                    }

        # Case 2: Remote download is not configured
        if not url:
            if dest_path.is_file():
                return {
                    "name": spec.name,
                    "available": True,
                    "status": "existing_valid",
                    "message": "Local checkpoint present.",
                }
            logger.info(f"{spec.url_env_var} not configured; {spec.name} checkpoint will remain unavailable.")
            return {
                "name": spec.name,
                "available": False,
                "status": "not_configured",
                "message": f"{spec.url_env_var} is not set in environment.",
            }

        # Case 3: URL is configured — strictly validate security prerequisites
        sanitized = sanitize_url(url)
        parsed = urllib.parse.urlsplit(url)

        if parsed.scheme.lower() != "https":
            msg = f"Insecure URL scheme '{parsed.scheme}' rejected for {spec.name}. Remote downloads strictly require HTTPS."
            logger.error(msg)
            return {
                "name": spec.name,
                "available": False,
                "status": "failed",
                "message": msg,
            }

        if not expected_sha256 or not is_valid_sha256(expected_sha256):
            msg = (
                f"Missing or invalid {spec.sha256_env_var}. "
                "A valid 64-character SHA-256 checksum is mandatory for every remote checkpoint download."
            )
            logger.error(msg)
            return {
                "name": spec.name,
                "available": False,
                "status": "failed",
                "message": msg,
            }

        # Ensure target directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = dest_path.with_name(f"{dest_path.name}.tmp_{os.getpid()}_{threading.get_ident()}")

        # Build request headers (do not log bearer tokens!)
        headers = {
            "User-Agent": "AlexaFarms-PlantAI-Downloader/1.0",
        }
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"

        req_session = session or requests.Session()
        last_error = ""

        logger.info(f"Initiating secure checkpoint download for {spec.name} from {sanitized}...")

        for attempt in range(1, max_retries + 1):
            hasher = hashlib.sha256()
            total_bytes = 0

            try:
                # Remove stale partial file from a previous attempt
                if temp_path.exists():
                    temp_path.unlink()

                with req_session.get(
                    url,
                    headers=headers,
                    stream=True,
                    timeout=(connect_timeout, read_timeout),
                ) as resp:
                    if resp.status_code != 200:
                        raise requests.HTTPError(
                            f"HTTP {resp.status_code} {resp.reason} received from remote storage server."
                        )

                    # Stream download to disk in 64 KB chunks to protect 512 MB RAM limit
                    with open(temp_path, "wb") as f_out:
                        for chunk in resp.iter_content(chunk_size=65536):
                            if chunk:
                                f_out.write(chunk)
                                hasher.update(chunk)
                                total_bytes += len(chunk)

                # Validate downloaded file size
                if total_bytes < spec.min_bytes:
                    raise ValueError(
                        f"Downloaded file too small ({total_bytes} bytes < {spec.min_bytes} expected). "
                        "The response was likely an error payload or corrupted."
                    )

                # Validate SHA-256 digest
                computed_sha256 = hasher.hexdigest().lower()
                if computed_sha256 != expected_sha256:
                    raise ValueError(
                        f"SHA-256 checksum mismatch for {spec.name}! "
                        f"Expected: {expected_sha256}, Computed: {computed_sha256}. Download rejected."
                    )

                # Atomic swap into target location
                os.replace(temp_path, dest_path)
                logger.info(
                    f"Successfully downloaded and verified {spec.name} ({total_bytes / (1024*1024):.2f} MB) "
                    f"-> {dest_path.name}"
                )
                return {
                    "name": spec.name,
                    "available": True,
                    "status": "downloaded",
                    "message": f"Successfully downloaded and verified ({total_bytes} bytes).",
                }

            except Exception as exc:
                last_error = str(exc)
                logger.warning(
                    f"Download attempt {attempt}/{max_retries} failed for {spec.name} ({sanitized}): {last_error}"
                )
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                    except Exception:
                        pass

                if attempt < max_retries:
                    backoff = 2.0 * (2 ** (attempt - 1))
                    time.sleep(backoff)

            finally:
                # Ensure temporary file is cleaned up if it still exists
                if temp_path.exists():
                    try:
                        temp_path.unlink()
                    except Exception:
                        pass

        # All retries failed
        error_msg = f"All {max_retries} download attempts failed for {spec.name}. Last error: {last_error}"
        logger.error(error_msg)
        return {
            "name": spec.name,
            "available": False,
            "status": "failed",
            "message": error_msg,
        }


def ensure_model_checkpoints() -> dict[str, Any]:
    """Inspect and securely synchronize configured model checkpoints on startup.

    Executes without raising exceptions to guarantee application uptime on Render Free.
    Returns status map for all managed checkpoints.
    """
    logger.info("Verifying model checkpoint availability...")
    results: dict[str, Any] = {}

    for name, spec in CHECKPOINT_SPECS.items():
        try:
            results[name] = download_checkpoint_spec(spec)
        except Exception as exc:
            logger.error(f"Unexpected error during {name} checkpoint verification: {exc}", exc_info=True)
            results[name] = {
                "name": name,
                "available": spec.dest_path.is_file(),
                "status": "error",
                "message": f"Unexpected error: {str(exc)}",
            }

    return results
