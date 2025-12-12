import streamlit as st

from core.extraction import extract_resume, extract_job_skills
from core.resources import recommend_resources, load_skill_list
from core.scoring import compute_similarity
from core.charts import categorize_skills
from core.learning_plan import build_learning_plan
from core.pdf_reports import build_pdf_report
from core.utils import save_history, JOB_ROLE_FILES
from core.ats import analyze_ats
from core.ui import inject_global_ui, card_open, card_close, badge, score_ring


# --------------------------------------------------
# GLOBAL UI + HEADER
# --------------------------------------------------
inject_global_ui()

st.markdown("""
<h1>Career Analyzer</h1>
<div class="sb-muted">
Upload your resume and get a clean snapshot of your skill alignment.
</div>
""", unsafe_allow_html=True)

skills_list = load_skill_list()


# --------------------------------------------------
# INPUTS (MAIN SCREEN)
# --------------------------------------------------
card_open("🚀 Get Started", "Upload your resume and select a target role")

c1, c2 = st.columns([1.3, 1])
with c1:
    uploaded_file = st.file_uploader("Resume (PDF)", type=["pdf"])
with c2:
    role = st.selectbox("Target Role", list(JOB_ROLE_FILES.keys()))

card_close()

if not uploaded_file or not role:
    st.info("Upload a resume and choose a role to continue.")
    st.stop()


# --------------------------------------------------
# EXTRACTION + SCORING
# --------------------------------------------------
resume_text, resume_skills = extract_resume(uploaded_file, skills_list)
job_text, job_skills = extract_job_skills(role, skills_list)

matched, missing = categorize_skills(resume_skills, job_skills)
match_percent = int(compute_similarity(resume_text, job_text) * 100)

recs = recommend_resources(missing)
plan = build_learning_plan(missing, recs)
ats = analyze_ats(resume_text, job_skills)

save_history(role, match_percent, resume_skills, matched, missing)

if match_percent >= 75:
    st.balloons()


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
card_open("📊 Overview", "High-level snapshot")

o1, o2, o3, o4 = st.columns([1.4, 1, 1, 1])

with o1:
    score_ring(match_percent)
    st.caption("Match Score")

o2.metric("ATS Score", ats["ats_score"])
o3.metric("Skills Found", len(resume_skills))
o4.metric("Missing Skills", len(missing))

st.markdown(
    f"<div class='sb-muted'><b>Target role:</b> {role}</div>",
    unsafe_allow_html=True
)

card_close()


# --------------------------------------------------
# SKILLS SNAPSHOT (CHIPS)
# --------------------------------------------------
card_open("🧩 Skills Snapshot", "Clear view of what you have vs what you need")

st.markdown("**Matched Skills**")
if matched:
    for skill in matched:
        badge(skill.title(), "good")
else:
    st.info("No matched skills detected.")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("**Missing Skills**")
if missing:
    for skill in missing:
        badge(skill.title(), "bad")
else:
    st.success("You meet all required skills for this role.")

card_close()


# --------------------------------------------------
# ATS BREAKDOWN
# --------------------------------------------------
card_open("🧠 ATS Resume Analysis")

a1, a2, a3 = st.columns(3)
a1.metric("Formatting", ats["formatting_score"])
a2.metric("Sections", ats["section_score"])
a3.metric("Length", ats["length_score"])

a4, a5, a6 = st.columns(3)
a4.metric("Action Verbs", ats["verb_score"])
a5.metric("Keyword Match", ats["keyword_score"])
a6.metric("Word Count", ats["word_count"])

card_close()


# --------------------------------------------------
# LEARNING PLAN
# --------------------------------------------------
card_open("🗓️ Personalized Learning Plan")

if plan:
    for item in plan:
        st.markdown(
            f"""
            **{item['Week']}** — **{item['Skill'].title()}**  
            [Start learning →]({item['Resource']})
            """
        )
else:
    st.info("No learning plan needed.")

card_close()


# --------------------------------------------------
# PDF EXPORT
# --------------------------------------------------
card_open("📄 Download Report")

pdf = build_pdf_report(
    role,
    match_percent,
    resume_skills,
    job_skills,
    matched,
    missing,
    recs
)

st.download_button(
    "Download PDF Summary",
    pdf,
    "skillbridge_report.pdf",
    "application/pdf"
)

card_close()


# --------------------------------------------------
# RAW TEXT (OPTIONAL)
# --------------------------------------------------
with st.expander("📘 View Extracted Resume Text"):
    st.text(resume_text)
