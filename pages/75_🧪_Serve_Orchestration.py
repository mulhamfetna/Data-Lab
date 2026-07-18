import streamlit as st

from workshop import ui

st.set_page_config(page_title="Orchestration", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Orchestration — the pipeline that runs itself at 2am",
    "A data pipeline you have to run by hand isn't a system — it's a chore that gets forgotten. "
    "Orchestration schedules every step in the right order, retries failures, and alerts a human "
    "only when something actually breaks. It's what makes 'the numbers are ready every morning' "
    "true.",
)

st.markdown("#### A scheduled pipeline (a DAG — directed acyclic graph)")
st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent"; node[shape=box,style="rounded,filled",fontname=sans,color="#c9ccd1"];
  extract[label="Extract\\norders", fillcolor="#cfe6f5"];
  api[label="Fetch\\nrates (API)", fillcolor="#cfe6f5"];
  clean[label="Clean", fillcolor="#fbe6c2"];
  transform[label="Build\\nstar schema", fillcolor="#fbe6c2"];
  load[label="Load\\nto warehouse", fillcolor="#d4efe4"];
  report[label="Refresh\\ndashboard", fillcolor="#c9f0d8", shape=oval];
  train[label="Retrain\\nmodel", fillcolor="#c9f0d8", shape=oval];
  extract -> clean; api -> transform; clean -> transform -> load;
  load -> report; load -> train;
  label="⏰ runs every night at 02:00"; labelloc="b"; fontname="sans"; }
""")
st.caption("Each box is a task; arrows are dependencies. The scheduler runs them in order, only "
           "starting a step when its inputs are ready — and retries the one that fails without "
           "redoing the rest.")

st.markdown("#### What an orchestrator gives you")
c1, c2, c3 = st.columns(3)
c1.info("**Schedule**\n\nRun on a clock (nightly) or a trigger (new file lands).")
c2.info("**Dependencies & retries**\n\nCorrect order; auto-retry the failed step only.")
c3.info("**Observability**\n\nSee what ran, what failed, how long — and get alerted.")
st.success("Tools: **Airflow**, **Dagster**, **Prefect**, or a humble **cron** job. The step up "
           "from 'someone runs the script' to 'it just happens' is the whole point.")
ui.leader_takeaway("If your reports depend on someone remembering to run something, they'll "
                   "eventually be late or wrong — orchestration is the cheap insurance against that.")
