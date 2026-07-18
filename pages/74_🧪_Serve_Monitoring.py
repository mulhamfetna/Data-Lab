import pandas as pd
import streamlit as st

from workshop import monitoring as mon, ui

st.set_page_config(page_title="Monitoring", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Monitoring & Retraining — keeping a model alive",
    "Deploying a model is the start, not the finish. Left alone it decays as the world moves. The "
    "MLOps loop — monitor, detect the drop, retrain, redeploy — is what keeps it earning instead "
    "of quietly going wrong.",
)

retrain = st.toggle("Retrain when accuracy drops?", value=True)
retrain_week = 8 if retrain else None
acc = mon.accuracy_over_time(weeks=16, retrain_week=retrain_week, seed=0)

st.line_chart(pd.DataFrame({"week": range(len(acc)), "accuracy": acc}), x="week", y="accuracy")

if retrain:
    st.success("At week 8 the team retrained on fresh data — accuracy jumps back up. This is the "
               "loop: **monitor → detect decay → retrain → redeploy**, forever.")
else:
    st.error(f"No retraining: accuracy slid from {acc[0]*100:.0f}% to {acc[-1]*100:.0f}% while "
             "everyone assumed the model was 'done'. This is how models fail — silently.")
st.caption("Drift monitoring (previous demo) is the trigger; retraining is the response. Together "
           "they're most of what 'MLOps' means.")
ui.leader_takeaway("A model is a product with maintenance, not a project you finish — budget for "
                   "the loop, not just the launch.")
