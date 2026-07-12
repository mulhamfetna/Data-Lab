import streamlit as st

st.set_page_config(page_title="The Lifecycle", page_icon="📊", layout="wide")
st.title("📊 The Data Lifecycle — from collection to decision")

st.markdown(
    "Every number you ever trust travelled this road. Roughly **80% of the work is the "
    "unglamorous middle** — collecting and cleaning — long before any chart appears."
)

st.graphviz_chart("""
digraph {
  rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#eef", fontname="sans"];
  Collect -> Clean -> Filter -> Analyze -> Engineer -> Predict -> Decision
  [color="#556"]; Decision [fillcolor="#dfd"];
}
""")

stages = {
    "Collect": "Gather raw data — from websites, APIs, databases, sensors, or synthetic generation.",
    "Clean": "Fix duplicates, missing values, and inconsistent labels. The unglamorous 80%.",
    "Filter": "Zoom in on the slice that answers your question.",
    "Analyze": "Turn rows into an insight a leader can act on.",
    "Engineer": "Make it repeatable — a pipeline that runs every day, not a one-off.",
    "Predict": "Learn from the past to anticipate the future.",
    "Decision": "The point of all of it: a better, evidence-backed call.",
}
for name, desc in stages.items():
    st.markdown(f"**{name}** — {desc}")

st.info("Each 🧪 demo in the sidebar is one of these stages — all following the same small "
        "business, *Nour Store*, from raw mess to a decision.")
