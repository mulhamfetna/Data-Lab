import pandas as pd
import streamlit as st

from workshop import imputation as im, store_data as sd, ui

st.set_page_config(page_title="Imputation", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Imputation — filling the gaps without lying",
    "Real data has holes. You can drop the rows (and lose information), or fill them — but every "
    "fill is an assumption. Choosing how to fill missing values quietly shapes every number that "
    "follows.",
)

base = sd.clean_orders(sd.messy_orders())["amount"].reset_index(drop=True)
frac = st.slider("How much data is missing?", 0.05, 0.4, 0.15, 0.05)
gapped = im.with_missing(base, frac=frac, seed=0)
method = st.radio("Fill strategy", ["mean", "median", "zero", "drop"], horizontal=True)
filled = im.impute(gapped, method)

st.markdown("#### Effect on the numbers")
comp = pd.DataFrame({"original (no gaps)": im.summary(base),
                     "with gaps": im.summary(gapped),
                     f"after '{method}'": im.summary(filled)}).T
st.dataframe(comp, use_container_width=True)

st.markdown("#### Distribution before vs after filling")
st.bar_chart(pd.DataFrame({"after fill": filled.value_counts(bins=15, sort=False).values}))
if method == "zero":
    st.warning("Filling with zero drags the average down — a convenient lie that biases every "
               "downstream metric.")
elif method == "drop":
    st.info("Dropping is honest but throws away real rows — costly when data is scarce.")
else:
    st.success(f"'{method}' keeps every row and barely moves the average — usually the safe default.")
ui.leader_takeaway("How you handle missing data is a hidden assumption baked into every report — "
                   "ask your analyst which fill they used.")
