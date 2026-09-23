# Indian Traffic Sign Recognition using Deep CNN

An end-to-end AI application that classifies Indian traffic signs using a Convolutional Neural Network trained on the **85-class Indian Traffic Sign Classification** dataset (`kannanwisen/Indian-Traffic-Sign-Classification`). The project features a FastAPI backend, a trained Keras CNN model (85 output classes), an interactive React + TypeScript + Tailwind CSS frontend, and deployment configurations for **Render**, **Hugging Face Spaces**, and **Vercel**.

---

## Features

- 🧠 **85-Class Deep CNN Classifier** trained on real-world Indian traffic sign categories with data augmentation and dropout regularization.
- 📤 **Interactive Image Upload** — drag-and-drop or file browser with instant preview.
- 📊 **Real-time Confidence Metrics** — top-3 predictions with class names and animated confidence bars.
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
│   │   ├── components/              ← Modular UI components (Hero, Uploader, ModelInfo, etc.)
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
│   ├── class_names.py               ← 85 Indian Traffic Sign class label mappings
│   └── requirements.txt             ← Python dependencies for backend (tensorflow-cpu)
│
├── ml/                              ← Model training & evaluation scripts
│   ├── train.py                     ← CNN training pipeline on Indian dataset (85 classes)
│   ├── evaluate.py                  ← Confusion matrix & classification report generator
│   └── indian_label_map.json        ← Extended Indian label mappings
│
├── models/
│   └── traffic_sign_cnn.keras       ← Trained Keras CNN model file (85 classes)
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

## Dataset

**Indian Traffic Sign Classification Dataset**
- **Source**: [kannanwisen/Indian-Traffic-Sign-Classification](https://huggingface.co/datasets/kannanwisen/Indian-Traffic-Sign-Classification)
- **Classes**: 85 distinct Indian traffic and road sign categories.
- **Content**: Real-world photographs of mandatory, cautionary, and informatory signs found on Indian roads under diverse lighting, angle, and weather conditions.

---

## Model Architecture

```
Input: 32 × 32 × 3 (RGB Image)

Conv2D(32, 3×3) → BatchNorm → Conv2D(32, 3×3) → MaxPool(2×2) → Dropout(0.25)
Conv2D(64, 3×3) → BatchNorm → Conv2D(64, 3×3) → MaxPool(2×2) → Dropout(0.25)
Conv2D(128, 3×3) → BatchNorm → Conv2D(128, 3×3) → MaxPool(2×2) → Dropout(0.25)

Flatten
Dense(512, ReLU) → BatchNorm → Dropout(0.5)
Dense(85, Softmax)
```

- **Output Layer**: 85 units with Softmax activation corresponding to each Indian traffic sign class.
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
Backend will be live at `http://localhost:8000`. Test interactive API documentation at `http://localhost:8000/docs`.

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
Render free instances go to sleep after 15 minutes of inactivity. Set up an external ping:

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
    "class_id": 74,
    "name": "Stop",
    "confidence": 98.45
  },
  "top_predictions": [
    { "class_id": 74, "name": "Stop", "confidence": 98.45 },
    { "class_id": 42, "name": "No Entry", "confidence": 1.12 },
    { "class_id": 26, "name": "Give Way", "confidence": 0.31 }
  ]
}
```

---

## 85 Indian Traffic Sign Classes

<details>
<summary>Click to expand all 85 classes</summary>

| ID | Class Name | ID | Class Name |
|---|---|---|---|
| 0 | All Motor Vehicles Prohibited | 43 | No Parking |
| 1 | Axle Load Limit | 44 | No Stopping or Standing |
| 2 | Barrier Ahead | 45 | Overtaking Prohibited |
| 3 | Bullock and Handcart Prohibited | 46 | Pass Either Side |
| 4 | Bullock Prohibited | 47 | Pedestrian Crossing |
| 5 | Cattle | 48 | Pedestrian Prohibited |
| 6 | Compulsory Ahead | 49 | Priority for Oncoming Vehicles |
| 7 | Compulsory Ahead or Turn Left | 50 | Quay Side or River Bank |
| 8 | Compulsory Ahead or Turn Right | 51 | Restriction Ends |
| 9 | Compulsory Cycle Track | 52 | Right Hair Pin Bend |
| 10 | Compulsory Keep Left | 53 | Right Hand Curve |
| 11 | Compulsory Keep Right | 54 | Right Reverse Bend |
| 12 | Compulsory Minimum Speed | 55 | Right Turn Prohibited |
| 13 | Compulsory Sound Horn | 56 | Road Widens Ahead |
| 14 | Compulsory Turn Left | 57 | Roundabout |
| 15 | Compulsory Turn Left Ahead | 58 | School Ahead |
| 16 | Compulsory Turn Right | 59 | Side Road Left |
| 17 | Compulsory Turn Right Ahead | 60 | Side Road Right |
| 18 | Cross Road | 61 | Slippery Road |
| 19 | Cycle Crossing | 62 | Speed Limit 15 |
| 20 | Cycle Prohibited | 63 | Speed Limit 20 |
| 21 | Dangerous Dip | 64 | Speed Limit 30 |
| 22 | Direction | 65 | Speed Limit 40 |
| 23 | Falling Rocks | 66 | Speed Limit 5 |
| 24 | Ferry | 67 | Speed Limit 50 |
| 25 | Gap in Median | 68 | Speed Limit 60 |
| 26 | Give Way | 69 | Speed Limit 70 |
| 27 | Guarded Level Crossing | 70 | Speed Limit 80 |
| 28 | Handcart Prohibited | 71 | Staggered Intersection |
| 29 | Height Limit | 72 | Steep Ascent |
| 30 | Horn Prohibited | 73 | Steep Descent |
| 31 | Hump or Rough Road | 74 | Stop |
| 32 | Left Hair Pin Bend | 75 | Straight Prohibited |
| 33 | Left Hand Curve | 76 | Tonga Prohibited |
| 34 | Left Reverse Bend | 77 | Traffic Signal |
| 35 | Left Turn Prohibited | 78 | Truck Prohibited |
| 36 | Length Limit | 79 | Turn Right |
| 37 | Load Limit | 80 | T Intersection |
| 38 | Loose Gravel | 81 | Unguarded Level Crossing |
| 39 | Men at Work | 82 | U-Turn Prohibited |
| 40 | Narrow Bridge | 83 | Width Limit |
| 41 | Narrow Road Ahead | 84 | Y Intersection |
| 42 | No Entry | | |

Full mapping defined in [`backend/class_names.py`](backend/class_names.py).
</details>

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
