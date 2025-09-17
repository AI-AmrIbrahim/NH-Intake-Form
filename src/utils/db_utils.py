import os
import streamlit as st
import json
import time
import logging
from typing import Optional, Tuple, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def init_connection() -> Client:
    """Initialize and return the Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """Retry a database operation with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    return None

def check_rate_limit(user_identifier: str) -> bool:
    """Check if user has exceeded rate limit (simple implementation using session state)."""
    current_time = time.time()
    rate_limit_key = f"rate_limit_{user_identifier}"

    if rate_limit_key not in st.session_state:
        st.session_state[rate_limit_key] = []

    # Remove timestamps older than 5 minutes
    st.session_state[rate_limit_key] = [
        timestamp for timestamp in st.session_state[rate_limit_key]
        if current_time - timestamp < 300  # 5 minutes
    ]

    # Check if user has made more than 5 submissions in 5 minutes
    if len(st.session_state[rate_limit_key]) >= 5:
        return False

    return True

def add_rate_limit_entry(user_identifier: str):
    """Add a rate limit entry for the user."""
    rate_limit_key = f"rate_limit_{user_identifier}"
    if rate_limit_key not in st.session_state:
        st.session_state[rate_limit_key] = []
    st.session_state[rate_limit_key].append(time.time())

def save_profile(supabase: Client, user_data: dict) -> Tuple[bool, str]:
    """Save user profile to the database with comprehensive error handling.

    Returns:
        Tuple[bool, str]: (success, message)
    """
    user_id = user_data.get('user_id', 'unknown')

    # Validate user data first
    is_valid, validation_error = validate_user_data(user_data)
    if not is_valid:
        logger.warning(f"Validation failed for user {user_id}: {validation_error}")
        return False, validation_error

    # Check rate limiting
    if not check_rate_limit(user_id):
        logger.warning(f"Rate limit exceeded for user {user_id}")
        return False, "Too many submissions. Please wait a few minutes before trying again."

    def _save_operation():
        response = supabase.table('user_profiles').insert(user_data).execute()
        if hasattr(response, 'data') and response.data:
            logger.info(f"Profile saved successfully for user {user_id}")
            return response
        else:
            raise DatabaseError("No data returned from database")

    try:
        response = retry_operation(_save_operation)
        add_rate_limit_entry(user_id)
        return True, "Profile saved successfully!"

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to save profile for user {user_id}: {error_msg}")

        # Provide user-friendly error messages
        if "timeout" in error_msg.lower():
            return False, "Request timed out. Please check your internet connection and try again."
        elif "connection" in error_msg.lower():
            return False, "Unable to connect to database. Please try again in a few moments."
        elif "duplicate" in error_msg.lower() or "unique" in error_msg.lower():
            return False, "A profile with this ID already exists. Please use the update option instead."
        else:
            return False, "An unexpected error occurred while saving your profile. Please try again or contact support if the problem persists."

def load_profile_from_db(supabase: Client, user_id: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Load the most recent user profile from the database based on user_id.

    Returns:
        Tuple[Optional[Dict], str]: (profile_data, message)
    """
    if not user_id or not user_id.strip():
        return None, "Please enter a valid profile ID."

    def _load_operation():
        response = supabase.table('user_profiles').select('*').eq('user_id', user_id.strip()).order('created_at', desc=True).limit(1).execute()
        return response

    try:
        response = retry_operation(_load_operation)

        if response and response.data:
            profile = response.data[0]

            # Process list fields
            list_fields = [
                'medical_conditions', 'current_medications', 'natural_supplements',
                'allergies', 'health_goals', 'interested_supplements'
            ]

            for field in list_fields:
                if field in profile and profile[field] is not None:
                    if isinstance(profile[field], str):
                        try:
                            parsed_data = json.loads(profile[field])
                            profile[field] = parsed_data
                        except (json.JSONDecodeError, TypeError):
                            logger.warning(f"Failed to parse JSON for field {field}")
                            profile[field] = []

            # Process text fields
            text_fields = ['additional_info', 'other_health_goal']
            for field in text_fields:
                if field in profile and profile[field] is not None:
                    profile[field] = str(profile[field])
                elif field in profile:
                    profile[field] = ""

            logger.info(f"Profile loaded successfully for user {user_id}")
            return profile, "Profile loaded successfully!"
        else:
            logger.info(f"No profile found for user {user_id}")
            return None, "Profile not found. Please check your Profile ID or create a new profile."

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to load profile for user {user_id}: {error_msg}")

        if "timeout" in error_msg.lower():
            return None, "Request timed out. Please check your internet connection and try again."
        elif "connection" in error_msg.lower():
            return None, "Unable to connect to database. Please try again in a few moments."
        else:
            return None, "An error occurred while loading your profile. Please try again or contact support."

def load_profile_by_security_questions(supabase: Client, security_questions: dict) -> Tuple[Optional[Dict[str, Any]], str]:
    """Load a user profile from the database based on security questions and answers.

    Returns:
        Tuple[Optional[Dict], str]: (profile_data, message)
    """
    # Validate input
    required_fields = [
        'security_question_1', 'security_answer_1',
        'security_question_2', 'security_answer_2',
        'security_question_3', 'security_answer_3'
    ]

    for field in required_fields:
        if not security_questions.get(field, '').strip():
            return None, f"Please fill in all security questions and answers."

    # Check rate limiting for security question attempts
    if not check_rate_limit("security_recovery"):
        return None, "Too many recovery attempts. Please wait a few minutes before trying again."

    def _load_operation():
        response = supabase.table('user_profiles').select('*')\
            .eq('security_question_1', security_questions['security_question_1'])\
            .eq('security_answer_1', security_questions['security_answer_1'].strip())\
            .eq('security_question_2', security_questions['security_question_2'])\
            .eq('security_answer_2', security_questions['security_answer_2'].strip())\
            .eq('security_question_3', security_questions['security_question_3'])\
            .eq('security_answer_3', security_questions['security_answer_3'].strip())\
            .order('created_at', desc=True).limit(1).execute()
        return response

    try:
        response = retry_operation(_load_operation)
        add_rate_limit_entry("security_recovery")

        if response and response.data:
            logger.info("Profile recovered successfully via security questions")
            return response.data[0], "Profile recovered successfully!"
        else:
            logger.info("No profile found matching security questions")
            return None, "No profile found matching your security questions and answers. Please verify your answers are correct."

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Failed to recover profile via security questions: {error_msg}")

        if "timeout" in error_msg.lower():
            return None, "Request timed out. Please check your internet connection and try again."
        elif "connection" in error_msg.lower():
            return None, "Unable to connect to database. Please try again in a few moments."
        else:
            return None, "An error occurred during profile recovery. Please try again or contact support."

def validate_user_data(user_data: dict) -> Tuple[bool, str]:
    """Validate user data before saving to database.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    required_fields = ['user_id', 'age_range', 'sex']

    for field in required_fields:
        if not user_data.get(field):
            return False, f"Required field '{field.replace('_', ' ').title()}' is missing."

    # Validate user_id format (should be XXX-XXX-XXX)
    user_id = user_data.get('user_id', '')
    if len(user_id) != 11 or user_id.count('-') != 2:
        return False, "Invalid user ID format."

    # Validate weight if provided
    weight = user_data.get('weight_lbs')
    if weight is not None:
        try:
            weight_float = float(weight)
            if weight_float <= 0 or weight_float > 1000:
                return False, "Weight must be between 1 and 1000 pounds."
        except (ValueError, TypeError):
            return False, "Invalid weight value."

    return True, ""

def get_database_health() -> Dict[str, Any]:
    """Check database connection health.

    Returns:
        Dict with health status information
    """
    try:
        supabase = init_connection()
        start_time = time.time()

        # Simple health check query
        response = supabase.table('user_profiles').select('count', count='exact').limit(1).execute()

        response_time = time.time() - start_time

        return {
            'status': 'healthy',
            'response_time_ms': round(response_time * 1000, 2),
            'timestamp': time.time()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': time.time()
        }