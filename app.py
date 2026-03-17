# from flask import Flask,jsonify,request

# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.image import imread
# import tensorflow as tf
# from keras.preprocessing import image
# import pandas as pd

# import firebase_admin
# from firebase_admin import credentials, storage
# import numpy as np
# import cv2


# import cv2
# import numpy as np
# import pandas as pd
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# import tensorflow as tf
# # from google.cloud import storage


# app = Flask(__name__)
# cred = credentials.Certificate("service_account_credentials.json")
# fire_app = firebase_admin.initialize_app(cred, { 'storageBucket' : 'myprojects-92838.appspot.com' })


# @app.route('/')
# def index():
#     return 'Successfully Working'


# @app.route('/detect')
# def app_abhi():
#     # Set image dimensions
#     img_height = 180
#     img_width = 180

#     # Load the pre-trained model
#     model = tf.keras.models.load_model('Mango_Fruit_Detection_Model.h5')

#     # Class names and mapping
#     class_names = ['Alternaria', 'Anthracnose', 'Black_Mould_Rot', 'Healthy', 'Stem_and_Rot']

#     # Read the dataset
#     df = pd.read_csv("mango_dataset/Mango_fruit_dataset.csv")
#     df = df.replace('', np.nan)
#     df = df.dropna(axis="columns", how="any")

#     # Image path
#     path = "mango_dataset/img/healty_img.jpg"


#     # Load image from Cloud Storage
#     bucket = storage.bucket()
#     blob = bucket.get_blob("detect_fruit.jpg")  # blob
#     blob = bucket.blob("detect_fruit.jpg")
#     blob.download_to_filename("test/download_file.jpg")
#     arr = np.frombuffer(blob.download_as_string(), np.uint8)  # array of bytes
#     img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # actual image
#     img = cv2.resize(img, (img_height, img_width))
#     cv2.imshow("image",img)

#     # Preprocess the image
#     # img = preprocess_input(img)
#     # img = np.expand_dims(img, axis=0)

#     import os

#     # Specify the directory path and file name
#     directory_path = "test/"
#     file_name = "download_file.jpg"

#     # Construct the full file path
#     path = os.path.join(directory_path, file_name)

#     # Check if the file exists before further processing
#     if os.path.exists(path):
#         print(f"The file path is: {path}")
#         # Your further processing logic here
#     else:
#         print(f"The file {path} does not exist.")


#     #something
#     img = image.load_img(path,target_size=(img_height,img_width))
#     img = image.img_to_array(img)
#     img = np.expand_dims(img,axis=0)


#     # Make predictions
#     prediction = model.predict(img)
#     predicted_class = np.argmax(prediction)

#     print(f"Predicted class: {predicted_class}")
#     print(f"Predict Disease: {class_names[predicted_class]}")

#     # Extract information from the dataset
#     Sn_no, Disease_Type, Severity, Location_Date, Description, Symptoms, Diagnosis, Precautions = df.loc[predicted_class, :]

#     print(f"\n\nDisease Type: {Disease_Type}\nSeverity: {Severity}\nDescription: {Description}\nSymptoms: {Symptoms}\nDiagnosis: {Diagnosis}\nPrecautions: {Precautions}")

#     path = os.path.abspath(path)
#     # Create a dictionary with the dataset information
#     dataset = {
#         "Disease_Type": Disease_Type,
#         "Severity": Severity,
#         "Description": Description,
#         "Symptoms": Symptoms,
#         "Diagnosis": Diagnosis,
#         "Precautions": Precautions
#     }

#     return dataset

# if __name__ == '__main__':
#    app.run(debug=True ,host='0.0.0.0',port=5000)

# from flask import Flask, jsonify, request
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# import pandas as pd
# import os
# from flask_cors import CORS
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# app = Flask(__name__)
# CORS(app)  # allow React frontend to call this API

# _MODEL = None
# _DF = None


# def _get_model():
#     """
#     Load and cache the Keras model.
#     Fixes Keras Lambda deserialization when the model contains preprocess_input.
#     """
#     global _MODEL
#     if _MODEL is not None:
#         return _MODEL

#     model_path = os.path.join(os.path.dirname(__file__), "Mango_Fruit_Detection_Model.h5")
#     if not os.path.exists(model_path):
#         raise FileNotFoundError(f"Model file not found: {model_path}")

#     _MODEL = tf.keras.models.load_model(
#         model_path,
#         custom_objects={"preprocess_input": preprocess_input},
#         compile=False,
#     )
#     return _MODEL


# def _get_dataset():
#     """Load and cache the CSV dataset."""
#     global _DF
#     if _DF is not None:
#         return _DF

#     csv_path = os.path.join(os.path.dirname(__file__), "mango_dataset", "Mango_fruit_dataset.csv")
#     if not os.path.exists(csv_path):
#         # Dataset is optional (some projects only have image folders).
#         # If it's missing, we still return predictions.
#         _DF = None
#         return None

#     df = pd.read_csv(csv_path)
#     df = df.replace("", np.nan)
#     df = df.dropna(axis="columns", how="all")
#     _DF = df
#     return _DF


# @app.route('/')
# def index():
#     return '✅ Mango Fruit Disease Detection API is running!'


# @app.route('/detect', methods=['POST'])
# def detect():
#     """
#     Detect mango disease from an uploaded image file.
#     Expects a multipart/form-data POST with field name 'image'.
#     """
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided. Use form field name 'image'."}), 400

#     file = request.files['image']
#     if file.filename == '':
#         return jsonify({"error": "Empty filename."}), 400

#     # Save uploaded image to a temporary path
#     upload_dir = "uploads"
#     os.makedirs(upload_dir, exist_ok=True)
#     img_path = os.path.join(upload_dir, file.filename)
#     file.save(img_path)

#     # Set image dimensions (must match your training setup)
#     img_height = 224
#     img_width = 224

#     # Load model (cached)
#     model = _get_model()

#     # Class names (match your dataset folder names)
#     # image_dataset_from_directory sorts folders alphabetically, so keep this order.
#     class_names = ['Alternaria', 'Anthracnose', 'Black Mould Rot', 'Healthy', 'Stem end Rot']

#     # Load dataset (cached)
#     df = _get_dataset()

#     # Load and preprocess image
#     img = image.load_img(img_path, target_size=(img_height, img_width))
#     img = image.img_to_array(img)

#     # 🔥 Required for MobileNetV2
#     img = preprocess_input(img)

#     img = np.expand_dims(img, axis=0)

#     # Predict
#     prediction = model.predict(img)
#     predicted_class = int(np.argmax(prediction))

#     predicted_disease_display = class_names[predicted_class]

#     # Optional: Extract info from dataset row if CSV exists
#     Disease_Type = ""
#     Severity = ""
#     Description = ""
#     Symptoms = ""
#     Diagnosis = ""
#     Precautions = ""

#     if df is not None:
#         # Use positional index to avoid index-label mismatch
#         row = df.iloc[predicted_class]
#         Disease_Type = row.get("Disease_Type", "")
#         Severity = row.get("Severity", "")
#         Description = row.get("Description", "")
#         Symptoms = row.get("Symptoms", "")
#         Diagnosis = row.get("Diagnosis", "")
#         Precautions = row.get("Precautions", "")

#     result = {
#         "predicted_class_index": predicted_class,
#         "predicted_disease": predicted_disease_display,
#         "disease_type": str(Disease_Type),
#         "severity": str(Severity),
#         "description": str(Description),
#         "symptoms": str(Symptoms),
#         "diagnosis": str(Diagnosis),
#         "precautions": str(Precautions),
#         "has_dataset_csv": df is not None,
#     }

#     return jsonify(result)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, jsonify, request
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import pandas as pd
import os
from flask_cors import CORS

# 🔥 IMPORTANT: Needed because model uses MobileNet preprocessing internally
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

app = Flask(__name__)
CORS(app)

# Global cache variables (to avoid loading model again and again)
_MODEL = None
_DF = None

# ✅ IMPORTANT: Class names MUST match training order
# Using sorted() because image_dataset_from_directory uses alphabetical order
class_names = sorted([
    'Alternaria',
    'Anthracnose',
    'Black Mould Rot',
    'Healthy',
    'Stem end Rot'
])


# =========================
# LOAD MODEL (FIXED)
# =========================
def _get_model():
    global _MODEL

    if _MODEL is not None:
        return _MODEL

    model_path = os.path.join(os.path.dirname(__file__), "Mango_Fruit_Detection_Model.h5")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # 🔥 FIX: pass preprocess_input to solve loading error
    _MODEL = tf.keras.models.load_model(
        model_path,
        custom_objects={"preprocess_input": preprocess_input},
        compile=False
    )

    print("✅ Model Loaded Successfully")
    return _MODEL


# =========================
# LOAD DATASET (OPTIONAL)
# =========================
def _get_dataset():
    global _DF

    if _DF is not None:
        return _DF

    csv_path = os.path.join(os.path.dirname(__file__), "mango_dataset", "Mango_fruit_dataset.csv")

    if not os.path.exists(csv_path):
        _DF = None
        return None

    df = pd.read_csv(csv_path)
    df = df.replace("", np.nan)
    df = df.dropna(axis="columns", how="all")

    _DF = df
    print("✅ Dataset Loaded")
    return _DF


# =========================
# HOME ROUTE
# =========================
@app.route('/')
def index():
    return '✅ Mango Disease Detection API Running'


# =========================
# DETECT ROUTE
# =========================
@app.route('/detect', methods=['POST'])
def detect():

    # Check image input
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save uploaded image
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    img_path = os.path.join(upload_dir, file.filename)
    file.save(img_path)

    # =========================
    # IMAGE PREPROCESSING
    # =========================

    # ✅ Resize to 224 (MobileNet requirement)
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)

    # ❌ DO NOT use preprocess_input here
    # ❌ DO NOT use img/255
    # Because model already has preprocessing layer inside

    img = np.expand_dims(img, axis=0)

    print("📸 Image shape:", img.shape)

    # =========================
    # LOAD MODEL
    # =========================
    model = _get_model()

    # =========================
    # PREDICTION
    # =========================
    prediction = model.predict(img)

    print("📊 Prediction array:", prediction)

    predicted_class = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    print("🎯 Predicted index:", predicted_class)
    print("🔥 Confidence:", confidence)

    predicted_disease = class_names[predicted_class]

    # =========================
    # LOAD DATASET INFO (OPTIONAL)
    # =========================
    df = _get_dataset()

    Disease_Type = ""
    Severity = ""
    Description = ""
    Symptoms = ""
    Diagnosis = ""
    Precautions = ""

    if df is not None and predicted_class < len(df):
        row = df.iloc[predicted_class]

        Disease_Type = row.get("Disease_Type", "")
        Severity = row.get("Severity", "")
        Description = row.get("Description", "")
        Symptoms = row.get("Symptoms", "")
        Diagnosis = row.get("Diagnosis", "")
        Precautions = row.get("Precautions", "")

    # =========================
    # FINAL RESPONSE
    # =========================
    return jsonify({
        "predicted_class_index": predicted_class,
        "predicted_disease": predicted_disease,
        "confidence": confidence,
        "disease_type": str(Disease_Type),
        "severity": str(Severity),
        "description": str(Description),
        "symptoms": str(Symptoms),
        "diagnosis": str(Diagnosis),
        "precautions": str(Precautions),
        "has_dataset_csv": df is not None
    })


# =========================
# RUN SERVER
# =========================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
