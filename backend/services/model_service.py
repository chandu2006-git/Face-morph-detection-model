from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import requests
import gdown


print("🚀 Starting model service...")

MODEL_PATH = "model.h5"

if not os.path.exists(MODEL_PATH):
    print("⬇️ Downloading model...")

    url = "https://drive.google.com/uc?id=11-gMkZkul3OYVLhl6ygIpzjg-PStnkeI"
    gdown.download(url, MODEL_PATH, quiet=False)

    print("✅ Model downloaded")

print("📦 Loading model now...")
model = load_model(MODEL_PATH)
print("✅ Model fully loaded")
print("✅ Full model loaded")

# 🔥 Preprocess
def preprocess(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# 🔥 Predict
def predict_image(file):
    image = Image.open(file).convert("RGB")
    processed = preprocess(image)

    prediction = model.predict(processed)[0][0]

    if prediction >= 0.5:
        label = "Morph"
    else:
        label = "Real"

    return {
        "prediction": label,
        "confidence": float(prediction),
        "real_prob": float(1 - prediction),
        "morph_prob": float(prediction)
    }