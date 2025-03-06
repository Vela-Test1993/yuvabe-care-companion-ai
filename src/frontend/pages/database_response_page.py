import streamlit as st
from app import homepage
from app import common_fuctions

homepage.config_homepage()
st.title("Database Response")
st.write("This page is used to get the response from the database")
prompt = st.text_input("Enter your prompt")
if st.button("Get DB response"):
    response = common_fuctions.get_api_response("/chat/dbresponse",prompt)
    for metadata_group in response["metadatas"]:
        for entry in metadata_group:
            st.write("Question:", entry["question"])
            st.write("Answer:", entry["answer"])
            st.write("-" * 80) 