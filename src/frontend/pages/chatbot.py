import streamlit as st
import requests
from app import common_functions
from datetime import datetime

API_URL = "http://localhost:8000/chat/get-health-advice/"
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
common_functions.config_homepage()
common_functions.set_page_title()
# Initialize conversation history
def initialize_conversation():
    assistant_message = ("Hello! I am your Yuvabe Care Companion AI, here to assist you with general medicine queries. " 
                         "How can I help you today?")
    
    return [{"role": "assistant", "content": assistant_message}]
system_message = ("Hello! I am your Yuvabe Care Companion AI, here to assist you with general medicine queries. " 
                         "How can I help you today?")

# Function to fetch advice from the API
def fetch_health_advice(conversation_history):
    try:
        response = requests.post(
            API_URL,
            json={"conversation_history": conversation_history}
        )
        response.raise_for_status()
        return response.json().get("reply", "I couldn't process your request at the moment.")
    except requests.exceptions.RequestException as e:
        st.error(f"API Connection Error: {e}")
        return "I'm currently unable to respond. Please try again later."

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display chat history
for message in st.session_state.conversation_history [-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
    role = message["role"]
    avatar_image = "src/frontend/images/page_icon.jpg" if role == "assistant" else "src/frontend/images/page_icon.jpg" if role == "user" else None
    with st.chat_message(role, avatar=avatar_image):
        st.write(message["content"])

# User Input
user_input = st.chat_input("Ask your health-related question:")
with st.chat_message('ai'):
    common_functions.typewriter_effect(system_message)

if user_input:

    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = datetime.now().strftime("%Y-%m-%d")

    # Display user's input
    with st.chat_message('user'):
        common_functions.typewriter_effect(user_input)
        
    # Append user input to session history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # Fetch assistant response
    assistant_reply = fetch_health_advice(st.session_state.conversation_history)

    # Append assistant's reply to conversation history first
    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
    common_functions.store_chat_history_in_db(st.session_state.conversation_id,st.session_state.conversation_history)
    common_functions.display_chat_history(st,st.session_state.conversation_id)

    # Display only the assistant's latest response
    with st.chat_message('assistant'):
        common_functions.typewriter_effect(assistant_reply)
