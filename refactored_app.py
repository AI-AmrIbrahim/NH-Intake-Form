import streamlit as st
import datetime
import json
import uuid
import random
import string
from src.utils.file_utils import get_base64_of_bin_file
from src.utils.session_utils import clear_form
from src.utils.style_utils import inject_css
from src.view.personal_info import personal_info_form
from src.view.lifestyle import lifestyle_form
from src.view.medical_history import medical_history_form
from src.view.medications_allergies import medications_allergies_form
from src.view.health_goals import health_goals_form
from src.view.additional_info import additional_info_form
from src.utils.db_utils import init_connection, save_profile, load_profile_from_db
from src.models.user_profile import UserProfile
from pydantic import ValidationError

supabase = init_connection()

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


    # --- Custom CSS ---
    inject_css('src/style/style.css')


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

    # --- Profile State Management ---
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            "user_id": "", "age_range": "18-24", "sex": "Male", "height_m": "", "weight_kg": "",
            "physical_activity": "3-4 days", "energy_level": "Neutral", "diet": "I don't follow a specific diet",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "current_medications": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": ""
        }
    if 'errors' not in st.session_state:
        st.session_state.errors = {}

    user_profile = st.session_state.user_profile
    errors = st.session_state.errors

    if user_status == "Yes, I have filled out the intake form before":
        with st.container(border=True):
            user_id_input = st.text_input("Enter your Unique ID to load your profile:", key="load_user_id")
            if st.button("Load Profile", key="load_profile"):
                with st.spinner("Loading your profile..."):
                    profile = load_profile_from_db(supabase, user_id_input)
                    if profile:
                        clear_form()
                        def clean_profile_list_field(data, as_list=False):
                            if not data:
                                return [] if as_list else ""
                            if isinstance(data, str):
                                if data.strip().startswith('[') and data.strip().endswith(']'):
                                    try:
                                        data = json.loads(data)
                                    except (json.JSONDecodeError, TypeError):
                                        data = [item.strip() for item in data.split(',') if item.strip()]
                                else:
                                    data = [item.strip() for item in data.split(',') if item.strip()]
                            if isinstance(data, list):
                                cleaned_items = []
                                for item in data:
                                    if isinstance(item, str):
                                        clean_item = item.strip().strip('"').strip("'").strip()
                                        if clean_item:
                                            cleaned_items.append(clean_item)
                                    else:
                                        clean_item = str(item).strip()
                                        if clean_item:
                                            cleaned_items.append(clean_item)
                                if as_list:
                                    return cleaned_items
                                else:
                                    return ", ".join(cleaned_items)
                            clean_data = str(data).strip().strip('"').strip("'").strip()
                            if as_list:
                                return [clean_data] if clean_data else []
                            else:
                                return clean_data

                        st.session_state.age_range = str(profile.get("age_range", "18-24"))
                        st.session_state.sex = str(profile.get("sex", "Male"))
                        if profile.get("height_m"):
                            try:
                                total_inches = float(profile["height_m"]) * 39.3701
                                st.session_state.height_ft = int(total_inches // 12)
                                st.session_state.height_in = int(total_inches % 12)
                            except (ValueError, TypeError):
                                pass
                        if profile.get("weight_kg"):
                            try:
                                st.session_state.weight_lbs = str(round(float(profile["weight_kg"]) * 2.20462, 2))
                            except (ValueError, TypeError):
                                pass
                        st.session_state.physical_activity = str(profile.get("physical_activity", "3-4 days"))
                        st.session_state.energy_level = str(profile.get("energy_level", "Neutral"))
                        st.session_state.diet = str(profile.get("diet", "I don't follow a specific diet"))
                        st.session_state.meals_per_day = str(profile.get("meals_per_day", "3"))
                        st.session_state.sleep_quality = str(profile.get("sleep_quality", "Good"))
                        st.session_state.stress_level = str(profile.get("stress_level", "Moderate"))
                        st.session_state.pregnant_or_breastfeeding = str(profile.get("pregnant_or_breastfeeding", "Not Applicable"))
                        medical_conditions_raw = profile.get("medical_conditions")
                        medical_conditions_cleaned = clean_profile_list_field(medical_conditions_raw, as_list=False)
                        st.session_state.medical_conditions = str(medical_conditions_cleaned) if medical_conditions_cleaned else ""
                        medications_raw = profile.get("current_medications")
                        medications_cleaned = clean_profile_list_field(medications_raw, as_list=False)
                        st.session_state.medications = str(medications_cleaned) if medications_cleaned else ""
                        natural_supplements_raw = profile.get("natural_supplements")
                        natural_supplements_cleaned = clean_profile_list_field(natural_supplements_raw, as_list=False)
                        st.session_state.natural_supplements = str(natural_supplements_cleaned) if natural_supplements_cleaned else ""
                        allergies_raw = profile.get("allergies")
                        allergies_cleaned = clean_profile_list_field(allergies_raw, as_list=False)
                        st.session_state.allergies = str(allergies_cleaned) if allergies_cleaned else ""
                        health_goals_raw = profile.get("health_goals")
                        st.session_state.health_goals = clean_profile_list_field(health_goals_raw, as_list=True)
                        st.session_state.other_health_goal = str(profile.get("other_health_goal", ""))
                        interested_supplements_raw = profile.get("interested_supplements")
                        interested_supplements_cleaned = clean_profile_list_field(interested_supplements_raw, as_list=False)
                        st.session_state.interested_supplements = str(interested_supplements_cleaned) if interested_supplements_cleaned else ""
                        st.session_state.additional_info = str(profile.get("additional_info", ""))
                        st.session_state.user_profile = profile
                        st.success("Profile loaded successfully!")
                        st.rerun()
                    else:
                        st.error("Profile not found. Please check the Unique ID or create a new profile.")

    # --- Form Questions ---
    personal_info = personal_info_form(user_profile, errors)
    lifestyle = lifestyle_form(user_profile, errors)
    medical_history = medical_history_form(user_profile, personal_info["sex"], errors)
    medications_allergies = medications_allergies_form(user_profile, errors)
    health_goals = health_goals_form(user_profile, errors)
    additional_info = additional_info_form(user_profile, errors)

    # --- Submission ---
    st.write("---")

    if user_status == "Yes, I have filled out the intake form before":
        submit_button_text = "**Update My Profile**"
    else:
        submit_button_text = "**Create My Profile**"

    col1, col2 = st.columns(2)
    with col1:
        submitted = st.button(submit_button_text, use_container_width=True, key="create_profile")
    with col2:
        st.button("Clear Form", on_click=clear_form, use_container_width=True, key="clear_form")

    if submitted:
        st.session_state.errors = {}
        try:
            with st.spinner("Creating Your Profile, please wait to get your profile code..."):
                height_m = (personal_info["height_ft"] * 12 + personal_info["height_in"]) * 0.0254
                try:
                    weight_kg = float(personal_info["weight_lbs"]) * 0.453592
                except (ValueError, TypeError):
                    weight_kg = 0

                chat_set = string.ascii_letters + string.digits
                user_id_raw = ''.join(random.choices(chat_set, k=9))
                user_id_formatted = f"{user_id_raw[:3]}-{user_id_raw[3:6]}-{user_id_raw[6:]}"
                user_data = {
                    "user_id": user_id_formatted,
                    "age_range": personal_info["age_range"],
                    "sex": personal_info["sex"],
                    "height_ft": personal_info["height_ft"],
                    "height_in": personal_info["height_in"],
                    "weight_lbs": personal_info["weight_lbs"],
                    "physical_activity": lifestyle["physical_activity"],
                    "energy_level": lifestyle["energy_level"],
                    "diet": lifestyle["diet"],
                    "meals_per_day": lifestyle["meals_per_day"],
                    "sleep_quality": lifestyle["sleep_quality"],
                    "stress_level": lifestyle["stress_level"],
                    "pregnant_or_breastfeeding": medical_history["pregnant_or_breastfeeding"],
                    "medical_conditions": [s.strip() for s in medical_history["medical_conditions"].split(',') if s.strip()],
                    "current_medications": [s.strip() for s in medications_allergies["medications"].split(',') if s.strip()],
                    "natural_supplements": [s.strip() for s in medications_allergies["natural_supplements"].split(',') if s.strip()],
                    "allergies": [s.strip() for s in medications_allergies["allergies"].split(',') if s.strip()],
                    "health_goals": health_goals["health_goals"],
                    "other_health_goal": health_goals["other_health_goal"],
                    "interested_supplements": [s.strip() for s in health_goals["interested_supplements"].split(',') if s.strip()],
                    "additional_info": additional_info["additional_info"]
                }
                
                user_profile = UserProfile(**user_data)
                save_profile(supabase, user_profile.dict())

                with st.container(border=True):
                    st.subheader("Your Nutrition House Profile Code")
                    st.success(f"Profile created successfully! Your Profile Code is: {user_id_formatted}")
                    st.info("Please save this code in a safe space to load your profile for future visits.")
                st.session_state.errors = {}

        except ValidationError as e:
            st.session_state.errors = {err['loc'][0]: err['msg'] for err in e.errors()}
            st.rerun()

    if errors:
        st.components.v1.html(
            """
            <script>
            const errorElements = window.parent.document.querySelectorAll('.st-emotion-cache-1vzeuhh');
            if (errorElements.length > 0) {
                errorElements[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
            </script>
            """,
            height=0
        )

if __name__ == "__main__":
    main()
