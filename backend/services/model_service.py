import os
import gdown
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from backend.config import MODEL_PATH, MODEL_URL

# 🔥 DOWNLOAD MODEL IF NOT EXISTS
if not os.path.exists(MODEL_PATH):
    print("⬇️ Downloading model...")
    os.makedirs("model", exist_ok=True)
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    print("✅ Model downloaded")

# 🔥 LOAD MODEL
print("🚀 Loading model...")
model = load_model(MODEL_PATH, compile=False)
print("✅ Model loaded successfully")


def predict_image(file):
    try:
        img = Image.open(file).convert("RGB")
        img = img.resize((299, 299))

        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)[0][0]

        return {
            "prediction": "Morph" if pred > 0.5 else "Real",
            "confidence": float(pred),
            "real_prob": float(1 - pred),
            "morph_prob": float(pred)
        }

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return {"error": str(e)}