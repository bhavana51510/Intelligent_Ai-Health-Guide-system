import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Load trained CNN model
model = load_model("models/image_cnn_model.h5")

# Class labels (must match training order)
CLASS_NAMES = [
    "minor_burn",
    "cut_wound",
    "bee_sting",
    "skin_rash",
    "eye_redness"
]

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = model.predict(img_array)
    class_index = np.argmax(prediction)

    return CLASS_NAMES[class_index]