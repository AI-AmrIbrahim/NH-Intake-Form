import streamlit as st

def additional_info_form(user_profile):
    """Renders the additional information section of the form."""
    with st.container(border=True):
        st.header("📝 Additional Information")
        additional_info = st.text_area(
            "Is there anything else you would like to share that might be relevant to your health?",
            value=user_profile.get("additional_info", ""),
            placeholder="e.g., Previous sports injuries, aches, pains, depression, anxiety, etc."
        )

        return {
            "additional_info": additional_info
        }
