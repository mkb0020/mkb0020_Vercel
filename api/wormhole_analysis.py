from flask import Blueprint, request, jsonify
import psycopg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
DB_URL = os.environ.get("DATABASE_URL")

wormhole_analysis_bp = Blueprint('wormhole_analysis', __name__)


@wormhole_analysis_bp.route('/api/wormhole/upload', methods=['POST'])
def upload_session():
    try:
        data = request.get_json()

        meta        = data.get("meta", {})
        config      = data.get("configSnapshot", {})
        summary     = data.get("summary", {})
        events      = data.get("events", [])

        if not summary or not events:
            return jsonify({"success": False, "error": "Invalid payload"}), 400

        cp          = config.get("COSMIC_PRISM", {})
        enemies     = config.get("ENEMIES", {})
        types       = enemies.get("TYPES", {})
        basic       = types.get("BASIC", {})
        fast        = types.get("FAST", {})
        tank        = types.get("TANK", {})
        zigzag      = types.get("ZIGZAG", {})
        flimflam    = types.get("FLIMFLAM", {})
        slime       = config.get("SLIME_ATTACK", {})
        fractal     = config.get("FRACTAL_CASCADE", {})
        wave_cfgs   = config.get("WAVE_CONFIGS", [])

        def get_wave(i):
            if i < len(wave_cfgs):
                w = wave_cfgs[i]
                return (
                    ",".join(w.get("types", [])),
                    ",".join(str(x) for x in w.get("weights", [])),
                    w.get("maxEnemies")
                )
            return (None, None, None)

        w1, w2, w3, w4, w5 = (get_wave(i) for i in range(5))

        generated_at_str = meta.get("generatedAt")
        generated_at = datetime.fromisoformat(generated_at_str.replace("Z", "+00:00")) if generated_at_str else None

        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    INSERT INTO wormhole_session_summary (
                        "generatedAt",
                        "COSMIC_PRISM_HEAL_AMOUNT",
                        "ENEMIES_SPAWN_INTERVAL_MIN", "ENEMIES_SPAWN_INTERVAL_MAX",
                        "ENEMIES_TYPES_BASIC_HEALTH", "ENEMIES_TYPES_BASIC_LASER_INTERVAL", "ENEMIES_TYPES_BASIC_COMBAT_DURATION",
                        "ENEMIES_TYPES_FAST_HEALTH",  "ENEMIES_TYPES_FAST_LASER_INTERVAL",  "ENEMIES_TYPES_FAST_COMBAT_DURATION",
                        "ENEMIES_TYPES_TANK_HEALTH",  "ENEMIES_TYPES_TANK_LASER_INTERVAL",  "ENEMIES_TYPES_TANK_COMBAT_DURATION",
                        "ENEMIES_TYPES_ZIGZAG_HEALTH","ENEMIES_TYPES_ZIGZAG_LASER_INTERVAL","ENEMIES_TYPES_ZIGZAG_COMBAT_DURATION",
                        "ENEMIES_TYPES_FLIMFLAM_HEALTH","ENEMIES_TYPES_FLIMFLAM_LASER_INTERVAL","ENEMIES_TYPES_FLIMFLAM_COMBAT_DURATION",
                        "ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MIN","ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MAX",
                        "ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MIN","ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MAX",
                        "SLIME_ATTACK_FIRST_ATTACK_MIN","SLIME_ATTACK_FIRST_ATTACK_MAX","SLIME_ATTACK_REPEAT_INTERVAL",
                        "FRACTAL_CASCADE_FIRST_DELAY_MIN","FRACTAL_CASCADE_FIRST_DELAY_MAX",
                        "FRACTAL_CASCADE_COOLDOWN_MIN","FRACTAL_CASCADE_COOLDOWN_MAX",
                        "WAVE_CONFIGS_wave1_types","WAVE_CONFIGS_wave1_weights","WAVE_CONFIGS_wave1_maxEnemies",
                        "WAVE_CONFIGS_wave2_types","WAVE_CONFIGS_wave2_weights","WAVE_CONFIGS_wave2_maxEnemies",
                        "WAVE_CONFIGS_wave3_types","WAVE_CONFIGS_wave3_weights","WAVE_CONFIGS_wave3_maxEnemies",
                        "WAVE_CONFIGS_wave4_types","WAVE_CONFIGS_wave4_weights","WAVE_CONFIGS_wave4_maxEnemies",
                        "WAVE_CONFIGS_wave5_types","WAVE_CONFIGS_wave5_weights","WAVE_CONFIGS_wave5_maxEnemies",
                        "totalEvents","damageEvents","enemyKills","enemySpawns",
                        "playerDamageCount","hpHealCount","totalHpHealed",
                        "fractalCascadeCount","slimeAttackCount","ocularPrismCount",
                        "bossEntryShipHp","bossEntryShipLives",
                        "bossBattleDuration","avgTimeToKill",
                        "waveReached","waveCleared",
                        "bossReached","gameBeaten","runOutcome"
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """, (
                    generated_at,
                    cp.get("HEAL_AMOUNT"),
                    enemies.get("SPAWN_INTERVAL_MIN"), enemies.get("SPAWN_INTERVAL_MAX"),
                    basic.get("HEALTH"),    basic.get("LASER_INTERVAL"),    basic.get("COMBAT_DURATION"),
                    fast.get("HEALTH"),     fast.get("LASER_INTERVAL"),     fast.get("COMBAT_DURATION"),
                    tank.get("HEALTH"),     tank.get("LASER_INTERVAL"),     tank.get("COMBAT_DURATION"),
                    zigzag.get("HEALTH"),   zigzag.get("LASER_INTERVAL"),   zigzag.get("COMBAT_DURATION"),
                    flimflam.get("HEALTH"), flimflam.get("LASER_INTERVAL"), flimflam.get("COMBAT_DURATION"),
                    flimflam.get("PRISM_FIRST_DELAY_MIN"), flimflam.get("PRISM_FIRST_DELAY_MAX"),
                    flimflam.get("PRISM_COOLDOWN_MIN"),    flimflam.get("PRISM_COOLDOWN_MAX"),
                    slime.get("FIRST_ATTACK_MIN"), slime.get("FIRST_ATTACK_MAX"), slime.get("REPEAT_INTERVAL"),
                    fractal.get("FIRST_DELAY_MIN"), fractal.get("FIRST_DELAY_MAX"),
                    fractal.get("COOLDOWN_MIN"),    fractal.get("COOLDOWN_MAX"),
                    w1[0], w1[1], w1[2],
                    w2[0], w2[1], w2[2],
                    w3[0], w3[1], w3[2],
                    w4[0], w4[1], w4[2],
                    w5[0], w5[1], w5[2],
                    summary.get("totalEvents"),       summary.get("damageEvents"),
                    summary.get("enemyKills"),        summary.get("enemySpawns"),
                    summary.get("playerDamageCount"), summary.get("hpHealCount"),
                    summary.get("totalHpHealed"),     summary.get("fractalCascadeCount"),
                    summary.get("slimeAttackCount"),  summary.get("ocularPrismCount"),
                    summary.get("bossEntryShipHp"),   summary.get("bossEntryShipLives"),
                    summary.get("bossBattleDuration"),summary.get("avgTimeToKill"),
                    summary.get("waveReached"),       summary.get("waveCleared"),
                    summary.get("bossReached"),       summary.get("gameBeaten"),
                    summary.get("runOutcome")
                ))

                session_key = generated_at_str

                for event in events:
                    elapsed = event.get("time", 0) or 0
                    event_time = (generated_at + timedelta(seconds=elapsed)) if generated_at else None

                    cur.execute("""
                        INSERT INTO wormhole_events (
                            "session", "type", "time", "amount", "hp", "lives", "enemyType"
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        session_key,
                        event.get("type"),
                        event_time,
                        event.get("amount"),
                        event.get("hp"),
                        event.get("lives"),
                        event.get("enemyType")
                    ))

        return jsonify({"success": True, "session": session_key})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/summary', methods=['GET'])
def get_summary():
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*),
                        AVG("waveReached"),
                        AVG("enemySpawns"),
                        AVG("enemyKills"),
                        AVG("avgTimeToKill"),
                        AVG("playerDamageCount"),
                        AVG("hpHealCount"),
                        AVG("fractalCascadeCount"),
                        AVG("slimeAttackCount"),
                        AVG("ocularPrismCount"),
                        AVG(CASE WHEN "gameBeaten" = true THEN 1.0 ELSE 0.0 END)
                    FROM wormhole_session_summary
                """)
                row = cur.fetchone()

        return jsonify({
            "success": True,
            "data": {
                "total_sessions": row[0],
                "avg_wave":       float(row[1] or 0),
                "avg_spawns":      float(row[2] or 0),
                "avg_kills":      float(row[3] or 0),
                "avg_kill_time":      float(row[4] or 0),
                "avg_hp_loss":      float(row[5] or 0),
                "avg_hp_gain":      float(row[6] or 0),
                "avg_fractal":      float(row[7] or 0),
                "avg_slime":      float(row[8] or 0),
                "avg_ocular":      float(row[9] or 0),
                "win_rate":       float(row[10] or 0)
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/hp-timeline', methods=['GET'])
def get_hp_timeline():
    try:
        limit = int(request.args.get("limit", 5))
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT to_char("generatedAt" AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')
                    FROM wormhole_session_summary
                    ORDER BY "generatedAt" DESC
                    LIMIT %s
                """, (limit,))
                sessions = [row[0] for row in cur.fetchall()]

                if not sessions:
                    return jsonify({"success": True, "sessions": [], "data": {}})

                cur.execute("""
                    SELECT
                        e."session",
                        EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) AS elapsed_seconds,
                        e."hp"
                    FROM wormhole_events e
                    JOIN wormhole_session_summary s
                    ON e."session"::timestamptz = s."generatedAt"   -- ✅ was ::text, now parses the ISO string
                    WHERE e."session" = ANY(%s)
                    AND e."hp" IS NOT NULL
                    ORDER BY e."session", e."time" ASC
                """, (sessions,))

                rows = cur.fetchall()

        result = {s: [] for s in sessions}
        for session_key, elapsed, hp in rows:
            if session_key in result:
                result[session_key].append({"x": float(elapsed), "y": int(hp)})

        return jsonify({
            "success": True,
            "sessions": sessions,
            "data": result
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/hp-average', methods=['GET'])
def get_hp_average():
    try:
        bucket = int(request.args.get("bucket", 10)) 

        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        FLOOR(
                            EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) / %s
                        ) * %s AS bucket_start,
                        AVG(e."hp") AS avg_hp
                    FROM wormhole_events e
                    JOIN wormhole_session_summary s
                    ON e."session"::timestamptz = s."generatedAt"   -- ✅ same fix
                    WHERE e."hp" IS NOT NULL
                    GROUP BY bucket_start
                    ORDER BY bucket_start ASC
                """, (bucket, bucket))

                rows = cur.fetchall()

        data = [{"x": float(row[0]), "y": round(float(row[1]), 2)} for row in rows]

        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/scatter', methods=['GET'])
def get_scatter():
    stat = request.args.get("stat")
    if not stat:
        return jsonify({"success": False, "error": "Missing stat param"}), 400
    VALID_STATS = {
        "spawn_interval",
        "heal_amount",
        "avg_enemy_health",
        "fractal_interval",
        "slime_interval",
        "prism_interval",
        "avg_time_to_kill"
    }
    if stat not in VALID_STATS:
        return jsonify({"success": False, "error": f"Unknown stat: {stat}"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                if stat == "heal_amount":
                    cur.execute("""
                        SELECT "COSMIC_PRISM_HEAL_AMOUNT", "waveCleared"
                        FROM wormhole_session_summary
                        WHERE "COSMIC_PRISM_HEAL_AMOUNT" IS NOT NULL
                          AND "waveCleared" IS NOT NULL
                        ORDER BY "COSMIC_PRISM_HEAL_AMOUNT"
                    """)
                    rows = cur.fetchall()

                elif stat == "avg_enemy_health":
                    cur.execute("""
                        SELECT
                            (
                                "ENEMIES_TYPES_BASIC_HEALTH"   +
                                "ENEMIES_TYPES_FAST_HEALTH"    +
                                "ENEMIES_TYPES_TANK_HEALTH"    +
                                "ENEMIES_TYPES_ZIGZAG_HEALTH"  +
                                "ENEMIES_TYPES_FLIMFLAM_HEALTH"
                            ) / 5.0 AS avg_health,
                            "waveCleared"
                        FROM wormhole_session_summary
                        WHERE "ENEMIES_TYPES_BASIC_HEALTH"   IS NOT NULL
                          AND "ENEMIES_TYPES_FAST_HEALTH"    IS NOT NULL
                          AND "ENEMIES_TYPES_TANK_HEALTH"    IS NOT NULL
                          AND "ENEMIES_TYPES_ZIGZAG_HEALTH"  IS NOT NULL
                          AND "ENEMIES_TYPES_FLIMFLAM_HEALTH" IS NOT NULL
                          AND "waveCleared" IS NOT NULL
                        ORDER BY avg_health
                    """)
                    rows = cur.fetchall()

                elif stat == "avg_time_to_kill":
                    cur.execute("""
                        SELECT "avgTimeToKill", "waveCleared"
                        FROM wormhole_session_summary
                        WHERE "avgTimeToKill" IS NOT NULL
                          AND "waveCleared"   IS NOT NULL
                        ORDER BY "avgTimeToKill"
                    """)
                    rows = cur.fetchall()

                else:
                    event_type_map = {
                        "spawn_interval":   "enemy_spawn",
                        "fractal_interval": "fractal_cascade_attack",
                        "slime_interval":   "slime_attack",
                        "prism_interval":   "ocular_prism_attack"
                    }
                    event_type = event_type_map[stat]

                    cur.execute("""
                        WITH event_times AS (
                            SELECT
                                "session",
                                "time",
                                LAG("time") OVER (
                                    PARTITION BY "session"
                                    ORDER BY "time"
                                ) AS prev_time
                            FROM wormhole_events
                            WHERE "type" = %s
                              AND "time" IS NOT NULL
                        ),
                        session_avg AS (
                            SELECT
                                "session",
                                AVG(
                                    EXTRACT(EPOCH FROM ("time" - prev_time))
                                ) AS avg_interval
                            FROM event_times
                            WHERE prev_time IS NOT NULL
                            GROUP BY "session"
                            HAVING COUNT(*) > 1   -- need at least 2 events to get a gap
                        )
                        SELECT sa.avg_interval, s."waveCleared"
                        FROM session_avg sa
                        JOIN wormhole_session_summary s
                          ON sa."session"::timestamptz = s."generatedAt"
                        WHERE s."waveCleared" IS NOT NULL
                        ORDER BY sa.avg_interval
                    """, (event_type,))
                    rows = cur.fetchall()

        data = [
            {"x": round(float(row[0]), 4), "y": int(row[1])}
            for row in rows
            if row[0] is not None
        ]

        return jsonify({"success": True, "stat": stat, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@wormhole_analysis_bp.route('/api/wormhole/wave-analysis', methods=['GET'])
def get_wave_analysis():
    try:
        wave   = request.args.get("wave")    
        enemy  = request.args.get("enemy")   

        if not wave or not enemy:
            return jsonify({"success": False, "error": "Missing wave or enemy param"}), 400
        if wave not in {"1","2","3","4","5"}:
            return jsonify({"success": False, "error": "Invalid wave"}), 400

        VALID_ENEMIES = {"BASIC", "FAST", "TANK", "ZIGZAG", "FLIMFLAM"}
        if enemy not in VALID_ENEMIES:
            return jsonify({"success": False, "error": "Invalid enemy"}), 400

        types_col   = f"WAVE_CONFIGS_wave{wave}_types"
        weights_col = f"WAVE_CONFIGS_wave{wave}_weights"
        max_col     = f"WAVE_CONFIGS_wave{wave}_maxEnemies"

        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT "{max_col}", COUNT(*)
                    FROM wormhole_session_summary
                    WHERE "{max_col}" IS NOT NULL
                    GROUP BY "{max_col}"
                    ORDER BY "{max_col}"
                """)
                max_enemies_dist = [
                    {"maxEnemies": row[0], "count": row[1]}
                    for row in cur.fetchall()
                ]

                cur.execute(f"""
                    SELECT
                        "{types_col}",
                        "{weights_col}",
                        "WAVE_CONFIGS_wave1_types",
                        "WAVE_CONFIGS_wave2_types",
                        "WAVE_CONFIGS_wave3_types",
                        "WAVE_CONFIGS_wave4_types",
                        "WAVE_CONFIGS_wave5_types",
                        "waveCleared"
                    FROM wormhole_session_summary
                    WHERE "waveCleared" IS NOT NULL
                """)
                rows = cur.fetchall()

        wave_num     = int(wave)
        cleared_weights   = []  
        uncleared_weights = []  
        intro_wave_results = {1: [], 2: [], 3: [], 4: [], 5: []} 

        for row in rows:
            sel_types_str, sel_weights_str = row[0], row[1]
            all_wave_types = [row[2], row[3], row[4], row[5], row[6]]
            wave_cleared   = row[7]

            if sel_types_str and sel_weights_str:
                types   = [t.strip() for t in sel_types_str.split(",")]
                weights = [w.strip() for w in sel_weights_str.split(",")]

                if enemy in types:
                    idx = types.index(enemy)
                    try:
                        weight = float(weights[idx])
                        if wave_cleared >= wave_num:
                            cleared_weights.append(weight)
                        else:
                            uncleared_weights.append(weight)
                    except (ValueError, IndexError):
                        pass

            intro_wave = None
            for w_idx, types_str in enumerate(all_wave_types, start=1):
                if types_str:
                    types = [t.strip() for t in types_str.split(",")]
                    if enemy in types:
                        intro_wave = w_idx
                        break 

            if intro_wave is not None:
                intro_wave_results[intro_wave].append(wave_cleared)

        def safe_avg(lst):
            return round(sum(lst) / len(lst), 4) if lst else None

        weight_comparison = {
            "cleared": {
                "avg_weight": safe_avg(cleared_weights),
                "count":      len(cleared_weights)
            },
            "not_cleared": {
                "avg_weight": safe_avg(uncleared_weights),
                "count":      len(uncleared_weights)
            }
        }

        intro_wave_summary = {
            str(w): {
                "avg_wave_cleared": safe_avg(vals),
                "count":            len(vals)
            }
            for w, vals in intro_wave_results.items()
            if vals  
        }

        return jsonify({
            "success":           True,
            "wave":              wave,
            "enemy":             enemy,
            "max_enemies_dist":  max_enemies_dist,
            "weight_comparison": weight_comparison,
            "intro_wave_summary": intro_wave_summary
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/sessions', methods=['GET'])
def get_sessions():
    """Returns all sessions for the dropdown, newest first."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        to_char("generatedAt" AT TIME ZONE 'UTC',
                                 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') AS iso,
                        to_char("generatedAt" AT TIME ZONE 'UTC',
                                 'YYYY-MM-DD HH24:MI:SS')           AS label,
                        "waveCleared",
                        "gameBeaten"
                    FROM wormhole_session_summary
                    ORDER BY "generatedAt" DESC
                """)
                rows = cur.fetchall()

        sessions = [
            {
                "key":        row[0],
                "label":      row[1],
                "waveCleared": row[2],
                "gameBeaten":  row[3]
            }
            for row in rows
        ]
        return jsonify({"success": True, "sessions": sessions})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/damage-spikes', methods=['GET'])
def get_damage_spikes():
    """HP timeline + special attack timestamps for one session."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:

                cur.execute("""
                    SELECT "generatedAt"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at = row[0]

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "hp"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "hp" IS NOT NULL
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                hp_rows = cur.fetchall()

                cur.execute("""
                    SELECT
                        "type",
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN (
                            'fractal_cascade_attack',
                            'slime_attack',
                            'ocular_prism_attack'
                          )
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                attack_rows = cur.fetchall()

        hp_data = [
            {"x": round(float(r[0]), 2), "y": int(r[1])}
            for r in hp_rows if r[0] is not None
        ]

        attacks = {"fractal_cascade_attack": [], "slime_attack": [], "ocular_prism_attack": []}
        for event_type, elapsed in attack_rows:
            if elapsed is not None and event_type in attacks:
                attacks[event_type].append(round(float(elapsed), 2))

        return jsonify({
            "success":  True,
            "session":  session_key,
            "hp":       hp_data,
            "attacks":  attacks
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/health-kill-ratio', methods=['GET'])
def get_health_kill_ratio():
    """Scatter: avg enemy health vs kill ratio (kills / spawns) per session."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        (
                            "ENEMIES_TYPES_BASIC_HEALTH"    +
                            "ENEMIES_TYPES_FAST_HEALTH"     +
                            "ENEMIES_TYPES_TANK_HEALTH"     +
                            "ENEMIES_TYPES_ZIGZAG_HEALTH"   +
                            "ENEMIES_TYPES_FLIMFLAM_HEALTH"
                        ) / 5.0                              AS avg_health,
                        CASE
                            WHEN "enemySpawns" > 0
                            THEN ROUND("enemyKills"::numeric / "enemySpawns", 4)
                            ELSE NULL
                        END                                  AS kill_ratio
                    FROM wormhole_session_summary
                    WHERE "ENEMIES_TYPES_BASIC_HEALTH"    IS NOT NULL
                      AND "ENEMIES_TYPES_FAST_HEALTH"     IS NOT NULL
                      AND "ENEMIES_TYPES_TANK_HEALTH"     IS NOT NULL
                      AND "ENEMIES_TYPES_ZIGZAG_HEALTH"   IS NOT NULL
                      AND "ENEMIES_TYPES_FLIMFLAM_HEALTH" IS NOT NULL
                      AND "enemySpawns" > 0
                    ORDER BY avg_health
                """)
                rows = cur.fetchall()

        data = [
            {"x": float(r[0]), "y": float(r[1])}
            for r in rows if r[0] is not None and r[1] is not None
        ]
        return jsonify({"success": True, "data": data})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/insights', methods=['GET'])
def get_insights():
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG("waveReached"), AVG("playerDamageCount")
                    FROM wormhole_session_summary
                """)
                avg_wave, avg_damage = cur.fetchone()

        insights = []

        if avg_wave is not None and avg_wave < 3:
            insights.append("Early waves may be too difficult for players.")
        if avg_damage is not None and avg_damage > 20:
            insights.append("Players are taking high damage — consider tuning enemy frequency or healing.")
        if not insights:
            insights.append("Balance looks stable across current dataset.")

        return jsonify({"success": True, "insights": insights})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500