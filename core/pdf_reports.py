from fpdf import FPDF
from io import BytesIO

def _wrap_long_unbroken(text: str, chunk: int = 70) -> str:
    """
    FPDF can fail on very long 'words' (like URLs) with no spaces.
    This forces safe wrap points by inserting newlines every `chunk` chars
    if there aren't already line breaks.
    """
    if text is None:
        return ""
    text = str(text)
    # If it already has spaces/newlines, let FPDF wrap naturally
    if (" " in text) or ("\n" in text) or ("\t" in text):
        return text
    # Otherwise force breaks
    return "\n".join(text[i:i+chunk] for i in range(0, len(text), chunk))

def build_pdf_report(role, match_percent, resume_skills, job_skills, matched, missing, resources):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_left_margin(12)
    pdf.set_right_margin(12)

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
        # Safe lookup + safe wrapping
        r = resources.get(s, "")
        # Put skill on its own line, resource on the next (cleaner + safer)
        pdf.multi_cell(0, 6, f"- {s}")
        pdf.multi_cell(0, 6, _wrap_long_unbroken(r))
        pdf.ln(1)

    pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="replace")
    return BytesIO(pdf_bytes)
