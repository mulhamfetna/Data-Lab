import pandas as pd
import streamlit as st

from workshop import montecarlo as mc, ui

st.set_page_config(page_title="Monte Carlo", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Monte Carlo — run the future 10,000 times",
    "‘We’ll make $500’ is a guess dressed as a fact. The real questions are *what’s the range?* "
    "and *what’s the chance we lose money?* Monte Carlo answers both: simulate the outcome "
    "thousands of times, drawing the uncertain inputs from realistic ranges, and read the risk "
    "straight off the distribution.",
)

st.markdown("### A product launch with uncertain demand and margin")
c = st.columns(3)
units_mean = c[0].slider("Expected units sold", 200, 900, 500, 50)
margin_mean = c[1].slider("Expected margin per unit ($)", 2.0, 12.0, 6.0, 0.5)
fixed = c[2].slider("Fixed launch cost ($)", 1000, 4000, 2500, 250)
uncertainty = st.slider("How uncertain are we? (spread)", 0.05, 0.6, 0.3, 0.05,
                        help="Higher = wider ranges on demand and margin.")

outcomes = mc.simulate(units_mean=units_mean, units_sd=units_mean * uncertainty,
                       margin_mean=margin_mean, margin_sd=margin_mean * uncertainty,
                       fixed_cost=fixed)
s = mc.summary(outcomes)

c1, c2, c3 = st.columns(3)
c1.metric("Expected profit", f"${s['mean']:,.0f}")
c2.metric("90% range", f"${s['p5']:,.0f} … ${s['p95']:,.0f}")
c3.metric("Chance of a loss", f"{s['prob_loss']*100:.0f}%")

centers, counts = mc.histogram(outcomes)
hist = pd.DataFrame({"profit ($)": centers.round(0), "outcomes": counts})
st.bar_chart(hist, x="profit ($)", y="outcomes")

if s["prob_loss"] >= 0.25:
    st.error(f"About **{s['prob_loss']*100:.0f}%** of futures lose money — a single-number "
             "forecast would have hidden that risk entirely.")
else:
    st.success(f"Only about **{s['prob_loss']*100:.0f}%** of futures lose money — but you now "
               "know the downside, not just the average.")

ui.leader_takeaway("When someone hands you one number for an uncertain outcome, ask for the "
                   "distribution. The average rarely happens; the *range* and the *chance of "
                   "loss* are what you actually manage.")
ui.footer()
