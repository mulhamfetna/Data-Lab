import streamlit as st
import streamlit.components.v1 as components

from workshop import agenda, ui

st.set_page_config(page_title="Presenter Mode", page_icon="🎤", layout="wide")
ui.page_header(
    "🎤 Presenter Mode — the facilitator's cockpit",
    "Everything you need to run the room on time: the full agenda with time budgets, a talk-track "
    "cue per segment, and a countdown timer you can project during breaks.",
)

st.metric("Total planned time", f"{agenda.total_minutes()} min (~4 hours)")

st.markdown("#### Agenda")
for i, s in enumerate(agenda.SEGMENTS, 1):
    with st.expander(f"{i}. {s['title']}  ·  ⏱ {s['min']} min"):
        st.markdown(f"**Talk-track cue:** {s['note']}")

st.markdown("#### Countdown timer")
mins = st.number_input("Minutes", 1, 60, 10)
if st.button("▶️ Start countdown", type="primary"):
    components.html(f"""
      <div id="t" style="font-size:64px;font-weight:800;text-align:center;font-family:sans-serif"></div>
      <script>
        let end = Date.now() + {mins}*60*1000;
        function tick() {{
          let s = Math.max(0, Math.round((end - Date.now())/1000));
          let m = String(Math.floor(s/60)).padStart(2,'0');
          let ss = String(s%60).padStart(2,'0');
          document.getElementById('t').textContent = m + ':' + ss;
          document.getElementById('t').style.color = s < 30 ? '#d55e00' : '#009e73';
          if (s > 0) setTimeout(tick, 250);
        }}
        tick();
      </script>
    """, height=110)
ui.leader_takeaway("Running to time is a facilitation skill — a visible countdown keeps a 4-hour "
                   "room energised instead of drifting.")
