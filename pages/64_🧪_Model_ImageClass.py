import matplotlib.pyplot as plt
import streamlit as st

from workshop import cv, ui, visuals


@st.cache_resource
def _model():
    return cv.train(seed=0)

st.set_page_config(page_title="Image Classification", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Image Classification — teaching a machine to see",
    "The same idea behind reading X-rays or scanning number plates: show a model enough labelled "
    "images and it learns to recognise what's in a new one. Here it reads handwritten digits.",
)

m = _model()
st.metric("Accuracy on unseen digits", f"{m['accuracy']*100:.1f}%")

i = st.slider("Pick a test image", 0, len(m["images"]) - 1, 0)
col1, col2 = st.columns([1, 2])
with col1:
    fig, ax = plt.subplots(figsize=(2.2, 2.2))
    ax.imshow(m["images"][i], cmap="gray_r")
    ax.axis("off")
    st.pyplot(fig)
with col2:
    pred = cv.predict(m["clf"], m["Xte"][i])
    true = int(m["yte"][i])
    st.markdown(f"### Model reads: **{pred}**")
    st.markdown(f"Actual label: **{true}**")
    st.success("✅ Correct") if pred == true else st.error("❌ Misread — even good models slip")

st.info("This is a small model on tiny 8×8 images. Real-world vision — cancer scans, self-driving "
        "— uses deep **CNNs** and **vision transformers** trained on millions of images, but the "
        "principle is identical: labelled images in, a prediction out.")
ui.leader_takeaway("Image classification is mature and everywhere; the hard part is rarely the "
                   "model — it's getting enough correctly-labelled images (see the Labeling demo).")
