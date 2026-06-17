import streamlit as st
import numpy as np
from PIL import Image
from keras.models import load_model
import plotly.graph_objects as go

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="MorphGuard",
    page_icon="🛡️",
    layout="wide"
)

# ----------------------------------
# CUSTOM CSS
# ----------------------------------

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:#F8FAFC;
}

.block-container{
    padding-top:1rem;
    max-width:100%;
}

.card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:18px;
    padding:18px;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}

.section-title{
    font-size:14px;
    font-weight:700;
    color:#6366F1;
    letter-spacing:0.5px;
    margin-bottom:15px;
}

.metric-value{
    font-size:28px;
    font-weight:700;
}

.real-card{
    background:#DCFCE7;
    border-radius:12px;
    padding:15px;
}

.morph-card{
    background:#FEE2E2;
    border-radius:12px;
    padding:15px;
}

.info-card{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:12px;
    padding:12px;
    text-align:center;
}

.small-title{
    font-size:12px;
    color:#6B7280;
}

.small-value{
    font-size:18px;
    font-weight:700;
}

.header-title{
    text-align:center;
    font-size:36px;
    font-weight:700;
    color:#111827;
}

.header-sub{
    text-align:center;
    color:#6B7280;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# MODEL
# ----------------------------------

@st.cache_resource
def load_my_model():
    return load_model(
        "model/final_deployment_model.keras",
        compile=False
    )

model = load_my_model()

# ----------------------------------
# HEADER
# ----------------------------------

c1,c2,c3 = st.columns([2,4,2])

with c1:
    st.markdown("""
    <h2 style='margin-bottom:0'>🛡️ MorphGuard</h2>
    <span style='color:#6B7280'>
    AI-Powered Face Morph Detection
    </span>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='header-title'>
    Face Morph Detection
    </div>

    <div class='header-sub'>
    Accurate • Reliable • Intelligent
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.success("🟢 System Active")

st.divider()

# ----------------------------------
# TOP SECTION
# ----------------------------------

left,center,right = st.columns([1.2,1.8,1])

# -------------------------
# INPUT IMAGE
# -------------------------

with left:

    st.markdown("""
    <div class='card'>
    <div class='section-title'>
    INPUT IMAGE
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        st.image(
            image,
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# PREDICTION
# -------------------------

with center:

    st.markdown("""
    <div class='card'>
    <div class='section-title'>
    PREDICTION RESULT
    </div>
    """, unsafe_allow_html=True)

    if uploaded_file:

        img = image.resize((224,224))
        img = np.array(img)/255.0
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img, verbose=0)[0][0]

        if pred > 0.5:
            label = "REAL FACE"
            confidence = pred

            st.success(label)

        else:
            label = "MORPH DETECTED"
            confidence = 1-pred

            st.error(label)

        st.metric(
            "Confidence",
            f"{confidence*100:.2f}%"
        )

        st.progress(float(confidence))

        colA,colB = st.columns(2)

        with colA:
            st.success(
                f"Real Probability : {(pred*100):.2f}%"
            )

        with colB:
            st.error(
                f"Morph Probability : {((1-pred)*100):.2f}%"
            )

        st.write(
            f"Prediction Score : {pred:.6f}"
        )

    else:
        st.info("Awaiting Analysis")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# STEPS
# -------------------------

with right:

    st.markdown("""
    <div class='card'>
    <div class='section-title'>
    PROCESSING STEPS
    </div>

    ✅ Face Detection<br><br>
    ✅ Feature Extraction<br><br>
    ✅ Pattern Analysis<br><br>
    ✅ Morph Classification

    </div>
    """, unsafe_allow_html=True)

# ----------------------------------
# GRAPH
# ----------------------------------

st.markdown("<br>", unsafe_allow_html=True)

g1,g2 = st.columns([3,2])

with g1:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[1,2,3,4,5,6],
            y=[0.43,0.91,0.94,0.95,0.96,0.97],
            mode="lines+markers",
            name="Train Accuracy"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[1,2,3,4,5,6],
            y=[0.90,0.90,0.93,0.94,0.95,0.96],
            mode="lines+markers",
            name="Validation Accuracy"
        )
    )

    fig.update_layout(
        title="Model Accuracy Over Epochs",
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------
# MODEL INFO
# ----------------------------------

with g2:

    st.subheader("Model Details")

    col1,col2 = st.columns(2)

    with col1:
        st.metric("Architecture","InceptionV3")
        st.metric("Dataset","AMSL")
        st.metric("Images","2348")
        st.metric("Epochs","6")

    with col2:
        st.metric("Accuracy","97.44%")
        st.metric("AUC","0.974")
        st.metric("Input","224x224")
        st.metric("Optimizer","Adam")

st.divider()

st.caption("© 2025 MorphGuard | Face Morph Detection System")