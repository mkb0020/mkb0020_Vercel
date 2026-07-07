# api/appStore/checkout.py
# Stripe checkout flow for the "support this project" value-for-value model.
# All apps are free forever; this just handles the optional support payment.

import os
import psycopg2
import stripe
from flask import Blueprint, request, jsonify

appstore_checkout_bp = Blueprint('appstore_checkout', __name__, url_prefix='/api/appstore')

stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Pre-created in the Stripe Dashboard: Product > Price > "Customer chooses price".
# One shared price reused across every app -- metadata tells you which app it came from.
SUPPORT_PRICE_ID = os.environ.get('STRIPE_SUPPORT_PRICE_ID')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
SITE_URL = os.environ.get('SITE_URL', 'https://mkb0020.vercel.app')


@appstore_checkout_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    Called from an app's detail page when someone clicks "Support this project".
    Expects JSON body: { "app_id": "captron-x", "app_name": "CAPTRON-X" }
    Returns: { "url": "<stripe checkout url>" } for the frontend to redirect to.
    """
    data = request.get_json(silent=True) or {}
    app_id = data.get('app_id', 'unknown')
    app_name = data.get('app_name', 'Unknown App')

    if not SUPPORT_PRICE_ID:
        return jsonify({'error': 'STRIPE_SUPPORT_PRICE_ID is not configured'}), 500

    try:
        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{'price': SUPPORT_PRICE_ID, 'quantity': 1}],
            success_url=f'{SITE_URL}/appstore/support-success?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=f'{SITE_URL}/appstore/support-cancel?app_id={app_id}',
            metadata={'app_id': app_id, 'app_name': app_name},
            client_reference_id=app_id,
        )
        return jsonify({'url': session.url})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@appstore_checkout_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Used by the success page to show "thanks for supporting <app_name>"
    without relying solely on the webhook having already fired.
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return jsonify({
            'app_name': session.metadata.get('app_name'),
            'amount_total': session.amount_total,
            'currency': session.currency,
            'payment_status': session.payment_status,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@appstore_checkout_bp.route('/webhook', methods=['POST'])
def stripe_webhook():
    """
    Register this endpoint's full URL in the Stripe Dashboard
    (Developers > Webhooks) listening for checkout.session.completed.
    """
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return jsonify({'error': 'invalid signature'}), 400

    if event['type'] == 'checkout.session.completed':
        _record_support(event['data']['object'])

    return jsonify({'received': True})


def _record_support(session):
    """
    Logs a completed support payment to Neon.
    Swap this for your existing db connection helper if you have a shared one --
    the SQL and shape of what gets stored is the part that matters.
    """
    conn = None
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO appstore_supporters
                (app_id, app_name, amount_total, currency, stripe_session_id, customer_email, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (stripe_session_id) DO NOTHING
        """, (
            session.get('metadata', {}).get('app_id'),
            session.get('metadata', {}).get('app_name'),
            session.get('amount_total'),
            session.get('currency'),
            session.get('id'),
            (session.get('customer_details') or {}).get('email'),
        ))
        conn.commit()
        cur.close()
    except Exception as e:
        # Don't let a DB hiccup break the webhook ack -- Stripe will retry
        # the event anyway if you return a non-2xx, so just log for now.
        print(f"[appStore] Failed to record support event: {e}")
    finally:
        if conn:
            conn.close()