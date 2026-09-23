# Traffic Sign Recognition using Deep CNN

An end-to-end AI application that classifies traffic signs using a Convolutional Neural Network trained on the **GTSRB** (German Traffic Sign Recognition Benchmark) dataset. The project includes a high-performance FastAPI backend, a trained Keras CNN model, a modern React + TypeScript + Tailwind CSS frontend, and ready-to-use deployment configurations for **Render**, **Hugging Face Spaces**, and **Vercel**.

---

## Features

- 🧠 **43-class CNN classifier** trained on the GTSRB dataset with data augmentation and dropout regularization.
- 📤 **Interactive Image Upload** — drag-and-drop or file browser with instant preview.
- 📊 **Real-time Confidence Metrics** — top-3 predictions with animated confidence bars.
- ⚡ **FastAPI REST Backend** — `/predict` and `/health` endpoints with full CORS support.
- ⚛️ **Modern React Frontend** — built with Vite, TypeScript, and Tailwind CSS.
- 🚀 **Cloud Deployment Ready**:
  - Backend: One-click blueprint for **Render** (`render.yaml`), Docker container support, and **Hugging Face Spaces** (`app.py`).
  - Keep-Alive Cron: Built-in GitHub Actions workflow and cron-job setup to prevent free-tier spin-down.
  - Frontend: Pre-configured for **Vercel** with SPA rewrites (`vercel.json`).

---

## Project Structure

```
traffic-sign-recognition/
│
├── frontend/                        ← React + TypeScript + Vite + Tailwind
│   ├── src/
│   │   ├── api/predict.ts           ← API client for backend communication
│   │   ├── components/              ← Modular UI components (Hero, Uploader, Result, etc.)
│   │   ├── types/index.ts           ← TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── .env.example                 ← Example environment variables
│   ├── .env.production              ← Production environment configuration
│   ├── package.json
│   ├── vercel.json                  ← SPA routing rewrite rules for Vercel
│   └── vite.config.ts
│
├── backend/                         ← FastAPI application
│   ├── main.py                      ← REST API endpoints (/predict, /health) with CORS
│   ├── model_loader.py              ← Thread-safe singleton model loader
│   ├── preprocessing.py             ← Image resizing & normalization pipeline
│   ├── class_names.py               ← GTSRB 43 class label mappings
│   └── requirements.txt             ← Python dependencies for backend
│
├── ml/                              ← Model training & evaluation scripts
│   ├── train.py                     ← CNN training pipeline with callbacks & augmentation
│   ├── evaluate.py                  ← Confusion matrix & classification report generator
│   └── indian_label_map.json        ← Extended label mappings
│
├── models/
│   └── traffic_sign_cnn.keras       ← Trained Keras CNN model file
│
├── .github/workflows/
│   ├── deploy-check.yml             ← Automated deployment checks
│   └── keep-alive.yml               ← Periodic cron workflow to prevent Render spin-down
│
├── app.py                           ← Entry point for Hugging Face Spaces (Gradio + FastAPI)
├── Dockerfile                       ← Container definition for Docker-based deployments
├── render.yaml                      ← Render Infrastructure-as-Code blueprint
├── requirements.txt                 ← Root dependencies for cloud platform auto-detect
└── README.md
```

---

## Model Architecture

```
Input: 32 × 32 × 3 (RGB Image)

Conv2D(32, 3×3) → BatchNorm → Conv2D(32, 3×3) → MaxPool(2×2) → Dropout(0.25)
Conv2D(64, 3×3) → BatchNorm → Conv2D(64, 3×3) → MaxPool(2×2) → Dropout(0.25)
Conv2D(128, 3×3) → BatchNorm → Conv2D(128, 3×3) → MaxPool(2×2) → Dropout(0.25)

Flatten
Dense(512, ReLU) → BatchNorm → Dropout(0.5)
Dense(43, Softmax)
```

- **Optimizer**: Adam (`learning_rate=1e-3` with `ReduceLROnPlateau`)
- **Loss**: Sparse Categorical Cross-Entropy
- **Data Augmentation**: Rotation (±10°), Zoom (±10%), Width/Height shifts (±10%), Brightness adjustments (±20%)
- **Regularization**: Batch Normalization after every block + Dropout layers to prevent overfitting

---

## Local Development Setup

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Node.js 18+ & npm

### 1. Clone the Repository
```bash
git clone https://github.com/beingzpranav/Traffic_Recognition.git
cd Traffic_Recognition
```

### 2. Backend Setup
```bash
# Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000`. You can test the interactive API documentation at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd frontend
npm install

# Start Vite dev server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## Cloud Deployment Guide

### A. Deploy Backend on Render (Recommended)

1. Sign up / Log in to [Render](https://render.com) with GitHub.
2. Click **New +** → **Web Service**.
3. Connect your repository: `beingzpranav/Traffic_Recognition`.
4. Configure the service:
   - **Environment / Runtime**: `Python 3`
   - **Branch**: `main`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`
5. Under **Environment Variables**, add:
   - `ALLOWED_ORIGINS` = `*`
   - `PYTHON_VERSION` = `3.11.9`
6. Click **Deploy Web Service**. Render will generate your backend URL (e.g., `https://traffic-sign-api-xxxx.onrender.com`).

#### ⚡ Prevent Free-Tier Spin-Down (4-Minute Keep-Alive Cron)
Render free instances go to sleep after 15 minutes of inactivity. Set up a free external ping:

- **Option 1: Using [cron-job.org](https://cron-job.org) (Recommended)**
  1. Create a free account on [cron-job.org](https://cron-job.org).
  2. Create a new cron job with:
     - **URL**: `https://<YOUR-RENDER-URL>.onrender.com/health`
     - **Schedule**: Every `4` minutes
  3. Save. Your service will now remain awake 24/7.

- **Option 2: Using GitHub Actions**
  1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** → **Variables**.
  2. Add variable `RENDER_SERVICE_URL` with value `https://<YOUR-RENDER-URL>.onrender.com`.
  3. The [.github/workflows/keep-alive.yml](.github/workflows/keep-alive.yml) workflow will periodically ping the server.

---

### B. Deploy Frontend on Vercel

1. Log in to [Vercel](https://vercel.com) and click **Add New...** → **Project**.
2. Import `beingzpranav/Traffic_Recognition`.
3. Configure the deployment:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend` *(Important: click Edit and select `frontend`)*
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add Environment Variable:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://<YOUR-BACKEND-URL>.onrender.com` (or your Hugging Face Space URL)

> **Note on Vercel's Public Prefix Warning**:
> When adding `VITE_API_URL`, Vercel may display:
> *"Remove the public framework prefix to keep this value private. Public prefixes expose values to the browser."*
> **This is completely normal and expected.** Vite requires client-side environment variables to start with `VITE_` so the browser application can read them to know which API server to call. Since this is your public API URL and contains no secret keys, it is 100% safe to leave as `VITE_API_URL`.

5. Click **Deploy**. Vercel will build and provide your production frontend link.

---

### C. Deploy Backend on Hugging Face Spaces (Alternative)

This repository includes a Gradio SDK wrapper in [app.py](app.py):
1. Create a new Space on [Hugging Face](https://huggingface.co/new-space).
2. Set Space SDK to **Gradio**, Hardware to **CPU Basic** (Free).
3. The Space will run `app.py`, which provides both an interactive web GUI and exposes `/health` and `/predict` endpoints for your Vercel frontend.

---

## API Reference

### Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### Predict Traffic Sign
```http
POST /predict
Content-Type: multipart/form-data
```
**Request Body**:
- `file`: Image file (PNG, JPG, JPEG, WEBP, up to 10 MB)

**Response:**
```json
{
  "prediction": {
    "class_id": 14,
    "name": "Stop",
    "confidence": 98.45
  },
  "top_predictions": [
    { "class_id": 14, "name": "Stop", "confidence": 98.45 },
    { "class_id": 17, "name": "No Entry", "confidence": 1.12 },
    { "class_id": 13, "name": "Yield", "confidence": 0.31 }
  ]
}
```

---

## Dataset & Model Classes

Trained on the **German Traffic Sign Recognition Benchmark (GTSRB)** comprising 43 classes including:
- Speed Limits (20, 30, 50, 60, 70, 80, 100, 120 km/h)
- Regulatory Signs (Stop, Yield, No Entry, Priority Road, Keep Right)
- Warning Signs (General Caution, Pedestrians, Children Crossing, Slippery Road)
- Full list of all 43 classes available in [`backend/class_names.py`](backend/class_names.py).

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
