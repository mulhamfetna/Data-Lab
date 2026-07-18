import streamlit as st

from workshop import export, ui

st.set_page_config(page_title="Export", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Export My Session — take the work home",
    "A workshop you can't take with you is a workshop you'll forget. Bundle the artifacts — the "
    "report, the cleaned dataset — into one file to keep, share, or reproduce.",
)

st.markdown("Your session bundle contains:")
st.markdown("- **nour_store_report.txt** — the performance report\n"
            "- **nour_store_clean.csv** — the cleaned dataset\n"
            "- **README.txt** — what's inside")

st.download_button("⬇️ Download my session (zip)", export.bundle(),
                   file_name="data_lab_session.zip", mime="application/zip",
                   type="primary")
ui.leader_takeaway("The value of a session is what you do *after* it — leaving with real artifacts "
                   "beats leaving with notes.")
