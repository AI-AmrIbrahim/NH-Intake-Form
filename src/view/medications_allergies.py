import streamlit as st
from src.config.form_defaults import FORM_FIELDS

def medications_allergies_form(user_profile):
    """Renders the medications and allergies section of the form."""
    with st.container(border=True):
        st.header("💊 Medications & Allergies")
        
        # Initialize session state for medications
        if "medications" not in st.session_state:
            stored_medications = user_profile.get("medications", FORM_FIELDS.get("medications", []))
            if isinstance(stored_medications, list):
                st.session_state.medications = ", ".join(stored_medications)
            else:
                st.session_state.medications = str(stored_medications)
        
        # Initialize session state for natural supplements
        if "natural_supplements" not in st.session_state:
            stored_supplements = user_profile.get("natural_supplements", FORM_FIELDS.get("natural_supplements", []))
            if isinstance(stored_supplements, list):
                st.session_state.natural_supplements = ", ".join(stored_supplements)
            else:
                st.session_state.natural_supplements = str(stored_supplements)
        
        # Initialize session state for allergies
        if "allergies" not in st.session_state:
            stored_allergies = user_profile.get("allergies", FORM_FIELDS.get("allergies", []))
            if isinstance(stored_allergies, list):
                st.session_state.allergies = ", ".join(stored_allergies)
            else:
                st.session_state.allergies = str(stored_allergies)
        
        medications = st.text_area(
            "Please list any Over-the-Counter (OTC) or prescribed medications you are currently taking.",
            placeholder="e.g., Ibuprofen, Aspirin, Atorvastatin, Amlodipine, Metformin. Please separate each with a comma.",
            key="medications"
        )
        
        natural_supplements = st.text_area(
            "Please list any natural supplements you are currently taking.",
            placeholder="e.g., Melatonin, St. John's Wort, Fish Oil. Please separate each with a comma.",
            key="natural_supplements"
        )
        
        allergies = st.text_area(
            "Please list any known allergies.",
            placeholder="e.g., Peanuts, Penicillin, Sulfa. Please separate each with a comma.",
            key="allergies"
        )

        return {
            "medications": medications,
            "natural_supplements": natural_supplements,
            "allergies": allergies
        }