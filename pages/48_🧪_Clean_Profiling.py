import streamlit as st

from workshop import profiling, store_data as sd, ui

st.set_page_config(page_title="Data Profiling", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Data Profiling — the automated health check",
    "Before you trust any dataset, profile it: how much is missing, what's the range, where "
    "are the duplicates. One glance tells you whether the data is safe to build on — or a trap.",
)

which = st.radio("Profile which version of the orders?", ["Raw (messy)", "Cleaned"], horizontal=True)
df = sd.messy_orders() if which == "Raw (messy)" else sd.clean_orders(sd.messy_orders())
rep = profiling.profile(df)

c = st.columns(3)
c[0].metric("Rows", f"{rep['rows']:,}")
c[1].metric("Columns", rep["cols"])
c[2].metric("Quality warnings", len(rep["warnings"]))

st.dataframe(rep["table"], use_container_width=True)
if rep["warnings"]:
    st.markdown("#### Warnings")
    for w in rep["warnings"]:
        st.markdown("- " + w)
else:
    st.success("No quality warnings — this dataset is safe to build on.")
ui.leader_takeaway("A 10-second profile catches the problems that would otherwise surface as a "
                   "wrong number in next quarter's board deck.")
