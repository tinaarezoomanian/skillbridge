def categorize_skills(resume_skills, job_skills):
    """
    Categorize skills into matched and missing.
    """
    matched = sorted(set(resume_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(resume_skills))
    return matched, missing
