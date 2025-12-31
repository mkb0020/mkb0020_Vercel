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

support_bp = Blueprint('support', __name__)

@support_bp.route('/api/support', methods=['GET', 'POST', 'PATCH'])
def handle_support():
    """
    Handles GET (retrieve tickets), POST (submit ticket), and PATCH (update status) requests
    """
    
    if request.method == 'GET':
        try:
            with psycopg.connect(DB_URL) as conn:
                with conn.cursor() as cur:
                    # Only show tickets that aren't completed
                    cur.execute("""
                        SELECT * FROM support_tickets 
                        WHERE status != 'completed'
                        ORDER BY created_at DESC
                    """)
                    
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    
                    tickets = []
                    for row in rows:
                        row_dict = {}
                        for i, col in enumerate(columns):
                            value = row[i]
                            if hasattr(value, 'isoformat'):
                                value = value.isoformat()
                            row_dict[col] = value
                        tickets.append(row_dict)
                    
                    return jsonify({"success": True, "data": tickets})
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    elif request.method == 'PATCH':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400
            
            ticket_id = data.get("id")
            new_status = data.get("status")
            
            if not ticket_id or not new_status:
                return jsonify({"success": False, "error": "ID and status are required"}), 400
            
            if new_status not in ['pending', 'in_progress', 'completed']:
                return jsonify({"success": False, "error": "Invalid status"}), 400
            
            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        UPDATE support_tickets 
                        SET status = %s 
                        WHERE id = %s
                        RETURNING id
                        """,
                        (new_status, ticket_id)
                    )
                    
                    result = cur.fetchone()
                    if not result:
                        return jsonify({"success": False, "error": "Ticket not found"}), 404
            
            return jsonify({
                "success": True,
                "message": f"Ticket #{ticket_id} status updated to {new_status}"
            })
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data received"}), 400
            
            name = data.get("name", "").strip()
            page = data.get("page", "").strip()
            issue_description = data.get("issue_description", "").strip()
            
            if not name or not page or not issue_description:
                return jsonify({
                    "success": False, 
                    "error": "Name, page, and issue description are required"
                }), 400
            
            email = data.get("email", "").strip() or None
            
            if len(name) > 100:
                return jsonify({"success": False, "error": "Name too long (max 100 characters)"}), 400
            if email and len(email) > 100:
                return jsonify({"success": False, "error": "Email too long (max 100 characters)"}), 400
            if len(page) > 100:
                return jsonify({"success": False, "error": "Page name too long (max 100 characters)"}), 400
            if len(issue_description) > 2000:
                return jsonify({"success": False, "error": "Issue description too long (max 2000 characters)"}), 400
            
            with psycopg.connect(DB_URL, autocommit=True) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO support_tickets (name, email, page, issue_description)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id, created_at
                        """,
                        (name, email, page, issue_description)
                    )
                    
                    result = cur.fetchone()
                    ticket_id = result[0]
                    created_at = result[1]
            
            email_payload = {
                "from": "Niels <onboarding@resend.dev>",
                "to": [NOTIFY_EMAIL],
                "subject": f"🚨 NEW SUPPORT TICKET #{ticket_id} - {page}",
                "text": f"""New support ticket received:

Ticket ID: #{ticket_id}
Name: {name}
Email: {email if email else 'Not provided'}
Problem Page: {page}
Created: {created_at}

Issue Description:
{issue_description}

---
Reply to user: {email if email else 'No email provided'}
"""
            }
            
            requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                data=json.dumps(email_payload)
            )
            
            return jsonify({
                "success": True,
                "message": "Support ticket submitted successfully!",
                "ticket_id": ticket_id
            })
        
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500