"""
Indian Traffic Sign CNN — Training Script
==========================================
Uses HuggingFace dataset: kannanwisen/Indian-Traffic-Sign-Classification
85 classes of Indian traffic signs.

Run (in WSL with tf_gpu activated):
    python ml/train_indian.py

Generates:
  models/traffic_sign_cnn.keras   ← replaces existing model
  results/training_history.json
  results/training_accuracy.png
  results/training_loss.png
"""

import os
import sys
import io
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import train_test_split

# ──────────────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────────────

IMG_SIZE    = 32
NUM_CLASSES = 85      # Indian Traffic Sign dataset
BATCH_SIZE  = 64
EPOCHS      = 80
VAL_SPLIT   = 0.20
SEED        = 42

MODEL_PATH   = os.path.join(ROOT, "models", "traffic_sign_cnn.keras")
RESULTS_DIR  = os.path.join(ROOT, "results")
HISTORY_PATH = os.path.join(RESULTS_DIR, "training_history.json")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────────────
# GPU setup
# ──────────────────────────────────────────────────────────────────────────────

def configure_gpu():
    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        print(f"GPUs detected: {[g.name for g in gpus]}")
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU memory growth enabled.")
    else:
        print("No GPU detected. Training on CPU (may be slow).")


# ──────────────────────────────────────────────────────────────────────────────
# Dataset loading from HuggingFace
# ──────────────────────────────────────────────────────────────────────────────

def load_indian_dataset():
    """
    Downloads the Indian Traffic Sign dataset ZIP from HuggingFace,
    extracts it, and loads images into numpy arrays.

    Set HF_TOKEN env variable for authenticated access:
        export HF_TOKEN=hf_your_token_here
    """
    print("Loading dataset: kannanwisen/Indian-Traffic-Sign-Classification")

    import io as _io
    import zipfile
    import PIL.Image
    from huggingface_hub import hf_hub_download

    token = os.environ.get("HF_TOKEN")
    cache_dir = os.path.join(ROOT, ".hf_cache")
    os.makedirs(cache_dir, exist_ok=True)

    # ── Download ZIP ───────────────────────────────────────────────────────────
    zip_cache = os.path.join(cache_dir, "indian_traffic_signs.zip")
    if not os.path.exists(zip_cache):
        print("Downloading ZIP from HuggingFace...")
        zip_path = hf_hub_download(
            repo_id="kannanwisen/Indian-Traffic-Sign-Classification",
            filename="Indian-Traffic-Sign-Classification.zip",
            repo_type="dataset",
            token=token,
            local_dir=cache_dir,
        )
        import shutil
        shutil.copy(zip_path, zip_cache)
        print(f"Downloaded to: {zip_cache}")
    else:
        print(f"Using cached ZIP: {zip_cache}")

    # ── Extract ZIP ───────────────────────────────────────────────────────────
    extract_dir = os.path.join(cache_dir, "extracted")
    if not os.path.exists(extract_dir):
        print("Extracting ZIP...")
        with zipfile.ZipFile(zip_cache, "r") as zf:
            zf.extractall(extract_dir)
        print(f"Extracted to: {extract_dir}")

    # ── Find train folder ──────────────────────────────────────────────────────
    # Structure: extracted/ → Dataset/ → train/ + test/
    extract_root = extract_dir
    # Navigate into single-child dirs until we find train/ or class folders
    while True:
        entries = [e for e in os.listdir(extract_root) if not e.startswith(".")]
        subdirs = [e for e in entries if os.path.isdir(os.path.join(extract_root, e))]
        if "train" in subdirs:
            train_root = os.path.join(extract_root, "train")
            test_root  = os.path.join(extract_root, "test") if "test" in subdirs else None
            break
        elif len(subdirs) == 1:
            extract_root = os.path.join(extract_root, subdirs[0])
        else:
            # No train/ found — assume these ARE the class folders
            train_root = extract_root
            test_root  = None
            break

    class_dirs = sorted([
        d for d in os.listdir(train_root)
        if os.path.isdir(os.path.join(train_root, d))
    ])
    print(f"Train root    : {train_root}")
    print(f"Class folders : {len(class_dirs)}")
    if test_root:
        print(f"Test root     : {test_root}")

    # Build label map (alphabetical — matches backend/class_names.py)
    label_map = {name: idx for idx, name in enumerate(class_dirs)}

    def load_split(split_root, split_name):
        """Load all images from a split directory."""
        X_split, y_split = [], []
        all_files = [
            (cls, fname)
            for cls in class_dirs
            for fname in os.listdir(os.path.join(split_root, cls))
            if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".ppm"))
               and os.path.isdir(os.path.join(split_root, cls))
        ]
        print(f"Loading {split_name}: {len(all_files)} files...")
        for i, (cls_name, fname) in enumerate(all_files):
            fpath = os.path.join(split_root, cls_name, fname)
            try:
                img = PIL.Image.open(fpath).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
                X_split.append(np.array(img, dtype=np.float32) / 255.0)
                y_split.append(label_map[cls_name])
            except Exception:
                pass
            if (i + 1) % 1000 == 0:
                print(f"  {i+1}/{len(all_files)}...")
        return np.array(X_split, dtype=np.float32), np.array(y_split, dtype=np.int32)

    # ── Load images ────────────────────────────────────────────────────────────
    X, y = load_split(train_root, "train")
    if test_root:
        X_test, y_test = load_split(test_root, "test")
        X = np.concatenate([X, X_test], axis=0)
        y = np.concatenate([y, y_test], axis=0)


    print(f"\nLoaded {len(X):,} images across {len(np.unique(y))} classes")
    print(f"X shape: {X.shape},  y shape: {y.shape}")
    print(f"Label range: {y.min()} – {y.max()}")

    # Save label map for backend reference
    label_map_path = os.path.join(ROOT, "ml", "indian_label_map.json")
    with open(label_map_path, "w") as f:
        json.dump({str(v): k for k, v in label_map.items()}, f, indent=2)
    print(f"Label map saved: {label_map_path}")

    return X, y


# ──────────────────────────────────────────────────────────────────────────────
# tf.data pipelines
# ──────────────────────────────────────────────────────────────────────────────

def make_dataset(X: np.ndarray, y: np.ndarray, shuffle: bool, batch_size: int):
    ds = tf.data.Dataset.from_tensor_slices((X.astype(np.float32), y.astype(np.int32)))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(X), seed=SEED)
    ds = ds.batch(batch_size)
    return ds.prefetch(tf.data.AUTOTUNE)


# ──────────────────────────────────────────────────────────────────────────────
# Model — same CNN architecture, updated for 85 classes
# ──────────────────────────────────────────────────────────────────────────────

def build_model() -> keras.Model:
    inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

    # On-GPU data augmentation (skipped during inference)
    x = layers.RandomRotation(0.05)(inputs)
    x = layers.RandomTranslation(0.05, 0.05)(x)
    x = layers.RandomZoom(0.05)(x)
    x = layers.RandomFlip("horizontal")(x)

    # Block 1
    x = layers.Conv2D(32, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(32, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.2)(x)

    # Block 2
    x = layers.Conv2D(64, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(64, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.25)(x)

    # Block 3
    x = layers.Conv2D(128, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Conv2D(128, (3, 3), padding="same", kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.MaxPooling2D((2, 2))(x)
    x = layers.Dropout(0.3)(x)

    # Classifier head
    x = layers.Flatten()(x)
    x = layers.Dense(512, kernel_initializer="he_normal")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)  # 85 classes

    model = keras.Model(inputs, outputs, name="IndianTrafficSignCNN")
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


# ──────────────────────────────────────────────────────────────────────────────
# Plots
# ──────────────────────────────────────────────────────────────────────────────

def plot_history(hist_dict):
    plt.figure(figsize=(10, 5))
    plt.plot(hist_dict["accuracy"],     label="Train Accuracy",      color="#4F8EF7", lw=2)
    plt.plot(hist_dict["val_accuracy"], label="Validation Accuracy", color="#F4A900", lw=2, ls="--")
    plt.title("Training vs Validation Accuracy (Indian Signs)", fontsize=14, fontweight="bold")
    plt.xlabel("Epoch"); plt.ylabel("Accuracy")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
    path = os.path.join(RESULTS_DIR, "training_accuracy.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")

    plt.figure(figsize=(10, 5))
    plt.plot(hist_dict["loss"],     label="Train Loss",      color="#E05F5F", lw=2)
    plt.plot(hist_dict["val_loss"], label="Validation Loss", color="#8A2BE2", lw=2, ls="--")
    plt.title("Training vs Validation Loss (Indian Signs)", fontsize=14, fontweight="bold")
    plt.xlabel("Epoch"); plt.ylabel("Loss")
    plt.legend(); plt.grid(True, alpha=0.3); plt.tight_layout()
    path = os.path.join(RESULTS_DIR, "training_loss.png")
    plt.savefig(path, dpi=150); plt.close()
    print(f"Saved: {path}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    configure_gpu()

    # 1. Load dataset
    X_all, y_all = load_indian_dataset()

    # 2. Train / val split
    X_train, X_val, y_train, y_val = train_test_split(
        X_all, y_all,
        test_size=VAL_SPLIT,
        random_state=SEED,
        stratify=y_all,
    )
    print(f"\nTrain : {len(X_train):,} images")
    print(f"Val   : {len(X_val):,}   images")
    print(f"Classes: {len(np.unique(y_train))}")

    # 3. tf.data pipelines
    train_ds = make_dataset(X_train, y_train, shuffle=True,  batch_size=BATCH_SIZE)
    val_ds   = make_dataset(X_val,   y_val,   shuffle=False, batch_size=BATCH_SIZE)

    # 4. Build model
    model = build_model()
    model.summary()

    # 5. Callbacks
    callbacks = [
        ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
            verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1,
        ),
    ]

    # 6. Train
    print("\nStarting training …")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    hist_dict = history.history

    # 7. Save history + plots
    with open(HISTORY_PATH, "w") as f:
        json.dump({k: [float(v) for v in vals] for k, vals in hist_dict.items()}, f, indent=2)

    plot_history(hist_dict)

    # 8. Summary
    best_val_acc    = max(hist_dict["val_accuracy"]) * 100
    final_train_acc = hist_dict["accuracy"][-1] * 100
    print("\n" + "="*50)
    print(f"  Training Accuracy   : {final_train_acc:.2f}%")
    print(f"  Best Val Accuracy   : {best_val_acc:.2f}%")
    print("="*50)
    print(f"\nModel saved to: {MODEL_PATH}")
    print("Run  python ml/evaluate_indian.py  to generate the confusion matrix.")


if __name__ == "__main__":
    main()
