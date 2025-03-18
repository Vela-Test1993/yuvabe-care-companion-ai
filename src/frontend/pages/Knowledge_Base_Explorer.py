import streamlit as st
from app import pinecone_data_handler, common_functions

common_functions.config_homepage()

def render_knowledge_base_explorer():
    """Renders the Knowledge Base Explorer page with improved UI and navigation."""
    
    # Header Section
    st.title("📚 Knowledge Base Explorer")
    st.markdown("""
    ### Discover Helpful Information!
    Enter your concerns below to receive insights and solutions tailored to your needs.
    """)

    # Knowledge Base Section
    with st.expander("🔍 Explore the Knowledge Base"):
        pinecone_data_handler.render_metadata_fetch_form(st)

# Call the function to render the Knowledge Base Explorer
if __name__ == "__main__":
    render_knowledge_base_explorer()