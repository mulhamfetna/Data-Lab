import streamlit as st

from workshop import ui

st.set_page_config(page_title="Data Lineage", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Data Lineage — where did this number come from?",
    "When a figure in the board deck looks wrong, the first question is 'where did it come from?' "
    "Lineage traces every number back through its transforms to its raw source — the audit trail "
    "that makes data trustworthy and mistakes findable.",
)

st.markdown("#### The lineage of one number: *last month's revenue*")
st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent"; node[shape=box,style="rounded,filled",fontname=sans,color="#c9ccd1"];
  crm[label="CRM\\n(orders)", fillcolor="#cfe6f5"];
  pay[label="Payments\\nsystem", fillcolor="#cfe6f5"];
  clean[label="Clean\\n(dedupe, fix dates)", fillcolor="#fbe6c2"];
  join[label="Join\\norders + payments", fillcolor="#fbe6c2"];
  agg[label="Aggregate\\nby month", fillcolor="#fbe6c2"];
  metric[label="Revenue\\n(board deck)", fillcolor="#c9f0d8", shape=oval];
  crm -> clean; pay -> join; clean -> join -> agg -> metric; }
""")
st.caption("Follow the arrows backward from any number to see exactly which sources and steps "
           "produced it — and where a bug could have crept in.")

st.markdown("#### The three habits that make data trustworthy")
c1, c2, c3 = st.columns(3)
c1.info("**Lineage**\n\nTrace every metric to its source and transforms.")
c2.info("**Catalog**\n\nA searchable index of what data exists, who owns it, what it means.")
c3.info("**Versioning**\n\nSnapshot data & pipelines so any past number can be reproduced.")

st.success("Together these answer the three questions that kill trust in data: *Where did it come "
           "from? What does it mean? Can we reproduce it?*")
ui.leader_takeaway("If no one can trace a number back to its source, you can't trust it — demand "
                   "lineage before you bet a decision on a dashboard.")
