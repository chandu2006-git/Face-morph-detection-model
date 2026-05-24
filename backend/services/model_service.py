from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import os
import gdown

model = None

def build_model():
    base_model = InceptionV3(
        weights=None,
        include_top=False,
        input_shape=(299, 299, 3)   # ✅ CORRECT
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)   # must match training
    x = Dropout(0.5)(x)
    output = Dense(1, activation='sigmoid')(x)
     
    return Model(inputs=base_model.input, outputs=output)


def get_model():
    global model

    if model is None:
        print("🚀 Loading model...")

        model = build_model()

        WEIGHTS_PATH = "weights.h5"

        if not os.path.exists(WEIGHTS_PATH):
            print("⬇️ Downloading weights...")
            url = "https://drive.google.com/uc?id=1yLEYFHtPmInxoQOm10YweX0tKRjnlr02"
            gdown.download(url, WEIGHTS_PATH, quiet=False)
            print("✅ Weights downloaded")

        model.load_weights(WEIGHTS_PATH)
        print("✅ Model ready")

    return model


def preprocess(image):
    image = image.resize((299, 299))   # ✅ CORRECT
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)


def predict_image(file):
    model = get_model()

    image = Image.open(file).convert("RGB")
    processed = preprocess(image)

    prediction = model.predict(processed)[0][0]

    return {
        "prediction": "Morph" if prediction >= 0.5 else "Real",
        "confidence": float(prediction),
        "real_prob": float(1 - prediction),
        "morph_prob": float(prediction)
    }