"""
styles.py — Custom CSS injection for the OrientAI Streamlit app.

Loads the stylesheet from ``src/static/styles.css`` and injects it
into the Streamlit page.  Keeping the CSS in an external file lets
designers edit visual styles without touching Python code.
"""

import streamlit as st

from src.utils import loadStaticFile


def injectCustomCss() -> None:
    """Load the external CSS file and inject it into the page."""

    cssContent = loadStaticFile("styles.css")
    st.markdown(f"<style>{cssContent}</style>", unsafe_allow_html=True)
