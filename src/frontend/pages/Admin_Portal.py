import streamlit as st
from app import pinecone_data_handler


st.title("Admin Portal")

DataManager = st.tabs(["Pinecone Data Manager"])[0]

with DataManager:
    Upsert, Delete = st.tabs(["Upsert Data", "Delete Records"])

    with Upsert:
        pinecone_data_handler.upsert_data(st)
    with Delete:
        pinecone_data_handler.delete_records(st)


# with tab3:




# # Upsert Data Form
# st.header("Upsert Data")
# with st.form("upsert_form"):
#     input_text = st.text_area("Input", "What is mental health?")
#     output_text = st.text_area("Output", "Mental health refers to...")
#     instruction_text = st.text_input("Instruction", "Focus on general well-being.")
#     upsert_submit = st.form_submit_button("Upsert Data")

#     if upsert_submit:
#         payload = {"data": [{"input": input_text, "output": output_text, "instruction": instruction_text}]}
#         response = requests.post(f"{API_BASE_URL}/upsert-data", json=payload)
#         st.success(response.json()["message"]) if response.status_code == 200 else st.error(response.json()["detail"])

# # Delete Records Form
# st.header("Delete Records")
# with st.form("delete_form"):
#     ids_to_delete = st.text_area("IDs to Delete", "id_123, id_456").split(",")
#     delete_submit = st.form_submit_button("Delete Records")

#     if delete_submit:
#         payload = {"ids_to_delete": [id.strip() for id in ids_to_delete]}
#         response = requests.post(f"{API_BASE_URL}/delete-records", json=payload)
#         st.success(response.json()["message"]) if response.status_code == 200 else st.error(response.json()["detail"])

# # Fetch Metadata Form
# st.header("Fetch Metadata")
# with st.form("fetch_metadata_form"):
#     prompt_text = st.text_area("Prompt", "Tell me about mental health")
#     n_result = st.number_input("Number of Results", min_value=1, value=3)
#     score_threshold = st.number_input("Score Threshold", min_value=0.0, max_value=1.0, value=0.47)
#     metadata_submit = st.form_submit_button("Fetch Metadata")

#     if metadata_submit:
#         payload = {"prompt": prompt_text, "n_result": n_result, "score_threshold": score_threshold}
#         response = requests.post(f"{API_BASE_URL}/fetch-metadata", json=payload)
#         if response.status_code == 200:
#             st.json(response.json()["metadata"])
#         else:
            # st.error(response.json()["detail"])