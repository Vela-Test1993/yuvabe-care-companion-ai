import streamlit as st
from app import pinecone_data_handler
from app import common_functions

# Page Configuration
# st.set_page_config(page_title="Knowledge Base Explorer", page_icon="📚", layout="wide")

def render_knowledge_base_explorer():
    """Renders the Knowledge Base Explorer page with improved UI and navigation."""
    
    # Header Section
    # st.title("📚 Knowledge Base Explorer")
    # st.markdown("""
    # ### Discover Helpful Information!
    # Enter your concerns below to receive insights and solutions tailored to your needs.
    # """)

    # Knowledge Base Section
    with st.expander("🔍 Explore the Knowledge Base"):
        pinecone_data_handler.render_metadata_fetch_form(st)


    # # Sidebar for Navigation
    # st.sidebar.title("🔀 Navigation")
    # st.sidebar.markdown("[🏠 Home](http://localhost:8501)", unsafe_allow_html=True)
    # st.sidebar.markdown("[🔒 Admin Portal](http://localhost:8501/Admin_Portal)", unsafe_allow_html=True)

# Call the function to render the Knowledge Base Explorer
if __name__ == "__main__":
    render_knowledge_base_explorer()