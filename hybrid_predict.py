import tensorflow as tf
import numpy as np
import joblib
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from severity_engine import is_minor_case
from backend.first_aid import show_first_aid
from backend.hospital_service import get_recommendations

IMG_SIZE = 224

CLASS_NAMES = ['abrasion', 'bruise', 'burn', 'cut', 'normal', 'rash']

# Injury → Department Mapping
INJURY_TO_DEPT = {
    "abrasion": "Orthopedics",
    "bruise": "Orthopedics",
    "cut": "Orthopedics",
    "burn": "Dermatology",
    "rash": "Dermatology",
    "normal": "General"
}

# Load models
cnn_model = tf.keras.models.load_model("cnn/models/best_skin_cnn.h5")
text_model = joblib.load("models/symptom_category_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


# ---------------- IMAGE PREDICTION ----------------
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = cnn_model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))

    return CLASS_NAMES[predicted_index], confidence


# ---------------- TEXT PREDICTION ----------------
def predict_text(symptoms):
    vec = vectorizer.transform([symptoms])
    pred = text_model.predict(vec)[0]
    prob = max(text_model.predict_proba(vec)[0])
    return pred, float(prob)


# ---------------- HYBRID DECISION ----------------
def hybrid_predict(img_path=None, symptoms=""):

    image_provided = bool(img_path)
    text_provided = bool(symptoms.strip())

    image_label, image_conf = None, 0
    text_label, text_conf = None, 0

    # Image prediction
    if image_provided:
        image_label, image_conf = predict_image(img_path)
        print("\nImage Prediction:", image_label, "Confidence:", round(image_conf, 2))

    # Text prediction
    if text_provided:
        text_label, text_conf = predict_text(symptoms)
        print("Text Prediction:", text_label, "Confidence:", round(text_conf, 2))

    # ---------------- Final Department Decision ----------------
    if image_provided and text_provided:
        image_dept = INJURY_TO_DEPT.get(image_label, "General")

        if image_dept == text_label:
            final_department = image_dept
            source = "Both Models Agree"
        else:
            if image_conf > text_conf:
                final_department = image_dept
                source = "Image Model"
            else:
                final_department = text_label
                source = "Symptom Model"

    elif image_provided:
        final_department = INJURY_TO_DEPT.get(image_label, "General")
        source = "Image Only"

    elif text_provided:
        final_department = text_label
        source = "Text Only"

    else:
        print("No input provided.")
        return

    print("\nFINAL DEPARTMENT:", final_department)
    print("Decision Source:", source)


    # ---------------- Severity Engine ----------------
    minor = is_minor_case(
        image_pred=image_label,
        image_conf=image_conf,
        text=symptoms
    )

    if minor:
        print("\n⚕️ This appears to be a MINOR case.")
        print("Showing First Aid steps...")

        # If user typed symptoms → use that
        # If only image provided → use image label
        show_first_aid(symptoms if symptoms.strip() else image_label)

    print("\n🏥 Recommended Hospitals:")

    # You must provide user latitude & longitude
    user_lat = float(input("Enter your latitude: "))
    user_lon = float(input("Enter your longitude: "))

    hospitals = get_recommendations(final_department, user_lat, user_lon)

    if not hospitals:
        print("No hospitals found for this department.")
    else:
        for hosp in hospitals:
            print("\nHospital:", hosp["hospital_name"])
            print("Area:", hosp["area"], "-", hosp["city"])
            print("Phone:", hosp["phone"])
            print("Address:", hosp["address"])

            # add here
            maps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination_place_id={hosp['place_id']}"
            print("Get Directions:", maps_url)

            print("Doctors:")
            for doc in hosp["doctors"]:
                print("  -", doc["doctor_name"],
                      "| Exp:", doc["experience_years"], "yrs",
                      "| Fee:", doc["consultation_fee"])

# ---------------- TEST ----------------
if __name__ == "__main__":
    img_path = input("Enter image path (or press Enter to skip): ").strip().replace('"','')
    symptoms = input("Enter symptoms description (or press Enter to skip): ")

    hybrid_predict(img_path if img_path else None, symptoms)