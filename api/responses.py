import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

responses_bp = Blueprint('responses', __name__)

@responses_bp.route('/api/responses', methods=['GET', 'POST'])
def handle_responses():
    """
    GET  — retrieve stored A/B response pairs (paginated via ?limit=&offset=)
    POST — store a new prompt + A/B response pair
    """

    if request.method == 'GET':
        try:
            limit  = int(request.args.get('limit', 20))
            offset = int(request.args.get('offset', 0))

            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, prompt, response_a, response_b, source, created_at
                        FROM response_pairs
                        ORDER BY created_at DESC
                        LIMIT %s OFFSET %s
                    """, (limit, offset))

                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()

                    pairs = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        pairs.append(row_dict)

            return jsonify({"success": True, "data": pairs})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400

            prompt      = data.get("prompt", "").strip()
            response_a  = data.get("response_a", "").strip()
            response_b  = data.get("response_b", "").strip()
            source      = data.get("source", "manual").strip()

            if not prompt or not response_a or not response_b:
                return jsonify({
                    "success": False,
                    "error": "prompt, response_a, and response_b are all required"
                }), 400

            if len(prompt) > 2000:
                return jsonify({"success": False, "error": "Prompt too long (max 2000 chars)"}), 400
            if len(response_a) > 5000 or len(response_b) > 5000:
                return jsonify({"success": False, "error": "Response too long (max 5000 chars)"}), 400

            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO response_pairs (prompt, response_a, response_b, source)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id, created_at
                    """, (prompt, response_a, response_b, source))

                    result = cur.fetchone()
                    pair_id    = result[0]
                    created_at = result[1]

            return jsonify({
                "success": True,
                "message": "Response pair stored successfully!",
                "pair_id": pair_id,
                "created_at": created_at.isoformat()
            }), 201

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


@responses_bp.route('/api/responses/<int:pair_id>', methods=['GET', 'DELETE'])
def handle_single_response(pair_id):
    """
    GET    — fetch one pair by ID
    DELETE — remove a pair (cascades to its comparisons)
    """

    if request.method == 'GET':
        try:
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, prompt, response_a, response_b, source, created_at
                        FROM response_pairs WHERE id = %s
                    """, (pair_id,))

                    row = cur.fetchone()
                    if not row:
                        return jsonify({"success": False, "error": "Pair not found"}), 404

                    columns = [desc[0] for desc in cur.description]
                    result = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        if hasattr(value, 'isoformat'):
                            value = value.isoformat()
                        result[col] = value

            return jsonify({"success": True, "data": result})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM response_pairs WHERE id = %s RETURNING id",
                        (pair_id,)
                    )
                    deleted = cur.fetchone()

            if not deleted:
                return jsonify({"success": False, "error": "Pair not found"}), 404

            return jsonify({"success": True, "message": f"Pair #{pair_id} deleted"})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500