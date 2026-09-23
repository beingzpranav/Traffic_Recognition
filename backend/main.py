"""
Traffic Sign Recognition — FastAPI Backend
============================================
Start:
    cd backend
    uvicorn main:app --reload --port 8000
"""

import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.class_names  import CLASS_NAMES
from backend.preprocessing import preprocess_image
from backend.model_loader  import get_model, is_model_ready

# ──────────────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────────────

import os

app = FastAPI(
    title="Indian Traffic Sign Recognition API",
    description="Deep CNN classifier trained on 85 Indian Traffic Sign categories.",
    version="1.0.0",
)

# CORS — allow origins from environment or default to allow all origins in deployment
raw_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "https://traffic-vision.vercel.app,http://localhost:5173,http://localhost:3000"
)
allowed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Accepted image MIME types
ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/bmp",
    "image/ppm",
}

# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Health-check endpoint."""
    return {
        "status": "ok",
        "model_loaded": is_model_ready(),
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Accept a traffic sign image and return top-3 predictions.

    Request
    -------
    POST /predict
    Content-Type: multipart/form-data
    Body: file=<image>

    Response
    --------
    {
      "prediction": {"class_id": int, "name": str, "confidence": float},
      "top_predictions": [{"class_id": int, "name": str, "confidence": float}, ...]
    }
    """

    # ── Validate ──────────────────────────────────────────────────────────────
    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded.")

    content_type = (file.content_type or "").lower().strip()
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{content_type}'. "
                   f"Please upload a PNG, JPG, JPEG, or WEBP image.",
        )

    # ── Read bytes ────────────────────────────────────────────────────────────
    try:
        image_bytes = await file.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {exc}")

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(image_bytes) > 10 * 1024 * 1024:   # 10 MB limit
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10 MB.")

    # ── Preprocess ────────────────────────────────────────────────────────────
    img_array = preprocess_image(image_bytes)   # → (1, 32, 32, 3)

    # ── Load model & predict ──────────────────────────────────────────────────
    model = get_model()

    try:
        probabilities = model.predict(img_array, verbose=0)[0]   # shape (43,)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    # ── Top-3 results ─────────────────────────────────────────────────────────
    top3_indices = np.argsort(probabilities)[::-1][:3]

    top_predictions = [
        {
            "class_id":   int(idx),
            "name":       CLASS_NAMES[int(idx)],
            "confidence": round(float(probabilities[idx]) * 100, 4),
        }
        for idx in top3_indices
    ]

    return JSONResponse(content={
        "prediction":      top_predictions[0],
        "top_predictions": top_predictions,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Exception handler — never expose tracebacks
# ──────────────────────────────────────────────────────────────────────────────

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again."},
    )
