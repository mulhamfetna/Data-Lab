import pandas as pd
import streamlit as st

from workshop import llm, ui, zeroshot as zs

st.set_page_config(page_title="Zero-shot classifier", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Zero-shot classifier — sorting with no training data",
    "Routing tickets, tagging feedback, triaging emails — sorting text into buckets used to "
    "mean collecting thousands of labelled examples and training a model. With an LLM you just "
    "*name the buckets* and it sorts. For a manager, that turns a months-long data project into "
    "an afternoon.",
)

st.caption(f"Provider: **{llm.provider_label()}** — offline sorts by keyword overlap; a free "
           "provider does true zero-shot from the label names alone.")

st.markdown("#### The categories (just described, never trained)")
st.write(", ".join(f"**{k}**" for k in zs.LABELS))

st.markdown("#### Auto-routed support tickets")
rows = []
for t in zs.SAMPLE_TICKETS:
    r = zs.classify(t)
    rows.append({"Ticket": t, "Routed to": r["label"]})
st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

st.markdown("#### Try your own")
txt = st.text_input("A message to route",
                    "You charged my card but I never got a receipt.")
if txt.strip():
    r = zs.classify(txt)
    st.success(f"→ **{r['label']}**" + ("  ·  live model" if r["is_live"] else ""))
    if not r["is_live"]:
        sc = pd.DataFrame({"category": list(r["scores"]),
                           "keyword matches": list(r["scores"].values())})
        st.bar_chart(sc, x="category", y="keyword matches")
        if max(r["scores"].values()) == 0:
            st.warning("No keyword matched — offline this is a guess. A real zero-shot model "
                       "would still understand it; that's the gap a live provider closes.")

ui.leader_takeaway("Zero-shot classification is the fastest win in the whole GenAI toolbox: no "
                   "labelled data, no training, just clear category names — ideal for routing, "
                   "tagging, and triage.")
ui.footer()
