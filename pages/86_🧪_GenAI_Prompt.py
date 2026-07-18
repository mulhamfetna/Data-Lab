import pandas as pd
import streamlit as st

from workshop import llm, prompt as pr, ui

st.set_page_config(page_title="Prompt playground", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Prompt playground — the same AI, four different asks",
    "An LLM's answer is only as good as the question. The skill your team is really hiring "
    "for is *prompting*: giving context, a role, a format, and limits. Watch a lazy prompt and "
    "an engineered one pull very different answers out of the exact same model.",
)

st.caption(f"Provider: **{llm.provider_label()}** — set a free key "
           "(`GROQ_API_KEY`, `OPENROUTER_API_KEY`, `HF_TOKEN`, or `OLLAMA_HOST`) "
           "to see a live model answer each variant.")

task = st.text_input(
    "What do you want the AI to do?",
    "Tell an unhappy customer their late order is on the way")

variants = pr.build_variants(task)

st.markdown("#### The same task, asked four ways")
rows = []
for name, text in variants.items():
    s = pr.score_prompt(text)
    rows.append({"Prompt": name, "Score /5": s["score"],
                 "Missing": ", ".join(pr.label_for(k) for k, v in s["hits"].items() if not v) or "—"})
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

choice = st.radio("Inspect a prompt", list(variants), horizontal=True, index=3)
st.code(variants[choice], language="text")
s = pr.score_prompt(variants[choice])
cols = st.columns(len(pr.RUBRIC))
for col, (key, label, _pat) in zip(cols, pr.RUBRIC):
    col.metric(label.split("(")[0].strip(), "✅" if s["hits"][key] else "—")

if st.button("▶ Get the AI's answer"):
    text, live = llm.complete(variants[choice], max_tokens=300)
    if live:
        st.success(f"Live answer — {llm.provider_label()}:")
        st.write(text)
    else:
        st.info("🔌 Offline — no API key, so no real answer is generated. The *score* above "
                "still teaches the lesson: the engineered prompt gives the model everything it "
                "needs to answer well, the vague one leaves it guessing. Add a key to see the "
                "answers themselves diverge.")

ui.leader_takeaway("Before buying an 'AI feature', ask to see the prompt. A weak prompt makes a "
                   "great model look dumb; a strong one is often the whole product.")
ui.footer()
