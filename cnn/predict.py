import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os

IMG_SIZE = 224

# Class names must match your folder names exactly
CLASS_NAMES = ['abrasion', 'bruise', 'burn', 'cut', 'normal', 'rash']

# Load best model
model = tf.keras.models.load_model("cnn/models/best_skin_cnn.h5")

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))

    predicted_class = CLASS_NAMES[predicted_index]

    return predicted_class, confidence


if __name__ == "__main__":
    test_path = input("Enter image path: ").strip().replace('"', '')
    label, conf = predict_image(test_path)
    print(f"\nPrediction: {label}")
    print(f"Confidence: {conf:.2f}")