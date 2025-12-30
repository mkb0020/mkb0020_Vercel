import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

# BLUEPRINT 
comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/api/comments', methods=['GET', 'POST'])
def handle_comments():
    """
    Handles both GET (retrieve comments) and POST (submit comment) requests
    """
    
    if request.method == "GET":
        try:
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        SELECT id, commenter_name, comment_text, created_at
                        FROM game_comments
                        WHERE is_visible = TRUE
                        ORDER BY created_at DESC
                        """
                    )
                    
                    comments = []
                    for row in cur.fetchall():
                        comments.append({
                            "id": row[0],
                            "commenter_name": row[1] or "Anonymous",  
                            "comment_text": row[2],
                            "created_at": row[3].isoformat() if row[3] else None
                        })
                    
                    return jsonify({"success": True, "comments": comments})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    elif request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400
            
            comment_text = data.get("comment_text", "").strip()
            if not comment_text:
                return jsonify({"success": False, "error": "Comment cannot be empty"}), 400
            
            if len(comment_text) > 1000:
                return jsonify({"success": False, "error": "Comment too long (max 1000 characters)"}), 400
            
            commenter_name = data.get("commenter_name", "").strip() or None  
            
            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO game_comments (commenter_name, comment_text)
                        VALUES (%s, %s)
                        RETURNING id, created_at
                        """,
                        (commenter_name, comment_text)
                    )
                    
                    result = cur.fetchone()
                    new_id = result[0]
                    created_at = result[1]
            
            return jsonify({
                "success": True,
                "message": "Comment posted!",
                "comment": {
                    "id": new_id,
                    "commenter_name": commenter_name or "Anonymous",
                    "comment_text": comment_text,
                    "created_at": created_at.isoformat() if created_at else None
                }
            })
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    else:
        return jsonify({"success": False, "error": "Method not allowed"}), 405