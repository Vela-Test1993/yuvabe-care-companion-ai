import requests
from app import common_functions
import streamlit as st


API_BASE_URL = "http://localhost:8000/knowledge-base"

def upsert_data(st):
    st.header("Upsert Data")
    with st.form("upsert_form"):
        input_text = st.text_area("Input", "What is mental health?")
        output_text = st.text_area("Output", "Mental health refers to...")
        instruction_text = st.text_input("Instruction", "Focus on general well-being.")
        upsert_submit = st.form_submit_button("Upsert Data")

        if upsert_submit:
            payload = {"data": [{"input": input_text, "output": output_text, "instruction": instruction_text}]}
            response = requests.post(f"{API_BASE_URL}/upsert-data", json=payload)
            st.success(response.json()["message"]) if response.status_code == 200 else st.error(response.json()["detail"])

def delete_records(st):
    st.header("Delete Records")
    with st.form("delete_form"):
        ids_to_delete = st.text_area("IDs to Delete", "id_123, id_456").split(",")
        delete_submit = st.form_submit_button("Delete Records")

        if delete_submit:
            payload = {"ids_to_delete": [id.strip() for id in ids_to_delete]}
            response = requests.post(f"{API_BASE_URL}/delete-records", json=payload)
            st.success(response.json()["message"]) if response.status_code == 200 else st.error(response.json()["detail"])

# def render_metadata_fetch_form(st):
#     st.header("Fetch Metadata")
#     with st.form("fetch_metadata_form"):
#         prompt_text = st.text_area("Describe Your Concern", "e.g., I've been feeling anxious lately.")
#         n_result = st.number_input("Number of Results", min_value=1, value=3)
#         score_threshold = st.number_input("Score Threshold", min_value=0.0, max_value=1.0, value=0.47)
#         metadata_submit = st.form_submit_button("Fetch Metadata")

#         if metadata_submit:
#             payload = {
#                 "prompt": prompt_text,
#                 "n_result": n_result,
#                 "score_threshold": score_threshold
#             }
#             response = requests.post(f"{API_BASE_URL}/fetch-metadata", json=payload)
#             if response.status_code == 200:
#                 metadata = response.json().get('metadata', [])
#                 try:
#                     if metadata:
#                         st.subheader("Search Results")
#                         for index, entry in enumerate(metadata, start=1):
#                             st.markdown(f"### Result {index}")
#                             common_fuctions.typewriter_effect(st, f"**Question:** {entry['question']}")
#                             common_fuctions.typewriter_effect(st, f"**Answer:** {entry['answer']}")
#                             st.markdown(f"**Score:** {entry['score']}")
#                             st.markdown(f"**ID:** {entry['id']}")
#                             st.markdown("---")
#                 except Exception as e:
#                     st.info("There is not relevant data to fetch")

def render_metadata_fetch_form(st):
    st.header("Fetch Metadata")
    with st.form("fetch_metadata_form"):
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

        metadata_submit = st.form_submit_button("Fetch Metadata")

        if metadata_submit:
            payload = {
                "prompt": prompt_text.strip(),
                "n_result": n_result,
                "score_threshold": score_threshold
            }

            try:
                response = requests.post(f"{API_BASE_URL}/fetch-metadata", json=payload)
                response.raise_for_status()  # Ensures HTTP errors are caught
                metadata = response.json().get('metadata', [])

                if metadata:
                    st.subheader("Search Results")
                    for index, entry in enumerate(metadata, start=1):
                        st.markdown(f"### Result {index}")
                        common_functions.typewriter_effect(f"**Question:** {entry.get('question', 'N/A')}")
                        common_functions.typewriter_effect(f"**Answer:** {entry.get('answer', 'N/A')}")
                        st.markdown(f"**Score:** {entry.get('score', 'N/A')}")
                        st.markdown(f"**ID:** {entry.get('id', 'N/A')}")
                        st.markdown("---")
                else:
                    st.info("No relevant data found based on your input. Try refining your concern or adjusting the threshold.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
