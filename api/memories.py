# api/memories.py
import os
import json
import psycopg2
from functools import wraps
from flask import Blueprint, request, jsonify

memories_bp = Blueprint('memories_bp', __name__)

def get_db_connection():
    """
    Return a connection to your Neon database.
    """
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set")
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# 🛡️ The Security Checkpoint
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Grab the token from the incoming request headers
        client_key = request.headers.get('X-Access-Token')
        # The master password stored securely on your server
        server_key = os.environ.get('MEMORY_ACCESS_KEY') 
        
        # Failsafe: if you forgot to set the env variable, lock it down
        if not server_key:
            return jsonify({"error": "Server auth configuration missing."}), 500
            
        # Reject unauthorized access
        if not client_key or client_key != server_key:
            return jsonify({"error": "Access Denied: Invalid clearance level."}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@memories_bp.route('/api/memories', methods=['POST'])
@require_auth  # <--- Apply the security lock here
def create_memory():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    title        = data.get('title', '').strip()
    event_date   = data.get('event_date', '').strip()
    location     = data.get('location', '').strip()
    people       = data.get('people', [])
    description  = data.get('description', '').strip()
    significance = data.get('significance', '').strip()

    if not isinstance(people, list):
        people = []

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO events (title, event_date, location, people, description, significance)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (title, event_date, location, json.dumps(people), description, significance)
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"success": True, "id": new_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()