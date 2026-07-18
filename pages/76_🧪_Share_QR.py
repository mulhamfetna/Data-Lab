import streamlit as st

from workshop import qr, ui

st.set_page_config(page_title="Share (QR)", page_icon="📱", layout="wide")
ui.page_header(
    "📱 Share — put this in everyone's hands",
    "Hand the whole lab to the room: paste the app's URL, project the QR code, and let 30 people "
    "open it on their phones and follow along live.",
)

url = st.text_input("App URL to share", value="http://localhost:8501",
                    help="Use the Network URL that Streamlit prints, or your deployed streamlit.app link.")
if url.strip():
    c1, c2 = st.columns([1, 2])
    with c1:
        st.image(qr.make_qr(url), caption="Scan to open", width=260)
    with c2:
        st.markdown(f"### Open on your phone\n\n**{url}**\n\nPoint your camera at the QR code.")
st.caption("See DEPLOY.md for hosting this on Streamlit Community Cloud or Docker.")
ui.leader_takeaway("A workshop everyone can touch on their own phone beats one they only watch on "
                   "a projector.")
