import os
from functools import wraps
from flask import Blueprint, request, jsonify
from api.projects_helper import insert_new_project

projects_bp = Blueprint('projects_bp', __name__)

def require_admin_auth(f):
    """Replicated authentication validator testing incoming terminal stream core keys."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_password = os.environ.get("CATFORCE_ADMIN_PASSWORD")
        provided_password = request.headers.get("X-CatForce-Auth")
        
        if not admin_password:
            return jsonify({"status": "error", "message": "Server routing fault: Security key unmapped."}), 500
        
        if provided_password != admin_password:
            return jsonify({"status": "error", "message": "ACCESS DENIED: Digital handshake handshake failed."}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@projects_bp.route('/api/projects/submit', methods=['POST'])
@require_admin_auth
def api_submit_project():
    try:
        data = request.get_json() or {}
        
        # Pull transactional parameters from JSON stream
        name = data.get('project_name', '').strip()
        types = data.get('project_types', [])
        audiences = data.get('target_audiences', [])
        platform = data.get('platform', '')
        description = data.get('description', '').strip()

        # Validation assertions
        if not name or not platform or not description:
            return jsonify({"status": "error", "message": "Missing core properties: name, platform, or description required."}), 400

        # Execute insertion
        records = insert_new_project(
            name=name,
            types=types,
            audiences=audiences,
            platform=platform,
            description=description
        )

        return jsonify({"status": "success", "message": "Project record synchronized successfully.", "data": records}), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500