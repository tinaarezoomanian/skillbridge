from fpdf import FPDF
from io import BytesIO

def _wrap_long_unbroken(text: str, chunk: int = 70) -> str:
    if not text:
        return ""
    out = []
    for token in str(text).split(" "):
        if len(token) > chunk:
            out.append("\n".join(token[i:i+chunk] for i in range(0, len(token), chunk)))
        else:
            out.append(token)
    return " ".join(out)

def _safe_multi_cell(pdf: FPDF, h: float, txt: str, indent: float = 0):
    # always start from a known x
    pdf.set_x(pdf.l_margin + indent)

    # compute AVAILABLE width from current x to right margin
    avail_w = pdf.w - pdf.r_margin - pdf.get_x()

    # guarantee it's never too small (prevents the "single character" crash)
    if avail_w < 10:
        pdf.set_x(pdf.l_margin)
        avail_w = pdf.w - pdf.l_margin - pdf.r_margin
        if avail_w < 10:
            avail_w = 10

    pdf.multi_cell(avail_w, h, txt)

def build_pdf_report(role, match_percent, resume_skills, job_skills, matched, missing, resources):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    pdf.set_font("Arial", "B", 16)
    _safe_multi_cell(pdf, 10, "SkillBridge Report")

    pdf.set_font("Arial", "", 12)
    _safe_multi_cell(pdf, 7, f"Role: {role}")
    _safe_multi_cell(pdf, 7, f"Match: {match_percent}%")

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    _safe_multi_cell(pdf, 7, "Missing Skills:")

    pdf.set_font("Arial", "", 11)
    for s in missing:
        _safe_multi_cell(pdf, 6, f"- {s}:", indent=0)

        r = _wrap_long_unbroken(resources.get(s, ""))
        _safe_multi_cell(pdf, 6, r, indent=6)

        pdf.ln(1)

    pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="replace")
    return BytesIO(pdf_bytes)
