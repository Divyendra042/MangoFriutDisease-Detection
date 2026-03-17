# 🥭 Mango Fruit Disease Detection Web Application

---

## 📌 Overview

This project presents a **web-based intelligent system** for detecting mango fruit diseases using **Deep Learning (MobileNetV2)**.

The system allows users to upload mango images and receive:
- ✅ Instant disease prediction
- 📊 Confidence score
- 🧾 Disease details (symptoms, precautions, diagnosis)

The application integrates:
- 🌐 React Frontend (Modern UI)
- 🔙 Flask Backend API
- 🧠 Deep Learning Model (CNN + Transfer Learning)

---

## 🧠 Model Architecture (Research Based)

The model is developed using:

- **MobileNetV2 (Transfer Learning)**
- Fine-tuning of last layers
- Input size: `224 x 224`
- Output: Softmax classification

### 📂 Classes:
- Alternaria  
- Anthracnose  
- Black Mould Rot  
- Healthy  
- Stem End Rot  

---

## 🎯 Why MobileNetV2?

- Lightweight & fast  
- High accuracy with small dataset  
- Suitable for real-time prediction  
- Ideal for web & mobile deployment  

---

## 🌐 Website Features

### 🔹 Frontend (React)
- Image upload with preview  
- Mobile-style modern UI  
- Loading animation  
- Confidence visualization  
- Disease details display  

### 🔹 Backend (Flask API)
- `/detect` REST API  
- Image preprocessing  
- Model prediction  
- JSON response  

---

## ⚙️ Workflow

1. User uploads mango image  
2. Image sent to Flask API  
3. Model processes the image  
4. Prediction generated  
5. Result displayed on UI  

---

## 📊 Sample Output

- **Predicted Disease:** Anthracnose  
- **Confidence:** 99.78%  

---

## 🚀 Tech Stack

| Layer       | Technology |
|------------|-----------|
| Frontend   | React + CSS |
| Backend    | Flask |
| ML Model   | TensorFlow / Keras |
| Architecture | MobileNetV2 |
| Image Processing | OpenCV / PIL |

---

## 📑 Research Contribution

This project implements a **transfer learning-based CNN model using MobileNetV2** for efficient mango disease detection.

### 🔬 Key Contributions:
- Lightweight CNN model for real-time detection  
- Fine-tuned MobileNetV2 improves accuracy  
- Multi-class classification of mango diseases  
- Integration with web application for practical use  

### ⚙️ Training Strategy:
- Data augmentation applied  
- Fine-tuning last layers  
- Early stopping to avoid overfitting  

---
## Demo Images / Output

<img width="960" alt="Screenshot 2023-12-15 225608" src="https://github.com/user-attachments/assets/90160009-583c-435d-b35c-2a58cc78e52b">

<img width="960" alt="Screenshot 2023-12-15 225755" src="https://github.com/user-attachments/assets/36ca5053-fefb-4432-a315-68392252c7d7">

<img width="960" alt="Screenshot 2023-12-15 225830" src="https://github.com/user-attachments/assets/e6101b53-349a-44d2-9640-a40a077471a5">

<img width="960" alt="Screenshot 2023-12-15 225903" src="https://github.com/user-attachments/assets/cf756bae-3e0a-4470-8f1f-9a1b5b4431bd">



