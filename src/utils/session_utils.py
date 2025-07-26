
import streamlit as st

def clear_form():
    """
    Resets user profile data in Streamlit session state.

    For new users, it clears all profile data. For returning users, it preserves
    personal information while resetting lifestyle and health-related data to their
    default values.
    """
    user_status = st.session_state.get("user_status", "No, I have not filled out the intake form before")

    # Default user profile structure
    default_profile = {
        "first_name": "", "last_name": "", "email": "", "dob": None, "sex": "Male",
        "height_m": "", "weight_kg": "", "physical_activity": "3-4 days",
        "energy_level": "Neutral", "diet": "I don't follow a specific diet",
        "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
        "current_medications": [], "allergies": [], "health_goals": [],
        "other_health_goal": "", "interested_supplements": [], "additional_info": ""
    }

    if user_status == "Yes, I have filled out the intake form before":
        # Preserve personal info for returning users
        personal_info = {}
        personal_keys = ["first_name", "last_name", "email", "dob", "sex"]
        if "user_profile" in st.session_state:
            for key in personal_keys:
                if key in st.session_state.user_profile:
                    personal_info[key] = st.session_state.user_profile[key]

        # Reset profile but restore personal info
        st.session_state.user_profile = default_profile
        st.session_state.user_profile.update(personal_info)
    else:
        # Reset everything for new users
        st.session_state.user_profile = default_profile

    # Clear health_goals from session state regardless of user status
    if "health_goals" in st.session_state:
        st.session_state.health_goals = []
