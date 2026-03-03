import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ✅ Correct path to your trained model
MODEL_PATH = "cnn/models/best_skin_cnn.h5"

CLASS_NAMES = [
    "abrasion",
    "bruise",
    "burn",
    "cut",
    "normal",
    "rash"
]

model = None

def load_cnn():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        model = load_model(MODEL_PATH)
    return model


def predict_image(filepath):
    model = load_cnn()

    img = image.load_img(filepath, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    preds = model.predict(img_array)[0]
    idx = np.argmax(preds)
    confidence = float(np.max(preds))

    return CLASS_NAMES[idx], confidence