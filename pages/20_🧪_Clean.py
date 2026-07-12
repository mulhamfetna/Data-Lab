import streamlit as st

from workshop import cleaning, store_data as sd, ui

st.set_page_config(page_title="Clean", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Clean — the unglamorous 80%",
    "Real data arrives messy. Before any analysis you fix duplicates, missing values, "
    "and inconsistent labels — most of the work happens here, and skipping it poisons "
    "every decision downstream.",
)

messy = sd.messy_orders()
before = cleaning.issues(messy)

st.markdown("### Nour Store's raw orders — what's wrong with them?")
c = st.columns(4)
c[0].metric("Duplicate rows", before["duplicates"])
c[1].metric("Missing amounts", before["missing_amount"])
c[2].metric("Bad quantities", before["bad_quantity"])
c[3].metric("Messy city names", before["messy_city"])

st.markdown("### Turn on each fix and watch the mess disappear")
chosen = [name for name, label in cleaning.STEP_LABELS.items()
          if st.checkbox(label, value=True, key=name)]

cleaned = cleaning.apply_steps(messy, chosen)
after = cleaning.issues(cleaned)

c = st.columns(4)
c[0].metric("Duplicate rows", after["duplicates"], after["duplicates"] - before["duplicates"])
c[1].metric("Missing amounts", after["missing_amount"], after["missing_amount"] - before["missing_amount"])
c[2].metric("Bad quantities", after["bad_quantity"], after["bad_quantity"] - before["bad_quantity"])
c[3].metric("Messy city names", after["messy_city"], after["messy_city"] - before["messy_city"])

st.caption(f"Rows: {len(messy)} raw → {len(cleaned)} after cleaning")
st.dataframe(cleaned.head(30), use_container_width=True)
