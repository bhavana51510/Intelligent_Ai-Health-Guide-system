import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# ==============================
# Paths
# ==============================
TRAIN_DIR = "cnn/dataset/train"
VAL_DIR = "cnn/dataset/val"
MODEL_PATH = "cnn/minor_symptom_cnn.h5"

IMG_SIZE = (224, 224)
BATCH_SIZE = 8
EPOCHS = 15

# ==============================
# Data Generators
# ==============================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    zoom_range=0.15,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

val_data = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

NUM_CLASSES = len(train_data.class_indices)
print("Classes:", train_data.class_indices)

# ==============================
# CNN MODEL
# ==============================
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(64, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(128, (3,3), activation="relu"),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.4),
    layers.Dense(NUM_CLASSES, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==============================
# TRAIN
# ==============================
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ==============================
# SAVE MODEL
# ==============================
model.save(MODEL_PATH)
print("MODEL SAVED ->", MODEL_PATH)