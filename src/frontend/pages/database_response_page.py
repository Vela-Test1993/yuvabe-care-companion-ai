import streamlit as st
from app import homepage
from app import common_fuctions

SAMPLE_QUESTION_1 = "Last night I broke out in a sweat and got shaky then I felt like I was getting the flu so I went to bed at 7pm. I dont think I have the flu but I just ate two cookies and i got sweaty again. Im not feeling myself at all. I am 47 on hormones with a long history of family heart disease."
SAMPLE_QUESTION_2 = " I am feeling really weak today I was vomiting yesterday all day with a high heart rate and sweating like crazy. I thought I was just hungover but I don t think that s the case. I also have a small bump on my forehead that is swollen and tender to the touch."
SAMPLE_QUESTION_3 = "I just woke up now, It s 7pm. It was a bit of an offsleep, but when i woke up i felt really weak, shaky, almost lighter. I m still shaking now. I tried just waking up a bit, Drinking some water and milk, Went to the bathroom. But i still fell weak shaky and light"

homepage.config_homepage()
st.title("Database Response")
st.write("This page is used to get the response from the database")
prompt = st.text_input("Enter your prompt")
if prompt == "":
    selected_option = st.selectbox("Select a sample question", ["",SAMPLE_QUESTION_1, SAMPLE_QUESTION_2, SAMPLE_QUESTION_3])
    if selected_option not in ["", None]:
        prompt = selected_option
if prompt:
    if st.button("Get DB response"):
        endpoint = "/chat/db_response"
        response = common_fuctions.get_api_response(endpoint, [prompt])
        st.subheader("✅ Relevant question and answer pair found in the database.")
        for metadata_group in response["metadatas"]:
            for entry in metadata_group:
                st.write("Question:", entry["question"])
                st.write("Answer:", entry["answer"])
                st.write("-" * 80) 

        if st.button("Clear chat"):
            st.rerun()