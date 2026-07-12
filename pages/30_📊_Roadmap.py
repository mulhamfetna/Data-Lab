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
for i, p in enumerate(phases, 1):
    st.markdown(f"**Phase {i}** — {p}")

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
