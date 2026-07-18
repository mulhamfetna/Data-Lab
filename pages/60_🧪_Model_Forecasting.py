import pandas as pd
import streamlit as st

from workshop import forecasting as fc, ui

st.set_page_config(page_title="Forecasting", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Forecasting — next quarter, before it happens",
    "The past holds the shape of the future. Forecasting projects the trend forward — with an "
    "honest band of uncertainty — so you can plan stock, staff, and cash instead of reacting.",
)

periods = st.slider("Months to forecast", 3, 12, 6)
hist = fc.history()
fut = fc.forecast(hist, periods=periods)

chart = pd.concat([
    hist.rename(columns={"sales": "value"}).assign(kind="history")[["month", "value", "kind"]],
    fut.rename(columns={"forecast": "value"}).assign(kind="forecast")[["month", "value", "kind"]],
])
st.line_chart(chart, x="month", y="value", color="kind")

nxt = fut.iloc[0]
st.success(f"**Next month's projected sales: {nxt['forecast']:.0f}** "
           f"(likely between {nxt['lower']:.0f} and {nxt['upper']:.0f}).")
st.dataframe(fut, use_container_width=True)
st.caption("The band matters as much as the line: a forecast without uncertainty is a guess "
           "wearing a suit.")
ui.leader_takeaway("A forecast turns 'we'll see' into a plannable number with a stated "
                   "confidence range — the basis of every budget.")
