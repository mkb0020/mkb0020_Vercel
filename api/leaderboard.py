# api/leaderboard.py
# GET /api/leaderboard?mode=gameplay&limit=10

import os
import psycopg2
import psycopg2.extras
from flask import Blueprint, request, jsonify

leaderboard_bp = Blueprint('leaderboard', __name__)

VALID_MODES = {'gameplay', 'survival', 'bossBattle'}

def _get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')


@leaderboard_bp.route('/api/leaderboard', methods=['GET', 'OPTIONS'])
def get_leaderboard():
    # CORS — WILDCARD IS FINE, LEADERBOARD IS PUBLIC DATA
    # ITCH.IO SERVES GAMES FROM html-classic.itch.zone, NOT THE PUBLISHER DOMAIN
    headers = {
        'Access-Control-Allow-Origin':  '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    if request.method == 'OPTIONS':
        return ('', 200, headers)

    mode = request.args.get('mode', 'gameplay')
    if mode not in VALID_MODES:
        return (jsonify({'ok': False, 'error': 'Invalid mode'}), 400, headers)

    try:
        limit = max(1, min(100, int(request.args.get('limit', 10))))
    except (ValueError, TypeError):
        limit = 10

    try:
        conn = _get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT
                player_name  AS name,
                score,
                wave_reached AS wave,
                TO_CHAR(created_at AT TIME ZONE 'UTC', 'Mon DD YYYY') AS date
            FROM high_scores
            WHERE mode = %s
            ORDER BY score DESC
            LIMIT %s
        """, (mode, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return (jsonify({'ok': True, 'scores': [dict(r) for r in rows]}), 200, headers)

    except Exception as e:
        print(f'[leaderboard] DB error: {e}')
        return (jsonify({'ok': False, 'error': 'Database error'}), 500, headers)