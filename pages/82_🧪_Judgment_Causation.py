import streamlit as st

from workshop import causation as ca, ui

st.set_page_config(page_title="Correlation vs Causation", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Correlation ≠ Causation — the trap that launches bad strategies",
    "Two things move together, so one must cause the other — right? That leap is behind countless "
    "wasted budgets. The real driver is often a hidden third factor you forgot to look for.",
)

df = ca.data()
c = ca.correlations(df)

st.markdown("#### Ice-cream sales and drownings rise together")
st.scatter_chart(df, x="ice_cream_sales", y="drownings")
st.error(f"They correlate at **{c['ice_cream_vs_drownings']}** — strong! So… ban ice cream to "
         "stop drownings?")

st.markdown("#### The hidden cause")
col1, col2 = st.columns(2)
col1.metric("Temperature → ice-cream sales", c["temp_vs_ice_cream"])
col2.metric("Temperature → drownings", c["temp_vs_drownings"])
st.success("**Temperature drives both.** Hot days → more ice cream *and* more swimming (so more "
           "drownings). Ice cream causes nothing — the confounder explains the whole link.")
st.info("Before acting on a correlation, ask: **what third thing could cause both?** and **would "
        "changing one actually change the other?**")
ui.leader_takeaway("Acting on correlation as if it were cause is how organisations spend money "
                   "fixing the wrong thing — always hunt for the confounder.")
