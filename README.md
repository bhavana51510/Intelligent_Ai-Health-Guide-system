# 🏥 Intelligent AI Health Guide System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-black)
![TensorFlow](https://img.shields.io/badge/DeepLearning-TensorFlow-orange)
![Scikit-Learn](https://img.shields.io/badge/NLP-ScikitLearn-yellow)
![Status](https://img.shields.io/badge/Project-Active-success)

An AI-powered First Aid Guidance and Hospital Recommendation System that combines **Natural Language Processing (NLP)** and **Deep Learning (CNN)** to assist users with minor injuries and symptom-based guidance.

This system provides:
- 📝 Symptom-based classification using ML
- 🖼️ Image-based injury detection using CNN
- 🩹 Structured First Aid recommendations
- 🏥 Nearby hospital suggestions based on user location
- 🗺️ Google Maps integration for navigation

---

## 🚀 Key Features

- ✅ TF-IDF + Machine Learning symptom classifier  
- ✅ Custom CNN for minor injury image classification  
- ✅ Hybrid prediction logic (text + image)  
- ✅ Rule-based medical safety overrides  
- ✅ Hospital recommendation engine  
- ✅ Clean frontend interface  
- ✅ Modular backend architecture  

---

## 🧠 System Architecture

User Input (Text / Image)  
→ Frontend (HTML, CSS, JS)  
→ Flask Backend API  
→  
&nbsp;&nbsp;&nbsp;&nbsp;• NLP Model (TF-IDF + Classifier)  
&nbsp;&nbsp;&nbsp;&nbsp;• CNN Model (Injury Classification)  
→ Severity Engine  
→ First Aid Recommendation  
→ Nearby Hospital Ranking  
→ Response to User  

---

## 📂 Project Structure

```
Intelligent_Ai-Health-Guide-system/
│
├── backend/
│   ├── cnn_model.py
│   ├── hospital_service.py
│   ├── image_rules.py
│   ├── first_aid.py
│   ├── data_loader.py
│   └── integrity_checks.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── symptom_category_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── skin_cnn_final.h5
│
├── cnn/
│   ├── train_cnn.py
│   └── predict.py
│
├── hybrid_predict.py
├── severity_engine.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🔬 Machine Learning Components

### 1️⃣ Symptom Classification (NLP)
- TF-IDF Vectorizer
- Supervised ML classifier
- Category override safety logic
- Structured symptom-to-first-aid mapping

### 2️⃣ Image Classification (CNN)
- Custom Convolutional Neural Network
- Multi-class classification:
  - Abrasion
  - Burn
  - Cut
  - Bruise
  - Rash
  - Normal
- Trained using image dataset (train/validation split)

---

## ⚙️ Tech Stack

- **Backend:** Python, Flask  
- **Machine Learning:** Scikit-learn, TensorFlow, Keras  
- **Frontend:** HTML, CSS, JavaScript  
- **Location Services:** Geolocation API  
- **Maps Integration:** Google Maps Embed API  

---

## ▶️ How to Run Locally

###  Open in Browser

```
http://127.0.0.1:5000
```

---

## 🛡️ Safety Disclaimer

This system does **not** provide medical diagnosis.  
It is designed for educational and first-aid guidance purposes only.  
Always consult a certified healthcare professional for medical emergencies.

---

## 🏗️ Future Improvements

- Cloud deployment (AWS / Render )
- User authentication system
- Database-backed hospital system
- Improved CNN accuracy with data augmentation
- Real-time emergency severity scoring
- REST API versioning

---

