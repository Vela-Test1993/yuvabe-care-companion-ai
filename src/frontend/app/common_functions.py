import os
import base64
import requests
from dotenv import load_dotenv
from frontend.utils import logger
import json
import time
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
    """
    Configures the Streamlit homepage with essential settings.

    This function sets up the page title, icon, layout, and sidebar state.
    It also defines custom menu items for better navigation.

    Args:
        page_title (str): The title displayed on the browser tab (default is PAGE_TITLE).

    Key Features:
    - Ensures `st.set_page_config()` is called only once to avoid errors.
    - Uses constants for improved maintainability and consistency.
    - Provides links for help, bug reporting, and an 'About' section.

    Example:
        >>> config_homepage("My Custom App")
    """
    if "page_config_set" not in st.session_state:
        st.set_page_config(
            page_title=page_title,
            page_icon=PAGE_ICON,
            layout=PAGE_LAYOUT,
            initial_sidebar_state="collapsed",
            menu_items={
                "Get help": GITHUB_LINK,
                "Report a bug": GITHUB_LINK,
                "About": ABOUT_US
            }
        )
        st.session_state.page_config_set = True

def set_page_title(page_title=PAGE_TITLE, icon="⚕️", color="#2E7D32", font_size="36px"):
    """
    Sets a custom-styled page title for the Streamlit application.

    Parameters:
    -----------
    page_title : str
        The text to display as the page title. Defaults to the value of PAGE_TITLE.
    icon : str, optional
        An optional emoji or symbol to enhance the visual appeal of the title. Defaults to "⚕️".
    color : str, optional
        Hex color code for the title text. Defaults to a fresh green shade (#2E7D32).
    font_size : str, optional
        Font size for the title text. Defaults to "36px".

    Example Usage:
    ---------------
    set_page_title("Welcome to Yuvabe", icon="🌿", color="#1E88E5", font_size="42px")
    """
    
    st.markdown(f"""
        <h1 style="
            color: {color};
            font-size: {font_size};
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2); /* Adds depth for a cleaner look */
            padding: 10px 0;  /* Improved spacing */
        ">
            <i>{page_title} {icon}</i>
        </h1>
    """, unsafe_allow_html=True)

def img_to_base64(image_path):
    """Convert image to base64."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        logger.error(f"Error converting image to base64: {str(e)}")
        return None
    
def typewriter_effect(text, speed=0.03, gradient=False):
    """
    Displays text with a typewriter effect. 
    Supports optional gradient styling for enhanced visual appeal.

    Args:
        text (str): The text to display with the typing effect.
        speed (float): Typing speed in seconds (default 0.03).
        gradient (bool): If True, applies a gradient effect to the text.
    """
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        
        if gradient:
            placeholder.markdown(f"""
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
        else:
            placeholder.markdown(displayed_text)
        
        time.sleep(speed)

def custom_navbar():
    """
    Renders a custom navigation bar with a modern design for the Streamlit application.

    The navigation bar includes:
    - **Logo:** Displays "Yuvabe Care Companion AI" as the app's brand.
    - **Navigation Links:** Provides links to key sections like Home, Admin Portal, Knowledge Base Explorer, and Chatbot.

    Key Features:
    - Responsive Design: The layout adjusts for different screen sizes using media queries.
    - Enhanced UI: Includes a soft background, subtle shadow, and smooth hover effects for improved aesthetics.
    - Accessibility: Ensures text visibility and clickable elements for better user interaction.

    Example Usage:
        >>> custom_navbar()

    """
    st.markdown(
        """
        <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #FFFFFF;
            padding: 16px 32px;
            width: 100%;
            border-radius: 50px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            border-bottom: 3px solid #2E5D5B;
            box-sizing: border-box;
            white-space: nowrap;
            overflow-x: auto;
        }

        .logo {
            font-family: 'Arial', sans-serif;
            font-size: 28px;
            font-weight: bold;
            color: #1E293B;
        }

        .nav-links {
            display: flex;
            gap: 32px;
            align-items: center;
        }

        .nav-link {
            color: #1E293B !important;
            text-decoration: none;
            font-weight: 600;
            font-size: 22px;
            padding: 8px 16px;
            border-radius: 6px;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        .nav-link:hover {
            background-color: #2E5D5B;
            color: #FFFFFF !important;
            border-radius: 50px;
        }

        @media (max-width: 1024px) {
            .navbar {
                flex-direction: column;
                text-align: center;
                padding: 12px 24px;
            }

            .nav-links {
                flex-direction: column;
                gap: 12px;
                width: 100%;
            }

            .nav-link {
                width: 100%;
                text-align: center;
            }
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

def set_bg_image(file_path, opacity=0.5):
    """
    Sets a background image for the Streamlit application with optional opacity control.

    This function applies a background image to the entire Streamlit app (`.stApp` container) 
    using CSS with a linear gradient overlay. The overlay enhances text readability by adding 
    a semi-transparent dark layer over the image.

    Args:
        file_path (str): The file path of the background image (supports PNG, JPG, etc.).
        opacity (float, optional): The opacity level of the dark overlay. 
                                   Values range from 0 (fully transparent) to 1 (fully opaque). 
                                   Default is 0.5, providing balanced readability and background visibility.

    Example Usage:
        ```python
        set_bg_image("src/frontend/images/health_care_banner.png", opacity=0.6)
        ```

    Notes:
    - Ensure the provided `file_path` is accessible and the image is properly encoded in base64 format.
    - For optimal results, use high-resolution images with suitable contrast to enhance readability.

    """
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
        logger.info(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logger.info(f"An error occurred: {err}")
    
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

def display_message_box(role, content):
    """
    Displays a styled message box for user or assistant content.

    Args:
        role (str): The role of the speaker (e.g., 'User' or 'Assistant').
        content (str): The text content to display.
    """
    # Define styles based on role
    background_color = "#E3F2FD" if role.lower() == 'user' else "#E8F5E9"
    border_color = "#1E88E5" if role.lower() == 'user' else "#43A047"
    text_align = "left" if role.lower() == 'user' else "right"
    flex_direction = "row" if role.lower() == 'user' else "row-reverse"
    avatar = "path_to_user_avatar.png" if role.lower() == 'user' else "path_to_assistant_avatar.png"

    st.markdown(f"""
        <div style="
            display: flex; 
            flex-direction: {flex_direction}; 
            align-items: center; 
            margin-bottom: 10px;
            gap: 10px;">
            
            <img src="{avatar}" alt="{role} avatar" style="width: 40px; height: 40px; border-radius: 50%;">

            <div style="
                background-color: {background_color}; 
                padding: 15px; 
                border-left: 5px solid {border_color}; 
                border-radius: 8px; 
                box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
                width: 100%;">
                
                <strong style="color: #333; font-size: 16px;">{role}:</strong>
                <div style="margin-top: 5px; color: #555; font-size: 14px;">
                    {content}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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

            if st.sidebar.button(f"Show History for {button_text} : {conversation_id}", key=f"show_history_{conversation_id}"):
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

def get_bucket_items():
    API_URL = "http://127.0.0.1:8000/chat-history/bucket-items"
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
            logger.error(f"Failed to get the bucket items {e}")
