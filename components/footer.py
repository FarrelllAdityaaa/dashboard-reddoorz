# components/footer.py

import streamlit as st
import textwrap
from config.styles import footer_css, footer_html

def render_footer():
    """Render footer dengan team info"""
    html_full = footer_css + textwrap.dedent(footer_html)
    st.markdown(html_full, unsafe_allow_html=True)