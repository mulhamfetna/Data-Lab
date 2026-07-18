import pandas as pd
import streamlit as st

from workshop import formats, store_data as sd, ui, visuals

st.set_page_config(page_title="File Formats", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 File Formats — the same data wears many clothes",
    "CSV, JSON, Excel, Parquet — same records, wildly different size and speed. Choosing the "
    "right format is a quiet decision that makes storage cheaper and pipelines faster.",
)

df = sd.clean_orders(sd.messy_orders())
sizes = formats.sizes(df)

st.markdown(f"#### Storing the same {len(df):,} Nour Store orders")
size_df = pd.DataFrame({"format": list(sizes), "kilobytes": [round(v / 1024, 1) for v in sizes.values()]})
st.bar_chart(size_df, x="format", y="kilobytes", color=visuals.PALETTE[0])

ratio = sizes["CSV"] / sizes["Parquet"]
st.success(f"**Parquet is {ratio:.1f}× smaller than CSV here** — and columnar, so analytics "
           "read only the columns they need. It's why data warehouses prefer it.")

st.markdown("#### Round-trip: every format recovers the same rows")
st.write(formats.roundtrip_rows(df))

st.markdown("#### Parsing a table out of a document")
st.caption("Data is often trapped in tables inside pages and PDFs. Here we pull one from HTML "
           "(PDFs use tools like camelot/tabula).")
html = ("<table><tr><th>Product</th><th>Price</th></tr>"
        "<tr><td>Coffee 250g</td><td>4.5</td></tr><tr><td>Olive Oil 1L</td><td>8.0</td></tr></table>")
st.code(html, language="html")
st.dataframe(formats.parse_table(html), use_container_width=True)
ui.leader_takeaway("Default to Parquet for analytics at scale; CSV only for tiny, human-readable "
                   "handoffs.")
