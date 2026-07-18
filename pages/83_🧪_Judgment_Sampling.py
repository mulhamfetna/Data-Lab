import numpy as np
import pandas as pd
import streamlit as st

from workshop import sampling as sm, ui

st.set_page_config(page_title="Sampling Bias", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Sampling Bias — who you ask decides the answer",
    "A survey is only as honest as its sample. Poll only the customers who still love you and "
    "you'll 'prove' everyone's delighted — while the unhappy ones already left and were never "
    "asked. The bias is invisible in the result; it's baked into who showed up.",
)

pop = sm.population()
bias = st.slider("How much do you over-survey your happiest customers?", 0.0, 4.0, 0.0, 0.5)
sample = sm.biased_sample(pop, bias)
est = sm.estimates(pop, sample)

c = st.columns(3)
c[0].metric("True satisfaction (everyone)", est["true_mean"])
c[1].metric("Your survey says", est["sample_mean"], f"{est['gap']:+.1f}")
c[2].metric("Overstatement", f"{est['gap']:+.1f} pts")

chart = pd.DataFrame({"value": np.concatenate([pop, sample]),
                      "group": ["everyone"] * len(pop) + ["your sample"] * len(sample)})
st.bar_chart(chart.pivot_table(index=pd.cut(chart["value"], 20, labels=False),
                               columns="group", values="value", aggfunc="count").fillna(0))
if est["gap"] > 3:
    st.error("Your sample sits well above the true population — a rosy number built on who you "
             "chose to ask.")
else:
    st.success("A fair, representative sample lands right on the true value.")
ui.leader_takeaway("Before trusting any survey, ask *who was left out* — the missing voices are "
                   "usually the ones that would change the answer.")
