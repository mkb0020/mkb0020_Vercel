import os
import random
from functools import wraps
from flask import Blueprint, request, jsonify
from api.supabase_helper import (
    upload_media_to_supabase,
    insert_social_post,
    fetch_posts,
    update_last_used,
    fetch_all_ready_posts
)

catforce_bp = Blueprint('catforce_bp', __name__)

def require_admin_auth(f):
    """Security decorator validating structural password parameters on restricted endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_password = os.environ.get("CATFORCE_ADMIN_PASSWORD")
        provided_password = request.headers.get("X-CatForce-Auth")
        
        if not admin_password:
            return jsonify({"status": "error", "message": "Server configuration error: Auth unset."}), 500
        
        if provided_password != admin_password:
            return jsonify({"status": "error", "message": "ACCESS DENIED: Invalid encryption credentials."}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@catforce_bp.route('/api/catforce/upload', methods=['POST'])
@require_admin_auth
def api_upload_post():
    try:
        text_content = request.form.get('text_content', '').strip()
        platform = request.form.get('platform', 'all')
        media_file = request.files.get('media_file')

        if not text_content:
            return jsonify({"status": "error", "message": "Missing required field: text_content"}), 400

        media_url = None
        storage_path = None
        media_type = "none"

        if media_file and media_file.filename != '':
            file_bytes = media_file.read()
            media_url, storage_path, media_type = upload_media_to_supabase(
                file_name=media_file.filename,
                file_bytes=file_bytes,
                mimetype=media_file.content_type
            )

        records = insert_social_post(
            text_content=text_content,
            platform=platform,
            media_url=media_url,
            storage_path=storage_path,
            media_type=media_type
        )

        return jsonify({"status": "success", "message": "Content payload deployed to Supabase.", "data": records}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@catforce_bp.route('/api/catforce/posts', methods=['GET'])
@require_admin_auth
def api_get_posts():
    try:
        platform_filter = request.args.get('platform')
        posts = fetch_posts(platform_filter=platform_filter)
        return jsonify({"status": "success", "posts": posts}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@catforce_bp.route('/api/catforce/mark-used', methods=['POST'])
@require_admin_auth
def api_mark_used():
    try:
        data = request.get_json() or {}
        post_id = data.get('post_id')
        
        if not post_id:
            return jsonify({"status": "error", "message": "Missing targeting variable: post_id"}), 400
            
        updated_records = update_last_used(post_id)
        return jsonify({"status": "success", "updated": updated_records}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@catforce_bp.route('/api/catforce/random', methods=['GET'])
@require_admin_auth
def api_get_random_ready():
    try:
        ready_posts = fetch_all_ready_posts()
        if not ready_posts:
            return jsonify({"status": "success", "post": None, "message": "Queue depleted: No ready records found."}), 200
        
        # Pull a random element out of the active batch
        selected_post = random.choice(ready_posts)
        return jsonify({"status": "success", "post": selected_post}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500