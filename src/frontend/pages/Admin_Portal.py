import streamlit as st
from app import pinecone_data_handler
from app import common_functions

# # Page Configuration
common_functions.config_homepage()

def render_admin_portal():
    """Renders the enhanced Admin Portal page with improved UI and navigation."""

    # Header Section
    st.markdown("<h1 class='header-text'>🛠️ Admin Portal</h1>", unsafe_allow_html=True)
    st.markdown("""
        Welcome to the **Admin Portal**.  
        Manage your Pinecone database with secure and efficient tools.
    """)
    st.divider()

    # Data Manager Tabs
    DataManager = st.tabs(["📂 Pinecone Data Manager"])[0]

    with DataManager:
        Upsert, Delete = st.tabs(["Upsert Data", "Delete Records"])

        # Upsert Section
        with Upsert:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### 📥 Upsert Data")
            st.info(
                "Use this section to **insert** or **update** records in Pinecone."
                "\n\n✅ Ensure your data is correctly formatted before uploading."
            )
            st.markdown("---")
            pinecone_data_handler.upsert_data(st)
            st.markdown("</div>", unsafe_allow_html=True)

        # Delete Section
        with Delete:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### ⚠️ Delete Records")
            st.error(
                "❗ **Warning:** Deleting data is irreversible.\n"
                "Proceed with caution."
            )
            # Confirmation Dialog for Safety
            pinecone_data_handler.delete_records(st)

# Call the function to render the Admin Portal
if __name__ == "__main__":
    render_admin_portal()