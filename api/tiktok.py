"""
api/tiktok.py
TikTok OAuth 2.0 + Content Posting blueprint for mkb0020 Vercel app.

Endpoints:
  POST /api/tiktok/exchange   — exchanges PKCE auth code for tokens, stores in Supabase
  POST /api/tiktok/refresh    — refreshes an expiring access token
  GET  /api/tiktok/status     — returns current token status (connected / expired / missing)
  POST /api/tiktok/post       — initiates inbox upload (draft) for a video from social-marketing-vids bucket
  GET  /api/tiktok/post/status — polls publish status by publish_id

Token storage: supabase table `tiktok_tokens` (see migration at bottom of file)
"""

import os
import time
import requests
from flask import Blueprint, request, jsonify
from .supabase_helper import get_supabase_client

tiktok_bp = Blueprint("tiktok", __name__)

TIKTOK_TOKEN_URL   = "https://open.tiktokapis.com/v2/oauth/token/"
TIKTOK_REVOKE_URL  = "https://open.tiktokapis.com/v2/oauth/revoke/"
TIKTOK_POST_INIT   = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"
TIKTOK_POST_STATUS = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

CLIENT_KEY    = os.environ.get("TIKTOK_CLIENT_KEY")
CLIENT_SECRET = os.environ.get("TIKTOK_CLIENT_SECRET")
AUTH_PASSWORD = os.environ.get("CATFORCE_ADMIN_PASSWORD")  # reuse existing auth header pattern

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")  # service role — server side only


# ---------------------------------------------------------------------------
# Auth guard (same X-CatForce-Auth pattern used elsewhere in the app)
# ---------------------------------------------------------------------------

def _check_auth():
    provided = request.headers.get("X-CatForce-Auth", "")
    if not AUTH_PASSWORD or provided != AUTH_PASSWORD:
        return jsonify({"error": "unauthorized"}), 401
    return None


# ---------------------------------------------------------------------------
# Supabase token helpers
# ---------------------------------------------------------------------------

def _save_tokens(open_id: str, access_token: str, refresh_token: str,
                 access_expires_in: int, refresh_expires_in: int):
    """Upsert token row keyed on open_id."""
    sb = get_supabase_client()
    now = int(time.time())
    sb.table("tiktok_tokens").upsert({
        "open_id":              open_id,
        "access_token":         access_token,
        "refresh_token":        refresh_token,
        "access_expires_at":    now + access_expires_in,
        "refresh_expires_at":   now + refresh_expires_in,
        "updated_at":           "now()",
    }, on_conflict="open_id").execute()


def _load_tokens():
    """Return the first (and only expected) token row, or None."""
    sb = get_supabase_client()
    result = sb.table("tiktok_tokens").select("*").limit(1).execute()
    if result.data:
        return result.data[0]
    return None


def _get_valid_access_token():
    """
    Returns a valid access_token, auto-refreshing if within 5 min of expiry.
    Raises RuntimeError if tokens are missing or refresh_token is also expired.
    """
    row = _load_tokens()
    if not row:
        raise RuntimeError("no_tokens")

    now = int(time.time())

    # Refresh token itself expired — need full re-auth
    if now >= row["refresh_expires_at"]:
        raise RuntimeError("refresh_expired")

    # Access token still valid (with 5-min buffer)
    if now < row["access_expires_at"] - 300:
        return row["access_token"], row["open_id"]

    # Access token needs refresh
    resp = requests.post(
        TIKTOK_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"},
        data={
            "client_key":     CLIENT_KEY,
            "client_secret":  CLIENT_SECRET,
            "grant_type":     "refresh_token",
            "refresh_token":  row["refresh_token"],
        },
    )
    resp.raise_for_status()
    data = resp.json()

    if "access_token" not in data:
        raise RuntimeError(f"refresh_failed: {data}")

    _save_tokens(
        open_id             = data.get("open_id", row["open_id"]),
        access_token        = data["access_token"],
        refresh_token       = data.get("refresh_token", row["refresh_token"]),
        access_expires_in   = data.get("expires_in", 86400),
        refresh_expires_in  = data.get("refresh_expires_in", 31536000),
    )
    return data["access_token"], data.get("open_id", row["open_id"])


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@tiktok_bp.route("/api/tiktok/exchange", methods=["POST"])
def exchange_code():
    """
    Exchanges PKCE auth code for tokens and persists them.
    Body (JSON): { code, code_verifier, redirect_uri }
    redirect_uri must match what was used to initiate the flow
    (e.g. http://localhost:PORT/callback — dynamic port from tauri-plugin-oauth).
    """
    err = _check_auth()
    if err:
        return err

    body         = request.get_json(force=True)
    code         = body.get("code")
    code_verifier = body.get("code_verifier")
    redirect_uri = body.get("redirect_uri")

    if not all([code, code_verifier, redirect_uri]):
        return jsonify({"error": "missing_fields", "required": ["code", "code_verifier", "redirect_uri"]}), 400

    resp = requests.post(
        TIKTOK_TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"},
        data={
            "client_key":     CLIENT_KEY,
            "client_secret":  CLIENT_SECRET,
            "code":           code,
            "grant_type":     "authorization_code",
            "redirect_uri":   redirect_uri,
            "code_verifier":  code_verifier,
        },
    )

    if resp.status_code != 200:
        return jsonify({"error": "tiktok_exchange_failed", "detail": resp.text}), 502

    data = resp.json()
    if "access_token" not in data:
        return jsonify({"error": "no_access_token", "detail": data}), 502

    _save_tokens(
        open_id             = data["open_id"],
        access_token        = data["access_token"],
        refresh_token       = data["refresh_token"],
        access_expires_in   = data.get("expires_in", 86400),
        refresh_expires_in  = data.get("refresh_expires_in", 31536000),
    )

    return jsonify({
        "ok":      True,
        "open_id": data["open_id"],
        "scope":   data.get("scope", ""),
    })


@tiktok_bp.route("/api/tiktok/refresh", methods=["POST"])
def refresh_token():
    """Manually trigger a token refresh (called by CatForce on startup if token is stale)."""
    err = _check_auth()
    if err:
        return err

    try:
        access_token, open_id = _get_valid_access_token()
        return jsonify({"ok": True, "open_id": open_id})
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 401


@tiktok_bp.route("/api/tiktok/status", methods=["GET"])
def token_status():
    """Returns connection status — used by NovaPanel to show TikTok connected state."""
    err = _check_auth()
    if err:
        return err

    row = _load_tokens()
    if not row:
        return jsonify({"status": "disconnected"})

    now = int(time.time())
    if now >= row["refresh_expires_at"]:
        return jsonify({"status": "expired", "open_id": row["open_id"]})
    if now >= row["access_expires_at"]:
        return jsonify({"status": "needs_refresh", "open_id": row["open_id"]})

    return jsonify({
        "status":              "connected",
        "open_id":             row["open_id"],
        "access_expires_at":   row["access_expires_at"],
        "refresh_expires_at":  row["refresh_expires_at"],
    })


@tiktok_bp.route("/api/tiktok/post", methods=["POST"])
def post_to_tiktok():
    """
    Initiates a TikTok inbox upload (draft) for a video stored in the
    social-marketing-vids Supabase bucket.

    Body (JSON):
    {
        "post_id":    "uuid matching social_posts.id",
        "video_url":  "public supabase storage URL for the video",
        "caption":    "post text / caption with hashtags",
        "privacy":    "PUBLIC_TO_EVERYONE" | "SELF_ONLY" (default SELF_ONLY for unaudited)
    }

    Flow:
    1. Gets a valid access token (auto-refreshes if needed).
    2. Calls TikTok inbox upload init with PULL_FROM_URL.
    3. Stores publish_id in posting_history so status can be polled later.
    4. Returns publish_id to CatForce so Nova can poll for completion.
    """
    err = _check_auth()
    if err:
        return err

    body      = request.get_json(force=True)
    post_id   = body.get("post_id")
    video_url = body.get("video_url")
    caption   = body.get("caption", "")
    privacy   = body.get("privacy", "SELF_ONLY")

    if not all([post_id, video_url]):
        return jsonify({"error": "missing_fields", "required": ["post_id", "video_url"]}), 400

    try:
        access_token, open_id = _get_valid_access_token()
    except RuntimeError as e:
        return jsonify({"error": str(e), "action": "reauth_required"}), 401

    # Initiate inbox upload via PULL_FROM_URL
    tiktok_resp = requests.post(
        TIKTOK_POST_INIT,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type":  "application/json; charset=UTF-8",
        },
        json={
            "source_info": {
                "source":    "PULL_FROM_URL",
                "video_url": video_url,
            }
        },
    )

    if tiktok_resp.status_code != 200:
        return jsonify({"error": "tiktok_post_init_failed", "detail": tiktok_resp.text}), 502

    tiktok_data = tiktok_resp.json()
    publish_id  = tiktok_data.get("data", {}).get("publish_id")

    if not publish_id:
        return jsonify({"error": "no_publish_id", "detail": tiktok_data}), 502

    # Log to posting_history (reuses existing table pattern)
    sb = get_supabase_client()
    sb.table("posting_history").insert({
        "social_post_id": post_id,
        "platform":       "tiktok",
        "status":         "uploading",
        "tiktok_publish_id": publish_id,
        "open_id":        open_id,
    }).execute()

    # Update last_used_at on the source post
    sb.table("social_posts").update({"last_used_at": "now()"}).eq("id", post_id).execute()

    return jsonify({
        "ok":         True,
        "publish_id": publish_id,
        "note":       "Video sent to TikTok inbox as draft. Open TikTok app to review and post.",
    })


@tiktok_bp.route("/api/tiktok/post/status", methods=["GET"])
def post_status():
    """
    Polls TikTok for publish status.
    Query param: ?publish_id=v_inbox_file~v2.xxx
    """
    err = _check_auth()
    if err:
        return err

    publish_id = request.args.get("publish_id")
    if not publish_id:
        return jsonify({"error": "missing publish_id"}), 400

    try:
        access_token, _ = _get_valid_access_token()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 401

    resp = requests.post(
        TIKTOK_POST_STATUS,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type":  "application/json; charset=UTF-8",
        },
        json={"publish_id": publish_id},
    )

    if resp.status_code != 200:
        return jsonify({"error": "status_check_failed", "detail": resp.text}), 502

    data   = resp.json().get("data", {})
    status = data.get("status", "unknown")

    # Keep posting_history in sync
    sb = get_supabase_client()
    sb.table("posting_history") \
      .update({"status": status.lower()}) \
      .eq("tiktok_publish_id", publish_id) \
      .execute()

    return jsonify({"ok": True, "publish_id": publish_id, "status": status, "detail": data})


