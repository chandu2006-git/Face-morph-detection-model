from backend.model_architecture import build_model
from PIL import Image
import numpy as np

MODEL = None


def load_my_model():
    global MODEL

    if MODEL is None:
        print("Loading deployment model...")

        MODEL = build_model()

        MODEL.load_weights(
            "model/inception_weights_v2.weights.h5"
        )

        print("DEPLOYMENT MODEL LOAD SUCCESS")

    return MODEL


def preprocess_image(file):
    img = Image.open(file).convert("RGB")

    img = img.resize((224, 224))

    img = np.array(img)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img


def predict_image(file):

    model = load_my_model()

    image = preprocess_image(file)

    prediction = model.predict(image)[0][0]

    real_prob = float(prediction)
    morph_prob = float(1 - prediction)

    if prediction >= 0.5:
        label = "REAL"
        confidence = real_prob * 100
    else:
        label = "MORPH"
        confidence = morph_prob * 100

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "real_probability": round(real_prob * 100, 2),
        "morph_probability": round(morph_prob * 100, 2),
        "raw_prediction": float(prediction)
    }