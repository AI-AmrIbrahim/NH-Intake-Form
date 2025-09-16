import streamlit as st
from src.config.form_defaults import FORM_FIELDS
from streamlit_extras.stylable_container import stylable_container

def personal_info_form(user_profile, errors):
    """Renders the personal information section of the form."""
    with stylable_container(key="personal_info_container", css_styles='''
    {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    '''):
        st.header("👤 Personal Information")

        # Initialize session state for all fields if they don't exist
        if "weight_lbs" not in st.session_state:
            weight_value = user_profile.get("weight_lbs", FORM_FIELDS["weight_lbs"])
            st.session_state.weight_lbs = str(weight_value) if weight_value is not None else ""
        if "sex" not in st.session_state:
            st.session_state.sex = user_profile.get("sex", FORM_FIELDS["sex"])
        if "height_ft" not in st.session_state:
            st.session_state.height_ft = user_profile.get("height_ft", FORM_FIELDS["height_ft"])
        if "height_in" not in st.session_state:
            st.session_state.height_in = user_profile.get("height_in", FORM_FIELDS["height_in"])
        if "age_range" not in st.session_state:
            st.session_state.age_range = user_profile.get("age_range", "18-24")

        # Age Range
        age_range = st.selectbox(
            "Age Range",
            ("18-24", "25-34", "35-44", "45-54", "55-64", "65+"),
            key="age_range"
        )
        if "age_range" in errors:
            st.error(errors["age_range"])

        # Height
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

        # Weight
        weight_input = st.text_input(
            "Weight (in lbs)",
            key="weight_lbs"
        )
        if "weight_lbs" in errors:
            st.error(errors["weight_lbs"])

        st.write("")

        # Sex
        sex = st.radio(
            "Biological Sex",
            ('Male', 'Female'),
            key="sex"
        )

        return {
            "age_range": age_range,
            "height_ft": height_ft,
            "height_in": height_in,
            "weight_lbs": weight_input,
            "sex": sex
        }
