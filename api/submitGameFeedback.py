import os
import psycopg
from flask import Flask, request, jsonify  
import json
import requests  
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")  

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL")  

def handler(request):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        jump_physics = data.get("jump_physics[]", [])
        if isinstance(jump_physics, list):
            jump_physics_str = ", ".join(jump_physics)
        else:
            jump_physics_str = jump_physics

        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO tester_feedback (
                        name,
                        beat_game,
                        feel_smile,
                        feel_chuckle,
                        final_thoughts,
                        mechanics_natural,
                        engagement_slider,
                        challenge_slider,
                        save_feature,
                        quantum_explanation_needed,
                        jump_physics,
                        horizontal_speed,
                        longer_levels,
                        level_frustration,
                        boss_frustration,
                        bug_descriptions,
                        pay_what_needed,
                        pay_amount
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data.get("name"),
                        data.get("beat_game"),
                        data.get("feel_smile"),
                        data.get("feel_chuckle"),
                        data.get("final_thoughts"),
                        data.get("mechanics_natural"),
                        data.get("engagement_slider"),
                        data.get("challenge_slider"),
                        data.get("save_feature"),
                        data.get("quantum_explanation_needed"),
                        jump_physics_str,
                        data.get("horizontal_speed"),
                        data.get("longer_levels"),
                        data.get("level_frustration"),
                        data.get("boss_frustration"),
                        data.get("bug_descriptions"),
                        data.get("pay_what_needed"),
                        data.get("pay_amount"),
                    ),
                )

        email_payload = {
            "from": "Niels <onboarding@resend.dev>",
            "to": [NOTIFY_EMAIL],
            "subject": "CATastrophe2 - NEW TESTER SUBMISSION!",
            "text": f"New feedback received:\n\n{json.dumps(data, indent=2)}"
        }

        requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps(email_payload)
        )

        return jsonify({"success": True, "message": "Feedback submitted!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500