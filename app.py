"""
HuggingFace Spaces entry point — Gradio SDK (free tier).

Mounts the existing FastAPI app at "/" so all API endpoints
(/health, /predict) work exactly as before. Gradio provides
the Spaces-compatible wrapper on port 7860.
"""

import gradio as gr
from backend.main import app as fastapi_app

# Minimal Gradio UI — just a status page
# The actual API is the mounted FastAPI app
demo = gr.Blocks()

with demo:
    gr.Markdown(
        """
        # 🚦 Traffic Sign Recognition API

        This Space hosts the **FastAPI backend** for traffic sign classification.

        ### API Endpoints
        - **`GET /health`** — Health check
        - **`POST /predict`** — Upload a traffic sign image for classification

        ### Frontend
        The web UI is deployed separately on Vercel.
        """
    )

# Mount the FastAPI app so /health and /predict work at the root
app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

# When Gradio launches via `python app.py`, it starts uvicorn on port 7860
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=7860)
