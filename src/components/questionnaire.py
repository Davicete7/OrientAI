"""
questionnaire.py — Form section components for the OrientAI questionnaire.

Contains the individual UI sections that make up the questionnaire form:
user info selection, gender selection, and Likert-scale questions.
"""

import streamlit as st

from src.config import (
    GENDER_OPTIONS,
    SCALE_LABELS,
    STAR_COLORS,
)

def renderUserInfoSection() -> dict | None:
    """
    Render the user information card.
    
    Returns:
        A dict with the user details if fully filled, otherwise None.
    """
    st.markdown("""
    <div class="card">
        <div class="card-title">00 · Personal Details</div>
        <div class="card-subtitle">
            Please enter your details to receive the survey results.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user_name = st.text_input("Name", value=st.session_state.user_name, key="input_user_name")
    user_surname = st.text_input("Surname", value=st.session_state.user_surname, key="input_user_surname")
    user_email = st.text_input("Email", value=st.session_state.user_email, key="input_user_email")
    
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)
    
    if user_name and user_surname and user_email:
        return {
            "name": user_name,
            "surname": user_surname,
            "email": user_email
        }
    return None

def renderGenderSection() -> str | None:
    """
    Render the gender-selection card.

    Returns:
        The selected gender string, or None if nothing was chosen.
    """
    st.markdown("""
    <div class="card">
        <div class="card-title">01 · Demographic Information</div>
        <div class="card-subtitle">
            Used for demographic analysis — does not affect the questionnaire flow.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Use session state to remember the value if the user goes back and forth
    default_index = 0
    if st.session_state.gender and st.session_state.gender in GENDER_OPTIONS:
        default_index = GENDER_OPTIONS.index(st.session_state.gender)

    genderValue = st.selectbox(
        "What is your gender?",
        options=GENDER_OPTIONS,
        index=default_index,
        key="gender_select",
    )

    selectedGender = None if genderValue == "— select —" else genderValue
    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

    return selectedGender


def renderSingleQuestion(question: dict, global_question_offset: int) -> dict:
    """
    Render a single Likert-scale question card.

    Args:
        question: the question dict to render.
        global_question_offset: To number the questions continuously.

    Returns:
        dict mapping the question ID to its selected value (or None).
    """
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Task Interest Rating</div>
        <div class="card-subtitle">Rate how much you would enjoy the following activity.</div>
    </div>
    """, unsafe_allow_html=True)

    questionNum = global_question_offset + 1
    responses: dict = {}

    st.markdown(
        f'<div class="q-label">'
        f'<span class="q-num">Q{questionNum}.</span>'
        f'{question["text"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    leftCol, rightCol = st.columns([3, 1])

    # Restore previous answer if it exists in session
    session_dict = st.session_state.q1_responses if not question["id"].startswith("q2_") else st.session_state.q2_responses
    prev_value = session_dict.get(question["id"])
    default_index = prev_value - 1 if prev_value else None

    with leftCol:
        value = st.radio(
            label=question["text"],
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: f"{x} — {SCALE_LABELS[x]}",
            index=default_index,
            key=question["id"],
            horizontal=True,
            label_visibility="collapsed",
        )

    with rightCol:
        if value is not None:
            stars = "★" * value + "☆" * (5 - value)
            colour = STAR_COLORS[value - 1]
            st.markdown(
                f'<div style="color:{colour};font-size:1.1rem;'
                f'padding-top:0.5rem">{stars}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="warn-pill">required</span>',
                unsafe_allow_html=True,
            )

    responses[question["id"]] = value

    st.markdown('<hr class="section-divider"/>', unsafe_allow_html=True)

    return responses
