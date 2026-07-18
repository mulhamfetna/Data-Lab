import pandas as pd
import streamlit as st

from workshop import stats_traps as stt, ui

st.set_page_config(page_title="CIs & p-hacking", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Confidence & p-hacking — when 'significant' means nothing",
    "Two numbers protect you from fooling yourself: the confidence interval (how sure are we?) "
    "and the p-value (is this real or luck?). Ignore them and you'll celebrate results that are "
    "pure noise — or get gamed by someone who tested 20 things and showed you the one that hit.",
)

st.markdown("#### 1 · More data → more certainty")
n = st.select_slider("Sample size", [30, 100, 300, 1000, 3000], value=100)
st.metric("95% confidence-interval width", f"± {stt.ci_width(n)/2:.1f}")
widths = pd.DataFrame({"n": [30, 100, 300, 1000, 3000],
                       "CI width": [stt.ci_width(x) for x in [30, 100, 300, 1000, 3000]]})
st.line_chart(widths, x="n", y="CI width")
st.caption("A small sample gives a wide, near-useless interval. Certainty is bought with data.")

st.markdown("#### 2 · Test enough things and something 'wins' by luck")
n_tests = st.slider("How many things do you test?", 10, 500, 200, 10)
r = stt.p_hacking(n_tests, seed=0)
c1, c2 = st.columns(2)
c1.metric("Comparisons run (all truly identical)", r["tests"])
c2.metric("'Significant' by pure chance", r["false_positives"], f"{r['rate']*100:.1f}%")
st.error(f"None of these groups differ at all — yet **{r['false_positives']} came out "
         "'significant' (p < 0.05)**. Report only those and you've 'proven' nonsense. That's "
         "**p-hacking**.")
ui.leader_takeaway("Ask two questions of any result: *how wide is the uncertainty?* and *how many "
                   "things were tested before this one was shown to me?*")
