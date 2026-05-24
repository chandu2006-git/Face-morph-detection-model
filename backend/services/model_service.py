from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import os

# 🔥 Build model
def build_model():
    base_model = InceptionV3(
        weights=None,
        include_top=False,
        input_shape=(224, 224, 3)
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=output)
    return model

# 🔥 Build model
model = build_model()

# 🔥 Absolute path fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../../model/final_weights.weights.h5")

model.load_weights(MODEL_PATH)

print("✅ Model ready for inference")

print("✅ Model ready for inference")

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