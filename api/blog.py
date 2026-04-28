import os
import re
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_URL = os.environ.get("DATABASE_URL")
ADMIN_SECRET = os.environ.get("BLOG_ADMIN_SECRET", "change-this-secret-key")

blog_bp = Blueprint('blog', __name__)

def slugify(title):
    """Convert title to a URL-friendly slug."""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

# ---------- PUBLIC ROUTES ----------
@blog_bp.route('/api/blog-posts', methods=['GET'])
def get_all_posts():
    """Return a list of all published posts (id, title, slug, created_at) for sidebar."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, title, slug, created_at
                    FROM blog_posts
                    WHERE is_published = TRUE
                    ORDER BY created_at DESC
                """)
                rows = cur.fetchall()
                posts = [{
                    "id": r[0],
                    "title": r[1],
                    "slug": r[2],
                    "created_at": r[3].isoformat() if r[3] else None
                } for r in rows]
                return jsonify({"success": True, "posts": posts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@blog_bp.route('/api/blog-posts/<int:post_id>', methods=['GET'])
def get_single_post(post_id):
    """Return full content of a single published post."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, title, content, created_at, slug
                    FROM blog_posts
                    WHERE id = %s AND is_published = TRUE
                """, (post_id,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Post not found"}), 404
                post = {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "created_at": row[3].isoformat() if row[3] else None,
                    "slug": row[4]
                }
                return jsonify({"success": True, "post": post})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ---------- ADMIN ROUTE ----------
@blog_bp.route('/api/blog-posts', methods=['POST'])
def create_post():
    """Create a new blog post. Requires admin secret in header."""
    auth_header = request.headers.get('X-Admin-Secret')
    if not auth_header or auth_header != ADMIN_SECRET:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data"}), 400

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({"success": False, "error": "Title and content are required"}), 400

    slug = slugify(title)
    with psycopg.connect(DB_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM blog_posts WHERE slug = %s", (slug,))
            if cur.fetchone():
                slug = f"{slug}-{int(datetime.now().timestamp())}"

            cur.execute("""
                INSERT INTO blog_posts (title, slug, content)
                VALUES (%s, %s, %s)
                RETURNING id, created_at
            """, (title, slug, content))
            new_id, created_at = cur.fetchone()
            conn.commit()

    return jsonify({
        "success": True,
        "message": "Post created!",
        "post": {
            "id": new_id,
            "title": title,
            "slug": slug,
            "created_at": created_at.isoformat() if created_at else None
        }
    }), 201