import streamlit as st
import datetime

def personal_info_form(user_profile, user_status):
    """Renders the personal information section of the form."""
    with st.container(border=True):
        st.header("👤 Personal Information")

        if user_status == "No, I have not filled out the intake form before":
            email_input = st.text_input("Email", key="email")
            st.write("Name")
            col1, col2 = st.columns(2)
            with col1:
                first_name_input = st.text_input("First Name", key="first_name")
            with col2:
                last_name_input = st.text_input("Last Name", key="last_name")
        else: # Returning User
            email_input = user_profile.get("email", "") # Use loaded profile data
            st.text_input("Email", value=email_input, disabled=True)
            st.write("Name")
            col1, col2 = st.columns(2)
            with col1:
                first_name_input = st.text_input("First Name", key="first_name", disabled=True)
            with col2:
                last_name_input = st.text_input("Last Name", key="last_name", disabled=True)

        st.write("Date of Birth")
        today = datetime.date.today()
        month_names = [datetime.date(2024, i, 1).strftime('%B') for i in range(1, 13)]

        # Load DOB from profile if it exists
        user_dob = user_profile.get("dob")
        if isinstance(user_dob, str):
            try:
                user_dob = datetime.datetime.strptime(user_dob, "%Y-%m-%d").date()
            except ValueError:
                user_dob = None

        initial_year = user_dob.year if user_dob else 1990
        initial_month_index = user_dob.month - 1 if user_dob else 0
        initial_day_index = user_dob.day - 1 if user_dob else 0

        # Avoid widget key conflict
        if "dob_year" not in st.session_state:
            st.session_state.dob_year = initial_year
        if "dob_month" not in st.session_state:
            st.session_state.dob_month = month_names[initial_month_index]
        if "dob_day" not in st.session_state:
            st.session_state.dob_day = initial_day_index + 1

        col1, col2, col3 = st.columns(3)
        with col1:
            month_name = st.selectbox("Month", month_names, key="dob_month")
            month = month_names.index(month_name) + 1
        with col2:
            day = st.selectbox("Day", list(range(1, 32)), key="dob_day")
        with col3:
            year = st.selectbox("Year", list(range(1920, today.year + 1)), key="dob_year")

        try:
            dob = datetime.date(year, month, day)
        except ValueError:
            st.error("Please enter a valid date of birth.")
            dob = None


        # Optional: set defaults in session state if not set already
        if "height_ft" not in st.session_state:
            st.session_state["height_ft"] = 5  # default to 5 feet
        if "height_in" not in st.session_state:
            st.session_state["height_in"] = 6  # default to 6 inches

        st.write("Height")
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.selectbox("Feet", list(range(4, 7)), key="height_ft")
        with col2:
            height_in = st.selectbox("Inches", list(range(0, 12)), key="height_in")


        weight_input = st.text_input("Weight (in lbs)", key="weight_lbs")
        st.write("") # Adds a little vertical space
        sex_options = ('Male', 'Female')
        sex = st.radio("Biological Sex", sex_options, index=sex_options.index(user_profile.get("sex", "Male")), key="sex")

        return {
            "email": email_input,
            "first_name": first_name_input,
            "last_name": last_name_input,
            "dob": dob,
            "height_ft": height_ft,
            "height_in": height_in,
            "weight_lbs": weight_input,
            "sex": sex
        }
