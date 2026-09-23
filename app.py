"""
HuggingFace Spaces entry point — Gradio SDK (Free CPU Tier).

Provides:
1. An interactive Gradio web UI at "/" for direct testing.
2. Custom REST API endpoints:
   - GET  /health   -> Health check
   - POST /predict  -> Predict endpoint used by the React / Vercel frontend
3. Full CORS support for cross-origin requests from Vercel / localhost.
"""

import io
import os
import numpy as np
from PIL import Image
import gradio as gr
from fastapi import File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.class_names import CLASS_NAMES
from backend.preprocessing import preprocess_image
from backend.model_loader import get_model, is_model_ready

# ── Accepted MIME types ──────────────────────────────────────────────────────
ALLOWED_CONTENT_TYPES = {
    "image/jpeg", "image/jpg", "image/png",
    "image/webp", "image/bmp", "image/ppm",
}


def predict_from_bytes(image_bytes: bytes):
    """Shared prediction logic for both Gradio UI and REST API."""
    if len(image_bytes) == 0:
        raise ValueError("Uploaded file is empty.")
    if len(image_bytes) > 10 * 1024 * 1024:
        raise ValueError("File too large. Maximum size is 10 MB.")

    img_array = preprocess_image(image_bytes)
    model = get_model()
    probabilities = model.predict(img_array, verbose=0)[0]
    top3_indices = np.argsort(probabilities)[::-1][:3]

    top_predictions = [
        {
            "class_id": int(idx),
            "name": CLASS_NAMES[int(idx)],
            "confidence": round(float(probabilities[idx]) * 100, 4),
        }
        for idx in top3_indices
    ]
    return top_predictions


def gradio_classify(image):
    """Callback for the interactive Gradio UI."""
    if image is None:
        return {}
    try:
        if isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image)
        else:
            pil_img = image

        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        top3 = predict_from_bytes(buf.getvalue())

        # Return dict format for gr.Label
        return {item["name"]: item["confidence"] / 100.0 for item in top3}
    except Exception as exc:
        return {f"Error: {exc}": 0.0}


# ── Define Gradio Interface ─────────────────────────────────────────────────
with gr.Blocks(title="Traffic Sign Recognition API") as demo:
    gr.Markdown(
        """
        # 🚦 Traffic Sign Recognition API & Demo
        Upload a traffic sign image below to test model inference directly,
        or connect your frontend to the REST API endpoints.

        ### REST API Endpoints:
        - `GET  /health`  — Service health check
        - `POST /predict` — Multipart image upload (`file`)
        """
    )
    with gr.Row():
        with gr.Column():
            img_input = gr.Image(type="pil", label="Upload Traffic Sign")
            btn = gr.Button("Classify Traffic Sign", variant="primary")
        with gr.Column():
            label_output = gr.Label(num_top_classes=3, label="Predictions")

    btn.click(fn=gradio_classify, inputs=img_input, outputs=label_output)


# ── Add CORS Middleware to Gradio's internal FastAPI app ─────────────────────
demo.app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Register Custom FastAPI Endpoints BEFORE launching ──────────────────────
@demo.app.get("/health")
async def health():
    """Health-check endpoint for frontend and deployment probes."""
    return {
        "status": "ok",
        "model_loaded": is_model_ready(),
    }


@demo.app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """REST API prediction endpoint consumed by the React/Vercel frontend."""
    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded.")

    content_type = (file.content_type or "").lower().strip()
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{content_type}'. Please upload PNG, JPG, or WEBP.",
        )

    try:
        image_bytes = await file.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read uploaded file: {exc}")

    try:
        top_predictions = predict_from_bytes(image_bytes)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    return JSONResponse(
        content={
            "prediction": top_predictions[0],
            "top_predictions": top_predictions,
        }
    )


# ── Start the Application ────────────────────────────────────────────────────
try:
    # Disable SSR mode to prevent Node.js proxy crash on HuggingFace Spaces
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        ssr_mode=False,
    )
except TypeError:
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )

