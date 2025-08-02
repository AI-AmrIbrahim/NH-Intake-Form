import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

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
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None
