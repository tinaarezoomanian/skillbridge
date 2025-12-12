# core/resources.py

def load_skill_list():
    return [
        "python", "sql", "pandas", "numpy", "java", "javascript",
        "html", "css", "bash", "excel", "tableau", "git",
        "machine learning", "deep learning", "statistics",
        "data visualization", "linux", "cloud", "aws",
        "react", "node", "security", "networking"
    ]


# --------------------------------------------------
# SKILL → REAL LEARNING RESOURCES
# --------------------------------------------------
SKILL_RESOURCES = {
    "python": "https://docs.python.org/3/tutorial/",
    "sql": "https://www.w3schools.com/sql/",
    "pandas": "https://pandas.pydata.org/docs/getting_started/index.html",
    "numpy": "https://numpy.org/learn/",
    "java": "https://dev.java/learn/",
    "javascript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
    "html": "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "css": "https://developer.mozilla.org/en-US/docs/Web/CSS",
    "bash": "https://www.codecademy.com/learn/learn-the-command-line",
    "excel": "https://www.coursera.org/learn/excel-data-analysis",
    "tableau": "https://www.tableau.com/learn/training",
    "git": "https://git-scm.com/book/en/v2",
    "machine learning": "https://www.coursera.org/learn/machine-learning",
    "deep learning": "https://www.deeplearning.ai/short-courses/",
    "statistics": "https://www.khanacademy.org/math/statistics-probability",
    "data visualization": "https://www.storytellingwithdata.com/",
    "linux": "https://linuxjourney.com/",
    "cloud": "https://cloud.google.com/learn",
    "aws": "https://explore.skillbuilder.aws/learn",
    "react": "https://react.dev/learn",
    "node": "https://nodejs.dev/en/learn/",
    "security": "https://www.cybrary.it/catalog/cybersecurity/",
    "networking": "https://www.netacad.com/courses/networking"
}


def recommend_resources(missing_skills):
    """
    Returns a dict: skill -> learning URL
    """
    recs = {}
    for skill in missing_skills:
        recs[skill] = SKILL_RESOURCES.get(
            skill,
            "https://www.coursera.org/browse/computer-science"
        )
    return recs
