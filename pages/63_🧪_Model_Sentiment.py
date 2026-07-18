import pandas as pd
import streamlit as st

from workshop import sentiment as se, ui

st.set_page_config(page_title="Sentiment", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Sentiment Analysis — are your customers happy?",
    "Thousands of reviews are unreadable one by one. Sentiment analysis reads them all in "
    "seconds and turns the mood into a number you can track — so a dip shows up on a chart "
    "before it shows up in churn.",
)

default = ("fast delivery and great value\nslow support, very unhelpful\namazing quality will buy again\n"
           "late and the item was damaged\nfriendly staff, quick service\ntoo expensive for what it is\n"
           "loved it, highly recommend\nnever ordering again")
text = st.text_area("Customer reviews (one per line)", value=default, height=170)
reviews = [r for r in text.splitlines() if r.strip()]

table = pd.DataFrame({"review": reviews,
                      "sentiment": [se.label(r) for r in reviews],
                      "score": [se.score(r) for r in reviews]})
st.dataframe(table, use_container_width=True)

summ = se.summarize(reviews)
st.bar_chart(summ)
pos = summ.get("positive", 0)
st.metric("Net mood", "🙂 positive" if pos >= summ.get("negative", 0) else "🙁 negative",
          f"{pos} positive / {summ.get('negative', 0)} negative")
st.info("This demo uses a **word lexicon** (positive/negative word lists). Production systems use "
        "trained models or LLMs that understand context and sarcasm ('great, another delay').")
ui.leader_takeaway("Sentiment turns a flood of free-text feedback into a trend line you can watch "
                   "— an early-warning system for customer happiness.")
