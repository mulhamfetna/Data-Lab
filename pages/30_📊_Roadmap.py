import streamlit as st

st.set_page_config(page_title="Learning Roadmap", page_icon="📊", layout="wide")
st.title("📊 Learning Roadmap — beginner to professional")

st.markdown("**One clear path — for you, your team, or your kids.** "
            "Depth over breadth: master ~15 tools through projects, not 50 superficially.")

phases = [
    "Python & Data Foundations", "Visualization & Exploration", "SQL & Data Engineering",
    "Statistics", "Machine Learning", "Deep Learning", "MLOps & Production",
    "Specialization (CV · NLP · LLMs · MLOps)",
]

st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent"; node [shape=box, style="rounded,filled",
  fontname="sans", color="#c9ccd1", fillcolor="#eef3f8"];
  p1 [label="1 · Python &\\nData Foundations"]; p2 [label="2 · Visualization"];
  p3 [label="3 · SQL & Data\\nEngineering"]; p4 [label="4 · Statistics"];
  p5 [label="5 · Machine\\nLearning", fillcolor="#fbe6c2"]; p6 [label="6 · Deep\\nLearning", fillcolor="#fbe6c2"];
  p7 [label="7 · MLOps &\\nProduction", fillcolor="#d4efe4"]; p8 [label="8 · Specialize", fillcolor="#c9f0d8", shape=oval];
  p1->p2->p3->p4->p5->p6->p7->p8;
  cv [label="Computer\\nVision", shape=note, fillcolor="#f7f7f5"]; nlp [label="NLP /\\nLLMs", shape=note, fillcolor="#f7f7f5"];
  ops [label="MLOps /\\nCloud", shape=note, fillcolor="#f7f7f5"];
  p8->cv; p8->nlp; p8->ops; }
""")
st.caption("A single path, branching only at the end into a specialization. "
           "Depth over breadth: ~15 tools mastered through projects, not 50 skimmed.")

st.markdown("### Anti-hype — what NOT to learn (yet)")
st.markdown(
    "| If you're *building* new AI research | If you're *integrating* AI into a business |\n"
    "|---|---|\n"
    "| Deep calculus, linear algebra, probability | Your high-school math is plenty |\n"
    "| Read arXiv papers daily | Learn Linux, APIs, deployment, governance |\n"
    "| Academia / research labs | MLOps, cloud, clean SQL |"
)
st.caption("“Don't spend 3 months on deep math if you can't yet write a clean SQL join.”")

st.markdown("### ✋ Where are you — or your team?")
c = st.columns(3)
who = c[0].selectbox("Who?", ["Me", "A team member", "My child"])
phase = c[1].selectbox("Start at", [f"Phase {i}: {p}" for i, p in enumerate(phases, 1)])
action = c[2].text_input("One next action", "install Python and finish week 1")
if action:
    st.success(f"**Commitment:** {who} will start **{phase}** by *{action}* — put a date on it.")
