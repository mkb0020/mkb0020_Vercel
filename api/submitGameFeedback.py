import os
import psycopg
from flask import Blueprint, request, jsonify  
import json
import requests  
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")  
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL")

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/api/feedback', methods=['GET', 'POST'])
def handle_feedback():
    """
    Handles both GET (retrieve feedback) and POST (submit feedback) requests
    """
    
    if request.method == 'GET':
        try:
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT 
                            id,
                            submitted_at,
                            name,
                            cat_name,
                            game_completed,
                            reason_not_complete,
                            smile,
                            puns_chuckle,
                            frustrated,
                            play_clear,
                            mechanics_slider,
                            engagement_slider,
                            challenge_slider,
                            reasonable_to_beat,
                            cat_connection,
                            more_levels,
                            save_feature,
                            color_slider,
                            animation_slider,
                            background_slider,
                            favorite_move,
                            familiar_with_box,
                            story_followed,
                            quantum_explanation_needed,
                            quantum_fun,
                            quantum_jokes,
                            jump_physics,
                            horizontal_speed,
                            platform_difficulty,
                            platform_sizes_good,
                            platform_spacing_good,
                            platform_height_good,
                            platform_quantity,
                            level_time,
                            enemies_fair,
                            enemies_placement,
                            enemies_quantity,
                            level_end_clear,
                            longer_levels,
                            faster_character,
                            level_frustration,
                            boss_transition,
                            boss_fair,
                            boss_progression,
                            boss_too_easy,
                            boss_pacing,
                            finish_fun,
                            favorite_finish_move,
                            boss_sounds_anim,
                            boss_frustration,
                            bugs_found,
                            bug_descriptions,
                            game_freeze,
                            freeze_when,
                            would_pay,
                            pay_what_needed,
                            pay_amount,
                            final_thoughts
                        FROM tester_feedback 
                        ORDER BY submitted_at DESC
                    """)
                    
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    
                    feedback = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        feedback.append(row_dict)
                    
                    return jsonify({"success": True, "data": feedback})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400

            def to_bool(value):
                if value == "Yes":
                    return True
                elif value == "No":
                    return False
                return None
            
            def clean_value(value):
                if value == "" or value is None:
                    return None
                return value

            jump_physics = data.get("jump_physics[]", [])
            if isinstance(jump_physics, list):
                jump_physics_str = ", ".join(jump_physics) if jump_physics else None
            else:
                jump_physics_str = clean_value(jump_physics)
            
            not_completed = data.get("not_completed_reasons", [])
            if isinstance(not_completed, list):
                not_completed_str = ", ".join(not_completed) if not_completed else None
            else:
                not_completed_str = clean_value(not_completed)

            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO tester_feedback (
                            name,
                            cat_name,
                            game_completed,
                            reason_not_complete,
                            smile,
                            puns_chuckle,
                            frustrated,
                            play_clear,
                            mechanics_slider,
                            engagement_slider,
                            challenge_slider,
                            reasonable_to_beat,
                            cat_connection,
                            more_levels,
                            save_feature,
                            color_slider,
                            animation_slider,
                            background_slider,
                            favorite_move,
                            familiar_with_box,
                            story_followed,
                            quantum_explanation_needed,
                            quantum_fun,
                            quantum_jokes,
                            jump_physics,
                            horizontal_speed,
                            platform_difficulty,
                            platform_sizes_good,
                            platform_spacing_good,
                            platform_height_good,
                            platform_quantity,
                            level_time,
                            enemies_fair,
                            enemies_placement,
                            enemies_quantity,
                            level_end_clear,
                            longer_levels,
                            faster_character,
                            level_frustration,
                            boss_transition,
                            boss_fair,
                            boss_progression,
                            boss_too_easy,
                            boss_pacing,
                            finish_fun,
                            favorite_finish_move,
                            boss_sounds_anim,
                            boss_frustration,
                            bugs_found,
                            bug_descriptions,
                            game_freeze,
                            freeze_when,
                            would_pay,
                            pay_what_needed,
                            pay_amount,
                            final_thoughts
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            clean_value(data.get("name")),
                            clean_value(data.get("cat_name")),
                            to_bool(data.get("game_completed")),
                            not_completed_str,
                            to_bool(data.get("smile")),
                            to_bool(data.get("puns_chuckle")),
                            to_bool(data.get("frustrated")),
                            to_bool(data.get("play_clear")),
                            clean_value(data.get("mechanics_slider")),
                            clean_value(data.get("engagement_slider")),
                            clean_value(data.get("challenge_slider")),
                            to_bool(data.get("reasonable_to_beat")),
                            to_bool(data.get("cat_connection")),
                            to_bool(data.get("more_levels")),
                            to_bool(data.get("save_feature")),
                            clean_value(data.get("color_slider")),
                            clean_value(data.get("animation_slider")),
                            clean_value(data.get("background_slider")),
                            clean_value(data.get("favorite_move")),
                            clean_value(data.get("familiar_with_box")),
                            clean_value(data.get("story_followed")),
                            to_bool(data.get("quantum_explanation_needed")),
                            to_bool(data.get("quantum_fun")),
                            clean_value(data.get("quantum_jokes")),
                            jump_physics_str,
                            clean_value(data.get("horizontal_speed")),
                            to_bool(data.get("platform_difficulty")),
                            to_bool(data.get("platform_sizes_good")),
                            to_bool(data.get("platform_spacing_good")),
                            to_bool(data.get("platform_height_good")),
                            clean_value(data.get("platform_quantity")),
                            clean_value(data.get("level_time")),
                            to_bool(data.get("enemies_fair")),
                            to_bool(data.get("enemies_placement")),
                            clean_value(data.get("enemies_quantity")),
                            to_bool(data.get("level_end_clear")),
                            to_bool(data.get("longer_levels")),
                            to_bool(data.get("faster_character")),
                            clean_value(data.get("level_frustration")),
                            to_bool(data.get("boss_transition")),
                            to_bool(data.get("boss_fair")),
                            to_bool(data.get("boss_progression")),
                            to_bool(data.get("boss_too_easy")),
                            clean_value(data.get("boss_pacing")),
                            to_bool(data.get("finish_fun")),
                            clean_value(data.get("favorite_finish_move")),
                            to_bool(data.get("boss_sounds_anim")),
                            clean_value(data.get("boss_frustration")),
                            to_bool(data.get("bugs_found")),
                            clean_value(data.get("bug_descriptions")),
                            to_bool(data.get("game_freeze")),
                            clean_value(data.get("freeze_when")),
                            to_bool(data.get("would_pay")),
                            clean_value(data.get("pay_what_needed")),
                            clean_value(data.get("pay_amount")),
                            clean_value(data.get("final_thoughts")),
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
            print(f"Error: {str(e)}")
            return jsonify({"success": False, "error": str(e)}), 500