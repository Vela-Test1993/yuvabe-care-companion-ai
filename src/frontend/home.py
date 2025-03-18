import streamlit as st
from app import common_functions
from pages import Admin_Portal as admin_page
from pages import Knowledge_Base_Explorer as knowledge_base_explorer_page
import time

# # Page Configuration
common_functions.config_homepage()
common_functions.set_bg_image("src/frontend/images/health_care_baner.png")
common_functions.custom_navbar()

# def render_homepage():
#     """Renders the Yuvabe Care Companion AI homepage."""

    # # Welcome Section with Visual
    # st.image("src/frontend/images/health_care_baner.png", 
    #          use_container_width=True, 
    #          caption="Your AI-Powered Health Companion")

    # # Navigation Tabs
    # Home, Admin_Portal, Knowledge_Base_Explorer = st.tabs(
    #     ["🏠 Home", "🔒 Admin Portal", "📚 Knowledge Base Explorer"]
    # )

    # with Home:
    # st.markdown("""
    # ### 👋 Welcome to the Yuvabe Care Companion AI!
    # This platform offers comprehensive tools to support your healthcare journey. Use the tabs above to navigate:
    # """)

    # # Feature Overview Section
    # st.markdown("""
    # ### 🔹 Key Features
    # - **Admin Portal** — Manage records, data, and configurations efficiently.
    # - **Knowledge Base Explorer** — Leverage advanced vector search to find relevant knowledge entries with precision.
    # - **Patient Assistance** — Personalized guidance to help patients describe their concerns.

    # > 💡 *Explore each section for detailed functionality.*
    # """)

    # with Admin_Portal:
    #     admin_page.render_admin_portal()
    #     # if st.button("Go to Admin Portal"):
    #     #     st.switch_page("pages/admin_portal.py")

    # with Knowledge_Base_Explorer:
    #     knowledge_base_explorer_page.render_knowledge_base_explorer()
        # if st.button("Go to Knowledge Base Explorer"):
        #     st.switch_page("pages/knowledge_base_explorer.py")

# Render the Homepage
# render_homepage()


# Display the animated text
welcome_text = "👋 Welcome to the Yuvabe Care Companion AI!"
container = st.empty()
common_functions.type_text(container, welcome_text)