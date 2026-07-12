import streamlit as st

from workshop import sources, ui

st.set_page_config(page_title="Qualitative Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Qualitative → Quantitative — turning words into numbers",
    "Interviews, reviews, and open feedback are data too — but you can't average a "
    "paragraph. The pre-analysis step is *coding*: converting messy human language into "
    "structured numbers you can actually count and chart.",
)

st.markdown("#### The conversion, step by step")
st.graphviz_chart("""
digraph { rankdir=LR; bgcolor="transparent";
  node [shape=box, style="rounded,filled", fontname="sans", color="#c9ccd1"];
  raw [label="Raw text\\n(qualitative)", fillcolor="#fbe6c2"];
  code [label="Code / tag\\neach comment", fillcolor="#eef3f8"];
  num [label="0/1 per theme\\n(quantitative)", fillcolor="#d4efe4"];
  viz [label="Count & chart", fillcolor="#c9f0d8", shape=oval];
  raw -> code -> num -> viz; }
""")

default = ("the delivery was slow\ngreat product but slow support\nfast and friendly service\n"
           "delivery took too long\nloved it, will buy again\nsupport was unhelpful and slow\n"
           "quick delivery, great value\nexpensive but worth it")
themes = {"speed": ["slow", "fast", "long", "delivery", "quick"],
          "support": ["support", "help", "unhelpful", "friendly", "service"],
          "loyalty": ["again", "loved", "love", "great", "worth"],
          "price": ["expensive", "value", "cheap", "worth"]}

t1, t2, t3, t4 = st.tabs(["1 · Raw text", "2 · Coding (qual→quant)", "3 · Quantified", "4 · Visualized"])
text = st.session_state.get("qual_text", default)

with t1:
    st.markdown("**Raw, unstructured feedback** — the kind you already get every day.")
    text = st.text_area("Customer comments (one per line)", value=default, height=180)
    st.session_state.qual_text = text

feedback = [line for line in text.splitlines() if line.strip()]
coded = sources.code_feedback(feedback, themes)

with t2:
    st.markdown("**Coding:** tag every comment for each theme — a human (or an LLM) reads the "
                "text and marks 1 where the theme appears. This is the qualitative→quantitative "
                "conversion.")
    st.dataframe(coded, use_container_width=True)

with t3:
    st.markdown("**Quantified:** now it's just numbers — how many comments mention each theme.")
    counts = {theme: int(coded[theme].sum()) for theme in themes}
    st.write(counts)
    st.caption(f"{len(feedback)} comments → {len(themes)} countable signals.")

with t4:
    st.markdown("**Visualized:** the decision-ready view.")
    st.bar_chart({theme: int(coded[theme].sum()) for theme in themes})
    ui.leader_takeaway("‘Slow delivery’ said 4 different ways becomes one number you can track "
                       "month over month.")
