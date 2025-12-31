import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

tester_signup_bp = Blueprint('tester_signup', __name__)

@tester_signup_bp.route('/api/tester-signup', methods=['GET', 'POST'])
def handle_tester_signup():
    """
    Handles both GET (retrieve signups) and POST (submit signup) requests
    """
    
    if request.method == 'GET':
        try:
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT * FROM game_testers 
                        ORDER BY signed_up_at DESC
                    """)
                    
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    
                    testers = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        testers.append(row_dict)
                    
                    return jsonify({"success": True, "data": testers})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400
            
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            
            if not name or not email:
                return jsonify({
                    "success": False, 
                    "error": "Name and email are required"
                }), 400
            
            if len(name) > 100:
                return jsonify({"success": False, "error": "Name too long (max 100 characters)"}), 400
            if len(email) > 100:
                return jsonify({"success": False, "error": "Email too long (max 100 characters)"}), 400
            
            if '@' not in email or '.' not in email:
                return jsonify({"success": False, "error": "Please enter a valid email address"}), 400
            
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT id FROM game_testers WHERE email = %s",
                        (email,)
                    )
                    existing = cur.fetchone()
                    
                    if existing:
                        return jsonify({
                            "success": False, 
                            "error": "This email is already registered!"
                        }), 400
            
            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO game_testers (name, email)
                        VALUES (%s, %s)
                        RETURNING id, signed_up_at
                        """,
                        (name, email)
                    )
                    
                    result = cur.fetchone()
                    tester_id = result[0]
                    signed_up_at = result[1]
            
            return jsonify({
                "success": True,
                "message": "Successfully signed up as a game tester!",
                "tester_id": tester_id
            })
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500