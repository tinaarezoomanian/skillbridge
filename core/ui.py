import streamlit as st

def inject_global_ui():
    st.markdown("""
    <style>
    /* ================= FONT ================= */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 15px !important;
        color: #0F172A;
    }

    /* ================= BACKGROUND ================= */
    .stApp {
        background-color: #F8FAFC;
    }

    /* ================= LAYOUT ================= */
    .block-container {
        max-width: 1150px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* ================= HEADERS ================= */
    h1 {
        font-size: 2.6rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.7px;
        margin-bottom: 0.6rem;
        line-height: 1.15;
        color: #4F46E5;
    }

    h3 {
        font-size: 1.35rem !important;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }

    /* ================= GRADIENT TEXT (TEXT ONLY) ================= */
    .gradient-text {
        background: linear-gradient(90deg, #4F46E5, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* ================= GLASS CARDS ================= */
    .sb-card {
        background: #FFFFFF;
        border-radius: 18px;
        border: 1px solid #E5E7EB;
        padding: 1.6rem;
        margin-bottom: 1.8rem;

        box-shadow: 0 14px 34px rgba(15,23,42,0.08);
        transition:
            transform 180ms ease,
            box-shadow 180ms ease,
            border-color 180ms ease;
    }

    .sb-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 24px 54px rgba(79,70,229,0.18);
        border-color: #C7D2FE;
    }

    /* ================= MUTED TEXT ================= */
    .sb-muted {
        color: #64748B;
        font-size: 14px;
        margin-top: 0.2rem;
    }

    /* ================= BADGES ================= */
    .sb-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        margin: 6px 6px 0 0;
        font-size: 14px;
        font-weight: 600;
    }

    .sb-good {
        background: #EEF2FF;
        color: #3730A3;
        border: 1px solid #C7D2FE;
    }

    .sb-bad {
        background: #FEF2F2;
        color: #9F1239;
        border: 1px solid #FECACA;
    }

    /* ================= METRICS ================= */
    [data-testid="stMetricValue"] {
        font-size: 1.7rem;
        font-weight: 700;
        color: #3730A3;
    }

    /* ================= BUTTONS ================= */
    .stButton button,
    .stDownloadButton button {
        border-radius: 14px !important;
        padding: 0.65rem 1.1rem !important;
        font-weight: 700 !important;

        background: linear-gradient(135deg, #6366F1, #06B6D4) !important;
        color: white !important;
        border: none !important;

        box-shadow: 0 10px 28px rgba(79,70,229,0.35);
        transition: transform 150ms ease, box-shadow 150ms ease;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 40px rgba(79,70,229,0.55);
    }
    </style>
    """, unsafe_allow_html=True)


def card_open(title, subtitle=None):
    st.markdown(f"""
    <div class="sb-card">
        <h3>{title}</h3>
        {f"<div class='sb-muted'>{subtitle}</div>" if subtitle else ""}
    """, unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def badge(text, kind="good"):
    cls = "sb-good" if kind == "good" else "sb-bad"
    st.markdown(
        f"<span class='sb-badge {cls}'>{text}</span>",
        unsafe_allow_html=True
    )


def score_ring(percent):
    st.markdown(f"""
    <div style="
        width:130px;
        height:130px;
        border-radius:50%;
        background: conic-gradient(#6366F1 {percent}%, #E5E7EB 0);
        display:flex;
        align-items:center;
        justify-content:center;
        margin:auto;
        box-shadow: 0 0 26px rgba(99,102,241,0.4);
    ">
        <div style="
            width:92px;
            height:92px;
            border-radius:50%;
            background:#FFFFFF;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:28px;
            font-weight:800;
            color:#3730A3;
            border:1px solid #E5E7EB;
        ">
            {percent}%
        </div>
    </div>
    """, unsafe_allow_html=True)
