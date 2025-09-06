import streamlit as st
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
    Resets the form fields in the session state, including the user profile.
    """
    # Reset all form fields to their default values
    for key, default_value in FORM_FIELDS.items():
        st.session_state[key] = default_value

    # Reset the user_profile dictionary to its default state
    st.session_state.user_profile = {
            "user_id": "", "age_range": "18-24", "sex": "Male", "height_ft": 5, "height_in": 6, "weight_lbs": "",
            "physical_activity": "3-4 days", "energy_level": "Neutral", "diet": "I don't follow a specific diet",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "medications": [], "natural_supplements": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": "",
            "security_question_1": "", "security_answer_1": "",
            "security_question_2": "", "security_answer_2": "",
            "security_question_3": "", "security_answer_3": ""
        }
    st.session_state.errors = {}

    if "pdf_uploader" in st.session_state:
        st.session_state.pdf_uploader = None