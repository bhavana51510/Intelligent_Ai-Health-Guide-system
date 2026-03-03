import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/processed/custom_medical_dataset_final.csv")

X = df["symptoms"].astype(str)
y = df["category"].astype(str)

# -----------------------------
# Vectorizer
# -----------------------------
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_vec = vectorizer.fit_transform(X)

# -----------------------------
# Model (sklearn 1.8+ compatible)
# -----------------------------
model = LogisticRegression(
    max_iter=1000,
    solver="lbfgs",
    class_weight="balanced"
)

model.fit(X_vec, y)

# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, "models/symptom_category_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully.")
