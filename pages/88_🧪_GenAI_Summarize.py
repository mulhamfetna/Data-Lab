import streamlit as st

from workshop import llm, summarize as sm, ui

st.set_page_config(page_title="Summarization", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Summarization — 500 words in, 3 sentences out",
    "Every leader drowns in text: reports, reviews, tickets, contracts. Summarization is the "
    "most immediately useful AI task there is. But know the trade-off — *extractive* keeps the "
    "original words and can't invent, *abstractive* reads better but can drift. Ask which one "
    "a vendor is selling you.",
)

st.caption(f"Provider: **{llm.provider_label()}** — offline uses safe extractive "
           "summarization; a free provider unlocks abstractive rewriting.")

SAMPLE = (
    "Nour Store had its strongest quarter yet, with revenue up 22 percent over last year. "
    "Coffee remained the top category, driven by the fresh same-day roasting programme. "
    "Delivery complaints fell after we added same-day express, but a few customers still "
    "reported late orders during the holiday rush. The new loyalty points scheme brought back "
    "a large number of lapsed customers, and redemption rates were higher than expected. "
    "Refund requests stayed low and were mostly about sizing on the skincare line. "
    "Looking ahead, the biggest opportunity is international shipping, which many customers "
    "have asked for, though it will require a new logistics partner and customs handling.")

text = st.text_area("Paste text to summarize", SAMPLE, height=180)
n = st.slider("Summary length (sentences)", 1, 5, 3)

if text.strip():
    result = sm.summarize(text, n)
    c1, c2 = st.columns(2)
    c1.metric("Method", result["method"])
    c2.metric("Length vs original", f"{int(result['compression']*100)}%")

    if result["is_live"]:
        st.success(f"Abstractive summary — {llm.provider_label()}:")
    else:
        st.info("🔌 Offline extractive summary — the highest-signal sentences, kept word-for-word:")
    st.write(result["summary"])

    with st.expander("How the offline version picks sentences"):
        for s, score in sorted(sm.score_sentences(text), key=lambda t: -t[1]):
            st.progress(min(score / 6, 1.0), text=f"score {score}")
            st.caption(s)

ui.leader_takeaway("Summarization pays for itself fastest of any AI feature — but for anything "
                   "high-stakes (legal, medical, financial), prefer extractive or always keep a "
                   "link back to the source, because abstractive summaries can quietly reword.")
ui.footer()
