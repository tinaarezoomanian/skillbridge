import streamlit as st
from core.ui import inject_global_ui, card_open, card_close

inject_global_ui()

st.markdown("""
<h1 style="margin-bottom:6px;">About</h1>
<div class="sb-muted">What SkillBridge is and what it does.</div>
""", unsafe_allow_html=True)

card_open("SkillBridge", "CS 4610 Senior Project")
st.markdown("""
SkillBridge is an AI-powered career path and skill gap recommender that:
- extracts skills from resumes using NLP  
- compares them against target roles  
- identifies missing skills  
- recommends learning resources  
- generates a short learning plan  
- provides ATS-style signals and a PDF export  
""")
card_close()
