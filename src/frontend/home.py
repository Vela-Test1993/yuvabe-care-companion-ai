import streamlit as st
from frontend.app import common_functions

WELCOME_TEXT = "Welcome to the Yuvabe Care Companion AI!"   

# Page Configuration
common_functions.config_homepage()
common_functions.set_bg_image("src/frontend/images/health_care_baner.png")
common_functions.custom_navbar()
st.divider()

def render_homepage():
    """
    Renders the Yuvabe Care Companion AI homepage with improved visuals and enhanced user experience.

    Features:
    - Displays a warm welcome message with animated text.
    - Highlights key features using clean and modern UI design.
    - Encourages user engagement with a prominent 'Get Started' call-to-action.

    Visual Enhancements:
    - Consistent color theme with improved contrast for readability.
    - Box shadows and rounded corners for a modern touch.
    - Organized content using bullet points, ensuring clarity and focus.

    """
    
    # Welcome Text with Animation
    common_functions.typewriter_effect(WELCOME_TEXT, speed=0.02, gradient=True)
    
    # Key Features Section
    st.markdown(
        """
        <div style="
            background-color: #1B3C59;
            color: #FFFFFF;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
            margin-top: 20px;
        ">
            <h2 style="text-align: left; font-weight: bold;">Key Features</h2>
            <ul style="padding-left: 20px;">
                <li><b>🛠️ Admin Portal</b> — Effortlessly manage records, track data, and configure settings with ease.</li>
                <li><b>📚 Knowledge Base Explorer</b> — Discover precise and relevant insights using advanced vector search technology.</li>
                <li><b>💬 Chat with Us</b> — Engage with our intelligent assistant for personalized guidance.</li>
            </ul>
            <p style="margin-top: 15px; font-style: italic; font-weight: bold;">
                💡 Explore each section to unlock powerful features tailored to enhance your experience.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
   # Call-to-Action Section
    st.markdown(
        """
        <div style="
            text-align: center;
            margin-top: 30px;
            padding: 18px 35px;
            background-color: #4CAF50;
            color: #FFFFFF;
            font-weight: bold;
            font-size: 20px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        ">
            🌿 Ready to Get Started? Begin Your Journey Now! 🚀
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    render_homepage()
