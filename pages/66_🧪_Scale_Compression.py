import pandas as pd
import streamlit as st

from workshop import bigdata as bd, compression as cp, ui, visuals

st.set_page_config(page_title="Compression", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Serialization & Compression — smaller files, cheaper everything",
    "The format you save data in decides your storage bill and how fast every pipeline reads it. "
    "Switching from CSV to a compressed columnar format like Parquet routinely shrinks data "
    "several-fold — free savings, no data lost.",
)

n = st.select_slider("Dataset size (rows)", [50_000, 100_000, 200_000], value=100_000)
df = bd.make_big(n=n, seed=0)
sizes = cp.sizes(df)

st.markdown("#### Same data, three ways to store it")
size_df = pd.DataFrame({"format": list(sizes),
                        "megabytes": [round(v / 1e6, 2) for v in sizes.values()]})
st.bar_chart(size_df, x="format", y="megabytes", color=visuals.PALETTE[0])
ratio = sizes["CSV"] / sizes["Parquet"]
st.success(f"**Parquet is {ratio:.1f}× smaller than CSV** here — less storage, less network, "
           "less cost, at every step of every pipeline.")

st.markdown("#### Read speed (full-table load)")
speed = cp.read_speed_ms(df)
c = st.columns(2)
c[0].metric("CSV read", f"{speed['CSV']} ms")
c[1].metric("Parquet read", f"{speed['Parquet']} ms")
st.caption("For a full-table load the two are close; Parquet's real speed win is **columnar** — "
           "an analytics query reads only the columns it needs, skipping the rest entirely.")
ui.leader_takeaway("Defaulting analytics data to Parquet is one config change that quietly cuts "
                   "storage and compute bills across the whole stack.")
