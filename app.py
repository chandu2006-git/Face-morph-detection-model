import streamlit as st
import numpy as np
from PIL import Image
import os
from tensorflow.keras.models import load_model

@st.cache_resource
def load_my_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "FINAL_CLEAN_MODEL(1).h5")
    
    return load_model("model/final_clean_model.h5", compile=False)

model = load_my_model()

st.title("🧠 Face Morph Detection")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image)

    img = image.resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0][0]

    if pred > 0.5:
        st.error(f"⚠️ Morph ({pred:.2f})")
    else:
        st.success(f"✅ Real ({1-pred:.2f})")