import time

import pandas as pd
import streamlit as st

from workshop import streaming, ui

st.set_page_config(page_title="Streaming", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Streaming — data that never stops",
    "Some data doesn't arrive as a tidy file — it flows in continuously: every order, tap, "
    "or sensor reading, live. The skill is acting on it *as it arrives*, not waiting for a "
    "nightly batch.",
)

st.markdown("**Batch** = process a pile once a day. **Stream** = process each event the moment "
            "it lands. Press play and watch Nour Store's orders arrive live.")

speed = st.select_slider("Feed speed", ["slow", "normal", "fast"], value="normal")
delay = {"slow": 0.35, "normal": 0.15, "fast": 0.05}[speed]

if st.button("▶️ Start live feed", type="primary"):
    events = streaming.make_events(n=40, seed=0)
    metric_row = st.empty()
    table = st.empty()
    seen = []
    for e in events:
        seen.append(e)
        tot = streaming.running_totals(seen)
        with metric_row.container():
            c = st.columns(3)
            c[0].metric("Events processed", tot["events"])
            c[1].metric("Units sold", tot["units"])
            c[2].metric("Running revenue", f"${tot['revenue']:,.2f}")
        table.dataframe(pd.DataFrame(seen[::-1]).head(12), use_container_width=True)
        time.sleep(delay)
    st.success("Stream complete — every metric updated on each event, not at the end.")
    ui.leader_takeaway("Streaming lets you react in seconds (fraud, stock-outs, surges) instead "
                       "of finding out tomorrow.")
else:
    st.info("Press **Start live feed** to watch events stream in.")
