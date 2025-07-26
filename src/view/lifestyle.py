import streamlit as st

def lifestyle_form(user_profile):
    """Renders the lifestyle section of the form."""
    with st.container(border=True):
        st.header("🏃 Lifestyle")
        activity_options = ["0-1 days", "1-2 days", "3-4 days", "5-7 days"]
        physical_activity = st.selectbox(
            "How many days per week do you engage in physical activity (e.g., workout, sport, walking)?",
            activity_options,
            key="physical_activity"
        )
        energy_level = st.select_slider(
            "How would you rate your energy on a typical day?",
            options=["Very Low", "Low", "Neutral", "High", "Very High"],
            key="energy_level"
        )
        diet_options = ["Clean/Whole food", "High Protein", "Plant-based", "Low carb/keto", "Fast-food often", "I don't follow a specific diet"]
        diet = st.selectbox(
            "Which of the following best describes your typical diet?",
            diet_options,
            key="diet"
        )
        meals_per_day = st.selectbox(
            "How many meals do you typically eat per day?",
            ["1", "2", "3", "More than 3"],
            key="meals_per_day"
        )
        sleep_quality = st.select_slider(
            "How would you rate your overall sleep quality?",
            options=["Poor", "Fair", "Good", "Excellent"],
            key="sleep_quality"
        )
        stress_level = st.select_slider(
            "How would you rate your average daily stress level?",
            options=["Low", "Moderate", "High"],
            key="stress_level"
        )

        return {
            "physical_activity": physical_activity,
            "energy_level": energy_level,
            "diet": diet,
            "meals_per_day": meals_per_day,
            "sleep_quality": sleep_quality,
            "stress_level": stress_level
        }
