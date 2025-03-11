from app import common_fuctions
import streamlit as st
from app import homepage
from utils import logger

logger = logger.get_logger()

homepage.config_homepage()
st.title("Data Loader")

def load_data():
    st.sidebar.header("📊 Data Loading Parameters")
    start_index  = st.sidebar.number_input("Select start index", min_value=0, value=0)
    end_index  = st.sidebar.number_input("Select end index", min_value=0, value=100)

    if start_index > end_index:
        st.sidebar.error("⚠️ Start index must be earlier than the end index.")
        return
    
    if "load_clicked" not in st.session_state:
        st.session_state.load_clicked = False

    try:
        st.sidebar.info(f"Click the button to load data from index **{start_index} to {end_index}**.")
        if st.sidebar.button("🚀 Upsert Data", disabled=st.session_state.load_clicked, help="Click to insert data into the database"):
            st.session_state.load_clicked = True

            with st.spinner("⏳ Upserting data... Please wait"):
                response = common_fuctions.upsert_data_request(start_index, end_index)
                if response.get("status") == "success": 
                    st.success("Data upserted successfully!")
                else:
                    st.error("Error upserting data.")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        logger.error(f"Error loading data: {e}")
        st.session_state.load_clicked = False

load_data()