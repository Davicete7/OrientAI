"""
wizard.py — Handles pagination controls (Back/Next/Finish) for the questionnaires.
"""

import streamlit as st

def renderWizardControls(
    is_first_page: bool,
    is_last_page: bool,
    on_next: callable,
    on_back: callable,
    on_finish: callable,
) -> None:
    """
    Render Next, Back, and Finish buttons.

    Args:
        is_first_page: True if we are on the first page (hides Back button).
        is_last_page: True if we are on the last page (shows Finish instead of Next).
        on_next: Callback function when Next is clicked.
        on_back: Callback function when Back is clicked.
        on_finish: Callback function when Finish is clicked.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if not is_first_page:
            if st.button("⬅️ Back", use_container_width=True):
                on_back()

    with col3:
        if not is_last_page:
            if st.button("Next ➡️", use_container_width=True):
                on_next()
        else:
            if st.button("🚀 Finish & Submit", use_container_width=True):
                on_finish()
