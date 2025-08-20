import streamlit as st
from src.config.security_questions import SECURITY_QUESTIONS

def security_questions_form(user_profile, errors):
    """Renders the security questions section of the form."""
    with st.container(border=True):
        st.header("🔒 Security Questions")
        st.write("Please select three unique security questions and provide answers. These will be used to recover your profile if you forget your Unique ID.")

        # Initialize session state for security questions if they don't exist
        if "security_question_1" not in st.session_state:
            st.session_state.security_question_1 = SECURITY_QUESTIONS[0]
        if "security_answer_1" not in st.session_state:
            st.session_state.security_answer_1 = ""
        if "security_question_2" not in st.session_state:
            st.session_state.security_question_2 = SECURITY_QUESTIONS[1]
        if "security_answer_2" not in st.session_state:
            st.session_state.security_answer_2 = ""
        if "security_question_3" not in st.session_state:
            st.session_state.security_question_3 = SECURITY_QUESTIONS[2]
        if "security_answer_3" not in st.session_state:
            st.session_state.security_answer_3 = ""

        # Security Question 1
        sq1 = st.selectbox("Security Question 1", SECURITY_QUESTIONS, key="security_question_1")
        sa1 = st.text_input("Answer 1", key="security_answer_1")
        if "security_question_1" in errors:
            st.error(errors["security_question_1"])
        if "security_answer_1" in errors:
            st.error(errors["security_answer_1"])

        # Security Question 2
        sq2 = st.selectbox("Security Question 2", SECURITY_QUESTIONS, key="security_question_2")
        sa2 = st.text_input("Answer 2", key="security_answer_2")
        if "security_question_2" in errors:
            st.error(errors["security_question_2"])
        if "security_answer_2" in errors:
            st.error(errors["security_answer_2"])

        # Security Question 3
        sq3 = st.selectbox("Security Question 3", SECURITY_QUESTIONS, key="security_question_3")
        sa3 = st.text_input("Answer 3", key="security_answer_3")
        if "security_question_3" in errors:
            st.error(errors["security_question_3"])
        if "security_answer_3" in errors:
            st.error(errors["security_answer_3"])

        return {
            "security_question_1": sq1,
            "security_answer_1": sa1,
            "security_question_2": sq2,
            "security_answer_2": sa2,
            "security_question_3": sq3,
            "security_answer_3": sa3
        }