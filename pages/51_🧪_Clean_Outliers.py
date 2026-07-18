import pandas as pd
import streamlit as st

from workshop import outliers as ol, store_data as sd, ui

st.set_page_config(page_title="Outliers", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Outliers — the number that's too good to be true",
    "One fat-fingered order of $80,000 can swing your whole average. Outlier detection finds "
    "these before they poison a report — but deciding whether to delete or cap them is a "
    "judgement call, not an automatic one.",
)

base = sd.clean_orders(sd.messy_orders())["amount"].reset_index(drop=True)
data = ol.inject(base, n=6, seed=1)
method = st.radio("Detection method", ["iqr", "zscore"], horizontal=True)
k = st.slider("Sensitivity (k)", 1.0, 3.0, 1.5, 0.5)
mask, lo, hi = ol.detect(data, method, k)

c = st.columns(3)
c[0].metric("Outliers flagged", int(mask.sum()))
c[1].metric("Max before", f"${data.max():,.0f}")
treat = st.radio("Treatment", ["cap to bounds", "remove"], horizontal=True)
treated = ol.cap(data, lo, hi) if treat.startswith("cap") else ol.remove(data, mask)
c[2].metric("Max after", f"${treated.max():,.0f}")

st.markdown("#### Distribution after treatment")
st.bar_chart(pd.DataFrame({"amount": treated.value_counts(bins=20, sort=False).values}))
st.caption(f"Flagging anything outside [{lo:,.0f}, {hi:,.0f}]. "
           "Cap keeps the row but tames it; remove deletes it entirely.")
ui.leader_takeaway("An unexamined outlier is how a single typo becomes a wrong strategic decision.")
