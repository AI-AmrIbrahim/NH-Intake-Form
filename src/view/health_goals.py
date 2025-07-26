import streamlit as st

def health_goals_form(user_profile):
    """Renders the health goals section of the form."""
    with st.container(border=True):
        st.header("🎯 Health Goals")
        health_goals_options = [
            "Improve Energy", "Boost Immunity", "Support Joint Health",
            "Enhance Sleep Quality", "Improve Digestive Health", "Support Heart Health",
            "Strengthen Bones", "Improve Mood & Focus", "Other"
        ]
        
        # Limit multiselect to 2 options
        if 'health_goals' not in st.session_state:
            st.session_state.health_goals = user_profile.get("health_goals", [])

        def limit_multiselect():
            if len(st.session_state.health_goals) > 2:
                st.session_state.health_goals = st.session_state.health_goals[:2]

        health_goals = st.multiselect(
            "What are your primary health goals? (Select up to 2)",
            health_goals_options,
            key="health_goals",
            on_change=limit_multiselect
        )

        other_health_goal = ""
        if "Other" in health_goals:
            other_health_goal = st.text_input(
                "Please specify your other health goal:",
                value=user_profile.get("other_health_goal", "")
            )

        interested_supplements = st.text_area(
            "Are there any specific vitamins or supplements you are interested in?",
            value=", ".join(user_profile.get("interested_supplements", [])),
            placeholder="e.g., Vitamin D, Probiotics, Turmeric. Please separate each with a comma."
        )

        return {
            "health_goals": health_goals,
            "other_health_goal": other_health_goal,
            "interested_supplements": interested_supplements
        }
