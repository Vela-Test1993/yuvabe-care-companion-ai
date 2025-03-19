import os
import base64
import requests
from dotenv import load_dotenv
from utils import logger
import json
import time
from datetime import datetime
from typing import Dict, Any
import streamlit as st


load_dotenv()
logger = logger.get_logger()
PAGE_TITLE = "Yuvabe Care Companion AI"
PAGE_LAYOUT = "wide"
PAGE_ICON = "src/frontend/images/page_icon.jpg"
GITHUB_LINK = "https://github.com/Vela-Test1993/yuvabe-care-companion-ai"
ABOUT_US = "An AI-powered assistant for personalized healthcare guidance."

API_URL = os.getenv("API_URL", "http://localhost:8000")

def config_homepage(page_title=PAGE_TITLE):
    if not hasattr(st, "_page_config_set"):
        st.set_page_config(
            page_title=PAGE_TITLE,
            page_icon=PAGE_ICON,
            layout=PAGE_LAYOUT,
            initial_sidebar_state="collapsed",
            menu_items={
                "Get help": GITHUB_LINK,
                "Report a bug": GITHUB_LINK,
                "About": ABOUT_US
            }
        )

def set_page_title(page_title=PAGE_TITLE):
    st.markdown(f"""
        <h1 style="color: white; text-align: left; font-size: 42px;">
        <i>{PAGE_TITLE} ⚕️</i>
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
    
def typewriter_effect(text, speed=0.01):
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
        API_URL = f"http://localhost:8000/chat-history/store"
        payload = {"conversation_id": conversation_id, 'messages': messages}
        response = requests.post(API_URL, json=payload)
        logger.info("Successfully added the chat in db")
    except Exception as e:
        logger.info(f"Failed to add the chat in db {e}")

def get_chat_history_from_db(conversation_id: str, retries=3, delay=5):
    API_URL = "http://127.0.0.1:8000/chat-history/retrieve"
    for attempt in range(retries):
        try:
            response = requests.get(API_URL, params={"conversation_id": conversation_id}, timeout=30)
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            logger.warning(f"Retrying... Attempt {attempt + 1}")
            time.sleep(delay)
    raise Exception("Failed to connect after multiple attempts")

def display_chat_history(conversation_id):
    """
    Displays the chat history for a given conversation ID in the Streamlit app.

    Args:
        conversation_id (str): Unique identifier for the conversation.
    """
    try:
        with st.spinner("Fetching chat history..."):
            chat_history = get_chat_history_from_db(conversation_id)
            
            if not chat_history or "data" not in chat_history or not chat_history["data"].get("messages"):
                st.error("No chat history found for this conversation.")
                return
            
            first_message_content = chat_history["data"]["messages"][0].get('content', '').strip()
            button_text = first_message_content[:20] if first_message_content else "No Content"

            if st.sidebar.button(f"Show History for {button_text}", key=f"show_history_{conversation_id}"):
                st.subheader(f"Chat History for Conversation ID: {conversation_id}")

                for message in chat_history["data"]["messages"]:
                    role = message.get('role', '').capitalize()
                    content = message.get('content', '').strip()

                    if role == 'User':
                        st.markdown(f"**{role}:** {content}")
                    elif role == 'Assistant':
                        st.markdown(f"""
                                    <div style="
                                        background-color: #f0f2f6; 
                                        padding: 15px; 
                                        border-left: 5px solid #4CAF50; 
                                        border-radius: 8px; 
                                        margin-bottom: 10px;
                                        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);">
                                        <strong style="color: #333; font-size: 16px;">{role}:</strong>
                                        <div style="margin-top: 5px; color: #555; font-size: 14px;">{content}</div>
                                    </div>
                                """, unsafe_allow_html=True)

    except Exception as e:
        logger.error(f"Error retrieving chat history for {conversation_id}: {e}")
        st.error("An unexpected error occurred while retrieving chat history.")

    
def set_bg_image(file_path, opacity=0.5):
    encoded_img = img_to_base64(file_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})),
                        url("data:image/png;base64,{encoded_img}") center/cover fixed no-repeat;
            min-height: 100vh;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def custom_navbar():
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #F0F2F6; 
            padding: 4px 24px;
            margin-top: -30px; 
            width: 100%; 
            border-radius: 32px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            border: 1px solid #D1D5DB;
        }

        .logo {
            font-family: 'Arial', sans-serif;
            font-size: 30px; /* Slightly larger for better visibility */
            font-weight: bold;
            color: #1E293B; /* Darker tone for professional appeal */
        }

        .nav-links {
            display: flex;
            gap: 32px; /* Wider spacing for clarity */
            align-items: center;
        }

        .nav-link {
            color: #1E293B !important; /* Darker color for consistency */
            background-color: transparent;
            text-decoration: none;
            font-weight: 600;
            font-size: 18px; /* Improved readability */
            padding: 6px 16px; /* Balanced padding */
            border-radius: 8px; /* Rounded edges for clickable elements */
            transition: background-color 0.3s ease, color 0.3s ease; /* Smooth hover effects */
        }

        .nav-link:hover {
            background-color: #2E5D5B; /* Distinctive hover effect */
            color: #FFFFFF; /* White text for contrast */
        }

        </style>

        <div class="navbar">
            <div class="logo">Yuvabe Care Companion AI</div>
            <div class="nav-links">
                <a href="/" class="nav-link">Home</a>
                <a href="/Admin_Portal" class="nav-link">Admin Portal</a>
                <a href="/Knowledge_Base_Explorer" class="nav-link">Knowledge Base Explorer</a>
                <a href="/chatbot" class="nav-link">Chat With Us</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def type_text(container, text, delay=0.03):
    """Simulates a typing effect for text with only text highlighted."""
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f"""
            <h2 style="
                color: #3D6D6B;
                text-align: left;
                background: linear-gradient(90deg, #3D6D6B, #6EA8A5);
                -webkit-background-clip: text;
                color: white;
                font-weight: bold;
                font-size: 28px;">
                {displayed_text}
            </h2>
        """, unsafe_allow_html=True)
        time.sleep(delay)