import pandas as pd
import streamlit as st

from workshop import embeddings as em, ui

st.set_page_config(page_title="Embeddings", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Embeddings — turning meaning into numbers",
    "To let a machine find 'similar' things, you first turn each item into a vector of numbers, "
    "then measure distance. It's the engine behind search, recommendations, and how chatbots "
    "retrieve the right document.",
)

st.markdown("**Nour Store's catalogue** (each line becomes a vector):")
st.write(em.CORPUS)

query = st.text_input("Search for something", value="i want to buy coffee")
if query.strip():
    ranked = em.rank(query)
    st.markdown("#### Closest matches by similarity")
    st.dataframe(pd.DataFrame(ranked, columns=["catalogue item", "similarity"]),
                 use_container_width=True)
    st.success(f"Best match: **{ranked[0][0]}** — found by comparing number-vectors, not "
               "keywords.")

st.info("This demo uses **TF-IDF** vectors (word importance). Real systems use neural "
        "**embeddings** (sentence-transformers, OpenAI/Cohere) that capture meaning, so "
        "'car' and 'automobile' land close together even with no shared words.")
ui.leader_takeaway("Embeddings + similarity is the quiet workhorse behind modern search and "
                   "the 'retrieval' in retrieval-augmented chatbots.")
