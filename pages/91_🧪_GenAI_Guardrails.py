import streamlit as st

from workshop import guardrails as gr, ui

st.set_page_config(page_title="Guardrails", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Guardrails — why AI invents facts, and how to stop it",
    "An LLM is built to sound right, not to be right. Ask it something outside what it knows and "
    "it will confidently make something up — a *hallucination*. This is the risk every leader "
    "must price in. The main defence is grounding: force answers to come only from trusted text, "
    "and check them against it.",
)

st.markdown("#### 1 · Same question, with and without a guardrail")
st.caption("Scripted example. Source of truth:")
st.info(gr.SOURCE)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**🚫 Unguarded**")
    st.error(gr.HALLUCINATED_ANSWER)
    rep = gr.grounding_report(gr.HALLUCINATED_ANSWER, gr.SOURCE)
    st.caption(f"Grounded: **{int(rep['grounded_fraction']*100)}%** — invents a 30-day window "
               "and international shipping, neither in the source.")
with c2:
    st.markdown("**✅ Guarded (answer only from the source)**")
    st.success(gr.GROUNDED_ANSWER)
    rep = gr.grounding_report(gr.GROUNDED_ANSWER, gr.SOURCE)
    st.caption(f"Grounded: **{int(rep['grounded_fraction']*100)}%** — every claim traces back "
               "to the source.")

st.markdown("#### 2 · Check any answer against its source")
source = st.text_area("Trusted source text", gr.SOURCE, height=100)
answer = st.text_area("An answer to fact-check", gr.HALLUCINATED_ANSWER, height=80)
if source.strip() and answer.strip():
    rep = gr.grounding_report(answer, source)
    st.metric("Grounding score", f"{int(rep['grounded_fraction']*100)}%")
    for r in rep["sentences"]:
        icon = "✅" if r["supported"] else "⚠️"
        st.markdown(f"{icon} *{r['text']}*  — support {int(r['support']*100)}%")
        if not r["supported"]:
            st.caption("↳ Not supported by the source — a likely hallucination.")

ui.leader_takeaway("Never deploy an LLM on facts without grounding and a way to check it. The "
                   "right question for any AI vendor is: *where does this answer come from, and "
                   "what happens when it doesn't know?*")
ui.footer()
