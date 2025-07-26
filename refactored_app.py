import streamlit as st
import datetime
from src.utils.file_utils import get_base64_of_bin_file
from src.utils.session_utils import clear_form
from src.view.personal_info import personal_info_form
from src.view.lifestyle import lifestyle_form
from src.view.medical_history import medical_history_form
from src.view.medications_allergies import medications_allergies_form
from src.view.health_goals import health_goals_form
from src.view.additional_info import additional_info_form

def main():
    """
    Main function to run the Streamlit application for Nutrition House.
    This app serves as the intake form and will display recommendations.
    """
    # --- Page Configuration ---
    st.set_page_config(
        page_title="Nutrition House AI",
        page_icon="assets/NH_favicon.png",
        layout="centered"
    )

    # --- Set Background Image ---
    background_image_b64 = get_base64_of_bin_file('assets/background.png')
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
        st.image("assets/NH_logo.png", use_container_width=True)

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
    profiles = {}

    # --- Profile State Management ---
    # Ensure user_profile is initialized in session_state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            "first_name": "", "last_name": "", "email": "", "dob": None, "sex": "Male", "height_m": "", "weight_kg": "",
            "physical_activity": "3-4 days", "energy_level": "Neutral", "diet": "I don't follow a specific diet",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "current_medications": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": ""
        }
    user_profile = st.session_state.user_profile

    if user_status == "Yes, I have filled out the intake form before":
        with st.container(border=True):
            email_input = st.text_input("Enter your email to load your profile:", key="load_email")
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


    # --- Form Questions ---
    personal_info = personal_info_form(user_profile, user_status)
    lifestyle = lifestyle_form(user_profile)
    medical_history = medical_history_form(user_profile, personal_info["sex"])
    medications_allergies = medications_allergies_form(user_profile)
    health_goals = health_goals_form(user_profile)
    additional_info = additional_info_form(user_profile)

    # --- Submission ---
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.button("**Create My Profile**", use_container_width=True)
    with col2:
        st.button("Clear Form", on_click=clear_form, use_container_width=True)

    if submitted:
        if not personal_info["email"]:
            st.error("Please enter your email to save or retrieve your profile.")
        else:
            # Convert imperial height to metric
            height_m = (personal_info["height_ft"] * 12 + personal_info["height_in"]) * 0.0254

            # Convert weight from lbs to kg
            try:
                weight_kg = float(personal_info["weight_lbs"]) * 0.453592
            except ValueError:
                weight_kg = 0 # Or handle error appropriately

            user_data = {
                "first_name": personal_info["first_name"],
                "last_name": personal_info["last_name"],
                "email": personal_info["email"],
                "dob": personal_info["dob"].isoformat() if personal_info["dob"] else None,
                "sex": personal_info["sex"],
                "height_m": height_m,
                "weight_kg": weight_kg,
                "physical_activity": lifestyle["physical_activity"],
                "energy_level": lifestyle["energy_level"],
                "diet": lifestyle["diet"],
                "meals_per_day": lifestyle["meals_per_day"],
                "sleep_quality": lifestyle["sleep_quality"],
                "stress_level": lifestyle["stress_level"],
                "pregnant_or_breastfeeding": medical_history["pregnant_or_breastfeeding"],
                "medical_conditions": [c.strip() for c in medical_history["medical_conditions"].split(',') if c.strip()],
                "current_medications": [m.strip() for m in medications_allergies["medications"].split(',') if m.strip()],
                "natural_supplements": [ns.strip() for ns in medications_allergies["natural_supplements"].split(',') if ns.strip()],
                "allergies": [a.strip() for a in medications_allergies["allergies"].split(',') if a.strip()],
                "health_goals": health_goals["health_goals"],
                "other_health_goal": health_goals["other_health_goal"],
                "interested_supplements": [s.strip() for s in health_goals["interested_supplements"].split(',') if s.strip()],
                "additional_info": additional_info["additional_info"]
            }
            
            # Save the profile using email as the key
            profiles[personal_info["email"]] = user_data
            # save_profiles(profiles)

            st.success(f"Profile for {personal_info['first_name']} {personal_info['last_name']} saved! We're analyzing your profile...")
            
if __name__ == "__main__":
    main()
