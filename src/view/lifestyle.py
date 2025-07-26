import streamlit as st

def lifestyle_form(user_profile):
    """Renders the lifestyle section of the form."""
    with st.container(border=True):
        st.header("🏃 Lifestyle")
        activity_options = ["0-1 days", "1-2 days", "3-4 days", "5-7 days"]
        physical_activity = st.selectbox(
            "How many days per week do you engage in physical activity (e.g., workout, sport, walking)?",
            activity_options,
            index=activity_options.index(user_profile.get("physical_activity", "3-4 days"))
        )
        energy_level = st.select_slider(
            "How would you rate your energy on a typical day?",
            options=["Very Low", "Low", "Neutral", "High", "Very High"],
            value=user_profile.get("energy_level", "Neutral")
        )
        diet_options = ["Clean/Whole food", "High Protein", "Plant-based", "Low carb/keto", "Fast-food often", "I don't follow a specific diet"]
        diet = st.selectbox(
            "Which of the following best describes your typical diet?",
            diet_options,
            index=diet_options.index(user_profile.get("diet", "I don't follow a specific diet"))
        )
        meals_per_day = st.selectbox(
            "How many meals do you typically eat per day?",
            ["1", "2", "3", "More than 3"],
            index=0
        )
        sleep_quality = st.select_slider(
            "How would you rate your overall sleep quality?",
            options=["Poor", "Fair", "Good", "Excellent"],
            value=user_profile.get("sleep_quality", "Good")
        )
        stress_level = st.select_slider(
            "How would you rate your average daily stress level?",
            options=["Low", "Moderate", "High"],
            value=user_profile.get("stress_level", "Moderate")
        )

        return {
            "physical_activity": physical_activity,
            "energy_level": energy_level,
            "diet": diet,
            "meals_per_day": meals_per_day,
            "sleep_quality": sleep_quality,
            "stress_level": stress_level
        }
