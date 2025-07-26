import streamlit as st
import datetime

def personal_info_form(user_profile, user_status):
    """Renders the personal information section of the form."""
    with st.container(border=True):
        st.header("👤 Personal Information")
        
        # Determine if user is returning (for cleaner code)
        is_returning_user = user_status != "No, I have not filled out the intake form before"

        # Email
        email_input = st.text_input(
            "Email", 
            value=user_profile.get("email", ""), 
            disabled=is_returning_user, 
            key="email"
        )
        
        # Name
        st.write("Name")
        col1, col2 = st.columns(2)
        with col1:
            first_name_input = st.text_input(
                "First Name", 
                value=user_profile.get("first_name", ""), 
                disabled=is_returning_user, 
                key="first_name"
            )
        with col2:
            last_name_input = st.text_input(
                "Last Name", 
                value=user_profile.get("last_name", ""), 
                disabled=is_returning_user, 
                key="last_name"
            )

        # Date of Birth
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

        # Set defaults in session state if not already set
        if "dob_year" not in st.session_state:
            st.session_state.dob_year = initial_year
        if "dob_month" not in st.session_state:
            st.session_state.dob_month = month_names[initial_month_index]
        if "dob_day" not in st.session_state:
            st.session_state.dob_day = initial_day_index + 1

        col1, col2, col3 = st.columns(3)
        with col1:
            month_name = st.selectbox(
                "Month", 
                month_names, 
                index=initial_month_index, 
                disabled=is_returning_user, 
                key="dob_month"
            )
            month = month_names.index(month_name) + 1
        with col2:
            day = st.selectbox(
                "Day", 
                list(range(1, 32)), 
                index=initial_day_index, 
                disabled=is_returning_user, 
                key="dob_day"
            )
        with col3:
            year_list = list(range(1920, today.year + 1))
            if "dob_year" not in st.session_state:
                index = year_list.index(initial_year)
                year = st.selectbox("Year", year_list, index=index, key="dob_year")
            else:
                year = st.selectbox("Year", year_list, key="dob_year")

        try:
            dob = datetime.date(year, month, day)
        except ValueError:
            st.error("Please enter a valid date of birth.")
            dob = None

        # Height - editable for both new and returning users
        if "height_ft" not in st.session_state:
            st.session_state["height_ft"] = user_profile.get("height_ft", 5)
        if "height_in" not in st.session_state:
            st.session_state["height_in"] = user_profile.get("height_in", 6)

        st.write("Height")
        col1, col2 = st.columns(2)
        with col1:
            height_ft = st.selectbox("Feet", list(range(4, 7)), key="height_ft")
        with col2:
            height_in = st.selectbox("Inches", list(range(0, 12)), key="height_in")

        # Weight - editable for both new and returning users
        weight_input = st.text_input(
            "Weight (in lbs)", 
            value=str(user_profile.get("weight_lbs", "")), 
            key="weight_lbs"
        )
        
        st.write("")
        
        # Sex - disabled for returning users
        sex_options = ('Male', 'Female')
        sex = st.radio(
            "Biological Sex", 
            sex_options, 
            index=sex_options.index(user_profile.get("sex", "Male")), 
            disabled=is_returning_user, 
            key="sex"
        )

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