from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(resume_text, job_text):
    vect = TfidfVectorizer(stop_words="english")
    mat = vect.fit_transform([resume_text, job_text])
    score = cosine_similarity(mat[0:1], mat[1:2])[0][0]
    return score

def skill_gap(resume_skills, job_skills):
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    return matched, missing
