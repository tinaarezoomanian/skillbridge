import streamlit as st
import os
import pandas as pd
from datetime import datetime

def apply_theme():
    st.markdown("""
        <style>
        .block-container { padding-top: 2rem; }
        h1, h2, h3 { color: #1F6FFF !important; }
        </style>
    """, unsafe_allow_html=True)

JOB_ROLE_FILES = {
    "Data Analyst": "job_postings/data_analyst.txt",
    "Software Engineer": "job_postings/software_engineer.txt",
    "Data Scientist": "job_postings/data_scientist.txt",
    "Machine Learning Engineer": "job_postings/machine_learning_engineer.txt",
    "Cybersecurity Analyst": "job_postings/cybersecurity_analyst.txt",
    "Frontend Developer": "job_postings/frontend_developer.txt",
    "Backend Developer": "job_postings/backend_developer.txt",
}

HISTORY_PATH = "history/history.csv"

def save_history(role, score, resume_skills, matched, missing):
    os.makedirs("history", exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = {
        "timestamp": now,
        "role": role,
        "match_percent": score,
        "resume_skills": len(resume_skills),
        "matched": len(matched),
        "missing": len(missing),
    }

    if os.path.exists(HISTORY_PATH):
        df = pd.read_csv(HISTORY_PATH)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(HISTORY_PATH, index=False)
    return df

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return None
    return pd.read_csv(HISTORY_PATH)
