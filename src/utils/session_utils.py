import streamlit as st
import datetime
from src.config.form_defaults import FORM_FIELDS

def initialize_session_state():
    """Initializes the session state with default values for all form fields."""
    for key, default_value in FORM_FIELDS.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    if 'user_status' not in st.session_state:
        st.session_state['user_status'] = "No, I have not filled out the intake form before"

def clear_form():
    """
    Resets the form fields in the session state.
    If the user is returning, personal information is preserved.
    """
    user_status = st.session_state.get("user_status")

    personal_info_keys = [
        "first_name", "last_name", "email", 
        "dob_month", "dob_day", "dob_year", "sex",
        "load_email"
    ]

    for key, default_value in FORM_FIELDS.items():
        if user_status == "Yes, I have filled out the intake form before" and key in personal_info_keys:
            # Don't clear personal info for returning users
            continue
        st.session_state[key] = default_value