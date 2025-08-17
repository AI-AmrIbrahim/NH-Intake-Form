import streamlit as st
import datetime
from src.config.form_defaults import FORM_FIELDS

def personal_info_form(user_profile, user_status, errors):
    """Renders the personal information section of the form."""
    with st.container(border=True):
        st.header("👤 Personal Information")
        
        is_returning_user = user_status != "No, I have not filled out the intake form before"

        # Initialize session state for all fields if they don't exist
        if "weight_lbs" not in st.session_state:
            st.session_state.weight_lbs = str(user_profile.get("weight_lbs", FORM_FIELDS["weight_lbs"]))
        if "sex" not in st.session_state:
            st.session_state.sex = user_profile.get("sex", FORM_FIELDS["sex"])
        if "height_ft" not in st.session_state:
            st.session_state.height_ft = user_profile.get("height_ft", FORM_FIELDS["height_ft"])
        if "height_in" not in st.session_state:
            st.session_state.height_in = user_profile.get("height_in", FORM_FIELDS["height_in"])

        # Height - editable for both new and returning users
        st.write("Height")
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.selectbox("Feet", list(range(4, 7)), key="height_ft")
            if "height_ft" in errors:
                st.error(errors["height_ft"])
        with col2:
            height_in = st.selectbox("Inches", list(range(0, 12)), key="height_in")
            if "height_in" in errors:
                st.error(errors["height_in"])

        # Weight - editable for both new and returning users
        weight_input = st.text_input(
            "Weight (in lbs)", 
            key="weight_lbs"
        )
        if "weight_lbs" in errors:
            st.error(errors["weight_lbs"])
        
        st.write("")
        
        # Sex - disabled for returning users
        sex = st.radio(
            "Biological Sex", 
            ('Male', 'Female'), 
            disabled=is_returning_user, 
            key="sex"
        )

        return {
            "height_ft": height_ft,
            "height_in": height_in,
            "weight_lbs": weight_input,
            "sex": sex
        }