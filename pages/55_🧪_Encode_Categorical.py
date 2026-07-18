import pandas as pd
import streamlit as st

from workshop import encoding as en, store_data as sd, ui

st.set_page_config(page_title="Categorical Encoding", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Categorical Encoding — turning 'Aleppo' into math",
    "Models only do arithmetic, so text categories must become numbers first. *How* you encode "
    "them matters: get it wrong and the model thinks Homs is 'more than' Aleppo for no reason.",
)

cities = sd.clean_orders(sd.messy_orders())["city"].head(8).reset_index(drop=True)
st.markdown("**A city column:**")
st.write(list(cities))

c1, c2 = st.columns(2)
with c1:
    st.markdown("**One-hot** — one yes/no column per city. No fake ordering; the safe default "
                "for unordered categories.")
    st.dataframe(en.one_hot(cities, prefix="city"), use_container_width=True)
with c2:
    st.markdown("**Ordinal** — one number per category. Only valid when there's a real order "
                "(small < medium < large), *not* for cities.")
    sizes = pd.Series(["small", "large", "medium", "large", "small", "medium", "large", "small"])
    st.dataframe(pd.DataFrame({"size": sizes,
                               "encoded": en.ordinal(sizes, ["small", "medium", "large"])}),
                 use_container_width=True)

st.warning("Using ordinal encoding on cities would tell the model 'Damascus (2) > Aleppo (0)' — "
           "a meaningless ranking that quietly corrupts results. Match the encoding to the data.")
ui.leader_takeaway("Ask whether a category has a real order before it's turned into numbers — the "
                   "wrong choice invents relationships that aren't there.")
