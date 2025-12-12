from fpdf import FPDF
from io import BytesIO


def _sanitize(text: str) -> str:
    if text is None:
        return ""
    # Remove/control characters that can mess up layout
    s = str(text).replace("\r", " ").replace("\t", " ")
    return s


def _wrap_long_unbroken(text: str, chunk: int = 60) -> str:
    """
    Break very long unbroken tokens (like URLs) into smaller chunks by inserting
    newlines so FPDF has break points.
    """
    s = _sanitize(text)
    if not s:
        return ""

    out = []
    for token in s.split(" "):
        if len(token) <= chunk:
            out.append(token)
        else:
            pieces = [token[i : i + chunk] for i in range(0, len(token), chunk)]
            out.append("\n".join(pieces))
    return " ".join(out)


def _mc(pdf: FPDF, w: float, h: float, txt: str):
    """
    Safe multi_cell: reset X to left margin + use explicit width.
    """
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w, h, _sanitize(txt))


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

    content_w = pdf.w - pdf.l_margin - pdf.r_margin

    # Title
    pdf.set_font("Arial", "B", 16)
    _mc(pdf, content_w, 10, "SkillBridge Report")

    # Summary
    pdf.set_font("Arial", "", 12)
    _mc(pdf, content_w, 7, f"Role: {role}")
    _mc(pdf, content_w, 7, f"Match: {match_percent}%")
    pdf.ln(2)

    # Matched Skills
    pdf.set_font("Arial", "B", 12)
    _mc(pdf, content_w, 7, "Matched Skills:")
    pdf.set_font("Arial", "", 11)
    _mc(pdf, content_w, 6, ", ".join(matched) if matched else "None")
    pdf.ln(2)

    # Missing Skills + Resources
    pdf.set_font("Arial", "B", 12)
    _mc(pdf, content_w, 7, "Missing Skills & Recommendations:")
    pdf.set_font("Arial", "", 11)

    if not missing:
        _mc(pdf, content_w, 6, "No missing skills 🎉")
    else:
        for s in missing:
            pdf.set_font("Arial", "B", 11)
            _mc(pdf, content_w, 6, f"- {s}")

            pdf.set_font("Arial", "", 10)
            rec = resources.get(s, "")

            if isinstance(rec, (list, tuple)):
                for r in rec:
                    _mc(pdf, content_w, 5, _wrap_long_unbroken(r))
            elif isinstance(rec, dict):
                for k, v in rec.items():
                    _mc(pdf, content_w, 5, _wrap_long_unbroken(f"{k}: {v}"))
            else:
                _mc(pdf, content_w, 5, _wrap_long_unbroken(rec))

            pdf.ln(1)

    # output() return type depends on fpdf version
    out = pdf.output(dest="S")
    pdf_bytes = out.encode("latin-1", errors="replace") if isinstance(out, str) else bytes(out)
    return BytesIO(pdf_bytes)
