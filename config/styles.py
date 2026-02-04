# config/styles.py

import streamlit as st

# --- PERSISTENT HIGHLIGHT CSS ---
persistent_highlight_css = """
<style>
/* Judul utama: beri bayangan / floating look yang selalu aktif */
.stApp .block-container h1, .stApp .block-container h1 + div {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 8px;
    box-shadow: 0 18px 48px rgba(235,54,56,0.08);
    transform: translateY(0px);
    transition: box-shadow 0.22s ease, transform 0.22s ease;
    background: transparent;
}

/* Fallback jika judul dibungkus oleh span */
.stApp .block-container h1 span {
    display: inline;
}

/* Sidebar logo: target beberapa kemungkinan selector Streamlit */
section[data-testid="stSidebar"] img,
aside img,
div[role="complementary"] img,
div.css-1offfwp img {
    display: block !important;
    margin: 10px auto !important;
    max-width: 85% !important;
    height: auto !important;
    border-radius: 8px;
    box-shadow: 0 20px 56px rgba(235,54,56,0.12);
    transform: translateY(0px);
    transition: box-shadow 0.22s ease, transform 0.22s ease;
}

/* small visual tweak for mobile / narrow sidebar */
@media (max-width: 720px) {
    section[data-testid="stSidebar"] img,
    aside img {
        max-width: 68% !important;
        box-shadow: 0 10px 30px rgba(235,54,56,0.10);
    }
}
</style>
"""

# --- HOVER & INTERACTION CSS ---
hover_enhancements = """
<style>
div[data-testid="stPlotlyChart"] {
    transition: transform 0.22s cubic-bezier(.2,.8,.2,1), box-shadow 0.22s cubic-bezier(.2,.8,.2,1);
    border-radius: 12px;
}
div[data-testid="stPlotlyChart"]:nth-of-type(1):hover {
    transform: translateY(-10px);
    box-shadow: 0 22px 56px rgba(235,54,56,0.14);
}
div[data-testid="stPlotlyChart"]:nth-of-type(2):hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 48px rgba(0,0,0,0.20);
}
.info-box:hover {
    transform: translateY(-8px);
    box-shadow: 0 18px 40px rgba(0,0,0,0.12);
    cursor: pointer;
}
.info-box:hover .info-title {
    text-decoration: underline;
    text-underline-offset: 6px;
}
table.styled-table tbody tr {
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    transform-origin: left center;
}
table.styled-table tbody tr:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.06);
    cursor: pointer;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-8px);
    box-shadow: 0 16px 40px rgba(0,0,0,0.12);
    cursor: pointer;
}
div[data-testid="stMetric"]:hover {
    border-left-width: 8px;
}
div[data-testid="stMetric"]:hover > div:nth-child(1) { font-size: 0.95rem !important; color: #444 !important; }
div[data-testid="stMetric"]:hover > div:nth-child(2) { transform: scale(1.03); }
@media (max-width: 800px) {
    div[data-testid="stPlotlyChart"]:nth-of-type(1):hover,
    div[data-testid="stPlotlyChart"]:nth-of-type(2):hover {
        transform: none; box-shadow: none;
    }
}
</style>
"""

# --- METRIC CARDS STYLING ---
def style_metric_cards(
    background_color="#FFFFFF",
    border_left_color="#EB3638",
    border_color="#E6E6E6",
    box_shadow=True
):
    box_shadow_css = "box-shadow: 0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24);" if box_shadow else ""
    st.markdown(f"""
    <style>
    /* Normalize box-sizing */
    .stApp, .stApp * {{ box-sizing: border-box; }}

    /* Metric cards base */
    div[data-testid="stMetric"] {{
        background-color: {background_color};
        border: 1px solid {border_color};
        padding: 15px;
        border-radius: 10px;
        border-left: 6px solid {border_left_color};
        {box_shadow_css}
        transition: transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s ease;
        cursor: default;
    }}

    /* Info box base */
    .info-box {{
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        display: block;
        vertical-align: top;
        min-height: 260px !important;
        height: 100% !important;
        transition: transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s ease;
    }}
    .info-title {{
        font-size: 16px;
        font-weight: 700;
        color: #EB3638;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}
    .info-text {{
        font-size: 14px;
        color: #495057;
        line-height: 1.6;
        text-align: justify;
    }}

    /* Ensure the column containers don't add extra spacing that breaks height */
    .stApp .stColumns > div {{
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }}

    /* Safety target our two info-boxes */
    .stApp .block-container .stColumns > div > div {{
        min-height: 260px !important;
    }}

    /* Safety target our two info-boxes */
    .stApp .stColumns > div:nth-child(1) .info-box,
    .stApp .stColumns > div:nth-child(2) .info-box {{
        min-height: 260px !important;
        height: 100% !important;
    }}

    @media (max-width: 900px) {{
        .info-box {{
            min-height: 180px !important;
        }}
    }}

    /* ================
      TABEL STYLING
      ================ */
    table.styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        font-size: 14px;
    }}

    table.styled-table thead th {{
        background-color: #EB3638 !important;
        color: white !important;
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
    }}

    table.styled-table tbody td {{
        padding: 10px;
        border: 1px solid #ddd;
        background-color: white;
    }}

    table.styled-table tbody tr:nth-child(2),
    table.styled-table tbody tr:nth-child(4) {{
        background-color: #f5f5f5 !important;
    }}

    table.styled-table tr:hover td {{
        background-color: #fafafa;
    }}

    /* KPI styling */
    div[data-testid="stMetric"] > div:nth-child(1) {{
        font-weight: 700 !important;
        color: #666666;
    }}
    div[data-testid="stMetric"] > div:nth-child(2) {{
        font-weight: 900 !important;
        font-size: 1.6rem !important;
    }}
    .stMetricValue, .stMetricLabel {{
        font-weight: 900 !important;
    }}

    </style>
    """, unsafe_allow_html=True)

# --- FOOTER CSS & HTML ---
footer_css = """
<style>
.footer-container {
    background: transparent;
    padding: 18px 12px;
    border-radius: 10px;
    text-align: center;
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #333333;
    margin-top: 170px;
    border-top: 3px solid #EB3638;
    padding-top: 30px;
}
.footer-container .sponsor {
    color: #666666;
    font-size: 14px;
    margin-bottom: 6px;
}
.footer-container h2 {
    color: #EB3638 !important;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 0;
    font-size: 20px;
    display: inline-block;
    padding: 8px 14px;
    border-radius: 14px;
    box-shadow: 0 26px 60px rgba(235,54,56,0.10), inset 0 1px 0 rgba(255,255,255,0.2);
    transform: translateY(-4px);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}
.footer-container .team {
    display: flex;
    justify-content: center;
    gap: 18px;
    flex-wrap: wrap;
    margin-top: 12px;
    color: #2D2D2D;
    font-weight: 600;
    font-size: 15px;
}
.team-badge {
    padding: 8px 18px;
    border-radius: 24px;
    color: white;
    font-weight: 700;
    font-size: 14px;
    display: inline-block;
    margin: 6px;
    background-image: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(0,0,0,0.02));
    box-shadow: 0 18px 40px rgba(0,0,0,0.10), 0 6px 18px rgba(0,0,0,0.06);
    transform: translateY(-3px);
    transition: transform 0.35s ease, box-shadow 0.35s ease;
    text-shadow: 0 1px 0 rgba(0,0,0,0.18);
}
@keyframes float-subtle {
    0% { transform: translateY(-3px); }
    50% { transform: translateY(-1px); }
    100% { transform: translateY(-3px); }
}
.team-badge { animation: float-subtle 4.5s ease-in-out infinite; }
.team-badge[style*="#EB3638"] { background-color: #EB3638; color: white; }
.team-badge[style*="#FF7F50"] { background-color: #FF7F50; color: white !important; text-shadow: 0 1px 0 rgba(0,0,0,0.22); }
.team-badge[style*="#8B0000"] { background-color: #8B0000; color: white; }
@media (max-width: 600px) {
    .footer-container h2 { font-size: 18px; padding: 6px 10px; transform: translateY(0); box-shadow: 0 12px 28px rgba(235,54,56,0.08); }
    .team-badge { padding: 6px 12px; font-size: 13px; animation-duration: 5.5s; }
}
.footer-container .copyright { color: #999999; font-size: 12px; margin-top: 18px; }
</style>
"""

footer_html = """
<div class="footer-container">
  <div class="sponsor">Dashboard ini dipersembahkan oleh:</div>
  <h2>📊 SAFARI DATA 🐱</h2>

  <div class="team">
    <span class="team-badge" style="background:#EB3638;">👩🏻‍💻 Nabila Putri Asy Syifa</span>
    <span class="team-badge" style="background:#FF7F50;">🧑🏻‍💻 Farrel Paksi Aditya</span>
  </div>

  <div class="copyright">© 2025 Proyek Akhir Visualisasi Data | RedDoorz Analysis</div>
</div>
"""

def apply_all_styles():
    """Apply semua CSS styling ke aplikasi"""
    st.markdown(persistent_highlight_css, unsafe_allow_html=True)
    st.markdown(hover_enhancements, unsafe_allow_html=True)
    style_metric_cards()
