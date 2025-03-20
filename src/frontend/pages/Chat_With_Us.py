import streamlit as st
import requests
from frontend.app import common_functions
from datetime import datetime

API_URL = "http://localhost:8000/chat/get-health-advice/"
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
common_functions.config_homepage()
common_functions.set_page_title()
# common_functions.set_bg_image("src/frontend/images/health_care_baner_2.jpg")
# Initialize conversation history
def initialize_conversation():
    assistant_message = ("Hello! I am your Yuvabe Care Companion AI, here to assist you with general medicine queries. " 
                         "How can I help you today?")
    
    return [{"role": "assistant", "content": assistant_message}]

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
    
def render_chatbot():

    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = datetime.now().strftime("%Y-%m-%d")

    conversation_ids = common_functions.get_bucket_items()
    if conversation_ids:
        for conversation_id in conversation_ids[-3:]:
            common_functions.display_chat_history(conversation_id)

    # Display chat history
    for message in st.session_state.conversation_history [-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
        role = message["role"]
        avatar_image = "src/frontend/images/chat_doctor_logo.png" if role == "assistant" else "src/frontend/images/healthy.png" if role == "user" else None
        with st.chat_message(role, avatar=avatar_image):
            common_functions.display_message_box(role,message['content'])
            # st.write(message["content"])

    # User Input
    user_input = st.chat_input("Ask your health-related question:")
    if 'system_message' not in st.session_state:
        system_message = ("Hello! I am your Yuvabe Care Companion AI, here to assist you with general medicine queries. " 
                            "How can I help you today?")
        st.session_state.system_message = system_message
        with st.chat_message('ai'):
            common_functions.typewriter_effect(st.session_state.system_message)

    if user_input:

        # Display user's input
        user_avatar_image = "src/frontend/images/healthy.png"
        with st.chat_message('user',avatar=user_avatar_image):
            common_functions.typewriter_effect(user_input)
            
        # Append user input to session history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        
        # Fetch assistant response
        assistant_reply = fetch_health_advice(st.session_state.conversation_history)

        # Append assistant's reply to conversation history first
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        common_functions.store_chat_history_in_db(st.session_state.conversation_id,st.session_state.conversation_history)

        # Display only the assistant's latest response
        doctor_avatar_image = "src/frontend/images/chat_doctor_logo.png"
        with st.chat_message('assistant',avatar=doctor_avatar_image):
            common_functions.typewriter_effect(assistant_reply)

render_chatbot()
