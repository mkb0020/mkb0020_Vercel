import os
from supabase import create_client, Client

# Pull Catforce network credentials from environment variables
supabase_url = os.environ.get("CATFORCE_SUPABASE_URL")
supabase_key = os.environ.get("CATFORCE_SUPABASE_SERVICE_ROLE")

# Early exit warning if the environment is misconfigured
if not supabase_url or not supabase_key:
    raise RuntimeError(
        "Deployment Matrix Error: Missing Supabase environment variables. "
        "Ensure CATFORCE_SUPABASE_URL and CATFORCE_SUPABASE_SERVICE_ROLE are set in Vercel."
    )

# Initialize the Supabase database connection vector
supabase: Client = create_client(supabase_url, supabase_key)

def insert_new_project(name: str, types: list, audience: list, platform: str, description: str):
    """
    Commits a new project configuration matrix and metadata payload 
    directly into the Supabase Postgres 'projects' table.
    """
    payload = {
        "name": name,
        "types": types,          # Expects a list/array matrix
        "audience": audience,    # Expects a list/array matrix
        "platform": platform,
        "description": description
    }
    
    # Fire the insert command down the pipe to Supabase
    response = supabase.table("projects").insert(payload).execute()
    return response