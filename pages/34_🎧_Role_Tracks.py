import streamlit as st

from workshop import tracks, ui

st.set_page_config(page_title="Role tracks", page_icon="🎧", layout="wide")
ui.page_header(
    "🎧 Your track — the lab, curated for your role",
    "Eighty demos is a lot. Pick who you are and get a short, ordered playlist of the ones that "
    "matter most to you — with a one-line reason each. Explore the rest anytime; this is your "
    "fast path.",
)

role = st.radio("I am a…", tracks.roles(),
                format_func=lambda r: f"{tracks.track(r)['icon']} {r}", horizontal=True)
info = tracks.track(role)

st.markdown(f"### {info['icon']} {role}")
st.caption(info["blurb"])

for i, (file, title, why) in enumerate(info["demos"], 1):
    c1, c2 = st.columns([2, 3])
    with c1:
        try:
            st.page_link(file, label=f"**{i}. {title}**", icon="🧪")
        except Exception:
            st.markdown(f"**{i}. {title}**")
    c2.caption(why)

ui.leader_takeaway("You don't need all eighty demos — you need the six that match your decisions. "
                   "Start with your track, then wander.")
ui.footer()
