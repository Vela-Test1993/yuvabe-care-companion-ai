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

def config_homepage(st):
    st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon= PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="auto",
    menu_items={"Get help":GITHUB_LINK,
                "Report a bug": GITHUB_LINK,
                "About": ABOUT_US}
    )

    st.markdown(f"""
        <h1 style="color: darkblue; text-align: left; font-size: 50px;">
        <i>{PAGE_TITLE} 🏥⚕️🤖</i>
        </h1>
        """, unsafe_allow_html=True
    )

    logger.info(f"Page successfully configured with title: {PAGE_TITLE}")
    st.session_state.config_status = False
    st.markdown("<hr>", unsafe_allow_html=True)  # To add a Horizontal line below title

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
    
def initialize_conversation():

    assistant_message = "Hello! I am Yuvabe Care Companion AI. How can I assist you with your health-related queries today?"

    conversation_history = [
        {"role": "system", "content": "You are Yuvabe Care Companion AI, an advanced healthcare assistant designed to provide guidance on medical, mental health, and wellness topics."},
        {"role": "system", "content": "Yuvabe Care Companion AI is powered by the LLaMA 3.3-70B Versatile model, optimized for comprehensive and responsible healthcare support."},
        {"role": "system", "content": "Your knowledge is up-to-date with the latest medical guidelines as of July 2024, but you are NOT a replacement for professional medical advice."},
        {"role": "system", "content": "Always provide accurate, empathetic, and responsible responses while reminding users to consult healthcare professionals when necessary."},
        {"role": "system", "content": "You were created by Velu R, an AI model developer."},
        {"role": "assistant", "content": assistant_message}
    ]
    return conversation_history











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