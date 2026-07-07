# api/appStore/projects.py
# Serves the app catalog that powers the storefront grid + detail pages.

import os
import psycopg2
import psycopg2.extras
from flask import Blueprint, jsonify

appstore_projects_bp = Blueprint('appstore_projects', __name__, url_prefix='/api/appstore')


def _get_conn():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))


@appstore_projects_bp.route('/projects', methods=['GET'])
def list_projects():
    """Powers the storefront grid. Returns lightweight cards, not full descriptions."""
    conn = None
    try:
        conn = _get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT slug, name, tagline, hero_image_url, tags, is_featured
            FROM appstore_projects
            ORDER BY sort_order ASC, name ASC
        """)
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()


@appstore_projects_bp.route('/projects/<slug>', methods=['GET'])
def get_project(slug):
    """Powers a single app's detail page."""
    conn = None
    try:
        conn = _get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT slug, name, tagline, description, hero_image_url,
                   itch_url, ms_store_url, other_url, tags
            FROM appstore_projects
            WHERE slug = %s
        """, (slug,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return jsonify({'error': 'not found'}), 404
        return jsonify(row)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()