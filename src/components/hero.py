"""
hero.py — Hero banner component for the OrientAI application.

Loads the hero HTML from ``src/templates/hero.html`` and renders it
as the prominent introductory banner at the top of the page.
"""

import streamlit as st

from src.utils import loadTemplate


def renderHero() -> None:
    """Render the hero banner with gradient background and glow effects."""

    heroHtml = loadTemplate("hero.html")
    st.markdown(heroHtml, unsafe_allow_html=True)
