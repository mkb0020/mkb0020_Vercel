# api/scores.py
# POST /api/scores  { name, score, waveReached, mode }
import os
import re
import time
import psycopg2
import psycopg2.extras
from flask import Blueprint, request, jsonify

scores_bp = Blueprint('scores', __name__)

VALID_MODES  = {'gameplay', 'survival', 'bossBattle'}
MAX_SCORE    = 9_999_999
MAX_NAME_LEN = 20

# NAIVE IN-PROCESS RATE LIMIT — ip -> (count, reset_at)
# GOOD ENOUGH FOR LOW TRAFFIC; SWAP FOR REDIS IF NEEDED
_rate_map: dict = {}
RATE_WINDOW  = 60    # SECONDS
RATE_LIMIT   = 5     # MAX SUBMITS PER WINDOW PER IP

CORS_HEADERS = {
    'Access-Control-Allow-Origin':  '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    entry = _rate_map.get(ip)
    if not entry or now > entry['reset_at']:
        _rate_map[ip] = {'count': 1, 'reset_at': now + RATE_WINDOW}
        return False
    if entry['count'] >= RATE_LIMIT:
        return True
    entry['count'] += 1
    return False


def _sanitize_name(raw) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9 _\-]', '', str(raw or '').strip())
    return cleaned[:MAX_NAME_LEN] or 'PILOT'


def _get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')


@scores_bp.route('/api/scores', methods=['POST', 'OPTIONS'])
def post_score():
    if request.method == 'OPTIONS':
        return ('', 200, CORS_HEADERS)

    # RATE LIMIT
    ip = (request.headers.get('X-Forwarded-For', '') or request.remote_addr or 'unknown').split(',')[0].strip()
    if _is_rate_limited(ip):
        return (jsonify({'ok': False, 'error': 'Too many requests'}), 429, CORS_HEADERS)

    data = request.get_json(silent=True) or {}

    # VALIDATE
    name  = data.get('name', '')
    score = data.get('score')
    mode  = data.get('mode', 'gameplay')
    wave  = data.get('waveReached')

    if not name or not str(name).strip():
        return (jsonify({'ok': False, 'error': 'Name required'}), 400, CORS_HEADERS)

    if not isinstance(score, (int, float)) or not (0 <= int(score) <= MAX_SCORE):
        return (jsonify({'ok': False, 'error': 'Invalid score'}), 400, CORS_HEADERS)

    if mode not in VALID_MODES:
        return (jsonify({'ok': False, 'error': 'Invalid mode'}), 400, CORS_HEADERS)

    clean_name = _sanitize_name(name)
    clean_score = int(score)
    clean_wave  = int(wave) if isinstance(wave, (int, float)) and 0 <= wave <= 5 else None

    try:
        conn = _get_conn()
        cur  = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            INSERT INTO high_scores (player_name, score, wave_reached, mode)
            VALUES (%s, %s, %s, %s)
            RETURNING id, player_name AS name, score
        """, (clean_name, clean_score, clean_wave, mode))
        entry = dict(cur.fetchone())

        # RETURN THE PLAYER'S GLOBAL RANK SO WE CAN SHOW "YOU ARE #4 ALL-TIME!"
        cur.execute("""
            SELECT COUNT(*) + 1 AS rank
            FROM high_scores
            WHERE mode = %s AND score > %s
        """, (mode, clean_score))
        rank = int(cur.fetchone()['rank'])

        conn.commit()
        cur.close()
        conn.close()

        return (jsonify({'ok': True, 'entry': entry, 'rank': rank}), 201, CORS_HEADERS)

    except Exception as e:
        print(f'[scores POST] DB error: {e}')
        return (jsonify({'ok': False, 'error': 'Database error'}), 500, CORS_HEADERS)