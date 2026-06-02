"""
state.py — Session state management for OrientAI.

Centralizes the initialization of all required session state variables.
"""

import streamlit as st
from src.questions import getQuestions, getQuestionsQ2

def initState():
    """Initialize all session state variables."""
    if "current_stage" not in st.session_state:
        st.session_state.current_stage = "Q1"  # Stages: "Q1", "Q2", "RESULTS"
    
    if "q1_page_index" not in st.session_state:
        st.session_state.q1_page_index = 0     # 0: User Info, 1: Gender, 2-26: Questions

    if "q2_page_index" not in st.session_state:
        st.session_state.q2_page_index = 0     # 0-24: Questions

    if "payload" not in st.session_state:
        st.session_state.payload = None

    if "filePath" not in st.session_state:
        st.session_state.filePath = ""

    # Initialize dictionaries to hold responses so they persist across pages
    if "q1_responses" not in st.session_state:
        st.session_state.q1_responses = {}

    if "q2_responses" not in st.session_state:
        st.session_state.q2_responses = {}

    if "gender" not in st.session_state:
        st.session_state.gender = None

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if "user_surname" not in st.session_state:
        st.session_state.user_surname = ""
        
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""

    # Chatbot history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your OrientAI assistant. I can help you understand what this app does or explain any questions you might have. How can I help?"}
        ]

def resetState():
    """Reset all session state for a new submission."""
    st.session_state.current_stage = "Q1"
    st.session_state.q1_page_index = 0
    st.session_state.q2_page_index = 0
    st.session_state.payload = None
    st.session_state.filePath = ""
    st.session_state.q1_responses = {}
    st.session_state.q2_responses = {}
    st.session_state.gender = None
    st.session_state.user_name = ""
    st.session_state.user_surname = ""
    st.session_state.user_email = ""
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your OrientAI assistant. I can help you understand what this app does or explain any questions you might have. How can I help?"}
    ]
    
    # Clear radio/slider keys
    for question in getQuestions() + getQuestionsQ2():
        st.session_state.pop(question["id"], None)
    st.session_state.pop("gender_select", None)
