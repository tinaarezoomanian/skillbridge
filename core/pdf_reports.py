from fpdf import FPDF
from io import BytesIO

def build_pdf_report(role, match_percent, resume_skills, job_skills, matched, missing, resources):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SkillBridge Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Role: {role}", ln=True)
    pdf.cell(0, 10, f"Match: {match_percent}%", ln=True)

    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 8, "Missing Skills:", ln=True)

    pdf.set_font("Arial", "", 11)
    for s in missing:
        pdf.multi_cell(0, 6, f"- {s}: {resources[s]}")

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_bytes)
