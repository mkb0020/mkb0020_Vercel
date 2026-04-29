import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

compare_bp = Blueprint('compare', __name__)


@compare_bp.route('/api/compare', methods=['GET', 'POST'])
def handle_comparisons():
    """
    GET  — retrieve all stored preference votes (paginated)
    POST — submit a new preference vote for an A/B pair
    """

    if request.method == 'GET':
        try:
            limit  = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))

            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT id, response_pair_id, preferred, reason, created_at
                        FROM comparisons
                        ORDER BY created_at DESC
                        LIMIT %s OFFSET %s
                    """, (limit, offset))

                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()

                    comparisons = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        comparisons.append(row_dict)

            return jsonify({"success": True, "data": comparisons})

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400

            pair_id   = data.get("response_pair_id")
            preferred = data.get("preferred", "").strip().lower()
            reason    = data.get("reason", "").strip() or None

            if not pair_id or preferred not in ('a', 'b'):
                return jsonify({
                    "success": False,
                    "error": "response_pair_id and preferred ('a' or 'b') are required"
                }), 400

            if reason and len(reason) > 1000:
                return jsonify({"success": False, "error": "Reason too long (max 1000 chars)"}), 400

            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id FROM response_pairs WHERE id = %s", (pair_id,))
                    if not cur.fetchone():
                        return jsonify({"success": False, "error": f"Response pair #{pair_id} not found"}), 404

                    cur.execute("""
                        INSERT INTO comparisons (response_pair_id, preferred, reason)
                        VALUES (%s, %s, %s)
                        RETURNING id, created_at
                    """, (pair_id, preferred, reason))

                    result = cur.fetchone()

            return jsonify({
                "success": True,
                "message": "Vote recorded!",
                "comparison_id": result[0],
                "created_at": result[1].isoformat()
            }), 201

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500


@compare_bp.route('/api/compare/stats/<int:pair_id>', methods=['GET'])
def get_pair_stats(pair_id):
    """
    Returns vote tallies for a specific response pair.
    The frontend can call this after a vote to show live results.

    Example response:
      { "success": true, "pair_id": 1, "votes_a": 3, "votes_b": 7, "total": 10 }
    """
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*) FILTER (WHERE preferred = 'a') AS votes_a,
                        COUNT(*) FILTER (WHERE preferred = 'b') AS votes_b,
                        COUNT(*) AS total
                    FROM comparisons
                    WHERE response_pair_id = %s
                """, (pair_id,))

                row = cur.fetchone()

        return jsonify({
            "success": True,
            "pair_id": pair_id,
            "votes_a": row[0],
            "votes_b": row[1],
            "total":   row[2]
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500