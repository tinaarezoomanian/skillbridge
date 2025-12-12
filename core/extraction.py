import PyPDF2
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t + "\n"
    return text

def extract_skills(text, skill_list):
    doc = nlp(text.lower())
    return sorted({t.text for t in doc if t.text in skill_list})

def extract_resume(file, skill_list):
    text = extract_text_from_pdf(file)
    skills = extract_skills(text, skill_list)
    return text, skills

def extract_job_skills(role, skill_list):
    path = f"job_postings/{role.replace(' ','_').lower()}.txt"
    with open(path) as f:
        text = f.read()
    skills = extract_skills(text, skill_list)
    return text, skills
