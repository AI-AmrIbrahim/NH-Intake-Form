import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from src.config.form_defaults import FORM_FIELDS

def additional_info_form(user_profile, errors):
    """Renders the additional information section of the form."""
    with stylable_container(key="additional_info_container", css_styles='''
    {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    '''):
        st.header("📝 Additional Information")
        
        # Initialize session state if not exists
        if "additional_info" not in st.session_state:
            st.session_state.additional_info = user_profile.get("additional_info", FORM_FIELDS.get("additional_info", ""))
        
        additional_info = st.text_area(
            "Is there anything else you would like to share that might be relevant to your health?",
            placeholder="e.g., Previous sports injuries, aches, pains, depression, anxiety, etc.",
            key="additional_info"
        )
        if "additional_info" in errors:
            st.error(errors["additional_info"])

        return {
            "additional_info": additional_info
        }