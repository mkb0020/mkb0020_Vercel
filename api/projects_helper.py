import os
from supabase import create_client, Client

# Pull Catforce network credentials from environment variables
supabase_url = os.environ.get("CATFORCE_SUPABASE_URL")
supabase_key = os.environ.get("CATFORCE_SUPABASE_SERVICE_ROLE")

# Initialize client gracefully as None so Vercel can scan the file without crashing
supabase: Client = None
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

def insert_new_project(name: str, types: list, audience: list, platform: str, description: str):
    """
    Commits a new project configuration matrix and metadata payload 
    directly into the Supabase Postgres 'projects' table.
    """
    # Only crash if a user actually triggers the function and keys are missing
    if not supabase:
        raise RuntimeError(
            "Deployment Matrix Error: Supabase client is not initialized. "
            "Please verify that CATFORCE_SUPABASE_URL and CATFORCE_SUPABASE_SERVICE_ROLE "
            "are properly set in your Vercel Environment Variables dashboard."
        )

    # Corrected to map exactly to your Postgres database columns
    payload = {
        "project_name": name,
        "project_types": types,          
        "target_audiences": audience,    
        "platform": platform,
        "description": description
    }
    
    # Fire the insert command down the pipe to Supabase
    response = supabase.table("projects").insert(payload).execute()
    return response.data