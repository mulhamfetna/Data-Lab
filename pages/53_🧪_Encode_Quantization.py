import numpy as np
import pandas as pd
import streamlit as st

from workshop import quantize as qz, ui

st.set_page_config(page_title="Quantization", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Quantization — smaller data, almost the same meaning",
    "Quantization keeps fewer distinct values — fewer colors in an image, fewer decimals in a "
    "number, buckets instead of exact ages. It's how images compress and how giant AI models "
    "shrink to run on your phone, trading a little precision for a lot of size.",
)

img = qz.make_demo_image()
n = st.slider("Number of colors", 2, 64, 8)
q = qz.quantize_image(img, n)

c1, c2 = st.columns(2)
with c1:
    st.markdown(f"**Original** — {qz.unique_colors(img):,} colors · {qz.png_bytes(img)/1024:.1f} KB")
    st.image(img, use_container_width=True)
with c2:
    st.markdown(f"**Quantized to {n}** — {qz.unique_colors(q)} colors · {qz.png_bytes(q)/1024:.1f} KB")
    st.image(q, use_container_width=True)

st.success(f"Down to {n} colors and the picture is still readable — that's quantization: shrink "
           "the data, keep the meaning.")

st.markdown("#### The same idea on numbers: exact ages → buckets")
ages = pd.Series(np.random.default_rng(0).integers(18, 70, 400))
bins = st.slider("Number of age buckets", 2, 10, 5)
st.bar_chart(qz.bin_series(ages, bins))
ui.leader_takeaway("Quantization is why a 4K photo fits in a text message and why huge AI models "
                   "can run on a laptop — controlled loss of precision for massive savings.")
