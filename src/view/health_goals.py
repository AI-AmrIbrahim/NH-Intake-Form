import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from src.config.form_defaults import FORM_FIELDS

def health_goals_form(user_profile, errors):
    """Renders the health goals section of the form."""
    with stylable_container(key="health_goals_container", css_styles='''
    {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    '''):
        st.header("🎯 Health Goals")
        health_goals_options = [
            "Improve Energy", "Boost Immunity", "Support Joint Health",
            "Enhance Sleep Quality", "Improve Digestive Health", "Support Heart Health",
            "Strengthen Bones", "Improve Mood & Focus", "Other"
        ]
        
        # Initialize session state for health goals
        if 'health_goals' not in st.session_state:
            st.session_state.health_goals = user_profile.get("health_goals", FORM_FIELDS["health_goals"])
        
        # Initialize session state for interested supplements
        if "interested_supplements" not in st.session_state:
            stored_supplements = user_profile.get("interested_supplements", [])
            if isinstance(stored_supplements, list):
                st.session_state.interested_supplements = ", ".join(stored_supplements)
            else:
                st.session_state.interested_supplements = str(stored_supplements)

        # Initialize session state for other_health_goal
        if "other_health_goal" not in st.session_state:
            st.session_state.other_health_goal = user_profile.get("other_health_goal", "")

        def limit_multiselect():
            if len(st.session_state.health_goals) > 2:
                st.session_state.health_goals = st.session_state.health_goals[:2]

        health_goals = st.multiselect(
            "What are your primary health goals? (Select up to 2)",
            health_goals_options,
            key="health_goals",
            on_change=limit_multiselect
        )
        if "health_goals" in errors:
            st.error(errors["health_goals"])

        other_health_goal = ""
        if "Other" in health_goals:
            other_health_goal = st.text_input(
                "Please specify your other health goal:",
                key="other_health_goal"
            )
            if "other_health_goal" in errors:
                st.error(errors["other_health_goal"])

        interested_supplements = st.text_area(
            "Are there any specific vitamins or supplements you are interested in?",
            placeholder="e.g., Vitamin D, Probiotics, Turmeric. \n\nPlease separate each with a comma.",
            key="interested_supplements"
        )
        if "interested_supplements" in errors:
            st.error(errors["interested_supplements"])

        return {
            "health_goals": health_goals,
            "other_health_goal": other_health_goal,
            "interested_supplements": interested_supplements
        }