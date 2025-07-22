import streamlit as st
import re
import json
import os
import datetime
import base64

def clear_form():
    st.session_state.user_profile = {}

# --- Helper Functions ---
def get_base64_of_bin_file(bin_file):
    """Reads a binary file and returns its base64 encoded string."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- Profile Management Functions ---
def load_profiles():
    """Loads user profiles from a Supabase database."""
    pass

def save_profiles(profiles):
    """Saves user profiles to a Supabase database."""
    pass

def main():
    """
    Main function to run the Streamlit application for Nutrition House.
    This app serves as the intake form and will display recommendations.
    """
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Nutrition House AI",
        page_icon="NH_favicon.png",
        layout="centered"
    )

    # --- Set Background Image ---
    background_image_b64 = get_base64_of_bin_file('background.png')
    if background_image_b64:
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{background_image_b64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)


    # --- Custom CSS for a more appealing design ---
    st.markdown("""
    <style>
        /* Background fallback */
        .stApp {
            background-color: #000000;
        }

        /* Title and Headers */
        .form-title-container h1 {
            color: #222f62;
            text-align: center;
            font-weight: bold;
            font-size: 2.5em;
        }
        h2, h3 {
            color: #222f62;
        }

        /* Main text color */
        p, label, .st-emotion-cache-16txtl3, .st-emotion-cache-10trblm, div[data-baseweb="radio"] > label {
            color: #212529 !important;
        }
        .form-title-container p {
            text-align: center;
        }

        /* Button Styling */
        .stButton>button {
            border: 2px solid #222f62;
            background-color: #5db2e1;
            color: #FFFFFF;
            border-radius: 10px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #222f62;
            color: #FFFFFF;
        }

        /* Input widgets */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 5px;
            color: #212529;
        }

        /* Container Styling */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Custom container for title/description */
        .form-title-container {
            background-color: #FFFFFF;
            border: 1px solid #DDDDDD;
            border-radius: 10px;
            padding: 15px 25px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)


    # --- Header ---
    with st.container(border=True):
        st.image("NH_logo.png", use_container_width=True)

    st.markdown("""
    <div class="form-title-container">
        <h1>Create Your Nutrition House Profile</h1>
        <p>Please fill out the form below to create your profile. Our AI-powered recommendation engine is currently in development and will soon provide personalized vitamin and supplement recommendations based on your individual needs.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # --- User Status Selection ---
    with st.container(border=True):
        st.radio(
            "Do you have a profile with Nutrition House?",
            ("No, I have not filled out the intake form before", "Yes, I have filled out the intake form before"),
            key='user_status',
            on_change=clear_form
        )
    user_status = st.session_state.get('user_status', "No, I have not filled out the intake form before")

    email_input = ""
    user_profile = {}
    profiles = {}

    if user_status == "Yes, I have filled out the intake form before":
        with st.container(border=True):
            email_input = st.text_input("Enter your email to load your profile:")
            if st.button("Load Profile"):
                profile = load_profile_from_db(email_input)
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
                    st.error("Profile not found. Please check the email or create a new profile.")

    if 'user_profile' in st.session_state:
        user_profile = st.session_state.user_profile
    else:
        user_profile = {
            "first_name": "", "last_name": "", "email": "", "dob": None, "sex": "Male", "height_m": "", "weight_kg": "",
            "physical_activity": "3-4 days", "energy_level": "Neutral", "diet": "I don't follow a specific diet",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "current_medications": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": ""
        }

    # --- Form Questions ---
    with st.container(border=True):
        st.header("👤 Personal Information")

        if user_status == "No, I have not filled out the intake form before":
            email_input = st.text_input("Your Email (to save and retrieve your profile)")
            col1, col2 = st.columns(2)
            with col1:
                first_name_input = st.text_input("First Name", value=user_profile.get("first_name", ""))
            with col2:
                last_name_input = st.text_input("Last Name", value=user_profile.get("last_name", ""))
        else: # Returning User
            email_input = user_profile.get("email", "") # Use loaded profile data
            st.text_input("Email", value=email_input, disabled=True)
            col1, col2 = st.columns(2)
            with col1:
                first_name_input = st.text_input("First Name", value=user_profile.get("first_name", ""), disabled=True)
            with col2:
                last_name_input = st.text_input("Last Name", value=user_profile.get("last_name", ""), disabled=True)

        st.write("Date of Birth")
        today = datetime.date.today()
        month_names = [datetime.date(2024, i, 1).strftime('%B') for i in range(1, 13)]

        # Load DOB from profile if it exists
        user_dob = user_profile.get("dob")
        if isinstance(user_dob, str):
            try:
                user_dob = datetime.datetime.strptime(user_dob, "%Y-%m-%d").date()
            except ValueError:
                user_dob = None # Handle invalid format
        
        initial_year = user_dob.year if user_dob else 1990
        initial_month_index = user_dob.month - 1 if user_dob else 0
        initial_day_index = user_dob.day - 1 if user_dob else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            month_name = st.selectbox("Month", month_names, index=initial_month_index)
            month = month_names.index(month_name) + 1
        with col2:
            day = st.selectbox("Day", list(range(1, 32)), index=initial_day_index)
        with col3:
            year = st.selectbox("Year", list(range(1920, today.year + 1)), index=list(range(1920, today.year + 1)).index(initial_year))

        try:
            dob = datetime.date(year, month, day)
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        except ValueError:
            st.error("Please enter a valid date of birth.")
            age = 0
            dob = None

        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.selectbox("Height (ft)", list(range(4, 7)), 1)
        with col2:
            height_in = st.selectbox("Height (in)", list(range(0, 12)), 6)

        weight_input = st.text_input("Your Weight (in lbs)", value=str(user_profile.get("weight_lbs", "")))
        st.write("") # Adds a little vertical space
        sex_options = ('Male', 'Female')
        sex = st.radio("Biological Sex", sex_options, index=sex_options.index(user_profile.get("sex", "Male")))

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
                "Are you currently pregnant or breastfeeding?",
                pob_options,
                index=pob_index
            )
        medical_conditions = st.text_area(
            "Please list any pre-existing medical conditions.",
            value=", ".join(user_profile.get("medical_conditions", [])),
            placeholder="e.g., High blood pressure, Asthma, Diabetes. Please separate each condition with a comma."
        )

    with st.container(border=True):
        st.header("💊 Medications & Allergies")
        medications = st.text_area(
            "Please list any Over-the-Counter (OTC) or prescribed medications you are currently taking.",
            value=", ".join(user_profile.get("medications", [])),
            placeholder="e.g., Ibuprofen, Aspirin, Atorvastatin, Amlodipine, Metformin. Please separate each with a comma."
        )
        natural_supplements = st.text_area(
            "Please list any natural supplements you are currently taking.",
            value=", ".join(user_profile.get("natural_supplements", [])),
            placeholder="e.g., Melatonin, St. John's Wort, Fish Oil. Please separate each with a comma."
        )
        allergies = st.text_area(
            "Please list any known allergies.",
            value=", ".join(user_profile.get("allergies", [])),
            placeholder="e.g., Peanuts, Penicillin, Sulfa. Please separate each with a comma."
        )

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

    with st.container(border=True):
        st.header("📝 Additional Information")
        additional_info = st.text_area(
            "Is there anything else you would like to share that might be relevant to your health?",
            value=user_profile.get("additional_info", ""),
            placeholder="e.g., Previous sports injuries, aches, pains, depression, anxiety, etc."
        )

    # --- Submission ---
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.button("**Create My Profile**", use_container_width=True)
    with col2:
        st.button("Clear Form", on_click=clear_form, use_container_width=True)

    if submitted:
        if not email_input:
            st.error("Please enter your email to save or retrieve your profile.")
        else:
            # Convert imperial height to metric
            height_m = (height_ft * 12 + height_in) * 0.0254

            # Convert weight from lbs to kg
            try:
                weight_kg = float(weight_input) * 0.453592
            except ValueError:
                weight_kg = 0 # Or handle error appropriately

            user_data = {
                "first_name": first_name_input,
                "last_name": last_name_input,
                "email": email_input,
                "dob": dob.isoformat() if dob else None,
                "sex": sex,
                "height_m": height_m,
                "weight_kg": weight_kg,
                "physical_activity": physical_activity,
                "energy_level": energy_level,
                "diet": diet,
                "meals_per_day": meals_per_day,
                "sleep_quality": sleep_quality,
                "stress_level": stress_level,
                "pregnant_or_breastfeeding": pregnant_or_breastfeeding,
                "medical_conditions": [c.strip() for c in medical_conditions.split(',') if c.strip()],
                "current_medications": [m.strip() for m in medications.split(',') if m.strip()],
                "natural_supplements": [ns.strip() for ns in natural_supplements.split(',') if ns.strip()],
                "allergies": [a.strip() for a in allergies.split(',') if a.strip()],
                "health_goals": health_goals,
                "other_health_goal": other_health_goal,
                "interested_supplements": [s.strip() for s in interested_supplements.split(',') if s.strip()],
                "additional_info": additional_info
            }
            
            # Save the profile using email as the key
            profiles[email_input] = user_data
            save_profiles(profiles)

            st.success(f"Profile for {first_name_input} {last_name_input} saved! We're analyzing your profile...")
            
if __name__ == "__main__":
    main()