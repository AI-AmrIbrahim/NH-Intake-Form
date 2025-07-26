import streamlit as st

def medications_allergies_form(user_profile):
    """Renders the medications and allergies section of the form."""
    with st.container(border=True):
        st.header("💊 Medications & Allergies")
        medications = st.text_area(
            "Please list any Over-the-Counter (OTC) or prescribed medications you are currently taking.",
            value=", ".join(user_profile.get("medications", [])),
            placeholder="e.g., Ibuprofen, Aspirin, Atorvastatin, Amlodipine, Metformin. Please separate each with a comma.",
            key="medications"
        )
        natural_supplements = st.text_area(
            "Please list any natural supplements you are currently taking.",
            value=", ".join(user_profile.get("natural_supplements", [])),
            placeholder="e.g., Melatonin, St. John's Wort, Fish Oil. Please separate each with a comma.",
            key="natural_supplements"
        )
        allergies = st.text_area(
            "Please list any known allergies.",
            value=", ".join(user_profile.get("allergies", [])),
            placeholder="e.g., Peanuts, Penicillin, Sulfa. Please separate each with a comma.",
            key="allergies"
        )

        return {
            "medications": medications,
            "natural_supplements": natural_supplements,
            "allergies": allergies
        }
