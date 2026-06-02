"""
main.py — Entry point for the OrientAI Streamlit application.

Run from the project root with:
    streamlit run src/main.py

This module wires together all the sub-modules (styles, chatbot,
hero, questionnaire wizard, results) and manages the top-level page
configuration and session state.
"""

import sys
from pathlib import Path

_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import streamlit as st

from src.state import initState, resetState
from src.components.hero import renderHero
from src.components.chatbot import renderChatbot
from src.components.wizard import renderWizardControls
from src.components.questionnaire import (
    renderUserInfoSection,
    renderGenderSection,
    renderSingleQuestion,
)
from src.components.results import renderResults
from src.questions import getQuestions, getQuestionsQ2
from src.config import GENDER_MAP
from src.export import buildJsonPayload, saveResponse
from src import predict
from src.styles import injectCustomCss

st.set_page_config(
    page_title="ORIENT AI — Academic Orientation",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

def handle_q1_next(responses, page):
    if None in responses.values():
        st.error("Please answer all questions before proceeding.")
        return
    st.session_state.q1_responses.update(responses)
    st.session_state.q1_page_index += 1
    st.rerun()

def handle_q1_back():
    st.session_state.q1_page_index -= 1
    st.rerun()

def handle_q1_finish(responses):
    if None in responses.values():
        st.error("Please answer all questions before proceeding.")
        return
    st.session_state.q1_responses.update(responses)
    
    # Predict Q1
    modelVector = [GENDER_MAP[st.session_state.gender]]
    questions = getQuestions()
    for q in questions:
        modelVector.append(st.session_state.q1_responses[q["id"]])
    
    pred_field, pred_satis = predict.predict_q1(modelVector)
    
    st.session_state.q1_predictions = {
        "field_of_study": pred_field,
        "predicted_satisfaction_score": pred_satis
    }
    
    st.session_state.q1_payload_args = {
        "user_name": st.session_state.user_name,
        "user_surname": st.session_state.user_surname,
        "user_email": st.session_state.user_email,
        "gender": st.session_state.gender,
        "responses": st.session_state.q1_responses,
        "q1_predictions": st.session_state.q1_predictions
    }

    if pred_field.lower() in ("technologies", "technology"):
        st.session_state.current_stage = "Q1_RESULTS"
        payload = buildJsonPayload(**st.session_state.q1_payload_args)
        st.session_state.filePath = saveResponse(payload)
        st.session_state.payload = payload
    else:
        st.session_state.current_stage = "RESULTS"
        payload = buildJsonPayload(**st.session_state.q1_payload_args)
        st.session_state.filePath = saveResponse(payload)
        st.session_state.payload = payload
        
        # Trigger email report (survey completed)
        from src.email_sender import send_results_email
        from src.components.results import Q1_LINKS
        links = Q1_LINKS.get(pred_field, [])
        success, msg = send_results_email(
            user_name=st.session_state.user_name,
            user_surname=st.session_state.user_surname,
            user_email=st.session_state.user_email,
            field=pred_field,
            specialty=None,
            satisfaction=pred_satis,
            links=links
        )
        if success:
            st.toast(msg, icon="📧")
        else:
            st.toast(msg, icon="⚠️")
            
    st.rerun()

def handle_q2_next(responses):
    if None in responses.values():
        st.error("Please answer all questions before proceeding.")
        return
    st.session_state.q2_responses.update(responses)
    st.session_state.q2_page_index += 1
    st.rerun()

def handle_q2_back():
    st.session_state.q2_page_index -= 1
    st.rerun()

def handle_q2_finish(responses):
    if None in responses.values():
        st.error("Please answer all questions before proceeding.")
        return
    st.session_state.q2_responses.update(responses)
    
    questions = getQuestionsQ2()
    q2_vector = [st.session_state.q2_responses[q["id"]] for q in questions]
    pred_specialty = predict.predict_q2(q2_vector)
    
    args = st.session_state.q1_payload_args.copy()
    args["q2_responses"] = st.session_state.q2_responses
    args["q2_prediction"] = pred_specialty
    
    payload = buildJsonPayload(**args)
    st.session_state.filePath = saveResponse(payload)
    st.session_state.payload = payload
    st.session_state.current_stage = "RESULTS"
    
    # Trigger email report (survey completed)
    from src.email_sender import send_results_email
    from src.components.results import Q2_LINKS
    links = Q2_LINKS.get(pred_specialty, [])
    q1_sat = st.session_state.q1_predictions.get("predicted_satisfaction_score")
    success, msg = send_results_email(
        user_name=st.session_state.user_name,
        user_surname=st.session_state.user_surname,
        user_email=st.session_state.user_email,
        field=st.session_state.q1_predictions.get("field_of_study", "Technologies"),
        specialty=pred_specialty,
        satisfaction=q1_sat,
        links=links
    )
    if success:
        st.toast(msg, icon="📧")
    else:
        st.toast(msg, icon="⚠️")
        
    st.rerun()

def main() -> None:
    injectCustomCss()
    initState()
    renderChatbot()
    
    if st.session_state.current_stage == "Q1" and st.session_state.q1_page_index == 0:
        renderHero()

    if st.session_state.current_stage == "RESULTS" and st.session_state.payload:
        renderResults(st.session_state.payload, st.session_state.filePath, is_intermediate=False)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↩ Submit another response"):
            resetState()
            st.rerun()
        return

    if st.session_state.current_stage == "Q1_RESULTS" and st.session_state.payload:
        renderResults(st.session_state.payload, st.session_state.filePath, is_intermediate=True)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Continue to Engineering Questionnaire ➡️", use_container_width=True):
                st.session_state.current_stage = "Q2"
                st.rerun()
        return

    if st.session_state.current_stage == "Q1":
        page = st.session_state.q1_page_index
        
        st.progress(page / 26.0)
        st.markdown(f'<p style="font-size:0.82rem;color:#8899aa;text-align:right;margin-top:-0.5rem">Step {page+1} of 27</p>', unsafe_allow_html=True)
        
        if page == 0:
            user_info = renderUserInfoSection()
            def on_next_user_info():
                if not user_info:
                    st.error("Please fill out all personal details before proceeding.")
                    return
                st.session_state.user_name = user_info["name"]
                st.session_state.user_surname = user_info["surname"]
                st.session_state.user_email = user_info["email"]
                st.session_state.q1_page_index += 1
                st.rerun()
            renderWizardControls(is_first_page=True, is_last_page=False, on_next=on_next_user_info, on_back=None, on_finish=None)
            
        elif page == 1:
            gender = renderGenderSection()
            def on_next_gender():
                if not gender:
                    st.error("Please select your gender before proceeding.")
                    return
                st.session_state.gender = gender
                st.session_state.q1_page_index += 1
                st.rerun()
            renderWizardControls(is_first_page=False, is_last_page=False, on_next=on_next_gender, on_back=handle_q1_back, on_finish=None)
            
        elif 2 <= page <= 26:
            q_idx = page - 2
            questions = getQuestions()
            q = questions[q_idx]
            
            responses = renderSingleQuestion(q, q_idx)
            is_last = (page == 26)
            
            renderWizardControls(
                is_first_page=False, 
                is_last_page=is_last, 
                on_next=lambda: handle_q1_next(responses, page) if not is_last else None, 
                on_back=handle_q1_back, 
                on_finish=lambda: handle_q1_finish(responses) if is_last else None
            )

    elif st.session_state.current_stage == "Q2":
        page = st.session_state.q2_page_index
        q2_questions = getQuestionsQ2()
        
        st.progress(page / 24.0)
        st.markdown(f'<p style="font-size:0.82rem;color:#8899aa;text-align:right;margin-top:-0.5rem">Part 2: Step {page+1} of 25</p>', unsafe_allow_html=True)
        
        q = q2_questions[page]
        responses = renderSingleQuestion(q, page)
        
        is_first = (page == 0)
        is_last = (page == 24)
        
        renderWizardControls(
            is_first_page=is_first, 
            is_last_page=is_last, 
            on_next=lambda: handle_q2_next(responses) if not is_last else None, 
            on_back=handle_q2_back, 
            on_finish=lambda: handle_q2_finish(responses) if is_last else None
        )

if __name__ == "__main__":
    main()
