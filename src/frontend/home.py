import streamlit as st
from app import common_fuctions
from PIL import Image  

def render_homepage():
    """Renders the Yuvabe Care Companion AI homepage."""

    # Page Configuration
    common_fuctions.config_homepage(st)
    common_fuctions.set_page_title(st)


    # Welcome Section with Visual
    st.image("src/frontend/images/health_care_baner.png", 
             use_container_width=True, 
             caption="Your AI-Powered Health Companion")

    # Navigation Tabs
    Home, Admin_Portal, Knowledge_Base_Explorer = st.tabs(
        ["🏠 Home", "🔒 Admin Portal", "📚 Knowledge Base Explorer"]
    )

    with Home:
        # st.markdown("### 🌟 Getting Started")
        # st.markdown("""
        # - Select **Admin Portal** for system configurations and data management.
        # - Go to **Knowledge Base Explorer** to explore and manage knowledge entries.
        # """)
        st.markdown("""
        ### 👋 Welcome to the Yuvabe Care Companion AI!
        This platform offers comprehensive tools to support your healthcare journey. Use the tabs above to navigate:
        """)

        # Feature Overview Section
        st.markdown("""
        ### 🔹 Key Features
        - **Admin Portal** — Manage records, data, and configurations efficiently.
        - **Knowledge Base Explorer** — Leverage advanced vector search to find relevant knowledge entries with precision.
        - **Patient Assistance** — Personalized guidance to help patients describe their concerns.

        > 💡 *Explore each section for detailed functionality.*
        """)

    with Admin_Portal:
        if st.button("Go to Admin Portal"):
            st.switch_page("pages/admin_portal.py")

    with Knowledge_Base_Explorer:
        if st.button("Go to Knowledge Base Explorer"):
            st.switch_page("pages/knowledge_base_explorer.py")

# Render the Homepage
if __name__ == "__main__":
    render_homepage()