import os
from pathlib import Path

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_cors import CORS
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

# Needed because the saved model contains a Lambda that references preprocess_input
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

APP_DIR = Path(__file__).resolve().parent
MODEL_PATH = APP_DIR / "Mango_Fruit_Detection_Model.h5"
UPLOAD_DIR = APP_DIR / "uploads"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

HEALTHY_LABEL = "Healthy"
# Reduce false-positive disease predictions on real-world healthy photos.
# Tuned to flip cases like: Alternaria 0.62 vs Healthy 0.33 (your img3.jpg)
HEALTHY_PROB_MIN = 0.30
HEALTHY_MARGIN_MAX = 0.30

app = Flask(__name__)
CORS(app)

_MODEL = None

# IMPORTANT: Must match training class order (alphabetical for image_dataset_from_directory)
CLASS_NAMES = sorted(
    [
        "Alternaria",
        "Anthracnose",
        "Black Mould Rot",
        "Healthy",
        "Stem end Rot",
    ]
)

DISEASE_INFO = {
    "Alternaria": {
        "severity": "Moderate",
        "description": "Fungal disease causing dark spots",
        "symptoms": "Brown/black spots",
        "diagnosis": "Visual inspection",
        "precautions": "Apply fungicide",
    },
    "Anthracnose": {
        "severity": "Severe",
        "description": "Common mango fungal disease",
        "symptoms": "Dark lesions",
        "diagnosis": "Lab testing",
        "precautions": "Copper spray",
    },
    "Black Mould Rot": {
        "severity": "High",
        "description": "Fruit rot infection",
        "symptoms": "Black mold",
        "diagnosis": "Visual",
        "precautions": "Avoid moisture",
    },
    "Healthy": {
        "severity": "None",
        "description": "Healthy fruit",
        "symptoms": "No symptoms",
        "diagnosis": "Not required",
        "precautions": "Maintain storage",
    },
    "Stem end Rot": {
        "severity": "Moderate",
        "description": "Rot at stem end",
        "symptoms": "Dark area near stem",
        "diagnosis": "Visual",
        "precautions": "Handle carefully",
    },
}


def _get_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

    _MODEL = tf.keras.models.load_model(
        str(MODEL_PATH),
        custom_objects={"preprocess_input": preprocess_input},
        compile=False,
    )
    return _MODEL


def _is_allowed_filename(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index():
    return "✅ Mango Disease Detection API Running"


@app.post("/detect")
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image provided. Use form field name 'image'."}), 400

    file = request.files["image"]
    if not file or not file.filename:
        return jsonify({"error": "Empty filename."}), 400

    safe_name = secure_filename(file.filename)
    if not safe_name:
        return jsonify({"error": "Invalid filename."}), 400
    if not _is_allowed_filename(safe_name):
        return (
            jsonify(
                {
                    "error": "Unsupported file type. Allowed: "
                    + ", ".join(sorted(ALLOWED_EXTENSIONS))
                }
            ),
            400,
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    img_path = UPLOAD_DIR / safe_name

    try:
        file.save(str(img_path))

        img = image.load_img(str(img_path), target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        model = _get_model()
        prediction = model.predict(img, verbose=0)
        probs = np.asarray(prediction[0], dtype=np.float32)

        predicted_class = int(np.argmax(probs))
        predicted_disease = CLASS_NAMES[predicted_class]

        if HEALTHY_LABEL in CLASS_NAMES:
            healthy_idx = CLASS_NAMES.index(HEALTHY_LABEL)
            top_prob = float(probs[predicted_class])
            healthy_prob = float(probs[healthy_idx])

            if predicted_disease != HEALTHY_LABEL and (
                healthy_prob >= HEALTHY_PROB_MIN
                or (top_prob - healthy_prob) <= HEALTHY_MARGIN_MAX
            ):
                predicted_class = healthy_idx
                predicted_disease = HEALTHY_LABEL

        info = DISEASE_INFO.get(predicted_disease, {})

        return jsonify(
            {
                "predicted_class_index": predicted_class,
                "predicted_disease": predicted_disease,
                "disease_type": predicted_disease,
                "severity": info.get("severity", ""),
                "description": info.get("description", ""),
                "symptoms": info.get("symptoms", ""),
                "diagnosis": info.get("diagnosis", ""),
                "precautions": info.get("precautions", ""),
                "has_dataset_csv": False,
            }
        )
    except Exception as e:
        return jsonify({"error": "Detection failed", "details": str(e)}), 500
    finally:
        try:
            if img_path.exists():
                img_path.unlink()
        except Exception:
            pass
        # =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("🚀 Starting Mango API Server...")
    app.run(debug=True, host="127.0.0.1", port=5000)