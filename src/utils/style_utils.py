import streamlit as st
from .file_utils import get_base64_of_bin_file

def inject_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_page_background(png_file):
    """Sets the background of a Streamlit app from a PNG file."""
    bin_str = get_base64_of_bin_file(png_file)
    if bin_str:
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: scroll; # or 'fixed'
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

def display_message(message_type, message):
    if message_type == "success":
        st.success(message)
    elif message_type == "error":
        st.error(message)
