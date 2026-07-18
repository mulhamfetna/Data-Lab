import streamlit as st

from workshop import llm, rag, ui

st.set_page_config(page_title="RAG Q&A", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 RAG — teach the AI *your* documents without retraining",
    "A general AI doesn't know your refund policy or your delivery times. RAG "
    "(retrieval-augmented generation) fixes that cheaply: find the few relevant lines in "
    "your own documents, hand them to the model, and it answers from your facts — not a guess. "
    "It's how most 'chat with your docs' products actually work.",
)

st.caption(f"Provider: **{llm.provider_label()}**. Retrieval runs the same either way; a live "
           "provider only rephrases the grounded answer.")

with st.expander("📄 The company knowledge base (Nour Store)"):
    for i, doc in enumerate(rag.KNOWLEDGE_BASE, 1):
        st.markdown(f"**{i}.** {doc}")

examples = ["How long do I have to get a refund?",
            "Do you deliver same day?",
            "What is the capital of France?"]
q = st.selectbox("Ask a question", examples, index=0)
q = st.text_input("…or type your own", q)

if q:
    result = rag.answer(q)
    st.markdown("#### 1 · Retrieve — the most relevant snippets")
    for snippet, score in result["retrieved"]:
        st.progress(min(score * 3, 1.0), text=f"relevance {score:.2f}")
        st.caption(snippet)

    st.markdown("#### 2 · Answer — grounded in what was retrieved")
    if not result["grounded"]:
        st.warning(f"🛑 Nothing in the documents is relevant, so the honest answer is: "
                   f"*“{result['answer']}”* — RAG refuses to make things up.")
    elif result["is_live"]:
        st.success(f"Live answer — {llm.provider_label()}:")
        st.write(result["answer"])
    else:
        st.info("🔌 Offline — answering *extractively* by quoting the best-matching snippet. "
                "A live provider would rephrase it in its own words, still grounded in this text:")
        st.write(result["answer"])

ui.leader_takeaway("RAG is why 'chat with our documents' is usually cheaper and safer than "
                   "training a custom AI — and when the answer isn't in the documents, a good "
                   "RAG system says so instead of inventing one.")
ui.footer()
