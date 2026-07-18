import pandas as pd
import streamlit as st

from workshop import scaling as sc, store_data as sd, ui

st.set_page_config(page_title="Feature Scaling", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Feature Scaling — giving every feature a fair say",
    "If one column runs 0–5 and another runs 0–50,000, many models listen only to the big one. "
    "Scaling rewrites features onto a common range so each gets a fair vote — a small step that "
    "quietly decides whether a model works.",
)

amount = sd.clean_orders(sd.messy_orders())["amount"].reset_index(drop=True)
method = st.radio("Scaling method", ["min-max (0–1)", "z-score (mean 0, std 1)"], horizontal=True)
scaled = sc.minmax(amount) if method.startswith("min") else sc.zscore(amount)

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Before** (raw order amounts)")
    st.write(sc.summary(amount))
    st.bar_chart(pd.DataFrame({"count": amount.value_counts(bins=20, sort=False).values}))
with c2:
    st.markdown(f"**After** — {method}")
    st.write(sc.summary(scaled))
    st.bar_chart(pd.DataFrame({"count": scaled.value_counts(bins=20, sort=False).values}))

st.info("The **shape** is identical — only the axis changed. Min-max squeezes into 0–1; z-score "
        "centres on 0 with unit spread. Distance-based models (k-means, kNN) and neural nets need "
        "this; tree models don't care.")
ui.leader_takeaway("Unscaled features are a silent bug: the model isn't wrong, it's just been "
                   "listening to the loudest column.")
