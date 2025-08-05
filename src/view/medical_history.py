import streamlit as st
from src.config.form_defaults import FORM_FIELDS

def medical_history_form(user_profile, sex, errors):
    """Renders the medical history section of the form."""
    with st.container(border=True):
        st.header("⚕️ Medical History")
        
        # Initialize session state for medical conditions
        if "medical_conditions" not in st.session_state:
            stored_conditions = user_profile.get("medical_conditions", FORM_FIELDS.get("medical_conditions", []))
            if isinstance(stored_conditions, list):
                st.session_state.medical_conditions = ", ".join(stored_conditions)
            else:
                st.session_state.medical_conditions = str(stored_conditions)
        
        pregnant_or_breastfeeding = "Not Applicable"
        if sex == 'Female':
            # Initialize session state for pregnant_or_breastfeeding
            if "pregnant_or_breastfeeding" not in st.session_state:
                stored_pob = user_profile.get("pregnant_or_breastfeeding", FORM_FIELDS.get("pregnant_or_breastfeeding", "No"))
                pob_options = ('No', 'Yes')
                if stored_pob not in pob_options:
                    stored_pob = "No"
                st.session_state.pregnant_or_breastfeeding = stored_pob
            
            pregnant_or_breastfeeding = st.radio(
                "Are you currently pregnant or breastfeeding?",
                ('No', 'Yes'),
                key="pregnant_or_breastfeeding"
            )
            if "pregnant_or_breastfeeding" in errors:
                st.error(errors["pregnant_or_breastfeeding"])
        
        medical_conditions = st.text_area(
            "Please list any pre-existing medical conditions.",
            placeholder="e.g., High blood pressure, Asthma, Diabetes. Please separate each condition with a comma.",
            key="medical_conditions"
        )
        if "medical_conditions" in errors:
            st.error(errors["medical_conditions"])

        return {
            "pregnant_or_breastfeeding": pregnant_or_breastfeeding,
            "medical_conditions": medical_conditions
        }