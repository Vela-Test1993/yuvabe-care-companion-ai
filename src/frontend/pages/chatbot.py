import streamlit as st
import requests
from app import common_fuctions

API_URL = "http://localhost:8000/chat/get-health-advice/"
NUMBER_OF_MESSAGES_TO_DISPLAY = 20
common_fuctions.config_homepage(st)
common_fuctions.set_page_title(st)
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
        st.error(f"❗ API Connection Error: {e}")
        return "I'm currently unable to respond. Please try again later."

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = initialize_conversation()

# Display chat history
for message in st.session_state.conversation_history[-NUMBER_OF_MESSAGES_TO_DISPLAY:]:
    role = message["role"]
    avatar_image = "src/frontend/images/page_icon.jpg" if role == "assistant" else "src/frontend/images/page_icon.jpg" if role == "user" else None
    with st.chat_message(role, avatar=avatar_image):
        st.write(message["content"])

# for message in st.session_state.conversation_history:
#     with st.chat_message(message['role']):
#         st.markdown(message['content'])

# User Input
user_input = st.chat_input("Ask your health-related question:")

if user_input:
    # Display user's input
    with st.chat_message('user'):
        st.markdown(user_input)

    # Append user input to session history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Fetch assistant response
    assistant_reply = fetch_health_advice(st.session_state.conversation_history)

    # Append assistant's reply to conversation history first
    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})

    # Display only the assistant's latest response
    with st.chat_message('assistant'):
        common_fuctions.typewriter_effect(st,assistant_reply)
        # st.markdown(assistant_reply)
