import os
import base64
import requests
from dotenv import load_dotenv
from utils import logger
import json
import time

load_dotenv()
logger = logger.get_logger()
PAGE_TITLE = "Yuvabe Care Companion AI"
PAGE_LAYOUT = "wide"
PAGE_ICON = "src/frontend/images/page_icon.jpg"
GITHUB_LINK = "https://github.com/Vela-Test1993/yuvabe-care-companion-ai"
ABOUT_US = "An AI-powered assistant for personalized healthcare guidance."

API_URL = os.getenv("API_URL", "http://localhost:8000")

def config_homepage(st, page_title=PAGE_TITLE):
    st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon= PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="auto",
    menu_items={"Get help":GITHUB_LINK,
                "Report a bug": GITHUB_LINK,
                "About": ABOUT_US}
    )
    logger.info(f"Page successfully configured with title: {PAGE_TITLE}")

def set_page_title(st, page_title=PAGE_TITLE):
    st.markdown(f"""
        <h1 style="color: darkblue; text-align: left; font-size: 50px;">
        <i>{PAGE_TITLE} 🏥⚕️🤖</i>
        </h1>
        """, unsafe_allow_html=True
    )

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return None
    
def typewriter_effect(st, text, speed=0.01):
    """Displays text with a realistic typewriter effect (character by character)."""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(speed)
    
def get_api_response(endpoint:str, prompt: list):
    try:
        logger.info(f"Sending user prompt to API endpoint: {API_URL}{endpoint}")
        response = requests.post(f"{API_URL}{endpoint}", json={"prompt": prompt})
        if response.status_code == 200:
            return response.json()
        else:
            return "An error occurred while processing your request."
    except Exception as e:
        return f"An error occurred while processing your request: {str(e)}"
    

def upsert_data_request(start, end):
    headers = {"Content-Type": "application/json"}
    payload = {
        "start": start,
        "end": end
    }

    try:
        url = "http://localhost:8000/data/upsert_data"
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    
# def initialize_conversation():
#     """
#     Initialize the conversation history with system and assistant messages.

#     Returns:
#     - list: Initialized conversation history.
#     """
#     assistant_message = (
#         "Hello! I am your Yuvabe Care Companion AI, here to assist you with general medicine queries. "
#         "I can provide information about common symptoms, medications, treatments, and wellness tips. "
#         "How can I help you today?"
#     )

#     conversation_history = [
#         {"role": "system", "content": "You are Yuvabe Care Companion AI, an advanced healthcare assistant designed to provide guidance on medical, mental health, and wellness topics."},
#         {"role": "system", "content": "Yuvabe Care Companion AI is powered by the LLaMA 3.3-70B Versatile model, optimized for comprehensive and responsible healthcare support."},
#         {"role": "system", "content": "Your knowledge is up-to-date with the latest medical guidelines as of July 2024, but you are NOT a replacement for professional medical advice."},
#         {"role": "system", "content": "Always provide accurate, empathetic, and responsible responses while reminding users to consult healthcare professionals when necessary."},
#         {"role": "system", "content": "You were created by Velu R, an AI model developer."},
#         {"role": "assistant", "content": assistant_message}
#     ]
#     return conversation_history











def fetch_response(prompt, chat_history):
    try:
        # Prepare data for API request
        payload = {
            "chat_history": chat_history,
            "latest_prompt": prompt
        }
        response = requests.post(API_URL, json=payload, timeout=15)

        if response.status_code == 200:
            return response.json().get("response", "Sorry, I couldn't generate a response.")
        else:
            return "Error: Unable to connect to the backend."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    
def store_chat_history_in_db(conversation_id, messages):
    try:
        API_URL = f"http://localhost:8000/chat-db/store-history"
        payload = {"conversation_id": conversation_id, 'messages': messages}
        response = requests.post(API_URL, json=payload)
        logger.info("Successfully added the chat in db")
    except Exception as e:
        logger.info(f"Failed to add the chat in db {e}")

def get_chat_history_from_db(conversation_id):
    try:
        API_URL = f"http://127.0.0.1:8000/chat-db/get-history"
        response = requests.post(API_URL,params={"conversation_id": conversation_id})
        response.raise_for_status()
        logger.info(f"Successfully retrieved chat history for conversation ID: {conversation_id}")
        return response.json()
    except Exception as e:
        logger.info(f"Failed to get the chat history")
    return {"error": "Failed to retrieve chat history. Please try again later."}

def display_chat_history(st):
    conversation_id = st.session_state.get("conversation_id")
    if not conversation_id:
        st.warning("Conversation ID is missing. Please provide a valid ID.")
        return

    try:
        chat_history = get_chat_history_from_db(conversation_id)
        if chat_history and isinstance(chat_history, dict) and 'error' not in chat_history:
            st.success("Chat history loaded successfully!")
            if st.sidebar.button(f"Show History for {conversation_id}",key="show_history_button"):
                st.json(chat_history)
        else:
            st.info("No chat history found for this conversation ID or the data format is incorrect.")
    except Exception as e:
        st.error(f"Error retrieving chat history: {e}")