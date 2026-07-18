import streamlit as st

from workshop import indexing as ix, ui

st.set_page_config(page_title="Indexing", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Indexing — the difference between instant and forever",
    "Without an index, finding one row means reading every row — like finding a word by reading "
    "the whole book. An index is the book's index: jump straight to the page. It's why one query "
    "returns instantly and another times out.",
)

n = st.select_slider("Table size (rows)", [100_000, 300_000, 500_000], value=300_000)
if st.button("▶️ Look up one row — with vs without an index", type="primary"):
    df = ix.make_data(n=n, seed=0)
    r = ix.compare(df, key=n // 2, repeats=200)
    c1, c2 = st.columns(2)
    c1.metric("No index (full scan)", f"{r['unindexed_ms']:.0f} ms")
    c2.metric("With index", f"{r['indexed_ms']:.1f} ms", delta_color="inverse")
    st.success(f"**{r['speedup']:,.0f}× faster** for the exact same query — identical result, "
               "one config decision.")
    st.caption("The gap widens as the table grows: full scans get linearly slower, indexed "
               "lookups stay nearly instant. Partitioning applies the same idea to huge tables.")
else:
    st.info("Press the button to race a point-lookup with and without an index.")
ui.leader_takeaway("When a dashboard is 'slow', the fix is often a one-line index — not a bigger "
                   "database.")
