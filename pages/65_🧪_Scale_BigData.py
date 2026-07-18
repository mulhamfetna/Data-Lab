import time

import pandas as pd
import streamlit as st

from workshop import bigdata as bd, ui

st.set_page_config(page_title="Big Data", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Big Data — when the data won't fit in memory",
    "'Big data' really means: too big to load all at once. The fix isn't a bigger laptop — it's "
    "processing the data in chunks (or across many machines). Same answer, bounded memory.",
)

n = st.select_slider("Rows to process", [100_000, 250_000, 500_000, 1_000_000], value=500_000)
chunk = st.select_slider("Chunk size", [50_000, 100_000, 250_000], value=100_000)

if st.button("▶️ Process it two ways", type="primary"):
    df = bd.make_big(n=n, seed=0)
    mem_all = df.memory_usage(deep=True).sum() / 1e6

    t0 = time.time(); res_all = bd.sum_all(df); t_all = time.time() - t0
    t0 = time.time(); res_chunk = bd.sum_chunked(df, chunk=chunk); t_chunk = time.time() - t0
    mem_chunk = df.iloc[:chunk].memory_usage(deep=True).sum() / 1e6

    c1, c2 = st.columns(2)
    c1.metric("All-in-memory — peak RAM", f"{mem_all:.0f} MB", f"{t_all*1000:.0f} ms")
    c2.metric("Chunked — peak RAM", f"{mem_chunk:.0f} MB", f"{t_chunk*1000:.0f} ms",
              delta_color="inverse")
    st.success(f"Both give the **identical** answer, but chunking held only ~{mem_chunk:.0f} MB "
               f"at a time instead of {mem_all:.0f} MB — how you process data bigger than your RAM.")
    st.dataframe(pd.DataFrame({"city": res_all.keys(),
                               "revenue (all)": res_all.values(),
                               "revenue (chunked)": [res_chunk[k] for k in res_all]}),
                 use_container_width=True)
    st.info("At true scale (terabytes) you'd hand this to **Spark** or **Dask**, which chunk it "
            "across many machines automatically — same principle, more workers.")
else:
    st.info("Press the button to aggregate the dataset all-at-once vs in chunks.")
ui.leader_takeaway("‘We need big-data tools’ usually means ‘our data outgrew one machine’ — the "
                   "answer is chunking and distribution, not a pricier server.")
