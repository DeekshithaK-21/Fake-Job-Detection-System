import sys
import os
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.predict import predict_pipeline
from embeddings.distilbert_embedder import load_model
from PIL import Image

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Fraudulent Job Detection", layout="wide")

# ---------------- PRELOAD MODEL ----------------
@st.cache_resource
def preload():
    load_model()
    return True

with st.spinner("🚀 Initializing AI model..."):
    preload()

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = None

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "last_input_type" not in st.session_state:
    st.session_state.last_input_type = None

# ---------------- BLUE THEME ----------------
st.markdown("""
<style>
body { background-color: #f4f8ff; }

h1, h2, h3 { color: #1e40af; }

.block-container { padding-top: 2rem; }

.stButton>button {
    background: linear-gradient(90deg, #2563eb, #60a5fa);
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background: #1d4ed8;
}

.preview-box {
    border: 2px dashed #93c5fd;
    padding: 10px;
    border-radius: 10px;
    background: #eff6ff;
    text-align: center;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    text-align: center;
}

.fake { background: #fee2e2; color: #b91c1c; }
.real { background: #dcfce7; color: #166534; }
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🔍 Fraudulent Job Detection System")
st.write("AI-powered job post verification")

st.markdown("---")

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 1])

# ---------------- LEFT PANEL ----------------
with left:
    st.subheader("📥 Input")

    input_type = st.selectbox("Select Input Type", ["Text", "Image", "PDF"])

    # Reset when input type changes
    if st.session_state.last_input_type != input_type:
        st.session_state.result = None
        st.session_state.analyzed = False

    st.session_state.last_input_type = input_type

    uploaded_file = None
    text_input = None

    if input_type == "Text":
        text_input = st.text_area("Enter Job Description", height=200)

    else:
        uploaded_file = st.file_uploader("Upload File", type=["png", "jpg", "jpeg", "pdf"])

        if uploaded_file:
            st.markdown("### Preview")
            st.markdown('<div class="preview-box">', unsafe_allow_html=True)

            if input_type == "Image":
                image = Image.open(uploaded_file).convert("RGB")
                st.image(image, use_column_width=True)

            elif input_type == "PDF":
                st.info("📄 PDF preview not supported in Streamlit")

            st.markdown('</div>', unsafe_allow_html=True)

    analyze = st.button("🔍 Analyze")
    clear = st.button("🧹 Clear")

    if clear:
        st.session_state.result = None
        st.session_state.analyzed = False

# ---------------- RIGHT PANEL ----------------
with right:
    st.subheader("📊 Result")

    if analyze:
        st.session_state.analyzed = True

        if input_type == "Text" and not text_input:
            st.warning("Enter text first")
            st.session_state.result = None

        elif input_type != "Text" and not uploaded_file:
            st.warning("Upload file first")
            st.session_state.result = None

        else:
            with st.spinner("Analyzing..."):

                if input_type == "Text":
                    result = predict_pipeline(text_input, "text")

                else:
                    # -------- FIXED FILE SAVING --------
                    upload_dir = "uploads"
                    os.makedirs(upload_dir, exist_ok=True)

                    uploaded_file.seek(0)  # CRITICAL

                    file_bytes = uploaded_file.getvalue()

                    unique_name = str(uuid.uuid4()) + "_" + uploaded_file.name
                    file_path = os.path.join(upload_dir, unique_name)

                    with open(file_path, "wb") as f:
                        f.write(file_bytes)

                    # DEBUG
                    st.write("Saved path:", file_path)
                    st.write("File size:", os.path.getsize(file_path))

                    result = predict_pipeline(file_path, input_type.lower())

            st.session_state.result = result

    # -------- DISPLAY RESULT --------
    if st.session_state.analyzed and st.session_state.result:

        result = st.session_state.result

        if result["prediction"] == "Fake":
            st.markdown('<div class="result-box fake">🚨 HIGH RISK DETECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-box real">✅ VERIFIED SAFE</div>', unsafe_allow_html=True)

        fake = result["confidence"]["fake"]
        real = result["confidence"]["real"]

        st.write(f"Fake: {fake} | Real: {real}")
        st.progress(fake)

        st.markdown("### ⚠ Suspicious Words")

        if result["suspicious_words"]:
            for word in result["suspicious_words"]:
                st.markdown(f"- {word}")
        else:
            st.write("No suspicious words detected")

    else:
        st.info("Upload or enter data to analyze")