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
            "current_medications": [], "natural_supplements": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": "",
            "security_question_1": "", "security_answer_1": "",
            "security_question_2": "", "security_answer_2": "",
            "security_question_3": "", "security_answer_3": ""
        }
    st.session_state.errors = {}

def cleanup_session_state():
    """Clean up old session state data to prevent memory issues with high concurrency."""
    import time
    current_time = time.time()

    # Clean up old rate limit data
    keys_to_remove = []
    for key in st.session_state.keys():
        if key.startswith('rate_limit_'):
            # Remove rate limit entries older than 10 minutes
            if hasattr(st.session_state, key):
                cutoff_time = current_time - 600  # 10 minutes
                st.session_state[key] = [ts for ts in st.session_state[key] if ts > cutoff_time]

    # Mark session as cleaned
    st.session_state.last_cleanup = current_time