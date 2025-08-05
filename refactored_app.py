import streamlit as st
import datetime
import json
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

    email_input = ""
    profiles = {}

    # --- Profile State Management ---
    # Ensure user_profile is initialized in session_state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            "first_name": "", "last_name": "", "email": "", "phone_number": "", "dob": None, "sex": "Male", "height_m": "", "weight_kg": "",
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
            email_input = st.text_input("Enter your email to load your profile:", key="load_email")
            # Replace the profile loading section in your refactored_app.py with this:

            if st.button("Load Profile", key="load_profile"):
                profile = load_profile_from_db(supabase, email_input)
                if profile:
                    # Clear existing form state before loading new profile
                    clear_form()
                    
                    # Helper function to clean list-like data from the database
                    def clean_profile_list_field(data, as_list=False):
                        """
                        Clean and format profile list fields from database.
                        Returns either a list or comma-separated string based on as_list parameter.
                        """
                        if not data:
                            return [] if as_list else ""

                        # Handle string data that might be JSON
                        if isinstance(data, str):
                            # Try to parse JSON if it looks like a list
                            if data.strip().startswith('[') and data.strip().endswith(']'):
                                try:
                                    data = json.loads(data)
                                except (json.JSONDecodeError, TypeError):
                                    # If JSON parsing fails, treat as comma-separated string
                                    data = [item.strip() for item in data.split(',') if item.strip()]
                            else:
                                # Treat as comma-separated string
                                data = [item.strip() for item in data.split(',') if item.strip()]

                        # Handle list data
                        if isinstance(data, list):
                            cleaned_items = []
                            for item in data:
                                if isinstance(item, str):
                                    # Remove any quotes and extra whitespace
                                    clean_item = item.strip().strip('"').strip("'").strip()
                                    if clean_item:
                                        cleaned_items.append(clean_item)
                                else:
                                    # Convert non-string items to string
                                    clean_item = str(item).strip()
                                    if clean_item:
                                        cleaned_items.append(clean_item)
                            
                            if as_list:
                                return cleaned_items
                            else:
                                return ", ".join(cleaned_items)

                        # Handle single values
                        clean_data = str(data).strip().strip('"').strip("'").strip()
                        if as_list:
                            return [clean_data] if clean_data else []
                        else:
                            return clean_data

                    # --- Populate session_state directly for form widgets ---
                    
                    # Personal Info
                    st.session_state.email = str(profile.get("email", ""))
                    st.session_state.first_name = str(profile.get("first_name", ""))
                    st.session_state.last_name = str(profile.get("last_name", ""))
                    st.session_state.phone_number = str(profile.get("phone_number", ""))
                    
                    user_dob = profile.get("dob")
                    if isinstance(user_dob, str):
                        try:
                            user_dob = datetime.datetime.strptime(user_dob, "%Y-%m-%d").date()
                            st.session_state.dob_year = user_dob.year
                            st.session_state.dob_month = datetime.date(2024, user_dob.month, 1).strftime('%B')
                            st.session_state.dob_day = user_dob.day
                        except ValueError:
                            pass
                    
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

                    # Lifestyle
                    st.session_state.physical_activity = str(profile.get("physical_activity", "3-4 days"))
                    st.session_state.energy_level = str(profile.get("energy_level", "Neutral"))
                    st.session_state.diet = str(profile.get("diet", "I don't follow a specific diet"))
                    st.session_state.meals_per_day = str(profile.get("meals_per_day", "3"))
                    st.session_state.sleep_quality = str(profile.get("sleep_quality", "Good"))
                    st.session_state.stress_level = str(profile.get("stress_level", "Moderate"))

                    # Medical History - ENSURE STRINGS FOR TEXT WIDGETS
                    st.session_state.pregnant_or_breastfeeding = str(profile.get("pregnant_or_breastfeeding", "Not Applicable"))
                    
                    # Clean and ensure string format for text areas
                    medical_conditions_raw = profile.get("medical_conditions")
                    medical_conditions_cleaned = clean_profile_list_field(medical_conditions_raw, as_list=False)
                    st.session_state.medical_conditions = str(medical_conditions_cleaned) if medical_conditions_cleaned else ""

                    # Medications & Allergies - ENSURE STRINGS FOR TEXT WIDGETS
                    medications_raw = profile.get("current_medications")
                    medications_cleaned = clean_profile_list_field(medications_raw, as_list=False)
                    st.session_state.medications = str(medications_cleaned) if medications_cleaned else ""
                    
                    natural_supplements_raw = profile.get("natural_supplements")
                    natural_supplements_cleaned = clean_profile_list_field(natural_supplements_raw, as_list=False)
                    st.session_state.natural_supplements = str(natural_supplements_cleaned) if natural_supplements_cleaned else ""
                    
                    allergies_raw = profile.get("allergies")
                    allergies_cleaned = clean_profile_list_field(allergies_raw, as_list=False)
                    st.session_state.allergies = str(allergies_cleaned) if allergies_cleaned else ""

                    # Health Goals - KEEP AS LIST FOR MULTISELECT
                    health_goals_raw = profile.get("health_goals")
                    st.session_state.health_goals = clean_profile_list_field(health_goals_raw, as_list=True)
                    
                    st.session_state.other_health_goal = str(profile.get("other_health_goal", ""))
                    
                    interested_supplements_raw = profile.get("interested_supplements")
                    interested_supplements_cleaned = clean_profile_list_field(interested_supplements_raw, as_list=False)
                    st.session_state.interested_supplements = str(interested_supplements_cleaned) if interested_supplements_cleaned else ""

                    # Additional Info - ENSURE STRING FOR TEXT AREA
                    additional_info_raw = profile.get("additional_info", "")
                    st.session_state.additional_info = str(additional_info_raw) if additional_info_raw else ""
                    
                    # Also update the user_profile object for consistency
                    st.session_state.user_profile = profile
                    
                    st.success("Profile loaded successfully!")
                    st.rerun()
                else:
                    st.error("Profile not found. Please check the email or create a new profile.")

    # --- Form Questions ---
    personal_info = personal_info_form(user_profile, user_status, errors)
    lifestyle = lifestyle_form(user_profile, errors)
    medical_history = medical_history_form(user_profile, personal_info["sex"], errors)
    medications_allergies = medications_allergies_form(user_profile, errors)
    health_goals = health_goals_form(user_profile, errors)
    additional_info = additional_info_form(user_profile, errors)

    # --- Submission ---
    st.write("---")

    # Determine button text based on user status
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
            # Convert imperial height to metric
            height_m = (personal_info["height_ft"] * 12 + personal_info["height_in"]) * 0.0254

            # Convert weight from lbs to kg
            try:
                weight_kg = float(personal_info["weight_lbs"]) * 0.453592
            except (ValueError, TypeError):
                weight_kg = 0 # Or handle error appropriately

            user_data = {
                "first_name": personal_info["first_name"],
                "last_name": personal_info["last_name"],
                "email": personal_info["email"],
                "phone_number": personal_info["phone_number"],
                "dob": personal_info["dob"].isoformat() if personal_info["dob"] else None,
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

            st.success(f"Profile for {personal_info['first_name']} {personal_info['last_name']} saved! We're analyzing your profile...")
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
