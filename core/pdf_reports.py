from fpdf import FPDF
from io import BytesIO


def _wrap_long_unbroken(text: str, chunk: int = 60) -> str:
    """
    Insert zero-width break opportunities into very long unbroken strings
    (like URLs) so FPDF can wrap them inside multi_cell.
    """
    if not text:
        return ""

    out = []
    for token in str(text).split(" "):
        if len(token) <= chunk:
            out.append(token)
        else:
            # Break long token into smaller pieces
            pieces = [token[i : i + chunk] for i in range(0, len(token), chunk)]
            out.append("\n".join(pieces))
    return " ".join(out)


def build_pdf_report(
    role,
    match_percent,
    resume_skills,
    job_skills,
    matched,
    missing,
    resources,
):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SkillBridge Report", ln=True)

    # Summary
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Role: {role}", ln=True)
    pdf.cell(0, 8, f"Match: {match_percent}%", ln=True)
    pdf.ln(3)

    # Matched Skills
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Matched Skills:", ln=True)
    pdf.set_font("Arial", "", 11)
    if matched:
        pdf.multi_cell(0, 6, ", ".join(matched))
    else:
        pdf.multi_cell(0, 6, "None")
    pdf.ln(2)

    # Missing Skills + Resources
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Missing Skills & Recommendations:", ln=True)
    pdf.set_font("Arial", "", 11)

    if not missing:
        pdf.multi_cell(0, 6, "No missing skills 🎉")
    else:
        for s in missing:
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 6, f"- {s}")
            pdf.set_font("Arial", "", 11)

            rec = resources.get(s, "")
            if isinstance(rec, (list, tuple)):
                for r in rec:
                    pdf.multi_cell(0, 6, _wrap_long_unbroken(str(r)))
            elif isinstance(rec, dict):
                for k, v in rec.items():
                    line = f"{k}: {v}"
                    pdf.multi_cell(0, 6, _wrap_long_unbroken(line))
            else:
                pdf.multi_cell(0, 6, _wrap_long_unbroken(str(rec)))

            pdf.ln(1)

    # IMPORTANT: output() can return str OR bytes/bytearray depending on fpdf version
    pdf_bytes = pdf.output(dest="S")
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin-1", errors="replace")
    else:
        pdf_bytes = bytes(pdf_bytes)

    return BytesIO(pdf_bytes)
