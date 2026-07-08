"""
Admin routes for managing the App Store project catalog.

Protects two things behind HTTP Basic Auth (ADMIN_USER / ADMIN_PASS env vars):
  - GET  /admin/appstore/projects/new       -> the submission form page itself
  - POST /api/appstore/admin/projects       -> the endpoint that writes to Neon

Add these two env vars in Vercel before deploying:
  ADMIN_USER
  ADMIN_PASS
"""
import os
import re
from functools import wraps

import psycopg2
from flask import Blueprint, Response, jsonify, request, send_from_directory

appstore_admin_bp = Blueprint('appstore_admin_bp', __name__)


def require_admin_auth(f):
    """HTTP Basic Auth gate. Fails closed if env vars aren't configured —
    never falls back to 'no auth required'."""
    @wraps(f)
    def decorated(*args, **kwargs):
        expected_user = os.environ.get('ADMIN_USER')
        expected_pass = os.environ.get('ADMIN_PASS')

        if not expected_user or not expected_pass:
            return Response('Admin auth is not configured on the server', 500)

        auth = request.authorization
        if not auth or auth.username != expected_user or auth.password != expected_pass:
            return Response(
                'Authentication required', 401,
                {'WWW-Authenticate': 'Basic realm="Admin"'}
            )
        return f(*args, **kwargs)
    return decorated


def get_db_connection():
    # NOTE: swap this for your existing db helper if you already have one
    # (e.g. a shared api/db.py) instead of connecting directly here.
    return psycopg2.connect(os.environ.get('DATABASE_URL'))


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


# ---- Page: serves the admin form itself (also auth-gated) ----
@appstore_admin_bp.route('/admin/appstore/projects/new', methods=['GET'])
@require_admin_auth
def new_project_form():
    return send_from_directory('forms/appStore', 'admin_new_project.html')


# ---- API: creates a new appstore_projects row ----
@appstore_admin_bp.route('/api/appstore/admin/projects', methods=['POST'])
@require_admin_auth
def create_project():
    data = request.get_json(silent=True) or request.form

    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    raw_slug = (data.get('slug') or '').strip()
    slug = slugify(raw_slug) if raw_slug else slugify(name)
    if not slug:
        return jsonify({'error': 'Could not derive a valid slug from name'}), 400

    tagline = (data.get('tagline') or '').strip()
    description = (data.get('description') or '').strip()
    hero_image_url = (data.get('hero_image_url') or '').strip() or None
    itch_url = (data.get('itch_url') or '').strip() or None
    ms_store_url = (data.get('ms_store_url') or '').strip() or None
    other_url = (data.get('other_url') or '').strip() or None

    raw_tags = data.get('tags') or ''
    if isinstance(raw_tags, list):
        tags = [t.strip() for t in raw_tags if t.strip()]
    else:
        tags = [t.strip() for t in raw_tags.split(',') if t.strip()]

    is_featured = str(data.get('is_featured', False)).lower() in ('true', 'on', '1', 'yes')

    try:
        sort_order = int(data.get('sort_order') or 0)
    except (TypeError, ValueError):
        sort_order = 0

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO appstore_projects
                    (slug, name, tagline, description, hero_image_url,
                     itch_url, ms_store_url, other_url, tags, is_featured, sort_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING slug
                """,
                (
                    slug, name, tagline, description, hero_image_url,
                    itch_url, ms_store_url, other_url, tags, is_featured, sort_order,
                ),
            )
            result = cur.fetchone()
            conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return jsonify({'error': f'A project with slug "{slug}" already exists'}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'success': True, 'slug': result[0]}), 201