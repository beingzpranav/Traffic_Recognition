FROM python:3.11-slim

# Install system dependencies needed for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code, model, and Gradio entry point
COPY backend/ ./backend/
COPY models/ ./models/
COPY app.py .

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Run via the Gradio wrapper (starts uvicorn on port 7860)
CMD ["python", "app.py"]
