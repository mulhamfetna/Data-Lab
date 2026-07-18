import streamlit as st

from workshop import extract as ex, llm, ui

st.set_page_config(page_title="Structured extraction", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Structured extraction — messy text → a clean table",
    "Orders arrive as emails and chat messages, not spreadsheets. Turning that free text into "
    "rows and columns is where a huge amount of real 'AI' value lives — it's what lets the rest "
    "of your data tools work at all. And much of it needs no model: plain rules already handle "
    "the common cases.",
)

st.caption(f"Provider: **{llm.provider_label()}**. The table below is built with **rules only** "
           "(regex); a provider helps with text too irregular for rules.")

st.markdown("#### Three messy messages in…")
for m in ex.SAMPLE_MESSAGES:
    st.markdown(f"> {m}")

st.markdown("#### …one clean table out")
st.dataframe(ex.extract_table(), use_container_width=True, hide_index=True)

st.markdown("#### Try your own message")
txt = st.text_area("Paste a message",
                   "Layla Nasser, order #4610 for $19.99 on 2026-04-01, phone 0933-222-111")
if txt.strip():
    result = ex.extract(txt)
    st.json({k: v for k, v in result["fields"].items()})
    if result["is_live"]:
        st.success(f"Extracted by a live model — {llm.provider_label()}.")
    else:
        st.info("🔌 Extracted by rules (regex) — no model needed, and it can't invent a value "
                "that isn't in the text.")

ui.leader_takeaway("Before paying for an 'AI extraction' tool, check how much plain rules already "
                   "solve. Save the model for the genuinely messy 20% — that's the cost-smart split.")
ui.footer()
