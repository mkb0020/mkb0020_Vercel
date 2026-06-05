# /api/audio/rules_serve.py
#
# Two routes:
#
#   GET  /api/audio/rules.js
#       Serves the compiled rules.js string from audio_rules_cache in Neon.
#       meowREMIX.html imports this instead of the static forms/rules.js file.
#       Returns 503 with a stub module if the cache is empty (first deploy).
#
#   POST /api/audio/rebuild-rules
#       Triggers the full pipeline: analyze all songs → compile rules → save to Neon.
#       Called fire-and-forget from meowREMIX.html on page load so rules stay
#       fresh without any manual steps.
#       Runs in a background thread so the HTTP response returns immediately
#       (Vercel has a 10s response timeout on hobby plans; the full pipeline
#       takes longer than that).
#
# DB table required (run once in Neon):
#
#   CREATE TABLE IF NOT EXISTS audio_rules_cache (
#       id          INTEGER PRIMARY KEY DEFAULT 1,
#       rules_js    TEXT NOT NULL,
#       compiled_at TIMESTAMPTZ DEFAULT NOW(),
#       song_names  TEXT,
#       CHECK (id = 1)
#   );

import os
import threading
import logging
import psycopg2
from flask import Blueprint, Response, jsonify, request

logger = logging.getLogger(__name__)

rules_serve_bp = Blueprint('rules_serve', __name__)


def _connect():
    return psycopg2.connect(os.environ["DATABASE_URL"])


# ── SERVE RULES.JS FROM NEON ──────────────────────────────────────────────────

@rules_serve_bp.route('/api/audio/rules.js', methods=['GET'])
def serve_rules_js():
    """
    Serve the compiled rules.js from audio_rules_cache.
    meowREMIX.html imports this as an ES module.
    """
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("""
                SELECT rules_js, compiled_at, song_names
                FROM audio_rules_cache
                WHERE id = 1
            """)
            row = cur.fetchone()
        conn.close()

        if not row:
            # Cache empty — return a valid stub so the import doesn't crash
            stub = (
                "// rules.js not yet compiled — run POST /api/audio/rebuild-rules\n"
                "export const metadata = {};\n"
                "export const musicRules = {};\n"
                "export const ruleLibrary = {};\n"
            )
            return Response(stub, status=503, mimetype='application/javascript',
                            headers={'Cache-Control': 'no-store'})

        rules_js, compiled_at, song_names = row
        return Response(
            rules_js,
            status=200,
            mimetype='application/javascript',
            headers={
                # Cache for 5 minutes — short enough that a rebuild is picked up
                # quickly, long enough not to hammer Neon on every page load.
                'Cache-Control': 'public, max-age=300',
                'X-Compiled-At': str(compiled_at),
                'X-Song-Names':  song_names or '',
            }
        )

    except Exception as e:
        logger.exception("Failed to serve rules.js from Neon")
        error_stub = (
            f"// Error loading rules.js: {e}\n"
            "export const metadata = {};\n"
            "export const musicRules = {};\n"
            "export const ruleLibrary = {};\n"
        )
        return Response(error_stub, status=500, mimetype='application/javascript')


# ── REBUILD TRIGGER ───────────────────────────────────────────────────────────

def _run_pipeline():
    """
    Full pipeline run in a background thread:
      1. Analyze all songs (POST /api/audio/analyze/<id> for each)
      2. Compile rules and save to Neon via compile_rules()

    Step 1 calls the analyze endpoint over HTTP so it reuses all the existing
    analyze.py logic without importing it directly (avoids circular imports).
    """
    import requests as req

    base = os.environ.get("INGEST_URL", "").rstrip("/")
    if not base:
        logger.error("[rebuild] INGEST_URL not set — cannot run pipeline")
        return

    # ── Step 1: analyze all songs ─────────────────────────────────────────────
    try:
        conn = _connect()
        with conn.cursor() as cur:
            cur.execute("SELECT id, song_name FROM audio_songs ORDER BY id")
            songs = cur.fetchall()
        conn.close()
    except Exception as e:
        logger.error(f"[rebuild] Could not fetch song list: {e}")
        return

    logger.info(f"[rebuild] Analyzing {len(songs)} songs...")
    for song_id, song_name in songs:
        try:
            r = req.post(f"{base}/api/audio/analyze/{song_id}", timeout=120)
            result = r.json()
            pref_count = result.get('preference_records', 0)
            logger.info(f"[rebuild]   ✓ '{song_name}' — {result.get('phrases', 0)} phrases, "
                        f"{pref_count} preference records")
        except Exception as e:
            logger.warning(f"[rebuild]   ✗ '{song_name}' (id={song_id}): {e}")

    # ── Step 2: compile rules → save to Neon ─────────────────────────────────
    try:
        logger.info("[rebuild] Compiling rules (all songs blend)...")
        # Import here to avoid circular imports at module load time
        from api.audio.rules import compile_rules
        stats = compile_rules(all_songs=True, write_file=False)
        logger.info(f"[rebuild] ✓ rules.js saved — {stats['transitions']} transitions, "
                    f"{stats['motifs']} motifs, source: {stats['song_name']}")
    except Exception as e:
        logger.exception(f"[rebuild] Rule compilation failed: {e}")


@rules_serve_bp.route('/api/audio/rebuild-rules', methods=['POST'])
def rebuild_rules():
    """
    Fire-and-forget endpoint. Starts the full pipeline in a background thread
    and returns immediately so Vercel's response timeout isn't hit.

    Called by meowREMIX.html on every page load (fetch with keepalive).
    Also callable manually: POST /api/audio/rebuild-rules
    """
    t = threading.Thread(target=_run_pipeline, daemon=True)
    t.start()
    return jsonify({
        "success": True,
        "message": "Pipeline started in background. "
                   "Fresh rules.js will be available at /api/audio/rules.js "
                   "in ~30–60 seconds."
    }), 202