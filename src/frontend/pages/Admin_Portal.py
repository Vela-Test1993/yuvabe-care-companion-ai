import streamlit as st
from frontend.app import pinecone_data_handler,common_functions

# # Page Configuration
common_functions.config_homepage()
# common_functions.set_bg_image("src/frontend/images/health_care_baner.png")

def render_admin_portal():

    """
    Renders the enhanced Admin Portal page with improved UI, navigation, and user guidance.
    
    Features:
    - Upsert data functionality with informative tips.
    - Delete records feature with enhanced warnings and confirmation prompts.
    """

# Header Section
    st.markdown(
        """
        <div style="
            background-color: #1B3C59; 
            color: #FFFFFF; 
            padding: 10px; 
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border-radius: 80px;
        ">
            <h1>🛠️ Admin Portal</h1>
            <p style="font-size: 16px;">
                Manage your Pinecone database securely and efficiently.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.divider()

# Data Manager Tabs
    DataManager = st.tabs(["📂 Pinecone Data Manager"])[0]

    with DataManager:
        Upsert, Delete = st.tabs(["🟢 Upsert Data", "🔴 Delete Records"])

        # Upsert Section
        with Upsert:
            st.markdown(
                """
                <div style="
                    background-color: #E3F2FD; 
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
                ">
                    <h3>📥 Upsert Data</h3>
                    <p style="color: #1976D2;">
                        Use this section to <b>insert</b> or <b>update</b> records in Pinecone.
                    </p>
                    <p>
                        ✅ Ensure your data is correctly formatted before uploading.<br>
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )

            st.divider()

            # Call Upsert Function
            pinecone_data_handler.upsert_data()

        # Delete Section
        with Delete:
            st.markdown(
                """
                <div style="
                    background-color: #FFEBEE; 
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
                ">
                    <h3>⚠️ Delete Records</h3>
                    <p style="color: #D32F2F;">
                        ❗ <b>Warning:</b> Deleting data is irreversible.<br>
                        Please confirm your action before proceeding.
                    </p>
                </div>
                """, 
                unsafe_allow_html=True
            )

            st.divider()
            pinecone_data_handler.delete_records()

# Call the function to render the Admin Portal
if __name__ == "__main__":
    render_admin_portal()