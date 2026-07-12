from pathlib import Path

import streamlit as st

from workshop import pipeline as pl, store_data as sd, ui

st.set_page_config(page_title="Engineer", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Engineer — moving data reliably, on repeat",
    "A pipeline turns a one-off spreadsheet into a system: the same clean steps run every "
    "day, load into a database, and feed every report. This is what lets a business trust "
    "its numbers at scale.",
)

df = sd.clean_orders(sd.messy_orders())
db_path = Path("data/nour.db")

st.markdown("### The pipeline")
st.markdown(
    "1. **Extract** raw orders → 2. **Clean** them → 3. **Model** into a star schema "
    "(customers · products · orders) → 4. **Load** into a SQLite database."
)

if st.button("▶️ Run the pipeline", type="primary"):
    tables = pl.build_star_schema(df)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    pl.load_to_sqlite(tables, db_path)
    st.session_state.counts = pl.table_counts(db_path)
    st.session_state.tables = {k: v.head(8) for k, v in tables.items()}
    st.success(f"Loaded into {db_path}")

if st.session_state.get("counts"):
    cols = st.columns(len(st.session_state.counts))
    for col, (name, cnt) in zip(cols, st.session_state.counts.items()):
        col.metric(name, f"{cnt:,} rows")
    for name, preview in st.session_state.tables.items():
        st.markdown(f"**{name}**")
        st.dataframe(preview, use_container_width=True)
else:
    st.info("Press **Run the pipeline** to build and load the database.")
