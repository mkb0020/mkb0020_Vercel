import os
from supabase import create_client, Client

# === ALIGNED TO YOUR EXACT VERCEL CODENAMES ===
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SECRET")

# Initialize client gracefully as None so Vercel can scan the file without crashing
supabase: Client = None
if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

def insert_new_project(name: str, types: list, audiences: list, platform: str, description: str):
    """
    Commits a new project configuration matrix and metadata payload 
    directly into the Supabase Postgres 'projects' table.
    """
    if not supabase:
        raise RuntimeError(
            "Deployment Matrix Error: Supabase client is not initialized. "
            "Please verify that SUPABASE_URL and SUPABASE_SECRET "
            "are properly set in your Vercel Environment Variables dashboard."
        )

    payload = {
        "project_name": name,
        "project_types": types,          
        "target_audiences": audiences,   
        "platform": platform,
        "description": description
    }
    
    response = supabase.table("projects").insert(payload).execute()
    return response.data