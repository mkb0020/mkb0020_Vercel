# api/memories.py
import os
import json
import uuid
import psycopg2
from functools import wraps
from flask import Blueprint, request, jsonify
from supabase import create_client, Client

memories_bp = Blueprint('memories_bp', __name__)

# Initialize Supabase Client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if supabase_url and supabase_key:
    supabase: Client = create_client(supabase_url, supabase_key)
else:
    supabase = None

def get_db_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_key = request.headers.get('X-Access-Token')
        server_key = os.environ.get('MEMORY_ACCESS_KEY') 
        if not server_key:
            return jsonify({"error": "Server auth configuration missing."}), 500
        if not client_key or client_key != server_key:
            return jsonify({"error": "Access Denied: Invalid clearance level."}), 401
        return f(*args, **kwargs)
    return decorated_function

@memories_bp.route('/api/memories', methods=['POST'])
@require_auth
def create_memory():
    # Because we are using FormData, we extract data from request.form
    title        = request.form.get('title', '').strip()
    event_date   = request.form.get('event_date', '').strip()
    location     = request.form.get('location', '').strip()
    description  = request.form.get('description', '').strip()
    significance = request.form.get('significance', '').strip()
    
    # Parse the people array back out of the JSON string
    people_str = request.form.get('people', '[]')
    try:
        people = json.loads(people_str)
    except:
        people = []

    # Handle the Image Upload via Supabase
    photo_url = None
    if 'photo' in request.files and supabase:
        file = request.files['photo']
        if file.filename != '':
            # Generate a unique filename to prevent overwriting existing files
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4().hex}{file_ext}"
            file_bytes = file.read()
            
            try:
                # Push specifically to your 'lighthouse' bucket
                supabase.storage.from_("lighthouse").upload(unique_filename, file_bytes, {"content-type": file.content_type})
                # Grab the public URL to save in the database
                photo_url = supabase.storage.from_("lighthouse").get_public_url(unique_filename)
            except Exception as e:
                return jsonify({"error": f"Image upload failed: {str(e)}"}), 500

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO events (title, event_date, location, people, description, significance, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (title, event_date, location, json.dumps(people), description, significance, photo_url)
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"success": True, "id": new_id, "image": photo_url}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()