import streamlit as st
from app import pinecone_data_handler

# Page Configuration
# st.set_page_config(page_title="Admin Portal", page_icon="🔒", layout="wide")
def render_admin_portal():
    """Renders the Admin Portal page with improved UI and navigation."""
    
    # Header Section
    st.title("🔒 Admin Portal")
    st.markdown("""
    ### Welcome to the Admin Portal!
    Manage your Pinecone data efficiently with the options below.
    """)

    # Data Manager Tabs
    DataManager = st.tabs(["📂 Pinecone Data Manager"])[0]

    with DataManager:
        Upsert, Delete = st.tabs(["📥 Upsert Data", "🗑️ Delete Records"])

        with Upsert:
            st.markdown("### 📥 Upsert Data")
            st.info("Use this section to insert or update data in Pinecone.")
            pinecone_data_handler.upsert_data(st)

        with Delete:
            st.markdown("### 🗑️ Delete Records")
            st.warning("Use this section to delete records from Pinecone. Be cautious when performing deletions.")
            pinecone_data_handler.delete_records(st)

    # Sidebar for Navigation
    st.sidebar.title("🔀 Navigation")
    st.sidebar.markdown("[🏠 Home](http://localhost:8501)", unsafe_allow_html=True)
    st.sidebar.markdown("[🔒 Knowledge Base](http://localhost:8501/Knowledge_Base_Explorer)", unsafe_allow_html=True)

# Call the function to render the Admin Portal
if __name__ == "__main__":
    render_admin_portal()