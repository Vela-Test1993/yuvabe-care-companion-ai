import requests
from frontend.app import common_functions
import streamlit as st

API_BASE_URL = "http://localhost:8000/knowledge-base"

def upsert_data():
    """
    Displays a form to upsert data into the Pinecone database.

    Features:
    - Users can provide 'Input', 'Output', and 'Instruction'.
    - Displays appropriate success or error messages.
    - Improved error handling with detailed feedback.
    """

    st.subheader("Enter the data to upsert")
    with st.form("upsert_form"):
        # Input Fields
        input_text = st.text_area("Input", placeholder="Enter input text here...", height=150)
        output_text = st.text_area("Output", placeholder="Enter output text here...", height=150)
        instruction_text = st.text_input("Instruction", placeholder="Provide guidance for the data...")

        upsert_submit = st.form_submit_button("🚀 Upsert Data")

        if upsert_submit:
            # ✅ Validation Check
            if not input_text.strip() or not output_text.strip() or not instruction_text.strip():
                st.error("❗ All fields are required. Please fill out each section before submitting.")
                return

            # ✅ Payload Creation
            payload = {
                "data": [
                    {
                        "input": input_text.strip(),
                        "output": output_text.strip(),
                        "instruction": instruction_text.strip()
                    }
                ]
            }

            # API Call 
            with st.spinner("⏳ Processing your data..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/upsert-data", json=payload)
                    response_data = response.json()

                    if response.status_code == 200:
                        st.success(f"✅ Data successfully upserted: {response_data.get('message', 'Success')}")
                        st.toast("🎉 Upsert successful!")
                    elif response.status_code == 400:
                        st.warning(f"⚠️ Bad Request: {response_data.get('detail', 'Check your input data.')}")
                    elif response.status_code == 500:
                        st.error("❌ Internal Server Error. Please try again later.")
                    else:
                        st.error(f"❗ Unexpected error: {response_data.get('detail', 'Unknown issue occurred.')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Network error: {e}")

def delete_records():
    """
    Displays a form to delete records from the Pinecone database.

    Features:
    - Users can input comma-separated IDs for deletion.
    - Includes validation checks for empty or malformed IDs.
    - Enhanced error handling for better user feedback.
    """
    st.subheader("Enter id to delete")
    with st.form("delete_form"):
        ids_input = st.text_area("IDs to Delete", placeholder="Enter IDs separated by commas (e.g., id_123, id_456)")
        ids_to_delete = [id.strip() for id in ids_input.split(",") if id.strip()]

        delete_submit = st.form_submit_button("🗑️ Delete Records")

        if delete_submit:
            # ✅ Validation Check
            if not ids_to_delete:
                st.error("❗ Please provide at least one valid ID.")
                return

            # 🔒 Confirmation Prompt for Safety
            if not st.confirm("Are you sure you want to delete the selected records? This action is irreversible."):
                st.info("❗ Deletion canceled.")
                return

            # ✅ Payload Creation
            payload = {"ids_to_delete": ids_to_delete}

            # ✅ API Call with Improved Error Handling
            with st.spinner("⏳ Deleting records..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/delete-records", json=payload)
                    response_data = response.json()

                    if response.status_code == 200:
                        st.success(f"✅ {response_data.get('message', 'Records successfully deleted.')}")
                        st.toast("🎯 Deletion successful!")
                    elif response.status_code == 400:
                        st.warning(f"⚠️ Bad Request: {response_data.get('detail', 'Check the provided IDs.')}")
                    elif response.status_code == 404:
                        st.warning("⚠️ No matching records found. Please verify the provided IDs.")
                    elif response.status_code == 500:
                        st.error("❌ Internal Server Error. Please try again later.")
                    else:
                        st.error(f"❗ Unexpected error: {response_data.get('detail', 'Unknown issue occurred.')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Network error: {e}")

def render_metadata_fetch_form():
    """
    Renders a form to fetch metadata based on user concerns.
    
    Features:
    - Input validation to ensure meaningful data is provided.
    - Displays metadata in a visually appealing format.
    - Improved error handling with detailed messages.
    """
    st.header("📋 Fetch Metadata")
    with st.form("fetch_metadata_form"):
        # 📝 Input Fields
        prompt_text = st.text_area(
            "Describe Your Concern", 
            "e.g., I've been feeling anxious lately.",
            help="Provide a brief description of your concern to get relevant metadata."
        )
        n_result = st.number_input(
            "Number of Results", 
            min_value=1, 
            value=3,
            help="Specify the number of search results you'd like to retrieve."
        )
        score_threshold = st.number_input(
            "Score Threshold", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.47,
            help="Set the minimum relevance score for the results. Higher values ensure more accurate matches."
        )

        metadata_submit = st.form_submit_button("🔍 Fetch Metadata")

        if metadata_submit:
            # ✅ Input Validation
            if not prompt_text.strip():
                st.warning("❗ Please provide a valid concern description.")
                return

            payload = {
                "prompt": prompt_text.strip(),
                "n_result": n_result,
                "score_threshold": score_threshold
            }

            # 🔄 Enhanced API Request with Better Error Handling
            with st.spinner("⏳ Fetching metadata..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/fetch-metadata", json=payload)
                    response.raise_for_status()  
                    metadata = response.json().get('metadata', [])

                    # ✅ Display Results
                    if metadata:
                        st.success(f"✅ Found {len(metadata)} relevant result(s).")
                        st.subheader("Search Results")

                        for index, entry in enumerate(metadata, start=1):
                            common_functions.typewriter_effect(f"**🧠 Question:** {entry.get('question', 'N/A')}",speed=0)
                            common_functions.typewriter_effect(f"**💬 Answer:** {entry.get('answer', 'N/A')}",speed=0)
                            st.markdown(f"**📈 Score:** `{entry.get('score', 'N/A')}`")
                            st.markdown(f"**🆔 ID:** `{entry.get('id', 'N/A')}`")

                    else:
                        st.info("🤔 No relevant data found. Try refining your concern or adjusting the score threshold.")

                # Exception Handling for Specific Errors
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"❌ HTTP Error: {http_err}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Network error. Please check your internet connection.")
                except requests.exceptions.Timeout:
                    st.error("❌ Request timed out. Please try again later.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Unexpected error: {e}")
