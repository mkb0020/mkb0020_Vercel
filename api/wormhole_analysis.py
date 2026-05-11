from flask import Blueprint, request, jsonify
import psycopg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from api.config_score import (_score_ttk, _score_density, _score_hp,
                           _get_config_sessions,
                           TTK_WEIGHT, DENSITY_WEIGHT, HP_WEIGHT)

load_dotenv()
DB_URL = os.environ.get("DATABASE_URL")

wormhole_analysis_bp = Blueprint('wormhole_analysis', __name__)


# ─── CONFIG HASH ──────────────────────────────────────────────────────────────
_CFG_PARTS = [
    'COALESCE("COSMIC_PRISM_HEAL_AMOUNT"::text,\'N\')',
    'COALESCE("ENEMIES_SPAWN_INTERVAL_MIN"::text,\'N\')',
    'COALESCE("ENEMIES_SPAWN_INTERVAL_MAX"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_BASIC_HEALTH"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_BASIC_LASER_INTERVAL"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_BASIC_COMBAT_DURATION"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FAST_HEALTH"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FAST_LASER_INTERVAL"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FAST_COMBAT_DURATION"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_TANK_HEALTH"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_TANK_LASER_INTERVAL"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_TANK_COMBAT_DURATION"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_ZIGZAG_HEALTH"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_ZIGZAG_LASER_INTERVAL"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_ZIGZAG_COMBAT_DURATION"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_HEALTH"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_LASER_INTERVAL"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_COMBAT_DURATION"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MIN"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MAX"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MIN"::text,\'N\')',
    'COALESCE("ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MAX"::text,\'N\')',
    'COALESCE("SLIME_ATTACK_FIRST_ATTACK_MIN"::text,\'N\')',
    'COALESCE("SLIME_ATTACK_FIRST_ATTACK_MAX"::text,\'N\')',
    'COALESCE("SLIME_ATTACK_REPEAT_INTERVAL"::text,\'N\')',
    'COALESCE("FRACTAL_CASCADE_FIRST_DELAY_MIN"::text,\'N\')',
    'COALESCE("FRACTAL_CASCADE_FIRST_DELAY_MAX"::text,\'N\')',
    'COALESCE("FRACTAL_CASCADE_COOLDOWN_MIN"::text,\'N\')',
    'COALESCE("FRACTAL_CASCADE_COOLDOWN_MAX"::text,\'N\')',
    'COALESCE("WAVE_CONFIGS_wave1_types",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave1_weights",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave1_maxEnemies"::text,\'N\')',
    'COALESCE("WAVE_CONFIGS_wave2_types",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave2_weights",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave2_maxEnemies"::text,\'N\')',
    'COALESCE("WAVE_CONFIGS_wave3_types",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave3_weights",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave3_maxEnemies"::text,\'N\')',
    'COALESCE("WAVE_CONFIGS_wave4_types",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave4_weights",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave4_maxEnemies"::text,\'N\')',
    'COALESCE("WAVE_CONFIGS_wave5_types",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave5_weights",\'N\')',
    'COALESCE("WAVE_CONFIGS_wave5_maxEnemies"::text,\'N\')',
]
CONFIG_HASH_EXPR = "MD5(CONCAT(" + ",'|',".join(_CFG_PARTS) + "))"


def _get_config_sessions(cur, config_hash):
    """Returns all session ISO keys whose config snapshot matches the given hash."""
    cur.execute(f"""
        SELECT to_char("generatedAt" AT TIME ZONE 'UTC',
                       'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')
        FROM wormhole_session_summary
        WHERE {CONFIG_HASH_EXPR} = %s
        ORDER BY "generatedAt" DESC
    """, (config_hash,))
    return [row[0] for row in cur.fetchall()]


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
                    event_time = (generated_at + timedelta(seconds=elapsed / 1000)) if generated_at else None

                    cur.execute("""
                        INSERT INTO wormhole_events (
                            "session", "type", "time", "amount", "hp", "lives", "enemyId", "enemyType"
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        session_key,
                        event.get("type"),
                        event_time,
                        event.get("amount"),
                        event.get("hp"),
                        event.get("lives"),
                        event.get("id"),        
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
                        AVG(CASE WHEN "gameBeaten" = true THEN 1.0 ELSE 0.0 END),
                        AVG(CASE WHEN "bossReached" = true THEN "bossEntryShipHp" ELSE NULL END)
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
                "win_rate":       float(row[10] or 0),
                "avg_boss_entry_hp": float(row[11]) if row[11] is not None else None
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


@wormhole_analysis_bp.route('/api/wormhole/configs', methods=['GET'])
def get_configs():
    """Returns all distinct config groups ranked by balance score, with full config snapshot."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    WITH hashed AS (
                        SELECT *, {CONFIG_HASH_EXPR} AS cfg_hash
                        FROM wormhole_session_summary
                    )
                    SELECT
                        cfg_hash,
                        COUNT(*)                                                              AS session_count,
                        ROUND(AVG("waveCleared"::float)::numeric, 2)                         AS avg_waves_cleared,
                        ROUND(AVG(CASE WHEN "gameBeaten" THEN 1.0 ELSE 0.0 END)::numeric, 3) AS win_rate,
                        MAX("waveCleared")                                                    AS max_waves_cleared,
                        MAX(to_char("generatedAt" AT TIME ZONE 'UTC',
                                    'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'))                        AS latest_session,
                        MIN("COSMIC_PRISM_HEAL_AMOUNT"),
                        MIN("ENEMIES_SPAWN_INTERVAL_MIN"), MIN("ENEMIES_SPAWN_INTERVAL_MAX"),
                        MIN("ENEMIES_TYPES_BASIC_HEALTH"),    MIN("ENEMIES_TYPES_BASIC_LASER_INTERVAL"),    MIN("ENEMIES_TYPES_BASIC_COMBAT_DURATION"),
                        MIN("ENEMIES_TYPES_FAST_HEALTH"),     MIN("ENEMIES_TYPES_FAST_LASER_INTERVAL"),     MIN("ENEMIES_TYPES_FAST_COMBAT_DURATION"),
                        MIN("ENEMIES_TYPES_TANK_HEALTH"),     MIN("ENEMIES_TYPES_TANK_LASER_INTERVAL"),     MIN("ENEMIES_TYPES_TANK_COMBAT_DURATION"),
                        MIN("ENEMIES_TYPES_ZIGZAG_HEALTH"),   MIN("ENEMIES_TYPES_ZIGZAG_LASER_INTERVAL"),   MIN("ENEMIES_TYPES_ZIGZAG_COMBAT_DURATION"),
                        MIN("ENEMIES_TYPES_FLIMFLAM_HEALTH"), MIN("ENEMIES_TYPES_FLIMFLAM_LASER_INTERVAL"), MIN("ENEMIES_TYPES_FLIMFLAM_COMBAT_DURATION"),
                        MIN("ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MIN"), MIN("ENEMIES_TYPES_FLIMFLAM_PRISM_FIRST_DELAY_MAX"),
                        MIN("ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MIN"),    MIN("ENEMIES_TYPES_FLIMFLAM_PRISM_COOLDOWN_MAX"),
                        MIN("SLIME_ATTACK_FIRST_ATTACK_MIN"), MIN("SLIME_ATTACK_FIRST_ATTACK_MAX"), MIN("SLIME_ATTACK_REPEAT_INTERVAL"),
                        MIN("FRACTAL_CASCADE_FIRST_DELAY_MIN"), MIN("FRACTAL_CASCADE_FIRST_DELAY_MAX"),
                        MIN("FRACTAL_CASCADE_COOLDOWN_MIN"),    MIN("FRACTAL_CASCADE_COOLDOWN_MAX"),
                        MIN("WAVE_CONFIGS_wave1_types"), MIN("WAVE_CONFIGS_wave1_weights"), MIN("WAVE_CONFIGS_wave1_maxEnemies"),
                        MIN("WAVE_CONFIGS_wave2_types"), MIN("WAVE_CONFIGS_wave2_weights"), MIN("WAVE_CONFIGS_wave2_maxEnemies"),
                        MIN("WAVE_CONFIGS_wave3_types"), MIN("WAVE_CONFIGS_wave3_weights"), MIN("WAVE_CONFIGS_wave3_maxEnemies"),
                        MIN("WAVE_CONFIGS_wave4_types"), MIN("WAVE_CONFIGS_wave4_weights"), MIN("WAVE_CONFIGS_wave4_maxEnemies"),
                        MIN("WAVE_CONFIGS_wave5_types"), MIN("WAVE_CONFIGS_wave5_weights"), MIN("WAVE_CONFIGS_wave5_maxEnemies")
                    FROM hashed
                    GROUP BY cfg_hash
                """)
                rows = cur.fetchall()

                def val(v):
                    return float(v) if v is not None else None

                configs = []
                for row in rows:
                    cfg_hash = row[0]

                    sessions = _get_config_sessions(cur, cfg_hash)
                    ttk_score,     _ = _score_ttk(cur, sessions)
                    density_score, _ = _score_density(cur, sessions)
                    hp_score,      _ = _score_hp(cur, sessions)

                    valid_pillars = [
                        (ttk_score,     TTK_WEIGHT),
                        (density_score, DENSITY_WEIGHT),
                        (hp_score,      HP_WEIGHT),
                    ]
                    valid_pillars = [(s, w) for s, w in valid_pillars if s is not None]
                    if valid_pillars:
                        total_w     = sum(w for _, w in valid_pillars)
                        final_score = round(sum(s * w for s, w in valid_pillars) / total_w, 1)
                    else:
                        final_score = None
                    # ─────────────────────────────────────────────────────────

                    configs.append({
                        "config_hash":       cfg_hash,
                        "session_count":     int(row[1]),
                        "avg_waves_cleared": float(row[2]) if row[2] is not None else 0.0,
                        "win_rate":          float(row[3]) if row[3] is not None else 0.0,
                        "max_waves_cleared": int(row[4]) if row[4] is not None else 0,
                        "latest_session":    row[5],
                        "final_score":       final_score,
                        "ttk_score":         round(ttk_score,     1) if ttk_score     is not None else None,
                        "density_score":     round(density_score, 1) if density_score is not None else None,
                        "hp_score":          round(hp_score,      1) if hp_score      is not None else None,
                        "config": {
                            "COSMIC_PRISM": { "HEAL_AMOUNT": val(row[6]) },
                            "ENEMIES": {
                                "SPAWN_INTERVAL_MIN": val(row[7]),
                                "SPAWN_INTERVAL_MAX": val(row[8]),
                                "TYPES": {
                                    "BASIC":    { "HEALTH": val(row[9]),  "LASER_INTERVAL": val(row[10]), "COMBAT_DURATION": val(row[11]) },
                                    "FAST":     { "HEALTH": val(row[12]), "LASER_INTERVAL": val(row[13]), "COMBAT_DURATION": val(row[14]) },
                                    "TANK":     { "HEALTH": val(row[15]), "LASER_INTERVAL": val(row[16]), "COMBAT_DURATION": val(row[17]) },
                                    "ZIGZAG":   { "HEALTH": val(row[18]), "LASER_INTERVAL": val(row[19]), "COMBAT_DURATION": val(row[20]) },
                                    "FLIMFLAM": {
                                        "HEALTH":                val(row[21]), "LASER_INTERVAL": val(row[22]), "COMBAT_DURATION": val(row[23]),
                                        "PRISM_FIRST_DELAY_MIN": val(row[24]), "PRISM_FIRST_DELAY_MAX": val(row[25]),
                                        "PRISM_COOLDOWN_MIN":    val(row[26]), "PRISM_COOLDOWN_MAX":     val(row[27])
                                    }
                                }
                            },
                            "SLIME_ATTACK": {
                                "FIRST_ATTACK_MIN": val(row[28]), "FIRST_ATTACK_MAX": val(row[29]),
                                "REPEAT_INTERVAL":  val(row[30])
                            },
                            "FRACTAL_CASCADE": {
                                "FIRST_DELAY_MIN": val(row[31]), "FIRST_DELAY_MAX": val(row[32]),
                                "COOLDOWN_MIN":    val(row[33]), "COOLDOWN_MAX":    val(row[34])
                            },
                            "WAVE_CONFIGS": [
                                { "types": row[35], "weights": row[36], "maxEnemies": row[37] },
                                { "types": row[38], "weights": row[39], "maxEnemies": row[40] },
                                { "types": row[41], "weights": row[42], "maxEnemies": row[43] },
                                { "types": row[44], "weights": row[45], "maxEnemies": row[46] },
                                { "types": row[47], "weights": row[48], "maxEnemies": row[49] },
                            ]
                        }
                    })

        configs.sort(key=lambda c: (-(c['final_score'] if c['final_score'] is not None else -1), -c['session_count']))

        for i, c in enumerate(configs):
            c['rank'] = i + 1

        return jsonify({"success": True, "configs": configs})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/config-aggregate', methods=['GET'])
def get_config_aggregate():
    """Returns aggregate stats for all sessions sharing a config hash.
    Used by cards (damage spikes, TTK, density, insights) when in config-average mode."""
    config_hash = request.args.get("config")
    if not config_hash:
        return jsonify({"success": False, "error": "Missing config param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                sessions = _get_config_sessions(cur, config_hash)
        if not sessions:
            return jsonify({"success": False, "error": "No sessions found for this config"}), 404
        return jsonify({"success": True, "sessions": sessions, "count": len(sessions)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/session-config', methods=['GET'])
def get_session_config():
    """Returns all config snapshot values for a specific session."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
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
                        "waveCleared", "gameBeaten", "runOutcome"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()

        if not row:
            return jsonify({"success": False, "error": "Session not found"}), 404

        def val(v):
            return float(v) if v is not None else None

        config = {
            "COSMIC_PRISM": {
                "HEAL_AMOUNT": val(row[0])
            },
            "ENEMIES": {
                "SPAWN_INTERVAL_MIN": val(row[1]),
                "SPAWN_INTERVAL_MAX": val(row[2]),
                "TYPES": {
                    "BASIC":    { "HEALTH": val(row[3]),  "LASER_INTERVAL": val(row[4]),  "COMBAT_DURATION": val(row[5])  },
                    "FAST":     { "HEALTH": val(row[6]),  "LASER_INTERVAL": val(row[7]),  "COMBAT_DURATION": val(row[8])  },
                    "TANK":     { "HEALTH": val(row[9]),  "LASER_INTERVAL": val(row[10]), "COMBAT_DURATION": val(row[11]) },
                    "ZIGZAG":   { "HEALTH": val(row[12]), "LASER_INTERVAL": val(row[13]), "COMBAT_DURATION": val(row[14]) },
                    "FLIMFLAM": {
                        "HEALTH": val(row[15]), "LASER_INTERVAL": val(row[16]), "COMBAT_DURATION": val(row[17]),
                        "PRISM_FIRST_DELAY_MIN": val(row[18]), "PRISM_FIRST_DELAY_MAX": val(row[19]),
                        "PRISM_COOLDOWN_MIN":    val(row[20]), "PRISM_COOLDOWN_MAX":    val(row[21])
                    }
                }
            },
            "SLIME_ATTACK": {
                "FIRST_ATTACK_MIN": val(row[22]), "FIRST_ATTACK_MAX": val(row[23]),
                "REPEAT_INTERVAL":  val(row[24])
            },
            "FRACTAL_CASCADE": {
                "FIRST_DELAY_MIN": val(row[25]), "FIRST_DELAY_MAX": val(row[26]),
                "COOLDOWN_MIN":    val(row[27]), "COOLDOWN_MAX":    val(row[28])
            },
            "WAVE_CONFIGS": [
                { "types": row[29], "weights": row[30], "maxEnemies": row[31] },
                { "types": row[32], "weights": row[33], "maxEnemies": row[34] },
                { "types": row[35], "weights": row[36], "maxEnemies": row[37] },
                { "types": row[38], "weights": row[39], "maxEnemies": row[40] },
                { "types": row[41], "weights": row[42], "maxEnemies": row[43] }
            ]
        }

        return jsonify({
            "success":    True,
            "session":    session_key,
            "waveCleared": row[44],
            "gameBeaten":  row[45],
            "runOutcome":  row[46],
            "config":     config
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/damage-spikes', methods=['GET'])
def get_damage_spikes():
    """HP timeline + special attack timestamps for one session, or config-averaged across sessions."""
    session_key = request.args.get("session")
    config_hash = request.args.get("config")
    if not session_key and not config_hash:
        return jsonify({"success": False, "error": "Missing session or config param"}), 400

    ATTACK_TYPES = ('fractal_cascade_attack', 'slime_attack', 'ocular_prism_attack')

    def _fetch_session_data(cur, sess):
        """Return (hp_timeline, attack_dict) for a single session key."""
        cur.execute("""
            SELECT "generatedAt"
            FROM wormhole_session_summary
            WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                          'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
        """, (sess,))
        row = cur.fetchone()
        if not row:
            return None, None
        generated_at = row[0]

        cur.execute("""
            SELECT EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed, "hp"
            FROM wormhole_events
            WHERE "session" = %s AND "hp" IS NOT NULL
            ORDER BY "time" ASC
        """, (generated_at, sess))
        hp_rows = cur.fetchall()

        cur.execute("""
            SELECT "type", EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed
            FROM wormhole_events
            WHERE "session" = %s
              AND "type" IN ('fractal_cascade_attack', 'slime_attack', 'ocular_prism_attack')
            ORDER BY "time" ASC
        """, (generated_at, sess))
        attack_rows = cur.fetchall()

        timeline = [
            (round(float(r[0]), 2), int(r[1]))
            for r in hp_rows if r[0] is not None
        ]
        attacks = {t: [] for t in ATTACK_TYPES}
        for event_type, elapsed in attack_rows:
            if elapsed is not None and event_type in attacks:
                attacks[event_type].append(round(float(elapsed), 2))

        return timeline, attacks

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:

                # ── CONFIG-AVERAGE MODE ──────────────────────────────────────
                if config_hash:
                    sessions = _get_config_sessions(cur, config_hash)
                    if not sessions:
                        return jsonify({"success": False, "error": "No sessions found for this config"}), 404

                    from collections import defaultdict
                    buckets   = defaultdict(list)   
                    all_attacks = {t: [] for t in ATTACK_TYPES}

                    for sess in sessions:
                        timeline, atks = _fetch_session_data(cur, sess)
                        if not timeline:
                            continue
                        for elapsed, hp in timeline:
                            buckets[int(elapsed)].append(hp)
                        for t in ATTACK_TYPES:
                            all_attacks[t].extend(atks.get(t, []))

                    if not buckets:
                        return jsonify({
                            "success": True, "session": None, "config": config_hash,
                            "hp": [], "attacks": {t: [] for t in ATTACK_TYPES}
                        })

                    max_bucket = max(buckets.keys())
                    hp_data = [
                        {"x": float(t), "y": round(sum(buckets[t]) / len(buckets[t]), 1)}
                        for t in range(0, max_bucket + 1)
                        if t in buckets
                    ]

                    return jsonify({
                        "success": True,
                        "session": None,
                        "config":  config_hash,
                        "hp":      hp_data,
                        "attacks": all_attacks
                    })

                # ── SINGLE-SESSION MODE ──────────────────────────────────────
                else:
                    timeline, attacks = _fetch_session_data(cur, session_key)
                    if timeline is None:
                        return jsonify({"success": False, "error": "Session not found"}), 404

                    hp_data = [{"x": e, "y": hp} for e, hp in timeline]

                    return jsonify({
                        "success": True,
                        "session": session_key,
                        "config":  None,
                        "hp":      hp_data,
                        "attacks": attacks
                    })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@wormhole_analysis_bp.route('/api/wormhole/hp-insights', methods=['GET'])
def get_hp_insights():
    """Analyze HP timeline for a session and return structured, meaningful insights."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "waveCleared", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, wave_cleared, damage_count, heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "hp"
                    FROM wormhole_events
                    WHERE "session" = %s AND "hp" IS NOT NULL
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                hp_rows = cur.fetchall()

        if not hp_rows:
            return jsonify({"success": True, "session": session_key, "insights": [], "stats": {}})

        timeline = [(float(r[0]), int(r[1])) for r in hp_rows if r[0] is not None]
        total_duration = timeline[-1][0] if timeline else 1.0

        # ── 1. DEATH DETECTION 
        DEATH_FROM  = 15   
        DEATH_TO    = 85   
        deaths = []
        for i in range(1, len(timeline)):
            t_prev, hp_prev = timeline[i - 1]
            t_curr, hp_curr = timeline[i]
            if hp_prev <= DEATH_FROM and hp_curr >= DEATH_TO:
                deaths.append({
                    "time":        round(t_curr, 1),
                    "pct_through": round(t_curr / total_duration, 2)
                })

        # ── 2. SPIKE DETECTION (BURST: CUMULATIVE DAMAGE WITHIN A SHORT WINDOW)
        # ENEMIES DEAL ~10 HP PER HIT, SO WE DETECT BURSTS OF MULTIPLE RAPID HITS
        # RATHER THAN LOOKING FOR SINGLE LARGE BLOWS.
        WINDOW_SECONDS  = 5    # SECONDS TO ACCUMULATE BURST DAMAGE
        SPIKE_THRESHOLD = 20   # ≥ 2 HITS (~20 HP) IN THE WINDOW = SPIKE
        MEGA_THRESHOLD  = 30   # ≥ 3 HITS (~30 HP) IN THE WINDOW = MEGA SPIKE
        spikes = []
        last_spike_end = -1.0  # PREVENT OVERLAPPING WINDOWS FROM DOUBLE-COUNTING

        for i in range(len(timeline)):
            t_start, hp_start = timeline[i]
            if t_start <= last_spike_end:
                continue  # STILL INSIDE A PREVIOUSLY FLAGGED BURST WINDOW
            if hp_start <= DEATH_FROM:
                continue  # SKIP DEATH / POST-DEATH FRAMES

            min_hp = hp_start # SCAN FORWARD WITHIN BURST WINDOW - TRACKING MIN HP SEEN
            prev_hp = hp_start
            contains_respawn = False

            for j in range(i + 1, len(timeline)):
                t_j, hp_j = timeline[j]
                if t_j - t_start > WINDOW_SECONDS:
                    break
                if prev_hp <= DEATH_FROM and hp_j >= DEATH_TO: # STOPE IF A DESTH-RESPAWN JUMP OCCURS INSIDE THE WINDOW
                    contains_respawn = True
                    break
                min_hp = min(min_hp, hp_j)
                prev_hp = hp_j

            if contains_respawn:
                continue

            drop = hp_start - min_hp
            if drop >= SPIKE_THRESHOLD:
                spikes.append({
                    "time":    round(t_start, 1),
                    "drop":    drop,
                    "is_mega": drop >= MEGA_THRESHOLD
                })
                last_spike_end = t_start + WINDOW_SECONDS  

        # ── 3. OVERALL TREND (LINEAR REGRESSION ) 
        n      = len(timeline)
        times  = [p[0] for p in timeline]
        hps    = [p[1] for p in timeline]
        mean_t = sum(times) / n
        mean_h = sum(hps)   / n
        num    = sum((times[i] - mean_t) * (hps[i] - mean_h) for i in range(n))
        den    = sum((times[i] - mean_t) ** 2                 for i in range(n))
        slope  = num / den if den != 0 else 0  

        # ── 4. EARLY vs LATE PRESSURE 
        mid       = total_duration / 2
        early_hps = [hp for t, hp in timeline if t <  mid]
        late_hps  = [hp for t, hp in timeline if t >= mid]
        early_avg = sum(early_hps) / len(early_hps) if early_hps else 0
        late_avg  = sum(late_hps)  / len(late_hps)  if late_hps  else 0

        # ── 5. FLAT PERIOD DETECTION 
        FLAT_WINDOW = 20   
        FLAT_RANGE  = 5    
        flat_periods = []
        w_start = 0
        for i in range(1, n):
            t_start = timeline[w_start][0]
            t_curr  = timeline[i][0]
            if t_curr - t_start >= FLAT_WINDOW:
                window_hps = [hp for _, hp in timeline[w_start:i + 1]]
                if max(window_hps) - min(window_hps) <= FLAT_RANGE:
                    flat_periods.append({
                        "start":  round(t_start, 1),
                        "end":    round(t_curr, 1),
                        "avg_hp": round(sum(window_hps) / len(window_hps), 1)
                    })
                w_start = i

        dmg_events  = int(damage_count  or 0)
        heal_events = int(heal_count    or 0)

        insights = []

        early_deaths = [d for d in deaths if d["pct_through"] < 0.60]
        late_deaths  = [d for d in deaths if d["pct_through"] >= 0.60]
        if not deaths:
            insights.append({
                "category": "deaths", "status": "ok", "icon": "💚",
                "title":   "No Deaths",
                "message": ("No deaths this session — you made it through without hitting zero. "
                            "Since you're an experienced player, this is a good sign that the "
                            "damage level isn't catastrophically high.")
            })
        elif early_deaths:
            times_str = ", ".join(f"{d['time']}s" for d in early_deaths)
            insights.append({
                "category": "deaths", "status": "critical", "icon": "🛑",
                "title":   f"Early Death{'s' if len(early_deaths) > 1 else ''} ({len(early_deaths)}x)",
                "message": (f"Died {len(early_deaths)}x during the early game ({times_str}). "
                            f"Even as an experienced player you died before the 60% mark — "
                            f"this strongly suggests waves 1–3 are too punishing. "
                            f"Consider tuning enemy damage, spawn rate, or adding a healing buff early on.")
            })
        else:
            times_str = ", ".join(f"{d['time']}s" for d in late_deaths)
            insights.append({
                "category": "deaths", "status": "warning", "icon": "⚠️",
                "title":   f"Late-Game Death{'s' if len(late_deaths) > 1 else ''} ({len(late_deaths)}x)",
                "message": (f"Died {len(late_deaths)}x in the final stretch ({times_str}). "
                            f"Late deaths are expected and healthy — this signals the endgame "
                            f"has real teeth. For a normal player this will feel brutal; "
                            f"watch that it doesn't become unavoidable.")
            })

        mega_spikes = [s for s in spikes if s["is_mega"]]
        if not spikes:
            insights.append({
                "category": "spikes", "status": "warning", "icon": "⚠️",
                "title":   "No Noticeable Damage Bursts",
                "message": (f"HP never dropped more than {SPIKE_THRESHOLD} HP within any "
                            f"{WINDOW_SECONDS}-second window. "
                            "The game may feel like a slow grind rather than "
                            "dynamic combat — consider moments where multiple enemies "
                            "converge to create short bursts of pressure.")
            })
        elif len(mega_spikes) > 3:
            worst_few = sorted(mega_spikes, key=lambda s: -s["drop"])[:4]
            spike_str = ", ".join(f"{s['time']}s (−{s['drop']} HP)" for s in worst_few)
            insights.append({
                "category": "spikes", "status": "critical", "icon": "🛑",
                "title":   f"Way Too Many Intense Bursts ({len(mega_spikes)})",
                "message": (f"Found {len(mega_spikes)} windows where the player took "
                            f">{MEGA_THRESHOLD} HP within {WINDOW_SECONDS}s. "
                            f"Worst: {spike_str}. At this frequency, damage will feel "
                            f"relentless and unfair — players can't recover fast enough. "
                            f"Consider spreading out enemy attacks or increasing heal availability.")
            })
        elif mega_spikes:
            worst = max(mega_spikes, key=lambda s: s["drop"])
            insights.append({
                "category": "spikes", "status": "warning", "icon": "⚠️",
                "title":   f"{len(mega_spikes)} Heavy Burst{'s' if len(mega_spikes) > 1 else ''}",
                "message": (f"A few windows with >{MEGA_THRESHOLD} HP lost in {WINDOW_SECONDS}s detected. "
                            f"Biggest: −{worst['drop']} HP around {worst['time']}s. "
                            f"A couple of intense moments are fine for tension, "
                            f"but keep an eye on how often they occur.")
            })
        else:
            biggest = max(spikes, key=lambda s: s["drop"])
            insights.append({
                "category": "spikes", "status": "ok", "icon": "💚",
                "title":   f"Burst Pattern Looks Good ({len(spikes)} burst{'s' if len(spikes) != 1 else ''})",
                "message": (f"Damage bursts are present and add rhythm without being overwhelming. "
                            f"Biggest burst: −{biggest['drop']} HP over {WINDOW_SECONDS}s around {biggest['time']}s. "
                            f"This feels punchy but recoverable.")
            })

        if abs(slope) < 0.03:
            insights.append({
                "category": "trend", "status": "warning", "icon": "⚠️",
                "title":   "HP Almost Perfectly Flat",
                "message": (f"The overall HP trend is nearly flat ({slope:+.3f} HP/s). "
                            f"There's no meaningful net drain across the session — "
                            f"players may feel invincible. Try reducing heal amount or "
                            f"increasing damage frequency.")
            })
        elif slope < -0.4:
            insights.append({
                "category": "trend", "status": "critical", "icon": "🛑",
                "title":   "HP Declining Too Fast",
                "message": (f"Overall slope is {slope:.3f} HP/s — steep enough to "
                            f"feel like a death march with no breathing room. "
                            f"Consider increasing heal availability or reducing "
                            f"sustained enemy damage.")
            })
        else:
            insights.append({
                "category": "trend", "status": "ok", "icon": "💚",
                "title":   "HP Trend Looks Healthy",
                "message": (f"Overall slope of {slope:+.3f} HP/s — gradual pressure "
                            f"without a death spiral. Players should feel the weight "
                            f"of the session without feeling hopeless.")
            })

        pressure_diff = early_avg - late_avg
        if pressure_diff < 5:
            insights.append({
                "category": "escalation", "status": "warning", "icon": "⚠️",
                "title":   "Damage Doesn't Ramp Up Much",
                "message": (f"Avg HP early game: {early_avg:.0f} → late game: {late_avg:.0f} "
                            f"(only −{pressure_diff:.0f} HP difference). "
                            f"Waves 4–5 should feel harder than wave 1. "
                            f"Consider bumping enemy aggression, density, or special attack frequency in late waves.")
            })
        elif pressure_diff > 35:
            insights.append({
                "category": "escalation", "status": "warning", "icon": "⚠️",
                "title":   "Late Game May Be Too Brutal",
                "message": (f"HP drops from ~{early_avg:.0f} early to ~{late_avg:.0f} late "
                            f"(−{pressure_diff:.0f} HP). That's a big jump — "
                            f"normal players hitting waves 4–5 for the first time "
                            f"could feel overwhelmed with no ramp-up warning.")
            })
        else:
            insights.append({
                "category": "escalation", "status": "ok", "icon": "💚",
                "title":   "Escalation Feels Natural",
                "message": (f"HP goes from ~{early_avg:.0f} in the first half to "
                            f"~{late_avg:.0f} in the second half (−{pressure_diff:.0f} HP). "
                            f"A smooth ramp that should feel fair but increasingly tense.")
            })

        if heal_events == 0:
            insights.append({
                "category": "balance", "status": "warning", "icon": "⚠️",
                "title":   "No Healing This Session",
                "message": ("Zero healing events recorded. If the Cosmic Prism never "
                            "triggered or was never useful, it may feel like a dead ability. "
                            "Make sure healing opportunities arise naturally in the flow of combat.")
            })
        elif dmg_events > 0:
            ratio = dmg_events / heal_events
            if ratio < 1.5:
                insights.append({
                    "category": "balance", "status": "warning", "icon": "⚠️",
                    "title":   "Healing Outpacing Damage",
                    "message": (f"{dmg_events} damage events vs {heal_events} heals "
                                f"({ratio:.1f}:1 ratio). Players may feel too safe. "
                                f"Consider reducing heal frequency or heal amount, "
                                f"or increasing enemy pressure.")
                })
            elif ratio > 8:
                insights.append({
                    "category": "balance", "status": "warning", "icon": "⚠️",
                    "title":   "Healing Feels Rare",
                    "message": (f"{dmg_events} damage events vs {heal_events} heals "
                                f"({ratio:.1f}:1 ratio). Healing is very infrequent — "
                                f"the Cosmic Prism might feel useless or hard to trigger. "
                                f"Make sure it's available often enough to feel like a real lifeline.")
                })
            else:
                insights.append({
                    "category": "balance", "status": "ok", "icon": "💚",
                    "title":   "Damage/Heal Balance Is Good",
                    "message": (f"{dmg_events} damage events vs {heal_events} heals "
                                f"({ratio:.1f}:1). Healthy tension — "
                                f"players feel pressure but have recovery moments. "
                                f"The Cosmic Prism earns its place.")
                })

        if flat_periods:
            longest = max(flat_periods, key=lambda p: p["end"] - p["start"])
            dur     = round(longest["end"] - longest["start"])
            insights.append({
                "category": "pacing", "status": "warning", "icon": "⚠️",
                "title":   f"Dead Zone Detected (~{dur}s)",
                "message": (f"HP barely moved between {longest['start']}s and {longest['end']}s "
                            f"(avg HP {longest['avg_hp']}, swing ≤{FLAT_RANGE}). "
                            f"Something in this window isn't applying pressure — "
                            f"check if a wave transition, spawn delay, or lull in enemy AI "
                            f"is letting the player breathe for too long.")
            })

        stats = {
            "death_count":       len(deaths),
            "early_death_count": len(early_deaths),
            "spike_count":       len(spikes),
            "mega_spike_count":  len(mega_spikes),
            "max_spike_drop":    max((s["drop"] for s in spikes), default=0),
            "overall_slope":     round(slope, 4),
            "early_avg_hp":      round(early_avg, 1),
            "late_avg_hp":       round(late_avg, 1),
            "damage_events":     dmg_events,
            "heal_events":       heal_events,
            "duration":          round(total_duration, 1),
            "flat_period_count": len(flat_periods)
        }

        return jsonify({
            "success":  True,
            "session":  session_key,
            "insights": insights,
            "stats":    stats
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@wormhole_analysis_bp.route('/api/wormhole/density-insights', methods=['GET'])
def get_density_insights():
    """Per-wave density insight for a specific session and wave number."""
    session_key = request.args.get("session")
    wave_str    = request.args.get("wave")
    if not session_key or not wave_str:
        return jsonify({"success": False, "error": "Missing session or wave param"}), 400
    try:
        wave_num = int(wave_str)
        if wave_num not in range(1, 6):
            return jsonify({"success": False, "error": "Wave must be 1–5"}), 400
    except ValueError:
        return jsonify({"success": False, "error": "Invalid wave param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                max_col = f"WAVE_CONFIGS_wave{wave_num}_maxEnemies"
                cur.execute(f"""
                    SELECT "generatedAt", "waveCleared", "playerDamageCount", "hpHealCount",
                           "{max_col}"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, wave_cleared, damage_count, heal_count, cfg_max_enemies = row
                wave_cleared = int(wave_cleared or 5)

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events WHERE "session" = %s
                """, (session_key,))
                dur_row  = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed, "type"
                    FROM wormhole_events
                    WHERE "session" = %s AND "type" IN ('enemy_spawn','enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

        total_waves = max(wave_cleared, wave_num)
        wave_duration = duration / total_waves
        w_start = wave_duration * (wave_num - 1)
        w_end   = wave_duration *  wave_num

        density_in_wave = []
        count = 0
        for elapsed_raw, event_type in event_rows:
            elapsed = float(elapsed_raw)
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            if w_start <= elapsed <= w_end:
                density_in_wave.append(count)

        if not density_in_wave:
            return jsonify({
                "success": True,
                "session": session_key,
                "wave": wave_num,
                "insight": {
                    "status": "warning", "icon": "⚠️",
                    "title": "No Event Data for This Wave",
                    "message": ("No enemy spawn/kill events were recorded in this wave window. "
                                "The wave may not have been reached, or the timing estimate is off.")
                },
                "stats": {}
            })

        avg_density = sum(density_in_wave) / len(density_in_wave)
        max_density = max(density_in_wave)
        cfg_max     = int(cfg_max_enemies) if cfg_max_enemies is not None else None

        saturated_pct = (sum(1 for d in density_in_wave if cfg_max and d >= cfg_max)
                         / len(density_in_wave)) if cfg_max else 0.0

        WAVE_TARGETS = {
            1: {"min_density": 1.0, "max_density": 2.5, "label": "gentle warm-up"},
            2: {"min_density": 1.5, "max_density": 3.5, "label": "escalating"},
            3: {"min_density": 2.0, "max_density": 4.0, "label": "mid-game pressure"},
            4: {"min_density": 2.5, "max_density": 5.0, "label": "high pressure"},
            5: {"min_density": 3.0, "max_density": 6.0, "label": "intense endgame"},
        }
        target = WAVE_TARGETS[wave_num]

        cfg_str = f" (config maxEnemies: {cfg_max})" if cfg_max is not None else ""

        if avg_density < target["min_density"]:
            status = "warning"
            icon   = "⚠️"
            title  = f"Wave {wave_num} Feels Too Sparse"
            if cfg_max is not None and avg_density < cfg_max * 0.5:
                message = (
                    f"Average density in wave {wave_num} is only {avg_density:.1f} enemies on screen{cfg_str}. "
                    f"The maxEnemies cap of {cfg_max} is almost never being reached — "
                    f"either the spawn interval is too slow or enemies are dying before new ones arrive. "
                    f"For a {target['label']} feel, you want avg density around {target['min_density']}–{target['max_density']}. "
                    f"Consider raising the spawn rate rather than maxEnemies, since the cap isn't the bottleneck."
                )
            else:
                message = (
                    f"Average density in wave {wave_num} is {avg_density:.1f}{cfg_str}. "
                    f"Target for this wave ({target['label']}) is {target['min_density']}–{target['max_density']} avg enemies. "
                    f"The screen feels emptier than it should — players may find this wave too relaxing."
                )
        elif avg_density > target["max_density"]:
            status = "critical"
            icon   = "🛑"
            title  = f"Wave {wave_num} May Be Overcrowded"
            if saturated_pct > 0.4:
                message = (
                    f"Screen was at max capacity ({cfg_max} enemies) for {saturated_pct:.0%} of wave {wave_num}{cfg_str}. "
                    f"When the screen is constantly full, new spawns are suppressed and the wave loses rhythm — "
                    f"it just becomes a wall of enemies with no ebb and flow. "
                    f"Consider lowering maxEnemies for wave {wave_num} to around {max(1, (cfg_max or 6) - 2)}, "
                    f"or increasing kill incentives so the density cycles more naturally."
                )
            else:
                message = (
                    f"Average density of {avg_density:.1f} in wave {wave_num} is above the target of "
                    f"{target['max_density']}{cfg_str}. This wave might feel relentless — "
                    f"especially for a normal player who hasn't memorized patterns. "
                    f"A peak density of {max_density} was hit at points. "
                    f"Consider trimming maxEnemies slightly to give players a moment to breathe between bursts."
                )
        else:
            status = "ok"
            icon   = "💚"
            title  = f"Wave {wave_num} Density Looks Right"
            sat_note = ""
            if cfg_max and saturated_pct > 0.25:
                sat_note = (
                    f" The cap of {cfg_max} was hit for {saturated_pct:.0%} of the wave — "
                    f"that's on the high side; a slight reduction could create more satisfying burst moments."
                )
            elif cfg_max and saturated_pct < 0.05:
                sat_note = (
                    f" The maxEnemies cap of {cfg_max} was rarely reached, "
                    f"so spawn rate is the real pacing driver here — which is fine."
                )
            message = (
                f"Average density of {avg_density:.1f} enemies on screen fits the {target['label']} feel "
                f"expected from wave {wave_num} (target: {target['min_density']}–{target['max_density']}){cfg_str}. "
                f"Peak density hit: {max_density}.{sat_note}"
            )

        stats = {
            "avg_density":    round(avg_density, 2),
            "max_density":    max_density,
            "saturated_pct":  round(saturated_pct, 3),
            "cfg_max_enemies": cfg_max,
            "wave_window_start": round(w_start, 1),
            "wave_window_end":   round(w_end, 1),
            "target_min": target["min_density"],
            "target_max": target["max_density"],
        }

        return jsonify({
            "success": True,
            "session": session_key,
            "wave":    wave_num,
            "insight": {
                "status":  status,
                "icon":    icon,
                "title":   title,
                "message": message
            },
            "stats": stats
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


@wormhole_analysis_bp.route('/api/wormhole/time-to-kill', methods=['GET'])
def get_time_to_kill():
    """Per-enemy-type avg TTK for a specific session or all sessions sharing a config hash."""
    session_key  = request.args.get("session")
    config_hash  = request.args.get("config")
    if not session_key and not config_hash:
        return jsonify({"success": False, "error": "Missing session or config param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                if config_hash:
                    sessions = _get_config_sessions(cur, config_hash)
                    if not sessions:
                        return jsonify({"success": False, "error": "No sessions found for this config"}), 404
                    cur.execute("""
                        SELECT
                            s."enemyType",
                            AVG(EXTRACT(EPOCH FROM (k."time" - s."time"))) AS avg_ttk_sec,
                            COUNT(*) AS sample_count
                        FROM wormhole_events s
                        JOIN wormhole_events k
                          ON  k."session"  = s."session"
                          AND k."enemyId"  = s."enemyId"
                          AND k."type"     = 'enemy_killed'
                          AND s."type"     = 'enemy_spawn'
                        WHERE s."session" = ANY(%s)
                          AND s."enemyType" IS NOT NULL
                        GROUP BY s."enemyType"
                        ORDER BY s."enemyType"
                    """, (sessions,))
                else:
                    cur.execute("""
                        SELECT "generatedAt"
                        FROM wormhole_session_summary
                        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                    """, (session_key,))
                    row = cur.fetchone()
                    if not row:
                        return jsonify({"success": False, "error": "Session not found"}), 404
                    cur.execute("""
                        SELECT
                            s."enemyType",
                            AVG(EXTRACT(EPOCH FROM (k."time" - s."time"))) AS avg_ttk_sec,
                            COUNT(*) AS sample_count
                        FROM wormhole_events s
                        JOIN wormhole_events k
                          ON  k."session"  = s."session"
                          AND k."enemyId"  = s."enemyId"
                          AND k."type"     = 'enemy_killed'
                          AND s."type"     = 'enemy_spawn'
                        WHERE s."session" = %s
                          AND s."enemyType" IS NOT NULL
                        GROUP BY s."enemyType"
                        ORDER BY s."enemyType"
                    """, (session_key,))
                ttk_rows = cur.fetchall()

        ttk_by_type = {}
        for enemy_type, avg_ttk, count in ttk_rows:
            if avg_ttk is not None:
                ttk_by_type[enemy_type] = {
                    "avg_ttk": round(float(avg_ttk), 2),
                    "sample_count": int(count)
                }

        return jsonify({"success": True, "session": session_key, "config": config_hash, "ttk_by_type": ttk_by_type})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@wormhole_analysis_bp.route('/api/wormhole/enemy-density', methods=['GET'])
def get_enemy_density():
    """Enemy count on screen over time, plus pressure score.
    Accepts ?session=<key> for a single session, or ?config=<hash> to average across all
    sessions sharing that config (density is averaged bucket-by-bucket in 1s windows)."""
    session_key = request.args.get("session")
    config_hash = request.args.get("config")
    if not session_key and not config_hash:
        return jsonify({"success": False, "error": "Missing session or config param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                if config_hash:
                    sessions = _get_config_sessions(cur, config_hash)
                    if not sessions:
                        return jsonify({"success": False, "error": "No sessions found for this config"}), 404

                    cur.execute(f"""
                        SELECT SUM("playerDamageCount"), SUM("hpHealCount"), COUNT(*)
                        FROM wormhole_session_summary
                        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = ANY(%s)
                    """, (sessions,))
                    agg = cur.fetchone()
                    total_damage_count = float(agg[0] or 0)
                    total_heal_count   = float(agg[1] or 0)
                    n_sessions         = int(agg[2] or 1)


                    cur.execute("""
                        SELECT
                            s."session",
                            EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) AS elapsed,
                            e."type"
                        FROM wormhole_events e
                        JOIN wormhole_session_summary s
                          ON e."session"::timestamptz = s."generatedAt"
                        WHERE e."session" = ANY(%s)
                          AND e."type" IN ('enemy_spawn', 'enemy_killed')
                        ORDER BY e."session", e."time" ASC
                    """, (sessions,))
                    all_event_rows = cur.fetchall()

                    cur.execute("""
                        SELECT "session", EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                        FROM wormhole_events
                        WHERE "session" = ANY(%s)
                        GROUP BY "session"
                    """, (sessions,))
                    dur_map = {r[0]: float(r[1] or 1) for r in cur.fetchall()}

                    from collections import defaultdict
                    session_buckets = {}  
                    from itertools import groupby
                    from operator import itemgetter

                    current_session = None
                    count = 0
                    session_timeline = []

                    for row in all_event_rows:
                        sess, elapsed, etype = row[0], float(row[1]), row[2]
                        if sess != current_session:
                            if current_session is not None:
                                buckets = {}
                                for pt in session_timeline:
                                    b = int(pt[0])
                                    buckets[b] = pt[1]
                                session_buckets[current_session] = buckets
                            current_session = sess
                            count = 0
                            session_timeline = []
                        if etype == 'enemy_spawn':
                            count += 1
                        elif etype == 'enemy_killed':
                            count = max(0, count - 1)
                        session_timeline.append((elapsed, count))
                    if current_session and session_timeline:
                        buckets = {}
                        for pt in session_timeline:
                            b = int(pt[0])
                            buckets[b] = pt[1]
                        session_buckets[current_session] = buckets

                    all_buckets = set()
                    for b in session_buckets.values():
                        all_buckets.update(b.keys())

                    avg_duration = sum(dur_map.values()) / len(dur_map) if dur_map else 1.0
                    density_timeline = []
                    for b in sorted(all_buckets):
                        vals = [sb[b] for sb in session_buckets.values() if b in sb]
                        if vals:
                            density_timeline.append({"x": float(b), "y": round(sum(vals) / len(vals), 2)})

                    avg_density  = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
                    damage_rate  = (total_damage_count / n_sessions) / avg_duration
                    healing_rate = (total_heal_count   / n_sessions) / avg_duration
                    pressure     = round(damage_rate + avg_density - healing_rate, 3)

                    return jsonify({
                        "success":        True,
                        "config":         config_hash,
                        "session_count":  n_sessions,
                        "density":        density_timeline,
                        "avg_density":    round(avg_density, 2),
                        "damage_rate":    round(damage_rate, 4),
                        "healing_rate":   round(healing_rate, 4),
                        "pressure_score": pressure,
                        "duration":       round(avg_duration, 1)
                    })

                else:
                    cur.execute("""
                        SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                        FROM wormhole_session_summary
                        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                    """, (session_key,))
                    row = cur.fetchone()
                    if not row:
                        return jsonify({"success": False, "error": "Session not found"}), 404
                    generated_at, player_damage_count, hp_heal_count = row

                    cur.execute("""
                        SELECT EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed, "type"
                        FROM wormhole_events
                        WHERE "session" = %s AND "type" IN ('enemy_spawn', 'enemy_killed')
                        ORDER BY "time" ASC
                    """, (generated_at, session_key))
                    event_rows = cur.fetchall()

                    cur.execute("""
                        SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                        FROM wormhole_events WHERE "session" = %s
                    """, (session_key,))
                    dur_row  = cur.fetchone()
                    duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

                density_timeline = []
                count = 0
                for elapsed, event_type in event_rows:
                    if event_type == 'enemy_spawn':
                        count += 1
                    elif event_type == 'enemy_killed':
                        count = max(0, count - 1)
                    density_timeline.append({"x": round(float(elapsed), 2), "y": count})

                avg_density  = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
                damage_rate  = float(player_damage_count or 0) / duration
                healing_rate = float(hp_heal_count or 0) / duration
                pressure     = round(damage_rate + avg_density - healing_rate, 3)

                return jsonify({
                    "success":        True,
                    "session":        session_key,
                    "density":        density_timeline,
                    "avg_density":    round(avg_density, 2),
                    "damage_rate":    round(damage_rate, 4),
                    "healing_rate":   round(healing_rate, 4),
                    "pressure_score": pressure,
                    "duration":       round(duration, 1)
                })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time, plus pressure score.
    Accepts ?session=<key> for a single session, or ?config=<hash> to average across all
    sessions sharing that config (density is averaged bucket-by-bucket in 1s windows)."""
    session_key = request.args.get("session")
    config_hash = request.args.get("config")
    if not session_key and not config_hash:
        return jsonify({"success": False, "error": "Missing session or config param"}), 400

    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                if config_hash:
                    sessions = _get_config_sessions(cur, config_hash)
                    if not sessions:
                        return jsonify({"success": False, "error": "No sessions found for this config"}), 404

                    cur.execute(f"""
                        SELECT SUM("playerDamageCount"), SUM("hpHealCount"), COUNT(*)
                        FROM wormhole_session_summary
                        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = ANY(%s)
                    """, (sessions,))
                    agg = cur.fetchone()
                    total_damage_count = float(agg[0] or 0)
                    total_heal_count   = float(agg[1] or 0)
                    n_sessions         = int(agg[2] or 1)


                    cur.execute("""
                        SELECT
                            s."session",
                            EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) AS elapsed,
                            e."type"
                        FROM wormhole_events e
                        JOIN wormhole_session_summary s
                          ON e."session"::timestamptz = s."generatedAt"
                        WHERE e."session" = ANY(%s)
                          AND e."type" IN ('enemy_spawn', 'enemy_killed')
                        ORDER BY e."session", e."time" ASC
                    """, (sessions,))
                    all_event_rows = cur.fetchall()

                    cur.execute("""
                        SELECT "session", EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                        FROM wormhole_events
                        WHERE "session" = ANY(%s)
                        GROUP BY "session"
                    """, (sessions,))
                    dur_map = {r[0]: float(r[1] or 1) for r in cur.fetchall()}

                    from collections import defaultdict
                    session_buckets = {}  
                    from itertools import groupby
                    from operator import itemgetter

                    current_session = None
                    count = 0
                    session_timeline = []

                    for row in all_event_rows:
                        sess, elapsed, etype = row[0], float(row[1]), row[2]
                        if sess != current_session:
                            if current_session is not None:
                                buckets = {}
                                for pt in session_timeline:
                                    b = int(pt[0])
                                    buckets[b] = pt[1]
                                session_buckets[current_session] = buckets
                            current_session = sess
                            count = 0
                            session_timeline = []
                        if etype == 'enemy_spawn':
                            count += 1
                        elif etype == 'enemy_killed':
                            count = max(0, count - 1)
                        session_timeline.append((elapsed, count))
                    if current_session and session_timeline:
                        buckets = {}
                        for pt in session_timeline:
                            b = int(pt[0])
                            buckets[b] = pt[1]
                        session_buckets[current_session] = buckets

                    all_buckets = set()
                    for b in session_buckets.values():
                        all_buckets.update(b.keys())

                    avg_duration = sum(dur_map.values()) / len(dur_map) if dur_map else 1.0
                    density_timeline = []
                    for b in sorted(all_buckets):
                        vals = [sb[b] for sb in session_buckets.values() if b in sb]
                        if vals:
                            density_timeline.append({"x": float(b), "y": round(sum(vals) / len(vals), 2)})

                    avg_density  = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
                    damage_rate  = (total_damage_count / n_sessions) / avg_duration
                    healing_rate = (total_heal_count   / n_sessions) / avg_duration
                    pressure     = round(damage_rate + avg_density - healing_rate, 3)

                    return jsonify({
                        "success":        True,
                        "config":         config_hash,
                        "session_count":  n_sessions,
                        "density":        density_timeline,
                        "avg_density":    round(avg_density, 2),
                        "damage_rate":    round(damage_rate, 4),
                        "healing_rate":   round(healing_rate, 4),
                        "pressure_score": pressure,
                        "duration":       round(avg_duration, 1)
                    })

                else:
                    cur.execute("""
                        SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                        FROM wormhole_session_summary
                        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                    """, (session_key,))
                    row = cur.fetchone()
                    if not row:
                        return jsonify({"success": False, "error": "Session not found"}), 404
                    generated_at, player_damage_count, hp_heal_count = row

                    cur.execute("""
                        SELECT EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed, "type"
                        FROM wormhole_events
                        WHERE "session" = %s AND "type" IN ('enemy_spawn', 'enemy_killed')
                        ORDER BY "time" ASC
                    """, (generated_at, session_key))
                    event_rows = cur.fetchall()

                    cur.execute("""
                        SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                        FROM wormhole_events WHERE "session" = %s
                    """, (session_key,))
                    dur_row  = cur.fetchone()
                    duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

                density_timeline = []
                count = 0
                for elapsed, event_type in event_rows:
                    if event_type == 'enemy_spawn':
                        count += 1
                    elif event_type == 'enemy_killed':
                        count = max(0, count - 1)
                    density_timeline.append({"x": round(float(elapsed), 2), "y": count})

                avg_density  = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
                damage_rate  = float(player_damage_count or 0) / duration
                healing_rate = float(hp_heal_count or 0) / duration
                pressure     = round(damage_rate + avg_density - healing_rate, 3)

                return jsonify({
                    "success":        True,
                    "session":        session_key,
                    "density":        density_timeline,
                    "avg_density":    round(avg_density, 2),
                    "damage_rate":    round(damage_rate, 4),
                    "healing_rate":   round(healing_rate, 4),
                    "pressure_score": pressure,
                    "duration":       round(duration, 1)
                })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    """Enemy count on screen over time for a specific session, plus a pressure score."""
    session_key = request.args.get("session")
    if not session_key:
        return jsonify({"success": False, "error": "Missing session param"}), 400
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT "generatedAt", "playerDamageCount", "hpHealCount"
                    FROM wormhole_session_summary
                    WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                                  'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = %s
                """, (session_key,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": "Session not found"}), 404
                generated_at, player_damage_count, hp_heal_count = row

                cur.execute("""
                    SELECT
                        EXTRACT(EPOCH FROM ("time" - %s)) AS elapsed,
                        "type"
                    FROM wormhole_events
                    WHERE "session" = %s
                      AND "type" IN ('enemy_spawn', 'enemy_killed')
                    ORDER BY "time" ASC
                """, (generated_at, session_key))
                event_rows = cur.fetchall()

                cur.execute("""
                    SELECT EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
                    FROM wormhole_events
                    WHERE "session" = %s
                """, (session_key,))
                dur_row = cur.fetchone()
                duration = float(dur_row[0] or 1) if dur_row and dur_row[0] else 1.0

        density_timeline = []
        count = 0
        for elapsed, event_type in event_rows:
            if event_type == 'enemy_spawn':
                count += 1
            elif event_type == 'enemy_killed':
                count = max(0, count - 1)
            density_timeline.append({"x": round(float(elapsed), 2), "y": count})

        avg_density   = (sum(p["y"] for p in density_timeline) / len(density_timeline)) if density_timeline else 0.0
        damage_rate   = float(player_damage_count or 0) / duration
        healing_rate  = float(hp_heal_count or 0) / duration
        pressure      = round(damage_rate + avg_density - healing_rate, 3)

        return jsonify({
            "success":        True,
            "session":        session_key,
            "density":        density_timeline,
            "avg_density":    round(avg_density, 2),
            "damage_rate":    round(damage_rate, 4),
            "healing_rate":   round(healing_rate, 4),
            "pressure_score": pressure,
            "duration":       round(duration, 1)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500