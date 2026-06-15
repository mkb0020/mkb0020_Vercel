import os
import uuid
from datetime import datetime
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SECRET = os.environ.get("SUPABASE_SECRET")

# Initialize client safely for serverless environments
supabase: Client = None
if SUPABASE_URL and SUPABASE_SECRET:
    supabase = create_client(SUPABASE_URL, SUPABASE_SECRET)

def get_bucket_and_type(filename: str, mimetype: str):
    """Determines the correct Supabase storage bucket and media type based on file info."""
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    
    if ext == 'gif' or 'gif' in mimetype:
        return 'social-marketing-gifs', 'gif'
    elif ext in ['mp4', 'mov', 'avi', 'mkv', 'webm'] or 'video' in mimetype:
        return 'social-marketing-vids', 'video'
    else:
        return 'social-marketing-images', 'image'

def upload_media_to_supabase(file_name: str, file_bytes: bytes, mimetype: str):
    """Uploads binary data to the corresponding target storage bucket."""
    if not supabase:
        raise RuntimeError("Supabase client is not initialized. Check your environment variables.")

    bucket, media_type = get_bucket_and_type(file_name, mimetype)
    
    # Generate unique storage filename to avoid collisions
    unique_id = str(uuid.uuid4())
    ext = file_name.split('.')[-1] if '.' in file_name else 'bin'
    storage_path = f"uploads/{unique_id}.{ext}"

    # Execute upload
    supabase.storage.from_(bucket).upload(
        path=storage_path,
        file=file_bytes,
        file_options={"content-type": mimetype}
    )

    # Construct public URL
    public_url = supabase.storage.from_(bucket).get_public_url(storage_path)
    
    return public_url, storage_path, media_type

def insert_social_post(text_content: str, platform: str, media_url: str = None, storage_path: str = None, media_type: str = "none"):
    """Inserts metadata for a new post configuration into the social_posts Postgres table."""
    if not supabase:
        raise RuntimeError("Supabase client is not initialized.")

    post_data = {
        "text_content": text_content,
        "platform": platform,
        "media_type": media_type,
        "media_url": media_url,
        "storage_path": storage_path,
        "status": "ready",
        "tags": []  # Initialized empty, ready for custom JSON array parsing if expanded
    }

    response = supabase.table("social_posts").insert(post_data).execute()
    return response.data

def fetch_posts(platform_filter: str = None):
    """Fetches all post records, optionally filtered by destination network platform."""
    if not supabase:
        raise RuntimeError("Supabase client is not initialized.")

    query = supabase.table("social_posts").select("*").order("created_at", desc=True)
    if platform_filter and platform_filter != "all":
        query = query.eq("platform", platform_filter)

    response = query.execute()
    return response.data

def update_last_used(post_id: str):
    """Sets last_used_at timestamp to now to signal a publishing transaction execution."""
    if not supabase:
        raise RuntimeError("Supabase client is not initialized.")

    now_iso = datetime.utcnow().isoformat()
    response = supabase.table("social_posts").update({"last_used_at": now_iso, "status": "posted"}).eq("id", post_id).execute()
    return response.data

def fetch_all_ready_posts():
    """Fetches list of active entries whose delivery status flags are set to ready."""
    if not supabase:
        raise RuntimeError("Supabase client is not initialized.")

    response = supabase.table("social_posts").select("*").eq("status", "ready").execute()
    return response.data