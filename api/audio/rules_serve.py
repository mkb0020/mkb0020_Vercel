# /api/audio/rules_serve.py
#
# Routes:
#
#   GET  /api/audio/rules.js
#       Serves compiled rules.js from audio_rules_cache in Neon.
#
#   POST /api/audio/rebuild-rules
#       Step 1: analyze all songs (updates preference signals in DB).
#       Runs synchronously — Vercel keeps the function alive for the response.
#       Returns when all songs are analyzed.
#
#   POST /api/audio/compile-rules
#       Step 2: compile rules.py logic → save fresh rules.js to Neon.
#       Called by the frontend ~45s after rebuild-rules completes.
#       Fast (~5s) since it just fetches data and does math.
#
# The two-step split avoids Vercel's background thread killing problem:
# threads are terminated when the response is sent on serverless functions.
# Instead the frontend orchestrates the sequence with a setTimeout.

import os
import logging
import psycopg2
from flask import Blueprint, Response, jsonify

logger = logging.getLogger(__name__)

rules_serve_bp = Blueprint('rules_serve', __name__)


def _connect():
    return psycopg2.connect(os.environ["DATABASE_URL"])


# ── SERVE RULES.JS FROM NEON ──────────────────────────────────────────────────

@rules_serve_bp.route('/api/audio/rules.js', methods=['GET'])
def serve_rules_js():
    """Serve compiled rules.js from audio_rules_cache."""
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT rules_js, compiled_at, song_names
                FROM audio_rules_cache WHERE id = 1
            """)
            row = cur.fetchone()
        conn.close()

        if not row:
            stub = (
                "// rules.js not yet compiled — POST /api/audio/rebuild-rules\n"
                "export const metadata = {};\n"
                "export const musicRules = {};\n"
                "export const ruleLibrary = {};\n"
            )
            return Response(stub, status=503, mimetype='application/javascript',
                            headers={'Cache-Control': 'no-store'})

        rules_js, compiled_at, song_names = row
        return Response(
            rules_js, status=200, mimetype='application/javascript',
            headers={
                'Cache-Control': 'public, max-age=300',
                'X-Compiled-At': str(compiled_at),
                'X-Song-Names':  song_names or '',
            }
        )

    except Exception as e:
        logger.exception("Failed to serve rules.js")
        stub = (
            f"// Error: {e}\n"
            "export const metadata = {};\n"
            "export const musicRules = {};\n"
            "export const ruleLibrary = {};\n"
        )
        return Response(stub, status=500, mimetype='application/javascript')


# ── STEP 1: ANALYZE ALL SONGS ─────────────────────────────────────────────────

@rules_serve_bp.route('/api/audio/rebuild-rules', methods=['POST'])
def rebuild_rules():
    """
    Analyze all songs synchronously and return when done.
    The frontend waits for this response before triggering compile-rules.
    """
    import requests as req

    base = os.environ.get("INGEST_URL", "").rstrip("/")
    if not base:
        return jsonify({"success": False, "error": "INGEST_URL not set"}), 500

    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("SELECT id, song_name FROM audio_songs ORDER BY id")
            songs = cur.fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"success": False, "error": f"Could not fetch songs: {e}"}), 500

    results = []
    for song_id, song_name in songs:
        try:
            r = req.post(f"{base}/api/audio/analyze/{song_id}", timeout=120)
            result = r.json()
            results.append({
                "song_id":   song_id,
                "song_name": song_name,
                "phrases":   result.get("phrases", 0),
                "prefs":     result.get("preference_records", 0),
            })
            logger.info(f"[rebuild] ✓ '{song_name}' analyzed")
        except Exception as e:
            logger.warning(f"[rebuild] ✗ '{song_name}': {e}")
            results.append({"song_id": song_id, "song_name": song_name, "error": str(e)})

    return jsonify({
        "success": True,
        "songs_analyzed": len(results),
        "results": results,
        "message": "Analysis complete. Now POST /api/audio/compile-rules to rebuild rules.js"
    }), 200


# ── STEP 2: COMPILE RULES → NEON ─────────────────────────────────────────────

@rules_serve_bp.route('/api/audio/compile-rules', methods=['POST'])
def compile_rules_endpoint():
    """
    Compile rules from analyzed data and save fresh rules.js to Neon.
    Fast (~5-10s). Called by the frontend after rebuild-rules completes.
    """
    try:
        from api.audio.rules import compile_rules
        stats = compile_rules(all_songs=True, write_file=False)
        logger.info(f"[compile] ✓ rules.js saved — {stats['transitions']} transitions, "
                    f"{stats['motifs']} motifs")
        return jsonify({"success": True, **stats}), 200
    except Exception as e:
        logger.exception("[compile] Rule compilation failed")
        return jsonify({"success": False, "error": str(e)}), 500