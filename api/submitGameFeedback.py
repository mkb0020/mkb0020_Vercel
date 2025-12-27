#HANDLES TEST FORM SUBMISSIONS

# /api/submit.py
import os
import psycopg
from flask import Flask, request, jsonify  # Flask style for familiarity
import json
import requests  # For sending email via an API like Resend

# Optional: For local testing with .env
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment variable
DB_URL = os.environ.get("DATABASE_URL")  # Neon provides this

# Email config (example using Resend API)
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL")  # Your email

def handler(request):
    try:
        # 1️⃣ Parse JSON data from front-end
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        # 2️⃣ Insert into Neon DB
        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                # Simple example: only a few columns; expand to match your full schema
                cur.execute(
                    """
                    INSERT INTO tester_feedback (
                        cat_name,
                        beat_game,
                        feel_smile,
                        feel_chuckle,
                        final_thoughts
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        data.get("cat_name"),
                        data.get("beat_game"),
                        data.get("feel_smile"),
                        data.get("feel_chuckle"),
                        data.get("final_thoughts"),
                    ),
                )

        # 3️⃣ Send email notification
        email_payload = {
            "from": "KittyDex <no-reply@yourdomain.com>",
            "to": [NOTIFY_EMAIL],
            "subject": "New CATastrophe2 Feedback Submitted!",
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

        # 4️⃣ Return success response
        return jsonify({"success": True, "message": "Feedback submitted!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
