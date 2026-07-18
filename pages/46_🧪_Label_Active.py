import pandas as pd
import streamlit as st

from workshop import active, ui

st.set_page_config(page_title="Active Learning", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Active Learning — label the examples that actually matter",
    "Labeling is the expensive part, so don't label at random. Let the model tell you which "
    "few examples it's most confused about, label those first, and reach the same accuracy for "
    "a fraction of the labeling cost.",
)

steps = st.slider("Labeling budget (examples)", 5, 18, 18)
rand = active.learning_curve("random", seed=0, steps=steps)
unc = active.learning_curve("uncertainty", seed=0, steps=steps)

curve = pd.DataFrame({"labels": range(2, 2 + len(rand)),
                      "random order": rand, "smart (uncertainty)": unc})
st.line_chart(curve, x="labels", y=["random order", "smart (uncertainty)"])

st.success(f"With a budget of {steps} labels, smart selection reaches "
           f"**{unc[-1]*100:.0f}%** vs **{rand[-1]*100:.0f}%** for random — same effort, "
           "more accuracy, because it spent the budget on the confusing cases near the boundary.")
ui.leader_takeaway("Active learning is how teams cut labeling costs by half or more — a direct "
                   "budget lever on any AI project.")
