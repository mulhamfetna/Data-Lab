import json

import streamlit as st

from workshop import api, ui


@st.cache_resource
def _service():
    return api.build_service()

st.set_page_config(page_title="Model as API", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Model as an API — ship it, don't email it",
    "A model trapped in a notebook helps no one. Wrapping it in an API turns it into a service any "
    "app, website, or teammate can call with one request — the step that takes a model from "
    "experiment to product.",
)

clf, meta = _service()
st.markdown("#### `POST /predict` — describe a customer")
c = st.columns(3)
payload = {
    "n_orders": c[0].number_input("n_orders", 1, 30, 8),
    "total_qty": c[1].number_input("total_qty", 1, 100, 20),
    "avg_amount": c[2].number_input("avg_amount", 1.0, 60.0, 30.0),
}
st.markdown("**Request body**")
st.code(json.dumps(payload, indent=2), language="json")

if st.button("▶️ Send request", type="primary"):
    resp = api.handle_request(payload, clf, meta)
    st.markdown("**Response**")
    st.code(json.dumps(resp, indent=2), language="json")
    if resp["status"] == 200:
        st.success(f"The model answered in milliseconds: **{resp['prediction']}** "
                   f"({resp['confidence']*100:.0f}% confidence).")
st.info("In production this is a few lines with **FastAPI** or a managed endpoint — the same model "
        "you trained, now callable by your website, app, or partners at scale.")
ui.leader_takeaway("The gap between 'we built a model' and 'it makes us money' is an API — serving "
                   "is where ML becomes a product.")
