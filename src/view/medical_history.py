import streamlit as st

def medical_history_form(user_profile, sex):
    """Renders the medical history section of the form."""
    with st.container(border=True):
        st.header("⚕️ Medical History")
        pregnant_or_breastfeeding = "Not Applicable"
        if sex == 'Female':
            pob_options = ('No', 'Yes')
            # Handle legacy "Not Applicable" value for returning users
            stored_pob = user_profile.get("pregnant_or_breastfeeding", "No")
            if stored_pob not in pob_options:
                stored_pob = "No"
            pob_index = pob_options.index(stored_pob)
            pregnant_or_breastfeeding = st.radio(
                "Are you currently pregnant or breastfeeding?",
                pob_options,
                index=pob_index
            )
        medical_conditions = st.text_area(
            "Please list any pre-existing medical conditions.",
            value=", ".join(user_profile.get("medical_conditions", [])),
            placeholder="e.g., High blood pressure, Asthma, Diabetes. Please separate each condition with a comma."
        )

        return {
            "pregnant_or_breastfeeding": pregnant_or_breastfeeding,
            "medical_conditions": medical_conditions
        }
