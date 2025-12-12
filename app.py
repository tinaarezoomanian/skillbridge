import streamlit as st
from core.utils import apply_theme
from core.ui import inject_global_ui, card_open, card_close

st.set_page_config(
    page_title="SkillBridge",
    page_icon="🧭",
    layout="wide",
)

apply_theme()
inject_global_ui()

st.markdown("""
<h1>SkillBridge 🧭</h1>
<p class="sb-muted">
AI-powered resume analysis and skill gap recommendations.
</p>
""", unsafe_allow_html=True)

card_open("What SkillBridge does")
st.markdown("""
SkillBridge analyzes your resume against real job roles to:
- measure how well your skills align  
- identify missing or weak areas  
- suggest learning resources  
- generate a short, realistic learning plan  
""")
card_close()

st.success("Use the sidebar to open **Career Analyzer** and get started.")
