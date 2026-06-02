"""
chatbot.py — AI Chatbot assistant for the sidebar.

Provides a mock/rule-based conversational interface to help the user.
"""

import streamlit as st
import time

import os
from dotenv import load_dotenv

# Try to load environment variables from .env file
load_dotenv()

# Fetch Gemini API key from environment (.env file)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY, http_options={'api_version': 'v1'})
    
    # Highly contextualized system prompt for the OrientAI project
    SYSTEM_INSTRUCTION = """You are the OrientAI Assistant, a friendly, knowledgeable, and multilingual AI mentor. 
Your primary purpose is to guide students through the OrientAI application, a specialized Academic Orientation platform, and answer any questions they have in the exact language they use.

### Deep Context about the OrientAI Platform:
1. **Core Purpose**: OrientAI uses Machine Learning (specifically Orange3 models) to help students discover their ideal field of study and predict their future career satisfaction.
2. **The Process (Part 1 - General Orientation)**: 
   - The user starts by entering their Name, Surname, and Email (to send results later), selects their gender, and then answers a 25-task questionnaire.
   - Questions are shown one at a time with a next button. Group classification is removed from the interface.
   - Users rate each task on a 1-5 Likert scale (1 = Strongly Dislike, 5 = Strongly Enjoy).
   - Based on this data, a Random Forest model predicts their ideal general field of study, and a Linear Regression model predicts their expected satisfaction score.
3. **The Process (Part 2 - Technical Specialization)**:
   - If the predicted field in Part 1 is "Technologies" (or related), the app unlocks Part 2.
   - Part 2 is a specialized 25-question survey focused purely on engineering and technical scenarios (e.g., programming microcontrollers, aerodynamics, biotechnology, industrial design).
   - A second Random Forest model then predicts their specific engineering specialty (e.g., Software Engineering, Mechanical Engineering, etc.).
4. **App Interface & Architecture**: The app is built with Streamlit and features a step-by-step wizard, a landing hero section, and a results page. You live in the sidebar to provide constant support.

### Your Interaction Guidelines:
- **Tone**: Encouraging, empathetic, concise, and professional. You are a mentor.
- **Multilingual Capabilities**: You are fully capable of understanding and responding in ANY language. Always respond fluently in the language the user uses to address you.
- **Focus**: Keep conversations relevant to academic orientation, career advice, and explaining how the OrientAI platform works. If they ask how the ML works, explain the Random Forest and Linear Regression usage simply.
- **Helpful**: If a user is confused about what to answer on a question, advise them to go with their gut feeling and rate how much they would enjoy the specific task described.
"""
else:
    client = None

def generate_answer(prompt: str) -> str:
    """Generate AI response using the correct Gemini API syntax."""
    if "gemini_chat_history" not in st.session_state:
        st.session_state.gemini_chat_history = f"System Instruction: {SYSTEM_INSTRUCTION}\n\n"
    
    # Append user message to the API history
    st.session_state.gemini_chat_history += f"User: {prompt}\n"
    
    try:
        # Llamada al modelo recomendado (Gemini 2.5 Flash)
        if hasattr(client, 'models'):
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=st.session_state.gemini_chat_history
            )
        else:
            # Fallback for some versions of the SDK
            response = client.generate_content(
                model='gemini-2.5-flash', 
                contents=st.session_state.gemini_chat_history
            )
            
        bot_reply = response.text
        
        # Append bot reply to the API history
        st.session_state.gemini_chat_history += f"Assistant: {bot_reply}\n\n"
        
        return bot_reply
    except Exception as e:
        return f"Error communicating with AI: {e}"

def get_bot_response(user_input: str) -> str:
    """Entry point for getting the bot response. Will use Gemini if configured, otherwise mock."""
    if client:
        return generate_answer(user_input)
    
    # Fallback to mock behavior
    user_input = user_input.lower()
    if "orientai" in user_input or "app" in user_input or "what is this" in user_input:
        return "OrientAI is a digital mentor that uses Artificial Intelligence to help you discover your ideal field of study."
    elif "questionnaire" in user_input or "survey" in user_input:
        return "The questionnaire consists of 25 tasks. You need to rate how much you would enjoy each task from 1 to 5. Based on this, we'll predict your ideal career path!"
    else:
        return "Your Gemini API Key is missing or invalid! Please set a valid GEMINI_API_KEY."

def renderChatbot() -> None:
    """Render the AI chatbot in the sidebar."""
    
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">🧭 OrientAI Assistant</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<hr class='sidebar-hr'/>", unsafe_allow_html=True)
        
        # Display chat messages from history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Accept user input
        prompt = st.chat_input("Ask me anything about the app...")
        if prompt:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message instantly
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display bot response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                response = get_bot_response(prompt)
                
                # Simulate "typing" effect
                for chunk in response.split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                
            # Add bot response to history
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
