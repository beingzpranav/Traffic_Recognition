"""
Image preprocessing — must be identical to training pipeline.
"""

import io
import numpy as np
import cv2
from PIL import Image
from fastapi import HTTPException


IMG_SIZE = 32


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """
    Convert raw image bytes → model-ready NumPy array.

    Pipeline
    --------
    bytes → PIL decode → RGB → 32×32 → float32 → /255 → (1,32,32,3)
    """
    try:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not decode image: {exc}",
        )

    # PIL → OpenCV (RGB uint8)
    img = np.array(pil_img, dtype=np.uint8)

    # Resize
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)

    # Normalize
    img = img.astype(np.float32) / 255.0

    # Add batch dimension → (1, 32, 32, 3)
    img = np.expand_dims(img, axis=0)

    return img
