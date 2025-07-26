import streamlit as st
import datetime

# A dictionary of all form fields and their default values
FORM_FIELDS = {
    "first_name": "",
    "last_name": "",
    "email": "",
    "dob_month": "January",
    "dob_day": 1,
    "dob_year": 1990,
    "sex": "Male",
    "height_ft": 5,
    "height_in": 6,
    "weight_lbs": "",
    "physical_activity": "3-4 days",
    "energy_level": "Neutral",
    "diet": "I don't follow a specific diet",
    "meals_per_day": "3",
    "sleep_quality": "Good",
    "stress_level": "Moderate",
    "pregnant_or_breastfeeding": "No",
    "medical_conditions": "",
    "medications": "",
    "natural_supplements": "",
    "allergies": "",
    "health_goals": [],
    "other_health_goal": "",
    "interested_supplements": "",
    "additional_info": ""
}

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
        "dob_month", "dob_day", "dob_year", "sex"
    ]

    for key, default_value in FORM_FIELDS.items():
        if user_status == "Yes, I have filled out the intake form before" and key in personal_info_keys:
            # Don't clear personal info for returning users
            continue
        st.session_state[key] = default_value