from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import requests

MODEL_PATH = "model.h5"

if not os.path.exists(MODEL_PATH):
    print("⬇️ Downloading model...")

    url = "https://drive.google.com/uc?export=download&id=11-gMkZkul3OYVLhl6ygIpzjg-PStnkeI"

    session = requests.Session()
    response = session.get(url, stream=True)

    with open(MODEL_PATH, "wb") as f:
        for chunk in response.iter_content(1024):
            if chunk:
                f.write(chunk)

    print("✅ Model downloaded")

model = load_model(MODEL_PATH)

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