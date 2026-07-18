import pandas as pd
import streamlit as st

from workshop import byod, profiling, ui

st.set_page_config(page_title="Bring Your Own Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Bring Your Own Data — run the lab on *your* numbers",
    "Everything you've seen on Nour Store works on your real data too. Upload a CSV and watch it "
    "get profiled, charted, and questioned — the lifecycle, live, on data you brought.",
)

up = st.file_uploader("Upload a CSV", type=["csv"])
if up is None:
    st.info("No file yet — upload any CSV (customers, sales, survey results…) to begin. "
            "Nothing is stored; it stays in this session.")
    st.stop()

df = pd.read_csv(up)
s = byod.summary(df)
c = st.columns(4)
c[0].metric("Rows", f"{s['rows']:,}")
c[1].metric("Columns", s["cols"])
c[2].metric("Numeric", s["numeric"])
c[3].metric("Text/category", s["categorical"])

st.markdown("#### Preview")
st.dataframe(df.head(20), use_container_width=True)

st.markdown("#### Automated quality profile")
rep = profiling.profile(df)
st.dataframe(rep["table"], use_container_width=True)
for w in rep["warnings"]:
    st.markdown("- " + w)

st.markdown("#### Chart a column")
col = st.selectbox("Column", list(df.columns))
if col in byod.numeric_cols(df):
    st.bar_chart(pd.DataFrame({"count": df[col].value_counts(bins=20, sort=False).values}))
else:
    st.bar_chart(df[col].value_counts().head(20))
ui.leader_takeaway("The exact same tools apply to your data — the demos aren't a toy, they're the "
                   "real workflow at small scale.")
