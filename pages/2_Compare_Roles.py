import streamlit as st
import pandas as pd

from core.extraction import extract_resume, extract_job_skills
from core.resources import load_skill_list
from core.scoring import compute_similarity, skill_gap
from core.utils import JOB_ROLE_FILES
from core.ui import inject_global_ui, card_open, card_close

inject_global_ui()

st.markdown("""
<div class="sb-fadein" style="position:relative; z-index:1;">
  <h1 style="margin-bottom:0;">Compare Roles</h1>
  <div class="sb-muted" style="margin-top:6px;">
    See which roles your current resume fits best.
  </div>
</div>
""", unsafe_allow_html=True)

skills_list = load_skill_list()

with st.sidebar:
    st.markdown("## 📄 Upload")
    file = st.file_uploader("Upload resume (PDF)", type=["pdf"])

if not file:
    st.info("Upload a resume to compare your fit across roles.")
    st.stop()

resume_text, resume_skills = extract_resume(file, skills_list)

rows = []
for role in JOB_ROLE_FILES.keys():
    job_text, job_skills = extract_job_skills(role, skills_list)
    matched, missing = skill_gap(resume_skills, job_skills)
    score = compute_similarity(resume_text, job_text)
    rows.append({"Role": role, "Match %": int(score * 100), "Matched": len(matched), "Missing": len(missing)})

df = pd.DataFrame(rows).sort_values("Match %", ascending=False)

card_open("🏆 Best Fit Roles", "Sorted by match score")
st.dataframe(df.reset_index(drop=True), use_container_width=True, hide_index=True)
card_close()

card_open("📊 Match % by Role", "Quick visual of where you’re closest")
st.bar_chart(df.set_index("Role")[["Match %"]], height=240)
card_close()
