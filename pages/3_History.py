import streamlit as st
import pandas as pd
from core.utils import load_history
from core.ui import inject_global_ui, card_open, card_close

inject_global_ui()

st.markdown("""
<div class="sb-fadein" style="position:relative; z-index:1;">
  <h1 style="margin-bottom:0;">History</h1>
  <div class="sb-muted" style="margin-top:6px;">
    Track your match score over time as you improve your resume.
  </div>
</div>
""", unsafe_allow_html=True)

df = load_history()
if df is None or df.empty:
    st.info("No history yet. Run Career Analyzer first.")
    st.stop()

df_sorted = df.sort_values("timestamp", ascending=True)

card_open("📋 Past Analyses", "Your saved snapshots")
st.dataframe(df_sorted, use_container_width=True)
card_close()

card_open("📈 Match % Over Time", "Progress chart")
chart_df = df_sorted.set_index("timestamp")[["match_percent"]]
st.line_chart(chart_df, height=240)
card_close()
