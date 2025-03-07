import streamlit as st
from utils import logger
from app import common_fuctions

logger = logger.get_logger()

PAGE_TITLE = "Yuvabe Care Companion AI"
PAGE_LAYOUT = "wide"
PAGE_ICON = "src/frontend/images/page_icon.jpg"
GITHUB_LINK = "https://github.com/Vela-Test1993/yuvabe-care-companion-ai"
ABOUT_US = "An AI-powered assistant for personalized healthcare guidance."

def get_or_greet_user_name():
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
        logger.info("user_name not found in session_state, setting to None.")

    if st.session_state.user_name is None:
        logger.info("user_name is None, requesting user input.")
        user_name = st.text_input("Please let me know your name:",
                              placeholder="Enter your name buddy")
        if user_name:
            st.session_state.user_name = user_name
            logger.info(f"User entered name: {user_name}. Setting session_state.user_name.")
            st.toast(f"Hello {st.session_state.user_name} . Welcome to {PAGE_TITLE}")
            st.rerun()
    else:
        logger.info(f"User already entered a name: {st.session_state.user_name}. Displaying greeting.")
        return st._bottom.subheader(f"Hello {st.session_state.user_name}! How can I assist you today?")
    
def display_chat():
    logger.info("Displaying the chat history.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        logger.info(f"Displayed {len(st.session_state.messages)} messages from the chat history.")

def handle_user_input():

    logger.info("Waiting for user input...")
    prompt = st.chat_input("Ask me anything about health, physiotherapy, or medical advice!")
    if prompt:

        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            with st.spinner("Processing your query..."):
                try:
                    endpoint = "/chat/agent_response"
                    response = common_fuctions.get_api_response(endpoint, prompt)
                except Exception as e:
                    logger.error(f"AI response generation failed: {str(e)}")
                    response = "⚠️ Sorry, I couldn't process your request. Please try again later."
        except Exception as e:
            logger.exception("Error during similarity check or response generation.")
            response = "⚠️ Oops! Something went wrong. Please try again."

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        logger.info(f"Assistant response: {response[:100]}...")

def config_homepage():
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

def setup_homepage():

    config_homepage()
    img_base64 = common_fuctions.img_to_base64(PAGE_ICON)
    if img_base64:
        st.sidebar.markdown(
            f'<img src="data:image/png;base64,{img_base64}" class="cover-glow">',
            unsafe_allow_html=True,
    )
        
    st.sidebar.markdown("---")

    if get_or_greet_user_name():

        display_chat()

        handle_user_input()
