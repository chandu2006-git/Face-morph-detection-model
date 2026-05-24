import os
import gdown
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

MODEL_PATH = "model/final_render_model.h5"

# 🔥 DOWNLOAD MODEL
if not os.path.exists(MODEL_PATH):
    print("Downloading model from Drive...")

    url = "https://drive.google.com/uc?id=1gc3nQRwg2tPbdCeH3YKIoAobWTHW3lZ9"
    os.makedirs("model", exist_ok=True)
    gdown.download(url, MODEL_PATH, quiet=False)

    print("Model downloaded ✅")

# 🔥 LOAD MODEL
print("Loading model...")
model = load_model(MODEL_PATH, compile=False)
print("Model loaded successfully ✅")


def predict_image(file):
    img = Image.open(file).convert("RGB")
    img = img.resize((299, 299))

    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0][0]

    print("PRED:", pred)

    return {
        "prediction": "Morph" if pred > 0.5 else "Real",
        "confidence": float(pred),
        "real_prob": float(1 - pred),
        "morph_prob": float(pred)
    }