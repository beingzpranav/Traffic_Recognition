"""
Indian Traffic Sign CNN — Evaluation Script
============================================
Run AFTER training:
    python ml/evaluate.py

Generates:
  results/confusion_matrix.png
  results/classification_report.txt
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

# ──────────────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────────────

MODEL_PATH  = os.path.join(ROOT, "models", "traffic_sign_cnn.keras")
RESULTS_DIR = os.path.join(ROOT, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

SEED       = 42
IMG_SIZE   = 32
VAL_SPLIT  = 0.20

# 85 Indian traffic sign class names
CLASS_NAMES = {
    0:  "All Motor Vehicles Prohibited",
    1:  "Axle Load Limit",
    2:  "Barrier Ahead",
    3:  "Bullock and Handcart Prohibited",
    4:  "Bullock Prohibited",
    5:  "Cattle",
    6:  "Compulsory Ahead",
    7:  "Compulsory Ahead or Turn Left",
    8:  "Compulsory Ahead or Turn Right",
    9:  "Compulsory Cycle Track",
    10: "Compulsory Keep Left",
    11: "Compulsory Keep Right",
    12: "Compulsory Minimum Speed",
    13: "Compulsory Sound Horn",
    14: "Compulsory Turn Left",
    15: "Compulsory Turn Left Ahead",
    16: "Compulsory Turn Right",
    17: "Compulsory Turn Right Ahead",
    18: "Cross Road",
    19: "Cycle Crossing",
    20: "Cycle Prohibited",
    21: "Dangerous Dip",
    22: "Direction",
    23: "Falling Rocks",
    24: "Ferry",
    25: "Gap in Median",
    26: "Give Way",
    27: "Guarded Level Crossing",
    28: "Handcart Prohibited",
    29: "Height Limit",
    30: "Horn Prohibited",
    31: "Hump or Rough Road",
    32: "Left Hair Pin Bend",
    33: "Left Hand Curve",
    34: "Left Reverse Bend",
    35: "Left Turn Prohibited",
    36: "Length Limit",
    37: "Load Limit",
    38: "Loose Gravel",
    39: "Men at Work",
    40: "Narrow Bridge",
    41: "Narrow Road Ahead",
    42: "No Entry",
    43: "No Parking",
    44: "No Stopping or Standing",
    45: "Overtaking Prohibited",
    46: "Pass Either Side",
    47: "Pedestrian Crossing",
    48: "Pedestrian Prohibited",
    49: "Priority for Oncoming Vehicles",
    50: "Quay Side or River Bank",
    51: "Restriction Ends",
    52: "Right Hair Pin Bend",
    53: "Right Hand Curve",
    54: "Right Reverse Bend",
    55: "Right Turn Prohibited",
    56: "Road Widens Ahead",
    57: "Roundabout",
    58: "School Ahead",
    59: "Side Road Left",
    60: "Side Road Right",
    61: "Slippery Road",
    62: "Speed Limit 15",
    63: "Speed Limit 20",
    64: "Speed Limit 30",
    65: "Speed Limit 40",
    66: "Speed Limit 5",
    67: "Speed Limit 50",
    68: "Speed Limit 60",
    69: "Speed Limit 70",
    70: "Speed Limit 80",
    71: "Staggered Intersection",
    72: "Steep Ascent",
    73: "Steep Descent",
    74: "Stop",
    75: "Straight Prohibited",
    76: "Tonga Prohibited",
    77: "Traffic Signal",
    78: "Truck Prohibited",
    79: "Turn Right",
    80: "T Intersection",
    81: "Unguarded Level Crossing",
    82: "U-Turn Prohibited",
    83: "Width Limit",
    84: "Y Intersection",
}

SHORT_NAMES = [CLASS_NAMES[i] for i in range(85)]


# ──────────────────────────────────────────────────────────────────────────────
# Confusion matrix plot
# ──────────────────────────────────────────────────────────────────────────────

def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1, keepdims=True)

    fig, ax = plt.subplots(figsize=(28, 24))
    sns.heatmap(
        cm_norm,
        annot=False,
        fmt=".2f",
        cmap="Blues",
        xticklabels=SHORT_NAMES,
        yticklabels=SHORT_NAMES,
        linewidths=0.3,
        ax=ax,
    )
    ax.set_title("Confusion Matrix — Indian Traffic Signs (Normalized)", fontsize=16, fontweight="bold", pad=20)
    ax.set_xlabel("Predicted", fontsize=12)
    ax.set_ylabel("True", fontsize=12)
    ax.tick_params(axis="x", rotation=90, labelsize=6)
    ax.tick_params(axis="y", rotation=0,  labelsize=6)
    plt.tight_layout()

    path = os.path.join(RESULTS_DIR, "confusion_matrix.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: model not found at {MODEL_PATH}")
        print("Train first:  python ml/train.py")
        sys.exit(1)

    # Load model
    print(f"Loading model: {MODEL_PATH}")
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Model output shape: {model.output_shape}")

    # Load same dataset used for training and use same val split
    print("\nLoading dataset from HuggingFace for evaluation...")
    from datasets import load_dataset
    import PIL.Image

    ds = load_dataset("kannanwisen/Indian-Traffic-Sign-Classification")
    train_data = ds["train"]

    X, y = [], []
    for i, sample in enumerate(train_data):
        if i % 500 == 0:
            print(f"  Processing {i}/{len(train_data)}...")
        img = sample["image"]
        if not isinstance(img, PIL.Image.Image):
            img = PIL.Image.fromarray(img)
        img = img.convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        X.append(np.array(img, dtype=np.float32) / 255.0)
        y.append(int(sample["label"]))

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)

    # Same val split as training
    _, X_val, _, y_val = train_test_split(
        X, y,
        test_size=VAL_SPLIT,
        random_state=SEED,
        stratify=y,
    )
    print(f"Evaluating on {len(X_val):,} validation images...")

    # Predict
    y_pred_probs = model.predict(X_val, batch_size=64, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # Accuracy
    test_acc = np.mean(y_pred == y_val)
    print(f"\nValidation Accuracy: {test_acc * 100:.2f}%")

    # Classification report
    report = classification_report(y_val, y_pred, target_names=SHORT_NAMES, digits=4)
    print("\nClassification Report:")
    print(report)

    report_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    with open(report_path, "w") as f:
        f.write(f"Validation Accuracy: {test_acc * 100:.2f}%\n\n")
        f.write(report)
    print(f"Report saved to: {report_path}")

    # Confusion matrix
    plot_confusion_matrix(y_val, y_pred)

    # Load training history if available
    hist_path = os.path.join(RESULTS_DIR, "training_history.json")
    if os.path.exists(hist_path):
        with open(hist_path) as f:
            hist = json.load(f)
        best_val = max(hist.get("val_accuracy", [0])) * 100
        print(f"Best Validation Accuracy (from history): {best_val:.2f}%")

    print("\nEvaluation complete.")


if __name__ == "__main__":
    main()
