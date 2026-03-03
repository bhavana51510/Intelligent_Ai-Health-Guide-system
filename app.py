from flask import Flask, request, jsonify, send_from_directory
import joblib
import os
from werkzeug.utils import secure_filename

from backend.cnn_model import predict_image
from backend.hospital_service import get_recommendations
from backend.image_rules import IMAGE_SYMPTOM_RULES

print("### app.py LOADED ###")

# --------------------------------------------------
# Flask Setup (Serve Frontend Properly)
# --------------------------------------------------
app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------------------------
# Load ML Model
# --------------------------------------------------
model = joblib.load("models/symptom_category_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

# --------------------------------------------------
# Serve Frontend
# --------------------------------------------------
@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


# --------------------------------------------------
# TEXT SYMPTOMS API
# --------------------------------------------------
@app.route("/api/full-recommendation", methods=["POST"])
def full_recommendation():
    try:
        data = request.get_json(force=True)

        symptoms = data["symptoms"]
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        X = vectorizer.transform([symptoms])
        category = model.predict(X)[0]

        # Safety override
        s = symptoms.lower()
        if "eye" in s:
            category = "Ophthalmology"
        elif "ear" in s or "throat" in s:
            category = "ENT"
        elif "tooth" in s:
            category = "Dental"

        hospitals = get_recommendations(category, latitude, longitude)

        return jsonify({
            "predicted_category": category,
            "severity": "Consult Doctor",
            "first_aid": [],
            "hospitals": hospitals
        })

    except Exception as e:
        print("TEXT ERROR:", e)
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# IMAGE API
# --------------------------------------------------
@app.route("/api/image-upload", methods=["POST"])
def image_upload():
    try:

        file = request.files["image"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        predicted_label, confidence = predict_image(filepath)

        # Minor injuries go to General Medicine
        category = "General Medicine"

        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))

        hospitals = get_recommendations(category, latitude, longitude)

        return jsonify({
            "predicted_category": category,
            "severity": "Minor",
            "first_aid": IMAGE_SYMPTOM_RULES[predicted_label]["first_aid"],
            "hospitals": hospitals
        })

    except Exception as e:
        print("IMAGE ERROR:", e)
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------
# Run Server
# --------------------------------------------------
if __name__ == "__main__":
    print("### ROUTES REGISTERED ###")
    print(app.url_map)
    app.run(debug=True)