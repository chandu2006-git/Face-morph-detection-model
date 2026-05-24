from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np
from PIL import Image
import os
import gdown

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

model = build_model()

# 🔥 Download weights
WEIGHTS_PATH = "weights.h5"

if not os.path.exists(WEIGHTS_PATH):
    print("⬇️ Downloading weights...")

    url = "YOUR_WEIGHTS_LINK"   # <-- replace this
    gdown.download(url, WEIGHTS_PATH, quiet=False)

    print("✅ Weights downloaded")

# 🔥 Load weights
model.load_weights(WEIGHTS_PATH)

print("✅ Model ready for inference")