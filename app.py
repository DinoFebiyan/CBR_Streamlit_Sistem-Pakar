import streamlit as st
from page import main_page, tambah_gejala_page

st.set_page_config(
    page_title="Orange Checker",
    page_icon="🍊",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    main_page()
else:
    if st.session_state.page == "tambah_gejala":
        tambah_gejala_page()