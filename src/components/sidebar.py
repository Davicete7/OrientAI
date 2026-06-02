"""
sidebar.py — Sidebar component for the OrientAI application.

Renders the persistent sidebar containing the project logo,
version info, usage instructions, and the Likert-scale reference.
"""

import streamlit as st

from src.config import SCALE_LABELS


def renderSidebar() -> None:
    """Render the full sidebar panel."""

    with st.sidebar:
        # ── Logo & version ────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-logo">🧭 ORIENT AI</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="sidebar-version">'
            'v1.0 · Łódź University of Technology'
            '</div>',
            unsafe_allow_html=True,
        )

        # ── About section ─────────────────────────────────────────
        st.markdown(
            '<div class="sidebar-section">About</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sidebar-item">🎓 AI-driven academic orientation</div>
            <div class="sidebar-item">📊 25 questionnaire items</div>
            <div class="sidebar-item">🤖 ML model integration ready</div>
            """,
            unsafe_allow_html=True,
        )

        # ── How to use ────────────────────────────────────────────
        st.markdown('<hr class="sidebar-hr"/>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-section">How to use</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="sidebar-item">1. Enter personal details</div>
            <div class="sidebar-item">2. Select your gender</div>
            <div class="sidebar-item">3. Rate each task 1–5</div>
            <div class="sidebar-item">4. Submit the form</div>
            """,
            unsafe_allow_html=True,
        )

        # ── Scale reference ───────────────────────────────────────
        st.markdown('<hr class="sidebar-hr"/>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-section">Scale Reference</div>',
            unsafe_allow_html=True,
        )
        for numericValue, label in SCALE_LABELS.items():
            st.markdown(
                f'<div class="sidebar-item">'
                f'<b>{numericValue}</b> — {label}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # ── Footer ────────────────────────────────────────────────
        st.markdown('<hr class="sidebar-hr"/>', unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size:0.75rem;color:#55667a;text-align:center">'
            '© 2025 ORIENT AI Project'
            '</div>',
            unsafe_allow_html=True,
        )
