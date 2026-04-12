import os
import json
import requests
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL")

wormhole_feedback_bp = Blueprint('wormhole_feedback', __name__)


@wormhole_feedback_bp.route('/api/wormhole-feedback', methods=['POST'])
def handle_wormhole_feedback():
    """
    Accepts multipart/form-data (text fields + optional JSON file upload).
    Stores the submission in the `wormholes` table and fires a notification
    email via Resend that includes the session recording inline if provided.
    """
    try:
        name                = request.form.get("name", "").strip()
        device              = request.form.get("device", "").strip()
        phone_model         = request.form.get("phone_model", "").strip() or None
        controls_intuitive  = request.form.get("controls_intuitive", "").strip()
        did_beat            = request.form.get("did_beat", "").strip()
        difficulty          = request.form.get("difficulty", "").strip()
        lagging             = request.form.get("lagging", "").strip()
        lagging_details     = request.form.get("lagging_details", "").strip() or None
        notes               = request.form.get("notes", "").strip() or None

        required = {
            "name": name,
            "device": device,
            "controls_intuitive": controls_intuitive,
            "did_beat": did_beat,
            "difficulty": difficulty,
            "lagging": lagging,
        }
        missing = [k for k, v in required.items() if not v]
        if missing:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing)}"
            }), 400

        if len(name) > 100:
            return jsonify({"success": False, "error": "Name too long (max 100 chars)"}), 400
        if len(device) > 100:
            return jsonify({"success": False, "error": "Device too long (max 100 chars)"}), 400
        if notes and len(notes) > 2000:
            return jsonify({"success": False, "error": "Notes too long (max 2000 chars)"}), 400
        if lagging_details and len(lagging_details) > 500:
            return jsonify({"success": False, "error": "Lagging details too long (max 500 chars)"}), 400

        session_data = None
        session_text_for_email = None

        session_file = request.files.get("session_file")
        if session_file and session_file.filename:
            if not session_file.filename.lower().endswith(".json"):
                return jsonify({"success": False, "error": "Session file must be a .json file"}), 400
            try:
                raw = session_file.read().decode("utf-8")
                session_data = json.loads(raw)
                # Pretty-print for the email so it's human-readable
                session_text_for_email = json.dumps(session_data, indent=2)
            except (UnicodeDecodeError, json.JSONDecodeError) as parse_err:
                return jsonify({
                    "success": False,
                    "error": f"Could not parse session JSON: {parse_err}"
                }), 400

        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO wormholes (
                        name, device, phone_model,
                        controls_intuitive, did_beat, difficulty,
                        lagging, lagging_details, notes, session_data
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, created_at
                    """,
                    (
                        name, device, phone_model,
                        controls_intuitive, did_beat, difficulty,
                        lagging, lagging_details, notes,
                        json.dumps(session_data) if session_data else None,
                    )
                )
                result = cur.fetchone()
                feedback_id = result[0]
                created_at  = result[1]

        device_line = device
        if phone_model:
            device_line += f" ({phone_model})"

        session_section = (
            f"\n\nSESSION RECORDING\n{'─' * 40}\n{session_text_for_email}"
            if session_text_for_email
            else "\n\nSession recording: not provided"
        )

        email_body = f"""New playtester feedback for Wormholes All The Way Down!

Feedback ID : #{feedback_id}
Name        : {name}
Device      : {device_line}
Submitted   : {created_at}

─── GAMEPLAY ───────────────────────────────────
Controls intuitive : {controls_intuitive}
Beat the game      : {did_beat}
Difficulty         : {difficulty}

─── PERFORMANCE ────────────────────────────────
Lagging            : {lagging}
Lagging details    : {lagging_details or 'N/A'}

─── OTHER NOTES ────────────────────────────────
{notes or '(none)'}
{session_section}
"""

        email_payload = {
            "from": "Niels <onboarding@resend.dev>",
            "to": [NOTIFY_EMAIL],
            "subject": f"🌀 WORMHOLE PLAYTEST #{feedback_id} — {name} ({device})",
            "text": email_body,
        }

        requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(email_payload),
            timeout=10,
        )

        return jsonify({
            "success": True,
            "message": "Feedback submitted successfully!",
            "feedback_id": feedback_id,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500