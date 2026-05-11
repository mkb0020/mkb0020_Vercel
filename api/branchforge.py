"""
api/branchforge.py
──────────────────
BranchForge  ×  Neon  —  RLHF Pipeline Endpoints

Routes
------
POST  /api/branchforge/publish
      Publish (or re-publish) a full story from the Tauri app.
      Creates a bf_stories row (or updates if story_id is supplied),
      then upserts every scene.  Returns { story_id } so the client
      can write it back into story.json for future re-publishes.

GET   /api/branchforge/stories
      List all published stories (id, title, premise, node_count).

GET   /api/branchforge/stories/<story_id>/scenes
      Return all scenes for a story — used by Irreducible Inconvenience
      to drive the game.  Supports ?node_id= for a single scene lookup.

POST  /api/branchforge/prefer
      Log a player's A/B choice for a scene.
      Body: { scene_id, preferred, session_id?, reason? }

GET   /api/branchforge/stats/<scene_id>
      Vote tallies for one scene (A vs B).  Called after a player votes
      to show live results or feed the reward model.

GET   /api/branchforge/session/<session_id>
      Full playthrough log for an anonymous player session — useful
      for reconstructing the complete preference trajectory.
"""

import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

branchforge_bp = Blueprint("branchforge", __name__)


# ── HELPERS ──────────────────────────────────────────────────────────────────
def _row_to_dict(row, columns):
    d = {}
    for i, col in enumerate(columns):
        val = row[i]
        if hasattr(val, "isoformat"):
            val = val.isoformat()
        d[col] = val
    return d


def _compute_depth(nodes_dict, node_id, memo=None):
    """Walk up the parent chain to compute tree depth."""
    if memo is None:
        memo = {}
    if node_id in memo:
        return memo[node_id]
    node = nodes_dict.get(node_id)
    if not node or not node.get("parentId"):
        memo[node_id] = 0
        return 0
    depth = 1 + _compute_depth(nodes_dict, node["parentId"], memo)
    memo[node_id] = depth
    return depth


# ── PUBLISH ──────────────────────────────────────────────────────────────────
@branchforge_bp.route("/api/branchforge/publish", methods=["POST"])
def publish_story():
    """
    Body shape (mirrors BranchForge's data object):
    {
      "story_id":   123,          // optional — omit on first publish
      "title":      "Irreducible Inconvenience",
      "premise":    "...",
      "nodes": {
        "n1_abc": {
          "id":          "n1_abc",
          "prompt":      "Scene text...",
          "choices":     { "A": "Choice A text", "B": "Choice B text" },
          "parentId":    null,
          "parentChoice": null,
          "isFinal":     false,
          "metadata":    { "tone": "", "tags": "" }
        },
        ...
      },
      "rootId": "n1_abc"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        story_id  = data.get("story_id")        # NONE - CREATES NEW
        title     = (data.get("title") or "Untitled Story").strip()[:200]
        premise   = (data.get("premise") or "").strip()[:4000]
        nodes     = data.get("nodes", {})
        root_id   = data.get("rootId")

        if not nodes or not root_id:
            return jsonify({"success": False, "error": "nodes and rootId are required"}), 400

        depth_memo = {} # PRE-COMPUTE DEPTHS SO WE CAN ORDER SCENES IN THE GAME
        for nid in nodes: 
            _compute_depth(nodes, nid, depth_memo)

        node_count = len(nodes)

        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:

                # ── UPSERT STORY ──────────────────────────────────────
                if story_id:
                    cur.execute("""
                        UPDATE bf_stories
                           SET title      = %s,
                               premise    = %s,
                               node_count = %s,
                               updated_at = now()
                         WHERE id = %s
                        RETURNING id
                    """, (title, premise, node_count, story_id))
                    row = cur.fetchone()
                    if not row:
                        # story_id WAS STALE - CREATE FRESH
                        story_id = None

                if not story_id:
                    cur.execute("""
                        INSERT INTO bf_stories (title, premise, node_count)
                        VALUES (%s, %s, %s)
                        RETURNING id
                    """, (title, premise, node_count))
                    story_id = cur.fetchone()[0]

                # ── UPSERT SCENES ─────────────────────────────────────
                for node in nodes.values():
                    nid         = node.get("id", "")
                    scene_text  = (node.get("prompt") or "").strip()
                    choices     = node.get("choices") or {}
                    choice_a    = (choices.get("A") or "").strip()
                    choice_b    = (choices.get("B") or "").strip()
                    parent_id   = node.get("parentId")
                    parent_ch   = node.get("parentChoice")
                    is_final    = bool(node.get("isFinal", False))
                    is_root     = nid == root_id
                    depth       = depth_memo.get(nid, 0)
                    meta        = node.get("metadata") or {}
                    tone        = (meta.get("tone") or "").strip()[:200] or None
                    tags        = (meta.get("tags") or "").strip()[:500] or None

                    cur.execute("""
                        INSERT INTO bf_scenes
                            (story_id, node_id, parent_node_id, parent_choice,
                             scene_text, choice_a, choice_b,
                             is_final, is_root, depth, tone, tags, updated_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, now())
                        ON CONFLICT (story_id, node_id) DO UPDATE SET
                            parent_node_id = EXCLUDED.parent_node_id,
                            parent_choice  = EXCLUDED.parent_choice,
                            scene_text     = EXCLUDED.scene_text,
                            choice_a       = EXCLUDED.choice_a,
                            choice_b       = EXCLUDED.choice_b,
                            is_final       = EXCLUDED.is_final,
                            is_root        = EXCLUDED.is_root,
                            depth          = EXCLUDED.depth,
                            tone           = EXCLUDED.tone,
                            tags           = EXCLUDED.tags,
                            updated_at     = now()
                    """, (
                        story_id, nid, parent_id, parent_ch,
                        scene_text, choice_a, choice_b,
                        is_final, is_root, depth, tone, tags,
                    ))

                # ── PRUNE DELETED NODES ───────────────────────────────
                # ANY NODE_ID IN THE DB BUT NOT IN THIS PUBLISH IS GONE
                live_node_ids = list(nodes.keys())
                if live_node_ids:
                    cur.execute("""
                        DELETE FROM bf_scenes
                         WHERE story_id = %s
                           AND node_id != ALL(%s::text[])
                    """, (story_id, live_node_ids))

        return jsonify({
            "success":    True,
            "story_id":   story_id,
            "node_count": node_count,
            "message":    f"Story published — {node_count} scenes synced to Neon.",
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── LIST STORIES ──────────────────────────────────────────────────────────────

@branchforge_bp.route("/api/branchforge/stories", methods=["GET"])
def list_stories():
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, title, premise, node_count, created_at, updated_at
                      FROM bf_stories
                     ORDER BY updated_at DESC
                """)
                cols  = [d[0] for d in cur.description]
                rows  = [_row_to_dict(r, cols) for r in cur.fetchall()]
        return jsonify({"success": True, "data": rows})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── FETCH SCENES ──────────────────────────────────────────────────────────────

@branchforge_bp.route("/api/branchforge/stories/<int:story_id>/scenes", methods=["GET"])
def get_scenes(story_id):
    """
    Returns all scenes for a story, ordered by depth then id.
    Optional ?node_id=<id> to fetch a single scene.

    Used by Irreducible Inconvenience to drive the game loop:
      - Fetch root scene (is_root=true)
      - Player picks A or B  →  POST /api/branchforge/prefer
      - Fetch next scene via node_id from child_ids reconstruction
        (the game reconstructs the tree from parent_node_id links)
    """
    try:
        node_id_filter = request.args.get("node_id")

        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                if node_id_filter:
                    cur.execute("""
                        SELECT id, story_id, node_id, parent_node_id, parent_choice,
                               scene_text, choice_a, choice_b,
                               is_final, is_root, depth, tone, tags,
                               created_at, updated_at
                          FROM bf_scenes
                         WHERE story_id = %s AND node_id = %s
                    """, (story_id, node_id_filter))
                    row = cur.fetchone()
                    if not row:
                        return jsonify({"success": False, "error": "Scene not found"}), 404
                    cols = [d[0] for d in cur.description]
                    return jsonify({"success": True, "data": _row_to_dict(row, cols)})

                cur.execute("""
                    SELECT id, story_id, node_id, parent_node_id, parent_choice,
                           scene_text, choice_a, choice_b,
                           is_final, is_root, depth, tone, tags,
                           created_at, updated_at
                      FROM bf_scenes
                     WHERE story_id = %s
                     ORDER BY depth, id
                """, (story_id,))
                cols = [d[0] for d in cur.description]
                rows = [_row_to_dict(r, cols) for r in cur.fetchall()]

        return jsonify({"success": True, "data": rows, "count": len(rows)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── LOG PREFERENCE ────────────────────────────────────────────────────────────

@branchforge_bp.route("/api/branchforge/prefer", methods=["POST"])
def log_preference():
    """
    Body: { scene_id, preferred, session_id?, reason? }

    preferred must be 'A' or 'B'.
    session_id is a client-generated anonymous UUID — lets us reconstruct
    each player's full playthrough for the reward model.
    """
    try:
        data      = request.get_json()
        scene_id  = data.get("scene_id")
        preferred = (data.get("preferred") or "").strip().upper()
        session_id = (data.get("session_id") or "").strip()[:100] or None
        reason    = (data.get("reason") or "").strip()[:1000] or None

        if not scene_id or preferred not in ("A", "B"):
            return jsonify({
                "success": False,
                "error":   "scene_id and preferred ('A' or 'B') are required",
            }), 400

        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM bf_scenes WHERE id = %s", (scene_id,))
                if not cur.fetchone():
                    return jsonify({"success": False, "error": f"Scene #{scene_id} not found"}), 404

                cur.execute("""
                    INSERT INTO bf_preferences (scene_id, preferred, session_id, reason)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, created_at
                """, (scene_id, preferred, session_id, reason))
                pref_id, created_at = cur.fetchone()

        return jsonify({
            "success":    True,
            "pref_id":    pref_id,
            "created_at": created_at.isoformat(),
            "message":    "Preference logged.",
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── SCENE STATS ───────────────────────────────────────────────────────────────

@branchforge_bp.route("/api/branchforge/stats/<int:scene_id>", methods=["GET"])
def scene_stats(scene_id):
    """
    Vote tallies for one scene — call after a player chooses to show
    live community preference data (gamification hook).
    """
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*) FILTER (WHERE preferred = 'A') AS votes_a,
                        COUNT(*) FILTER (WHERE preferred = 'B') AS votes_b,
                        COUNT(*)                                 AS total
                      FROM bf_preferences
                     WHERE scene_id = %s
                """, (scene_id,))
                votes_a, votes_b, total = cur.fetchone()

        pct_a = round((votes_a / total * 100) if total else 0, 1)
        pct_b = round((votes_b / total * 100) if total else 0, 1)

        return jsonify({
            "success":  True,
            "scene_id": scene_id,
            "votes_a":  votes_a,
            "votes_b":  votes_b,
            "total":    total,
            "pct_a":    pct_a,
            "pct_b":    pct_b,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ── SESSION PLAYTHROUGH ───────────────────────────────────────────────────────

@branchforge_bp.route("/api/branchforge/session/<session_id>", methods=["GET"])
def get_session(session_id):
    """
    Full ordered preference log for one anonymous player session.
    Useful for reward model training — gives you the complete A/B
    trajectory a player took through the story.
    """
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        p.id           AS pref_id,
                        p.scene_id,
                        p.preferred,
                        p.reason,
                        p.created_at,
                        s.node_id,
                        s.parent_node_id,
                        s.parent_choice,
                        s.scene_text,
                        s.choice_a,
                        s.choice_b,
                        s.depth,
                        s.story_id
                      FROM bf_preferences p
                      JOIN bf_scenes s ON s.id = p.scene_id
                     WHERE p.session_id = %s
                     ORDER BY p.created_at
                """, (session_id,))
                cols = [d[0] for d in cur.description]
                rows = [_row_to_dict(r, cols) for r in cur.fetchall()]

        return jsonify({
            "success":    True,
            "session_id": session_id,
            "data":       rows,
            "count":      len(rows),
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500