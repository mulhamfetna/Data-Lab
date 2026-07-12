import streamlit as st

st.set_page_config(page_title="Tech Roles", page_icon="📊", layout="wide")
st.title("📊 Tech Roles — who to hire, who to manage")

st.markdown("You don't need to *do* these jobs — you need to *tell them apart* so you hire the "
            "right one and aren't oversold.")

st.graphviz_chart("""
digraph { rankdir=TB; node [shape=box, style=rounded, fontname="sans"]; DATA [label="DATA WORLD", shape=oval];
  DATA -> "Core Analytics"; DATA -> "Engineering"; DATA -> "Science & ML"; DATA -> "AI & Products"; DATA -> "Leadership";
  "Core Analytics" -> "Data Analyst\\nBI Analyst"; "Engineering" -> "Data Engineer\\nAnalytics Eng.";
  "Science & ML" -> "Data Scientist\\nML Engineer\\nMLOps"; "AI & Products" -> "AI Engineer\\nGenAI\\nNLP/CV";
  "Leadership" -> "Head of Data\\nCDO/CAO/CAIO"; }
""")

st.markdown("### Role → tools cheat sheet")
st.markdown(
    "| Role | Must know | Main tools |\n|---|---|---|\n"
    "| Data Analyst | SQL, Excel, basic stats | Power BI, Tableau, SQL |\n"
    "| Data Engineer | Python, pipelines, cloud | Spark, Airflow, dbt, SQL |\n"
    "| Data Scientist | Python, ML, statistics | scikit-learn, Jupyter |\n"
    "| ML Engineer | Deep learning, deployment | PyTorch, Docker, MLflow |\n"
    "| AI / GenAI Engineer | LLMs, APIs, system design | LangChain, vector DBs, FastAPI |"
)

st.markdown("> 📎 **Story — Zillow's $304M model.** Zillow trusted a price-prediction model too "
            "far, lost **$304M**, and shut its home-buying business in 2021. Knowing what a role "
            "can and can't promise is risk management.")

st.markdown("### ✋ Who do I hire?")
problems = {
    "10 years of sales data → I want a weekly dashboard": "Data Analyst",
    "I want a chatbot on my website": "AI / GenAI Engineer",
    "My data is in 6 systems and never agrees": "Data Engineer",
    "Predict which customers will churn": "Data Scientist",
    "Ship my model into the product, reliably": "ML Engineer",
}
roles = ["Data Analyst", "Data Engineer", "Data Scientist", "ML Engineer", "AI / GenAI Engineer"]
score = 0
for prob, answer in problems.items():
    pick = st.selectbox(prob, ["—"] + roles, key=prob)
    if pick == answer:
        score += 1
        st.caption("✅ Right role.")
    elif pick != "—":
        st.caption(f"❌ Better fit: **{answer}**.")
st.info(f"Score: **{score} / {len(problems)}** — the most expensive mistake is hiring a Data "
        "Scientist when you needed a Data *Analyst*.")
