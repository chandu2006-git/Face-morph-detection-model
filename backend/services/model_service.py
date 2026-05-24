from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import gdown

# 🔥 Global model
model = None

# 🔥 Lazy load full model
def get_model():
    global model

    if model is None:
        print("🚀 Initializing model...")

        MODEL_PATH = "model.h5"

        if not os.path.exists(MODEL_PATH):
            print("⬇️ Downloading model...")

            url = "https://drive.google.com/uc?id=11-gMkZkul3OYVLhl6ygIpzjg-PStnkeI"
            gdown.download(url, MODEL_PATH, quiet=False)

            print("✅ Model downloaded")

        print("📦 Loading model...")
        model = load_model(MODEL_PATH)
        print("✅ Model ready for inference")

    return model


# 🔥 Preprocess image
def preprocess(image):
    image = image.resize((299, 299))   # ✅ IMPORTANT
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


# 🔥 Prediction function
def predict_image(file):
    model = get_model()

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