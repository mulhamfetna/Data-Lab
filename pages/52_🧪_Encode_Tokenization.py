import streamlit as st

from workshop import tokenize as tk, ui, visuals

st.set_page_config(page_title="Tokenization", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Tokenization — how an AI actually reads text",
    "A language model doesn't see words — it sees *tokens*, little chunks of text turned into "
    "numbers. Tokens are also how you're billed and how context limits are counted, so "
    "'how many tokens?' is a real budget question.",
)

text = st.text_area("Type something", value="Nour Store sells the best coffee in Aleppo!",
                    height=90)
toks = tk.word_tokens(text)

st.markdown("#### Your text, split into tokens")
chips = " ".join(
    f'<span style="background:{visuals.PALETTE[i % len(visuals.PALETTE)]}22;'
    f'border:1px solid {visuals.PALETTE[i % len(visuals.PALETTE)]};border-radius:6px;'
    f'padding:2px 7px;margin:2px;display:inline-block">{tok}</span>'
    for i, tok in enumerate(toks))
st.markdown(chips, unsafe_allow_html=True)

s = tk.stats(text)
c = st.columns(3)
c[0].metric("Characters", s["characters"])
c[1].metric("Word tokens", s["words"])
c[2].metric("≈ LLM tokens", s["est_llm_tokens"])

st.info("Real LLMs use **subword** tokenization (BPE): common words are one token, rare words "
        "split into pieces — so 'tokenization' might be `token` + `ization`. Tools like "
        "`tiktoken` count them exactly; here we approximate (≈ chars ÷ 4).")
ui.leader_takeaway("Every prompt, document, and reply is billed and bounded in tokens — knowing "
                   "that is how you budget and size an AI feature.")
