import streamlit as st
import re
import json
import os

# --- Profile Management Functions ---
def load_profiles():
    """Loads user profiles from a JSON file."""
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {} # Return empty dict if file is empty or corrupted
    return {}

def save_profiles(profiles):
    """Saves user profiles to a JSON file."""
    with open("profiles.json", "w") as f:
        json.dump(profiles, f, indent=4)

# --- AI Recommendation Function ---
def get_recommendations(user_data):
    """Generates supplement recommendations using the Gemini API."""
    try:
        with open("recommendation_prompt.md", "r") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        st.error("The 'recommendation_prompt.md' file is missing.")
        return ""

    prompt = prompt_template.format(
        age=user_data["age"],
        sex=user_data["sex"],
        pregnant_or_breastfeeding=user_data["pregnant_or_breastfeeding"],
        medical_conditions=", ".join(user_data["medical_conditions"]),
        current_medications=", ".join(user_data["current_medications"]),
        allergies=", ".join(user_data["allergies"]),
        health_goals=", ".join(user_data["health_goals"]),
        interested_supplements=", ".join(user_data["interested_supplements"])
    )

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def main():
    """
    Main function to run the Streamlit application for NutritionHouse.
    This app serves as the intake form and will display recommendations.
    """
    # --- Page Configuration ---
    st.set_page_config(
        page_title="NutritionHouse AI",
        page_icon="💊",
        layout="centered"
    )

    # --- Load Profiles ---
    profiles = load_profiles()

    # --- Header ---
    st.title("NutritionHouse AI Recommender")
    st.write("Discover the perfect vitamins for you. Answer a few questions to get started!")
    st.write("---")

    # --- User Status Selection ---
    user_status = st.radio("Are you a new or returning user?", ("New User", "Returning User"))

    phone_number_input = ""
    user_profile = {}

    if user_status == "Returning User":
        phone_number_input = st.text_input("Enter your phone number to load your profile:")
        if st.button("Load Profile"):
            if phone_number_input in profiles:
                st.session_state.user_profile = profiles[phone_number_input]
                st.success("Profile loaded successfully!")
            else:
                st.error("Profile not found. Please check the phone number or create a new profile.")
    
    if 'user_profile' in st.session_state:
        user_profile = st.session_state.user_profile
    else:
        user_profile = {
            "name": "", "age": "", "sex": "Male", "pregnant_or_breastfeeding": "Not Applicable",
            "medical_conditions": [], "current_medications": [], "allergies": [],
            "health_goals": [], "interested_supplements": []
        }


    # --- Form Questions ---
    with st.container(border=True):
        st.header("👤 Personal Information")
        
        if user_status == "New User":
            phone_number_input = st.text_input("Your Phone Number (to save and retrieve your profile)")
            name_input = st.text_input("Your Name", value=user_profile.get("name", ""))
        else:
            st.text_input("Phone Number", value=phone_number_input, disabled=True)
            name_input = st.text_input("Your Name", value=user_profile.get("name", ""), disabled=True)

        age_input = st.text_input("Your Age", value=str(user_profile.get("age", "")))
        st.write("") # Adds a little vertical space
        sex_options = ('Male', 'Female')
        sex = st.radio("Biological Sex", sex_options, index=sex_options.index(user_profile.get("sex", "Male")))

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
                "Are you pregnant or breastfeeding?",
                pob_options,
                index=pob_index
            )
        medical_conditions = st.text_area(
            "List any pre-existing medical conditions (comma-separated).",
            value=", ".join(user_profile.get("medical_conditions", [])),
            placeholder="e.g., High blood pressure, Asthma, Diabetes"
        )

    with st.container(border=True):
        st.header("💊 Medications & Allergies")
        current_medications = st.text_area(
            "List any current medications (comma-separated).",
            value=", ".join(user_profile.get("current_medications", [])),
            placeholder="e.g., Lisinopril, Metformin, Ibuprofen"
        )
        allergies = st.text_area(
            "List any known allergies (comma-separated).",
            value=", ".join(user_profile.get("allergies", [])),
            placeholder="e.g., Peanuts, Penicillin, Sulfa"
        )

    with st.container(border=True):
        st.header("🎯 Health Goals")
        health_goals_options = [
            "Improve Energy", "Boost Immunity", "Support Joint Health",
            "Enhance Sleep Quality", "Improve Digestive Health", "Support Heart Health",
            "Strengthen Bones", "Improve Mood & Focus"
        ]
        health_goals = st.multiselect(
            "What are your primary health goals?",
            health_goals_options,
            default=user_profile.get("health_goals", [])
        )
        interested_supplements = st.text_area(
            "Any specific vitamins you're interested in (comma-separated)?",
            value=", ".join(user_profile.get("interested_supplements", [])),
            placeholder="e.g., Vitamin D, Probiotics, Turmeric"
        )

    # --- Submission ---
    st.write("---")
    submitted = st.button("**Get My Recommendations**")

    if submitted:
        if not phone_number_input:
            st.error("Please enter your phone number to save or retrieve your profile.")
        elif not re.match(r"^\d+$", age_input) or not (1 <= int(age_input) <= 120):
            st.error("Please enter a valid age (a number between 1 and 120).")
        else:
            user_data = {
                "name": name_input,
                "age": int(age_input),
                "sex": sex,
                "pregnant_or_breastfeeding": pregnant_or_breastfeeding,
                "medical_conditions": [c.strip() for c in medical_conditions.split(',') if c.strip()],
                "current_medications": [m.strip() for m in current_medications.split(',') if m.strip()],
                "allergies": [a.strip() for a in allergies.split(',') if a.strip()],
                "health_goals": health_goals,
                "interested_supplements": [s.strip() for s in interested_supplements.split(',') if s.strip()]
            }
            
            # Save the profile using phone number as the key
            profiles[phone_number_input] = user_data
            save_profiles(profiles)

            st.success(f"Profile for {name_input} saved! We're analyzing your profile...")
            with st.spinner("Our AI engine is generating your personalized recommendations..."):
                recommendations = get_recommendations(user_data)
                st.markdown(recommendations)

if __name__ == "__main__":
    main()