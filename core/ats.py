# core/ats.py

ACTION_VERBS = {
    "developed", "built", "designed", "implemented", "created", "led", "managed",
    "optimized", "improved", "analyzed", "automated", "deployed", "configured",
    "tested", "maintained", "integrated", "refactored", "debugged", "collaborated",
    "trained", "presented", "documented"
}

SECTION_HEADERS = [
    "education", "experience", "work experience", "projects",
    "skills", "technical skills", "summary", "profile"
]


def _section_score(text_lower: str) -> float:
    found = 0
    for sec in SECTION_HEADERS:
        if sec in text_lower:
            found += 1
    # max score if 4+ core sections appear
    return min(found / 4.0, 1.0) * 100.0


def _formatting_score(lines) -> float:
    total = len(lines) or 1
    bullet_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("-", "•", "*")):
            bullet_lines += 1

    bullet_ratio = bullet_lines / total

    if bullet_ratio >= 0.4:
        bullets_score = 100
    elif bullet_ratio >= 0.2:
        bullets_score = 85
    elif bullet_ratio >= 0.1:
        bullets_score = 70
    else:
        bullets_score = 50

    return float(bullets_score)


def _length_score(word_count: int) -> float:
    # simple heuristic: 250–900 words is ideal
    if 250 <= word_count <= 900:
        return 100.0
    if 150 <= word_count < 250 or 900 < word_count <= 1200:
        return 80.0
    return 60.0


def _verb_score(lines) -> float:
    bullet_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("-", "•", "*")):
            bullet_lines.append(stripped.lstrip("-•* ").lower())

    if not bullet_lines:
        return 60.0

    strong = 0
    for bl in bullet_lines:
        first_word = bl.split()[0] if bl.split() else ""
        if first_word in ACTION_VERBS:
            strong += 1

    ratio = strong / len(bullet_lines)
    if ratio >= 0.6:
        return 100.0
    if ratio >= 0.3:
        return 80.0
    return 60.0


def _keyword_score(text_lower: str, job_skills) -> float:
    if not job_skills:
        return 0.0
    matched = 0
    for skill in job_skills:
        if skill.lower() in text_lower:
            matched += 1
    return (matched / len(job_skills)) * 100.0


def analyze_ats(resume_text: str, job_skills):
    """
    Return a dict with ATS-style scores:
    - formatting_score
    - length_score
    - section_score
    - verb_score
    - keyword_score
    - ats_score (overall)
    """
    text_lower = resume_text.lower()
    lines = [ln for ln in resume_text.splitlines() if ln.strip()]
    word_count = len(text_lower.split())

    formatting_score = _formatting_score(lines)
    length_score = _length_score(word_count)
    section_score = _section_score(text_lower)
    verb_score = _verb_score(lines)
    keyword_score = _keyword_score(text_lower, job_skills)

    # weighted overall ATS score
    ats_score = (
        0.25 * formatting_score
        + 0.15 * length_score
        + 0.25 * keyword_score
        + 0.20 * section_score
        + 0.15 * verb_score
    )

    return {
        "formatting_score": round(formatting_score, 1),
        "length_score": round(length_score, 1),
        "section_score": round(section_score, 1),
        "verb_score": round(verb_score, 1),
        "keyword_score": round(keyword_score, 1),
        "ats_score": round(ats_score, 1),
        "word_count": word_count,
    }
