import streamlit as st
from src.config.security_questions import SECURITY_QUESTIONS

def security_questions_form(errors):
    """Renders the security questions section of the form."""
    with st.container(border=True):
        st.header("🔒 Security Questions")
        st.write("Please select and answer three security questions. These will be used to recover your profile if you forget your profile code.")

        # Question 1
        st.selectbox("Question 1", SECURITY_QUESTIONS, key="security_question_1")
        st.text_input("Answer 1", key="security_answer_1")
        if "security_question_1" in errors:
            st.error(errors["security_question_1"])
        if "security_answer_1" in errors:
            st.error(errors["security_answer_1"])

        # Question 2
        st.selectbox("Question 2", SECURITY_QUESTIONS, key="security_question_2")
        st.text_input("Answer 2", key="security_answer_2")
        if "security_question_2" in errors:
            st.error(errors["security_question_2"])
        if "security_answer_2" in errors:
            st.error(errors["security_answer_2"])

        # Question 3
        st.selectbox("Question 3", SECURITY_QUESTIONS, key="security_question_3")
        st.text_input("Answer 3", key="security_answer_3")
        if "security_question_3" in errors:
            st.error(errors["security_question_3"])
        if "security_answer_3" in errors:
            st.error(errors["security_answer_3"])

        return {
            "security_question_1": st.session_state.security_question_1,
            "security_answer_1": st.session_state.security_answer_1,
            "security_question_2": st.session_state.security_question_2,
            "security_answer_2": st.session_state.security_answer_2,
            "security_question_3": st.session_state.security_question_3,
            "security_answer_3": st.session_state.security_answer_3
        }
