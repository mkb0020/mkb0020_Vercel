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
                        AVG("enemyKills"),
                        AVG(CASE WHEN "gameBeaten" = true THEN 1.0 ELSE 0.0 END)
                    FROM wormhole_session_summary
                """)
                row = cur.fetchone()

        return jsonify({
            "success": True,
            "data": {
                "total_sessions": row[0],
                "avg_wave":       float(row[1] or 0),
                "avg_kills":      float(row[2] or 0),
                "win_rate":       float(row[3] or 0)
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
                    SELECT "session"
                    FROM wormhole_events
                    WHERE "session" IS NOT NULL
                    ORDER BY "session" DESC
                    LIMIT %s
                """, (limit,))

                sessions = [row[0].isoformat() for row in cur.fetchall()]

                if not sessions:
                    return jsonify({"success": True, "sessions": [], "data": {}})

                cur.execute("""
                    SELECT "session", "time", "hp"
                    FROM wormhole_events
                    WHERE "session" = ANY(%s)
                    ORDER BY "time" ASC
                """, (sessions,))

                rows = cur.fetchall()

        result = {s: {"labels": [], "hp": []} for s in sessions}

        for session, time, hp in rows:
            if session in result and time is not None:
                result[session]["labels"].append(time.isoformat())
                result[session]["hp"].append(hp)

        return jsonify({
            "success": True,
            "sessions": sessions,
            "data": result
        })

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