import streamlit as st
import datetime
import json
import uuid
import random
import string
from streamlit_extras.stylable_container import stylable_container
from src.utils.file_utils import get_base64_of_bin_file
from src.utils.session_utils import clear_form
from src.utils.style_utils import inject_css, display_message
from src.view.personal_info import personal_info_form
from src.view.lifestyle import lifestyle_form
from src.view.medical_history import medical_history_form
from src.view.medications_allergies import medications_allergies_form
from src.view.health_goals import health_goals_form
from src.view.additional_info import additional_info_form
from src.view.security_questions import security_questions_form
from src.utils.db_utils import init_connection, save_profile, load_profile_from_db, load_profile_by_security_questions
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
    with stylable_container(key="header_container", css_styles='''
    {
        display: flex;
        justify-content: center;
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    '''):
        st.image("assets/NH_logo.png")

    st.markdown("""
    <div class="form-title-container">
        <h1>Create Your Nutrition House Profile</h1>
        <p>Please fill out the form below to create your profile. Our AI-powered recommendation engine is currently in development and will soon provide personalized vitamin and supplement recommendations based on your individual needs.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # --- User Status Selection ---
    with stylable_container(key="user_status_container", css_styles='''
    {
        background-color: #FFFFFF;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    '''):
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
            "user_id": "", "age_range": "18-24", "sex": "Male", "height_ft": 5, "height_in": 6, "weight_lbs": "",
            "physical_activity": "3-4 days", "energy_level": "Neutral", "diet": "I don't follow a specific diet",
            "pregnant_or_breastfeeding": "Not Applicable", "medical_conditions": [],
            "medications": [], "natural_supplements": [], "allergies": [], "health_goals": [], "other_health_goal": "",
            "interested_supplements": [], "additional_info": "",
            "security_question_1": "", "security_answer_1": "",
            "security_question_2": "", "security_answer_2": "",
            "security_question_3": "", "security_answer_3": ""
        }
    if 'errors' not in st.session_state:
        st.session_state.errors = {}
    if 'recovery_mode' not in st.session_state:
        st.session_state.recovery_mode = False

    if user_status == "Yes, I have filled out the intake form before":
        with stylable_container(key="load_profile_container", css_styles='''
        {
            background-color: #FFFFFF;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        '''):
            if st.session_state.recovery_mode:
                st.header("Recover Your Profile Code")
                security_questions_recovery = security_questions_form(st.session_state.user_profile, st.session_state.errors)
                if st.button("Recover My Code", key="recover_code"):
                    with st.spinner("Recovering your profile code..."):
                        profile = load_profile_by_security_questions(supabase, security_questions_recovery)
                        if profile:
                            with stylable_container(key="profile_code_container", css_styles='''
                            {
                                background-color: #FFFFFF;
                                border-radius: 0.5rem;
                                padding: 1rem;
                            }
                            '''):
                                st.subheader("Your Nutrition House Profile Code")
                                st.success(f"Your Profile Code is: {profile['user_id']}")
                                st.info("Please save this code in a safe space to load your profile for future visits.")
                        else:
                            st.error("Profile not found. Please check your security questions and answers.")
                if st.button("Back to Load Profile", key="back_to_load"):
                    st.session_state.recovery_mode = False
                    st.rerun()
            else:
                user_id_input = st.text_input("Enter your Unique ID to load your profile:", key="load_user_id")
                st.write("")
                if st.button("Load Profile", key="load_profile"):
                    with st.spinner("Loading your profile..."):
                        profile = load_profile_from_db(supabase, user_id_input)
                        if profile:
                            st.session_state.user_profile = profile
                            st.success("Profile loaded successfully!")
                            st.rerun()
                        else:
                            st.error("Profile not found. Please check the Unique ID or create a new profile.")
                if st.button("Forgot your profile code?", key="forgot_code"):
                    st.session_state.recovery_mode = True
                    st.rerun()

    user_profile = st.session_state.user_profile
    errors = st.session_state.errors

    # --- Form Questions --
    personal_info = personal_info_form(user_profile, errors)
    lifestyle = lifestyle_form(user_profile, errors)
    medical_history = medical_history_form(user_profile, personal_info["sex"], errors)
    medications_allergies = medications_allergies_form(user_profile, errors)
    health_goals = health_goals_form(user_profile, errors)
    if user_status == "No, I have not filled out the intake form before":
        security_questions = security_questions_form(user_profile, errors)
    additional_info = additional_info_form(user_profile, errors)

    if user_status == "Yes, I have filled out the intake form before":
        with stylable_container(key="upload_container", css_styles='''
        {
            background-color: #FFFFFF;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        '''):
            st.header("Upload Test Kit Result")

            # Check if user has loaded their profile
            if not st.session_state.user_profile.get("user_id"):
                st.warning("⚠️ Please enter your Profile Code above and load your profile before uploading test kit results.")
                st.file_uploader("Upload your PDF test kit result", type="pdf", disabled=True)
            else:
                uploaded_file = st.file_uploader("Upload your PDF test kit result", type="pdf")
                if uploaded_file is not None:
                    if st.button("Upload and Save PDF"):
                        with st.spinner("Uploading your file..."):
                            # Generate a unique file name with user's original filename
                            original_name = uploaded_file.name.replace('.pdf', '').replace(' ', '_')
                            file_name = f"{st.session_state.user_profile['user_id']}_{original_name}_{uuid.uuid4().hex[:8]}.pdf"

                            # Upload the file to Supabase Storage
                            try:
                                # The bucket must exist.
                                supabase.storage.from_("test-kit-results").upload(file_name, uploaded_file.getvalue())

                                # Get the public URL
                                file_url = supabase.storage.from_("test-kit-results").get_public_url(file_name)

                                # Update the user's profile
                                update_data = {
                                    "test_kit_result_url": file_url,
                                    "test_kit_result_filename": uploaded_file.name
                                }
                                save_profile(supabase, {"user_id": st.session_state.user_profile['user_id'], **update_data})

                                st.success("File uploaded and profile updated successfully!")
                            except Exception as e:
                                st.error(f"An error occurred during file upload: {e}")

    # --- Submission ---
    st.write("---")

    if user_status == "No, I have not filled out the intake form before":
        submit_button_text = "**Create My Profile**"
    else:
        submit_button_text = "**Update My Profile**"

    col1, col2 = st.columns(2)
    with col1:
        submitted = st.button(submit_button_text, use_container_width=True, key="create_profile")
    with col2:
        st.button("Clear Form", on_click=clear_form, use_container_width=True, key="clear_form")

    if submitted:
        st.session_state.errors = {}
        try:
            if user_status == "No, I have not filled out the intake form before":
                with stylable_container(key="create_profile_container", css_styles='''
                {
                    background-color: #FFFFFF;
                    border-radius: 0.5rem;
                    padding: 1rem;
                }
                '''):
                    with st.spinner("Creating Your Profile, please wait to get your profile code..."):
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
                            "current_medications": [s.strip() for s in medications_allergies["current_medications"].split(',') if s.strip()],
                            "natural_supplements": [s.strip() for s in medications_allergies["natural_supplements"].split(',') if s.strip()],
                            "allergies": [s.strip() for s in medications_allergies["allergies"].split(',') if s.strip()],
                            "health_goals": health_goals["health_goals"],
                            "other_health_goal": health_goals["other_health_goal"],
                            "interested_supplements": [s.strip() for s in health_goals["interested_supplements"].split(',') if s.strip()],
                            "additional_info": additional_info["additional_info"],
                            "security_question_1": security_questions["security_question_1"],
                            "security_answer_1": security_questions["security_answer_1"],
                            "security_question_2": security_questions["security_question_2"],
                            "security_answer_2": security_questions["security_answer_2"],
                            "security_question_3": security_questions["security_question_3"],
                            "security_answer_3": security_questions["security_answer_3"]
                        }
                        
                        user_profile = UserProfile(**user_data)
                        save_profile(supabase, user_profile.model_dump())

                        st.header(f"**Your Profile Code is: {user_id_formatted}**")
                        st.info("Please save this code in a safe space to load your profile for future visits.")
                        st.session_state.errors = {}
            else:
                # This is an update
                if not st.session_state.user_profile.get("user_id"):
                    with stylable_container(key="error_container", css_styles='''
                    {
                        background-color: #FFFFFF;
                        border-radius: 0.5rem;
                        padding: 1rem;
                    }
                    '''):
                        display_message("error", "Please enter your profile code to load your profile, or create a new profile if you have not already.")
                else:
                    user_data = {
                        "user_id": st.session_state.user_profile["user_id"],
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
                        "current_medications": [s.strip() for s in medications_allergies["current_medications"].split(',') if s.strip()],
                        "natural_supplements": [s.strip() for s in medications_allergies["natural_supplements"].split(',') if s.strip()],
                        "allergies": [s.strip() for s in medications_allergies["allergies"].split(',') if s.strip()],
                        "health_goals": health_goals["health_goals"],
                        "other_health_goal": health_goals["other_health_goal"],
                        "interested_supplements": [s.strip() for s in health_goals["interested_supplements"].split(',') if s.strip()],
                        "additional_info": additional_info["additional_info"],
                        "security_question_1": st.session_state.user_profile["security_question_1"],
                        "security_answer_1": st.session_state.user_profile["security_answer_1"],
                        "security_question_2": st.session_state.user_profile["security_question_2"],
                        "security_answer_2": st.session_state.user_profile["security_answer_2"],
                        "security_question_3": st.session_state.user_profile["security_question_3"],
                        "security_answer_3": st.session_state.user_profile["security_answer_3"],
                    }
                    user_profile = UserProfile(**user_data)
                    save_profile(supabase, user_profile.model_dump())
                    with stylable_container(key="success_container", css_styles='''
                    {
                        background-color: #FFFFFF;
                        border-radius: 0.5rem;
                        padding: 1rem;
                    }
                    '''):
                        display_message("success", "Profile updated successfully!")

        except ValidationError as e:
            st.session_state.errors = {err['loc'][0] if err['loc'] else 'general': err['msg'] for err in e.errors()}
            with stylable_container(key="validation_error_container", css_styles='''
            {
                background-color: #FFFFFF;
                border-radius: 0.5rem;
                padding: 1rem;
            }
            '''):
                for field, message in st.session_state.errors.items():
                    display_message("error", f"{field.replace('_', ' ').title()}: {message}")

if __name__ == "__main__":
    main()