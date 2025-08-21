import streamlit as st

def inject_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def display_message(message_type, message):
    if message_type == "success":
        st.success(message)
    elif message_type == "error":
        st.error(message)