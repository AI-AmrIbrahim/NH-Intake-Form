import os
import streamlit as st
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

@st.cache_resource
def init_connection() -> Client:
    """Initialize and return the Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)

def save_profile(supabase: Client, user_data: dict):
    """Save user profile to the database as a new entry."""
    try:
        # Use insert to create a new record every time
        response = supabase.table('user_profiles').insert(user_data).execute()
        return response
    except Exception as e:
        print(f"Error saving profile: {e}")
        return None

def load_profile_from_db(supabase: Client, email: str):
    """Load the most recent user profile from the database based on email."""
    try:
        # Fetch the most recent profile by ordering by created_at descending
        response = supabase.table('user_profiles').select('*').eq('email', email).order('created_at', desc=True).limit(1).execute()
        if response.data:
            profile = response.data[0]
            
            # Clean up list fields that might be stored as JSON strings
            list_fields = [
                'medical_conditions', 'current_medications', 'natural_supplements', 
                'allergies', 'health_goals', 'interested_supplements'
            ]
            
            for field in list_fields:
                if field in profile and profile[field] is not None:
                    # If it's a string that looks like JSON, try to parse it
                    if isinstance(profile[field], str):
                        try:
                            # Try to parse as JSON
                            parsed_data = json.loads(profile[field])
                            profile[field] = parsed_data
                        except (json.JSONDecodeError, TypeError):
                            # If parsing fails, keep as string
                            pass
            
            # Ensure text fields are strings
            text_fields = ['additional_info', 'other_health_goal']
            for field in text_fields:
                if field in profile and profile[field] is not None:
                    profile[field] = str(profile[field])
                elif field in profile:
                    profile[field] = ""
            
            return profile
        return None
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None