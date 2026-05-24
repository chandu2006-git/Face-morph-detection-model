from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Step 1: Build architecture
def build_model():
    base_model = InceptionV3(
        weights=None,
        include_top=False,
        input_shape=(224, 224, 3)
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)   # IMPORTANT: must match training
    output = Dense(1, activation='sigmoid')(x)

    model = Model(inputs=base_model.input, outputs=output)
    return model

# Step 2: Create model
model = build_model()

# Step 3: Load weights (ONLY THIS)
model.load_weights("model/final_weights.weights.h5")

print("✅ Model rebuilt & weights loaded successfully")