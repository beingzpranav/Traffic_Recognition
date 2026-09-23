"""
Singleton model loader — loads the CNN once and caches it.
"""

import os
import threading
import tensorflow as tf
from fastapi import HTTPException

# Path to saved model (relative to project root, two levels up from this file)
_HERE    = os.path.dirname(os.path.abspath(__file__))
_ROOT    = os.path.dirname(_HERE)
MODEL_PATH = os.path.join(_ROOT, "models", "traffic_sign_cnn.keras")

_model = None
_lock  = threading.Lock()


def get_model() -> tf.keras.Model:
    """Return the cached model, loading it on first call."""
    global _model

    if _model is not None:
        return _model

    with _lock:
        if _model is not None:        # double-checked locking
            return _model

        if not os.path.exists(MODEL_PATH):
            raise HTTPException(
                status_code=503,
                detail=(
                    "Model file not found. "
                    "Please run  python ml/train.py  to train and save the model first."
                ),
            )

        try:
            _model = tf.keras.models.load_model(MODEL_PATH)
            print(f"[model_loader] Model loaded from: {MODEL_PATH}")
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to load model: {exc}",
            )

    return _model


def is_model_ready() -> bool:
    """Returns True if the model file exists."""
    return os.path.exists(MODEL_PATH)
