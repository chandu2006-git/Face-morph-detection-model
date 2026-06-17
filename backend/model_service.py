from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import tensorflow as tf

print("=" * 60)
print("TensorFlow Version:", tf.__version__)
print("=" * 60)

MODEL = None


def load_my_model():
    global MODEL

    if MODEL is None:

        print("Loading deployment model...")

        MODEL = load_model(
            "model/final_deployment_model.keras",
            compile=False
        )

        print("MODEL LOADED SUCCESSFULLY")
        print("MODEL PARAMETERS:", MODEL.count_params())

    return MODEL


def preprocess_image(file):

    img = Image.open(file).convert("RGB")

    img = img.resize((224, 224))

    img = np.array(img, dtype=np.float32)

    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img


def predict_image(file):

    model = load_my_model()

    image = preprocess_image(file)

    print("=" * 60)
    print("IMAGE SHAPE :", image.shape)
    print("IMAGE MIN   :", np.min(image))
    print("IMAGE MAX   :", np.max(image))
    print("=" * 60)

    prediction = model.predict(
        image,
        verbose=0
    )[0][0]

    print("=" * 60)
    print("RAW PREDICTION :", float(prediction))
    print("=" * 60)

    real_prob = float(prediction)
    morph_prob = float(1 - prediction)

    if prediction > 0.5:

        label = "REAL"
        confidence = real_prob * 100

    else:

        label = "MORPH"
        confidence = morph_prob * 100

    result = {
        "label": label,
        "confidence": round(confidence, 2),
        "real_probability": round(real_prob * 100, 2),
        "morph_probability": round(morph_prob * 100, 2),
        "raw_prediction": float(prediction)
    }

    print("RESULT:", result)

    return result