import streamlit as st
import re
import json
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# --- Supabase Initialization ---
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- Database Functions ---
def load_profile_from_db(phone_number):
    """Loads the most recent user profile from the database."""
    response = supabase.table('user_medical_profiles').select("*").eq('phone_number', phone_number).order('created_at', desc=True).limit(1).execute()
    if response.data:
        profile = response.data[0]
        if isinstance(profile.get('health_goals'), str):
            try:
                profile['health_goals'] = json.loads(profile['health_goals'])
            except json.JSONDecodeError:
                profile['health_goals'] = []
        return profile
    return None

def save_profile_to_db(user_data):
    """Saves a new user profile entry to the database."""
    supabase.table('user_medical_profiles').insert(user_data).execute()


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

    # This part is commented out as it requires a valid API key.
    # import google.generativeai as genai
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(prompt)
    # return response.text
    return "Recommendations will be generated here."


def clear_form(full_clear=False):
    if full_clear or st.session_state.get('user_status') == "New User":
        st.session_state.user_profile = {}
    else: # Partial clear for returning user
        profile = st.session_state.get('user_profile', {})
        st.session_state.user_profile = {
            "name": profile.get("name"),
            "phone_number": profile.get("phone_number")
        }


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

    # --- Header ---
    st.title("NutritionHouse AI Recommender")
    st.write("Discover the perfect vitamins for you. Answer a few questions to get started!")
    st.write("---")

    # --- User Status Selection ---
    st.radio(
        "Are you a new or returning user?",
        ("New User", "Returning User"),
        key='user_status',
        on_change=clear_form, args=(True,)
    )
    user_status = st.session_state.get('user_status', "New User")

    phone_number_input = ""
    user_profile = {}

    if user_status == "Returning User":
        phone_number_input = st.text_input("Enter your phone number to load your profile:")
        if st.button("Load Profile"):
            profile = load_profile_from_db(phone_number_input)
            if profile:
                # Convert metric height/weight from DB to imperial for display
                if profile.get("height_m"):
                    total_inches = profile["height_m"] * 39.3701
                    profile["height_ft"] = int(total_inches // 12)
                    profile["height_in"] = int(total_inches % 12)
                if profile.get("weight_kg"):
                    profile["weight_lbs"] = round(profile["weight_kg"] * 2.20462, 2)

                st.session_state.user_profile = profile
                st.success("Profile loaded successfully!")
            else:
                st.error("Profile not found. Please check the phone number or create a new profile.")

    if 'user_profile' in st.session_state:
        user_profile = st.session_state.user_profile
    else:
        user_profile = {
            "name": "", "age": "", "sex": "Male", "height_m": "", "weight_kg": "",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "current_medications": [], "allergies": [], "health_goals": [],
            "interested_supplements": []
        }

    # --- Form Questions ---
    with st.container(border=True):
        st.header("👤 Personal Information")

        if user_status == "New User":
            phone_number_input = st.text_input("Your Phone Number (to save and retrieve your profile)")
            name_input = st.text_input("Your Name", value=user_profile.get("name", ""))
        else: # Returning User
            phone_number_input = user_profile.get("phone_number", "") # Use loaded profile data
            st.text_input("Phone Number", value=phone_number_input, disabled=True)
            name_input = st.text_input("Your Name", value=user_profile.get("name", ""), disabled=True)

        age_input = st.text_input("Your Age", value=str(user_profile.get("age", "")))
        st.write("Your Height")
        col1, col2 = st.columns(2)
        with col1:
            feet_input = st.text_input("Feet", value=str(user_profile.get("height_ft", "")))
        with col2:
            inches_input = st.text_input("Inches", value=str(user_profile.get("height_in", "")))
        weight_input = st.text_input("Your Weight (in lbs)", value=str(user_profile.get("weight_lbs", "")))
        st.write("") # Adds a little vertical space
        sex_options = ('Male', 'Female')
        sex = st.radio("Biological Sex", sex_options, index=sex_options.index(user_profile.get("sex", "Male")))

    with st.container(border=True):
        st.header("⚕️ Medical History")
        pregnant_or_breastfeeding = "Not Applicable"
        if sex == 'Female':
            pob_options = ('No', 'Yes')
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
    col1, col2 = st.columns([1, 0.3])
    with col1:
        submitted = st.button("**Get My Recommendations**", use_container_width=True)
    with col2:
        st.button("Clear Form", on_click=clear_form, use_container_width=True)

    if submitted:
        if not phone_number_input:
            st.error("Please enter your phone number to save or retrieve your profile.")
        elif not re.match(r"^\d+$", age_input) or not (1 <= int(age_input) <= 120):
            st.error("Please enter a valid age (a number between 1 and 120).")
        else:
            try:
                feet = int(feet_input)
                inches = int(inches_input)
                weight_lbs = float(weight_input)

                # Convert to metric
                height_m = (feet * 12 + inches) * 0.0254
                weight_kg = weight_lbs * 0.453592
                bmi = round(weight_kg / (height_m ** 2), 2) if height_m > 0 else 0
            except (ValueError, ZeroDivisionError):
                st.error("Please enter valid numbers for height and weight.")
                st.stop()


            user_data = {
                "phone_number": phone_number_input,
                "name": name_input,
                "age": int(age_input),
                "sex": sex,
                "height_m": height_m,
                "weight_kg": weight_kg,
                "bmi": bmi,
                "pregnant_or_breastfeeding": pregnant_or_breastfeeding,
                "medical_conditions": [c.strip() for c in medical_conditions.split(',') if c.strip()],
                "current_medications": [m.strip() for m in current_medications.split(',') if m.strip()],
                "allergies": [a.strip() for a in allergies.split(',') if a.strip()],
                "health_goals": health_goals,
                "interested_supplements": [s.strip() for s in interested_supplements.split(',') if s.strip()]
            }

            save_profile_to_db(user_data)

            st.success(f"Profile for {name_input} saved! We're analyzing your profile...")
            with st.spinner("Our AI engine is generating your personalized recommendations..."):
                recommendations = get_recommendations(user_data)
                st.markdown(recommendations)

if __name__ == "__main__":
    main()