import streamlit as st

from workshop import misleading as ms, ui

st.set_page_config(page_title="Misleading Charts", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Misleading Charts — the same data, two opposite stories",
    "A chart can lie without changing a single number — just crop the axis. The most common trick "
    "in a bad slide deck is a y-axis that doesn't start at zero, turning a 4% wobble into a "
    "'skyrocketing' success. Learn to spot it and you can't be sold it.",
)

df = ms.series()
truncate = st.toggle("Start the y-axis near the data (truncate it)", value=True)
st.pyplot(ms.bar_fig(df, truncate))

if truncate:
    st.error("📈 Looks like explosive growth! — but the axis starts at 99. It's a **4% rise "
             "over six months** dressed up as a rocket.")
else:
    st.success("📊 The honest version (axis from 0): the same numbers, a modest, truthful trend.")

st.info("Spotting-the-trick checklist: **Does the y-axis start at zero? What's the actual range? "
        "Is the time window cherry-picked?**")
ui.leader_takeaway("When a chart looks dramatic, check the axis before you feel impressed — the "
                   "drama is often in the scale, not the data.")
