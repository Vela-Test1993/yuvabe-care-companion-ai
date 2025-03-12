from app import common_fuctions
import streamlit as st

common_fuctions.config_homepage(st)

def open_chat():

    prompt = st.chat_input("Ask me anything related to health care")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if prompt :

        with st.chat_message('user'):
            st.markdown(prompt)
        
        with st.spinner("Thinking..."):
            # response = common_fuctions.fetch_response(prompt, st.session_state.chat_history)
            response = common_fuctions.get_api_response("/test/relevant-response",prompt)

        with st.chat_message('assistant'):
            st.markdown(response)

                # Append to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

    # for chat in st.session_state.chat_history:
    #     with st.chat_message(chat["role"]):
    #         st.markdown(chat["content"])

open_chat()
