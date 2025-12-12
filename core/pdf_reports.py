from fpdf import FPDF
from io import BytesIO

def _page_text_width(pdf: FPDF) -> float:
    return pdf.w - pdf.l_margin - pdf.r_margin

def _wrap_long_unbroken(text: str, chunk: int = 80) -> str:
    # breaks super-long URLs/strings so FPDF can wrap them
    if not text:
        return ""
    parts = []
    for token in text.split(" "):
        if len(token) > chunk:
            parts.append("\n".join(token[i:i+chunk] for i in range(0, len(token), chunk)))
        else:
            parts.append(token)
    return " ".join(parts)

def build_pdf_report(role, match_percent, resume_skills, job_skills, matched, missing, resources):
    pdf = FPDF()
    pdf.add_page()
    w = _page_text_width(pdf)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(w, 10, "SkillBridge Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(w, 8, f"Role: {role}", ln=True)
    pdf.cell(w, 8, f"Match: {match_percent}%", ln=True)

    pdf.ln(3)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(w, 8, "Missing Skills:", ln=True)

    pdf.set_font("Arial", "", 11)
    for s in missing:
        # Skill title line
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w, 6, f"- {s}:")

        # Resource line (indented) – break long URLs/strings
        r = str(resources.get(s, ""))
        pdf.set_x(pdf.l_margin + 6)
        pdf.multi_cell(w - 6, 6, _wrap_long_unbroken(r))

        pdf.ln(1)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_bytes)
