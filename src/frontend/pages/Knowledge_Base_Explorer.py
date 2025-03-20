import streamlit as st
from frontend.app import pinecone_data_handler, common_functions

# Page Configuration
common_functions.config_homepage()

def render_knowledge_base_explorer():
    """Renders the Knowledge Base Explorer page for fetching accurate metadata from Pinecone Vector DB."""

    st.markdown(
        """
        <div style="
            background-color: #1B3C59; 
            color: #FFFFFF; 
            padding: 20px; 
            border-radius: 12px; 
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            text-align: center;
        ">
            <h1>📚 Knowledge Base Explorer</h1>
            <p>Powered by <b>Pinecone Vector DB</b> for precise metadata retrieval.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Guidance Section
    st.markdown(
        """
        ### How to Use the Knowledge Base Explorer  
        1. **Enter your query** related to health concerns.  
        2. Click **Fetch Metadata** to retrieve the most relevant insights.  
        3. Results are fetched from **Pinecone Vector DB**, ensuring fast and accurate responses.  

        ✅ **Pro Tip:** Use precise keywords for better results (e.g., "mental health tips" instead of "help").
        """
    )

    st.divider()

# Knowledge Base Section
    with st.expander("🔍 **Explore the Knowledge Base (Pinecone Vector DB)**", expanded=True):
        st.info(
            "💡 **Looking for specific metadata?**"
            "\nOur system intelligently maps your query to the most relevant results."
        )

        try:
            result = pinecone_data_handler.render_metadata_fetch_form()
            
            # if result:
            #     st.success("✅ **Metadata fetched successfully!**")
            #     st.write(result)
            # else:
            #     st.warning("⚠️ No relevant metadata found. Try refining your query for better results.")
        
        except Exception as e:
            st.error(f"❌ An error occurred while fetching metadata: {str(e)}")

    
# Call the function to render the Knowledge Base Explorer
if __name__ == "__main__":
    render_knowledge_base_explorer()