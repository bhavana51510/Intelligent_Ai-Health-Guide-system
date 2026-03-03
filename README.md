# 🏥 AI Health Guidance System

An intelligent AI-powered web application that analyzes user symptoms or minor injury images and provides:

- First Aid Guidance
- Department Recommendation
- Nearby Hospital Suggestions

⚠️ This system does NOT diagnose medical conditions. It provides guidance and hospital recommendations only.

---

## 🚀 Features

### 🔹 Symptom-Based Analysis
- TF-IDF + Machine Learning classifier
- Predicts medical department
- Provides first aid steps
- Suggests nearby hospitals based on user location

### 🔹 Image-Based Minor Injury Detection
- CNN model trained on skin injury dataset
- Detects minor visible injuries
- Provides basic first aid guidance
- Recommends general medicine hospitals

### 🔹 Location Integration
- Uses browser geolocation
- Embeds Google Maps
- Direct navigation to hospital

---

## 🧠 Tech Stack

**Backend**
- Flask
- Scikit-learn
- TensorFlow (CNN)
- Joblib

**Frontend**
- HTML
- CSS (Glass UI design)
- Vanilla JavaScript
- Google Maps Embed API

---

## 📁 Project Structure