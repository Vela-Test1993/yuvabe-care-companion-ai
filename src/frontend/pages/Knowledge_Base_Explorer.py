import streamlit as st
from app import pinecone_data_handler

st.title("Knowledge Base Explorer")

st.markdown("Enter your concerns below to receive helpful information.")

with st.expander("Knowledge Base"):
    pinecone_data_handler.render_metadata_fetch_form(st)