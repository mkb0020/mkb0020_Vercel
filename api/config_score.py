"""
/api/wormhole/config-score

Computes a composite balance score (0–100) for a given config hash across three pillars:

  TTK Score    (0–100) — are enemies taking the right amount of time to kill?
  Density Score(0–100) — is each wave putting the right number of enemies on screen?
  HP Score     (0–100) — does the HP/damage/heal curve feel right?

Final Score = TTK_WEIGHT * ttk + DENSITY_WEIGHT * density + HP_WEIGHT * hp

All three pillar scores use additive point buckets: each sub-signal is worth a fixed
number of points, awarded in full if the metric hits its target, zero if it doesn't.
This keeps the math transparent and easy to tune.

Usage:
    GET /api/wormhole/config-score?config=<hash>

Add to your blueprint file:
    from .config_score import config_score_bp
    app.register_blueprint(config_score_bp)
"""

from flask import Blueprint ,request ,jsonify 
import psycopg 
import os 
from dotenv import load_dotenv 

load_dotenv ()
DB_URL =os .environ .get ("DATABASE_URL")

config_score_bp =Blueprint ('config_score',__name__ )


# ── CONFIG HASH (KEEP IN SYNC WITH WORMHOLE_ANALYSIS.PY) ─────────────────────
_CFG_PARTS =[
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
CONFIG_HASH_EXPR ="MD5(CONCAT("+",'|',".join (_CFG_PARTS )+"))"


# ════════════════════════════════════════════════════════════════════════════════
# SCORING CONSTANTS — ALL TTK TARGETS CONFIRMED AGAINST GETTTKSTATUS() IN THE HTML
# ════════════════════════════════════════════════════════════════════════════════

# TTK TARGETS PER ENEMY TYPE (SECONDS). EACH ENEMY IS WORTH 20 POINTS → MAX 100.
# KEPT IN SYNC WITH TTK_TARGETS / GETTTKSTATUS() IN THE DASHBOARD HTML.
TTK_TARGETS ={
"BASIC":{"min":2.0 ,"max":4.0 },# GLIP GLOP — FAST FODDER
"ZIGZAG":{"min":4.0 ,"max":6.0 },# ZIP ZAP    — HARD TO HIT, MID TTK
"FAST":{"min":4.0 ,"max":6.0 },# PHIL       — QUICK BUT NOT FRAGILE
"TANK":{"min":5.0 ,"max":8.0 },# GLORK      — DURABLE BUT NOT A SPONGE
"FLIMFLAM":{"min":4.0 ,"max":7.0 },# FLIM FLAM  — SPECIAL MECHANICS ADD TIME
}
TTK_POINTS_PER_ENEMY =100 /len (TTK_TARGETS )# 20 PTS EACH

# DENSITY TARGETS PER WAVE — KEPT IN SYNC WITH WAVE_TARGETS IN GET_DENSITY_INSIGHTS().
# EACH WAVE IS WORTH 20 POINTS → MAX 100.
DENSITY_TARGETS ={
1 :{"min":1.0 ,"max":2.5 },
2 :{"min":1.5 ,"max":3.5 },
3 :{"min":2.0 ,"max":4.0 },
4 :{"min":2.5 ,"max":5.0 },
5 :{"min":3.0 ,"max":6.0 },
}
DENSITY_POINTS_PER_WAVE =100 /len (DENSITY_TARGETS )# 20 PTS EACH

# HP SUB-SIGNAL POINT BUDGETS (MUST SUM TO 100).
HP_POINTS ={
"dmg_heal_ratio":25 ,# DAMAGE-TO-HEAL RATIO IN THE HEALTHY BAND (1.5–8)
"no_early_deaths":25 ,# NO DEATHS IN THE FIRST 60% OF THE RUN
"slope":25 ,# HP TREND IS NEGATIVE (PLAYER IS UNDER PRESSURE OVER TIME)
"escalation":25 ,# EARLY VS LATE HP DROP IS NOTICEABLE BUT NOT CRUSHING (5–35 HP)
}

# DAMAGE/HEAL RATIO BAND THAT FEELS BALANCED (MIRRORS GET_HP_INSIGHTS THRESHOLDS)
DMG_HEAL_RATIO_MIN =1.5 
DMG_HEAL_RATIO_MAX =8.0 

# EARLY DEATH THRESHOLD: DEATHS BEFORE THIS FRACTION OF THE RUN ARE PENALISED
EARLY_DEATH_THRESHOLD =0.60 

# HP DROP FROM EARLY HALF → LATE HALF THAT FEELS LIKE NATURAL ESCALATION
ESCALATION_MIN =5 # LESS THAN THIS FEELS FLAT / NO RAMP
ESCALATION_MAX =35 # MORE THAN THIS FEELS LIKE A WALL

# MINIMUM SESSIONS REQUIRED BEFORE SCORING IS CONSIDERED MEANINGFUL
MIN_SESSIONS_FOR_SCORE =1 

# ── FINAL SCORE WEIGHTS (MUST SUM TO 1.0) ────────────────────────────────────
TTK_WEIGHT =0.40 
DENSITY_WEIGHT =0.30 
HP_WEIGHT =0.30 


# ════════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════════

def _get_config_sessions (cur ,config_hash ):
    cur .execute (f"""
        SELECT to_char("generatedAt" AT TIME ZONE 'UTC',
                       'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')
        FROM wormhole_session_summary
        WHERE {CONFIG_HASH_EXPR } = %s
        ORDER BY "generatedAt" DESC
    """,(config_hash ,))
    return [row [0 ]for row in cur .fetchall ()]


def _score_ttk (cur ,sessions ):
    """
    Returns (ttk_score 0–100, breakdown dict).
    Each enemy type scores TTK_POINTS_PER_ENEMY if its avg TTK falls inside target.
    Enemy types with no kill events are skipped (not penalised — they may not appear
    in every config's wave set).
    """
    cur .execute ("""
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
    """,(sessions ,))
    rows =cur .fetchall ()

    breakdown ={}
    total_pts =0.0 
    scored_types =0 

    for enemy_type ,avg_ttk ,count in rows :
        if avg_ttk is None or enemy_type not in TTK_TARGETS :
            continue 
        avg_ttk =float (avg_ttk )
        target =TTK_TARGETS [enemy_type ]
        in_range =target ["min"]<=avg_ttk <=target ["max"]
        pts =TTK_POINTS_PER_ENEMY if in_range else 0.0 
        total_pts +=pts 
        scored_types +=1 
        breakdown [enemy_type ]={
        "avg_ttk":round (avg_ttk ,2 ),
        "target_min":target ["min"],
        "target_max":target ["max"],
        "in_range":in_range ,
        "points":round (pts ,1 ),
        "max_points":round (TTK_POINTS_PER_ENEMY ,1 ),
        "samples":int (count ),
        }

        # IF NO ENEMY TYPES WERE OBSERVED AT ALL, SCORE IS NONE (NOT ENOUGH DATA)
    if scored_types ==0 :
        return None ,breakdown 

        # NORMALISE TO 100 BASED ON TYPES ACTUALLY OBSERVED, NOT THE FULL 5
        # (A CONFIG THAT NEVER SPAWNS TANK SHOULDN'T BE PENALISED FOR IT)
    ttk_score =round ((total_pts /(scored_types *TTK_POINTS_PER_ENEMY ))*100 ,1 )

    return ttk_score ,breakdown 


def _score_density (cur ,sessions ):
    """
    Returns (density_score 0–100, breakdown dict).
    Builds per-session density timelines, splits each session into 5 equal wave windows,
    averages the density per wave across all sessions, then checks against DENSITY_TARGETS.
    """
    # PULL ALL SPAWN/KILL EVENTS FOR THE CONFIG'S SESSIONS
    cur .execute ("""
        SELECT
            e."session",
            EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) AS elapsed,
            e."type"
        FROM wormhole_events e
        JOIN wormhole_session_summary s
          ON e."session"::timestamptz = s."generatedAt"
        WHERE e."session" = ANY(%s)
          AND e."type" IN ('enemy_spawn', 'enemy_killed')
        ORDER BY e."session", e."time" ASC
    """,(sessions ,))
    event_rows =cur .fetchall ()

    # DURATION PER SESSION
    cur .execute ("""
        SELECT "session", EXTRACT(EPOCH FROM (MAX("time") - MIN("time")))
        FROM wormhole_events
        WHERE "session" = ANY(%s)
        GROUP BY "session"
    """,(sessions ,))
    dur_map ={r [0 ]:float (r [1 ]or 1 )for r in cur .fetchall ()}

    if not event_rows or not dur_map :
        return None ,{}

        # BUILD DENSITY TIMELINE PER SESSION
    from itertools import groupby 
    from operator import itemgetter 

    session_events ={}
    for sess ,elapsed ,etype in event_rows :
        session_events .setdefault (sess ,[]).append ((float (elapsed ),etype ))

        # FOR EACH SESSION, COMPUTE AVG DENSITY IN EACH OF 5 EQUAL WAVE WINDOWS
    wave_densities ={w :[]for w in range (1 ,6 )}

    for sess ,events in session_events .items ():
        duration =dur_map .get (sess ,1.0 )
        wave_dur =duration /5.0 

        # BUILD RUNNING DENSITY COUNT
        density_timeline =[]
        count =0 
        for elapsed ,etype in sorted (events ,key =itemgetter (0 )):
            if etype =='enemy_spawn':
                count +=1 
            elif etype =='enemy_killed':
                count =max (0 ,count -1 )
            density_timeline .append ((elapsed ,count ))

        for wave_num in range (1 ,6 ):
            w_start =wave_dur *(wave_num -1 )
            w_end =wave_dur *wave_num 
            pts_in_wave =[d for t ,d in density_timeline if w_start <=t <=w_end ]
            if pts_in_wave :
                wave_densities [wave_num ].append (sum (pts_in_wave )/len (pts_in_wave ))

    breakdown ={}
    total_pts =0.0 
    scored_waves =0 

    for wave_num in range (1 ,6 ):
        vals =wave_densities [wave_num ]
        if not vals :
            continue 
        avg_density =sum (vals )/len (vals )
        target =DENSITY_TARGETS [wave_num ]
        in_range =target ["min"]<=avg_density <=target ["max"]
        pts =DENSITY_POINTS_PER_WAVE if in_range else 0.0 
        total_pts +=pts 
        scored_waves +=1 
        breakdown [f"wave{wave_num }"]={
        "avg_density":round (avg_density ,2 ),
        "target_min":target ["min"],
        "target_max":target ["max"],
        "in_range":in_range ,
        "points":round (pts ,1 ),
        "max_points":round (DENSITY_POINTS_PER_WAVE ,1 ),
        }

    if scored_waves ==0 :
        return None ,breakdown 

    density_score =round ((total_pts /(scored_waves *DENSITY_POINTS_PER_WAVE ))*100 ,1 )
    return density_score ,breakdown 


def _score_hp (cur ,sessions ):
    """
    Returns (hp_score 0–100, breakdown dict).
    Aggregates HP sub-signals across all sessions in the config:

      Sub-signal              Points  Condition
      ─────────────────────   ──────  ──────────────────────────────────────
      dmg_heal_ratio           25     avg ratio per session in [1.5, 8.0]
      no_early_deaths          25     avg early deaths per session < 0.5
      slope                    25     avg HP slope across sessions < 0
      escalation               25     avg (early_hp - late_hp) in [5, 35]
    """
    # PULL PER-SESSION SUMMARY STATS
    cur .execute ("""
        SELECT
            to_char("generatedAt" AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"'),
            "playerDamageCount",
            "hpHealCount"
        FROM wormhole_session_summary
        WHERE to_char("generatedAt" AT TIME ZONE 'UTC',
                      'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') = ANY(%s)
    """,(sessions ,))
    summary_rows ={r [0 ]:{"dmg":int (r [1 ]or 0 ),"heal":int (r [2 ]or 0 )}
    for r in cur .fetchall ()}

    # PULL HP EVENT TIMELINES PER SESSION
    cur .execute ("""
        SELECT
            e."session",
            EXTRACT(EPOCH FROM (e."time" - s."generatedAt")) AS elapsed,
            e."hp"
        FROM wormhole_events e
        JOIN wormhole_session_summary s
          ON e."session"::timestamptz = s."generatedAt"
        WHERE e."session" = ANY(%s)
          AND e."hp" IS NOT NULL
        ORDER BY e."session", e."time" ASC
    """,(sessions ,))
    hp_rows =cur .fetchall ()

    if not hp_rows :
        return None ,{}

        # GROUP HP EVENTS BY SESSION
    from collections import defaultdict 
    session_hp =defaultdict (list )
    for sess ,elapsed ,hp in hp_rows :
        session_hp [sess ].append ((float (elapsed ),int (hp )))

    DEATH_FROM =15 
    DEATH_TO =85 

    ratios =[]
    early_death_counts =[]
    slopes =[]
    escalations =[]

    for sess ,timeline in session_hp .items ():
        if not timeline :
            continue 
        total_duration =timeline [-1 ][0 ]if timeline else 1.0 
        mid =total_duration /2.0 

        # DAMAGE / HEAL RATIO
        sm =summary_rows .get (sess )
        if sm and sm ["heal"]>0 :
            ratios .append (sm ["dmg"]/sm ["heal"])
        elif sm and sm ["dmg"]>0 :
            ratios .append (999 )# NO HEALING AT ALL → OFF THE HIGH END

            # EARLY DEATHS
        early_deaths =0 
        for i in range (1 ,len (timeline )):
            t_prev ,hp_prev =timeline [i -1 ]
            t_curr ,hp_curr =timeline [i ]
            pct =t_curr /total_duration if total_duration >0 else 1.0 
            if hp_prev <=DEATH_FROM and hp_curr >=DEATH_TO and pct <EARLY_DEATH_THRESHOLD :
                early_deaths +=1 
        early_death_counts .append (early_deaths )

        # HP SLOPE (LINEAR REGRESSION OVER THE SESSION)
        n =len (timeline )
        times =[p [0 ]for p in timeline ]
        hps =[p [1 ]for p in timeline ]
        mean_t =sum (times )/n 
        mean_h =sum (hps )/n 
        num =sum ((times [i ]-mean_t )*(hps [i ]-mean_h )for i in range (n ))
        den =sum ((times [i ]-mean_t )**2 for i in range (n ))
        slope =num /den if den !=0 else 0 
        slopes .append (slope )

        # EARLY VS LATE HP
        early_hps =[hp for t ,hp in timeline if t <mid ]
        late_hps =[hp for t ,hp in timeline if t >=mid ]
        if early_hps and late_hps :
            escalations .append (sum (early_hps )/len (early_hps )-sum (late_hps )/len (late_hps ))

    breakdown ={}
    total_pts =0.0 

    # ── SUB-SIGNAL 1: DAMAGE / HEAL RATIO ────────────────────────────────────
    sig ="dmg_heal_ratio"
    max_pts =HP_POINTS [sig ]
    if ratios :
        avg_ratio =sum (ratios )/len (ratios )
        in_range =DMG_HEAL_RATIO_MIN <=avg_ratio <=DMG_HEAL_RATIO_MAX 
        pts =max_pts if in_range else 0.0 
        total_pts +=pts 
        breakdown [sig ]={
        "avg_ratio":round (avg_ratio ,2 ),
        "target_min":DMG_HEAL_RATIO_MIN ,
        "target_max":DMG_HEAL_RATIO_MAX ,
        "in_range":in_range ,
        "points":pts ,
        "max_points":max_pts ,
        }
    else :
        breakdown [sig ]={"skipped":True ,"reason":"No sessions with heal data"}

        # ── SUB-SIGNAL 2: NO EARLY DEATHS ────────────────────────────────────────
    sig ="no_early_deaths"
    max_pts =HP_POINTS [sig ]
    if early_death_counts :
        avg_early_deaths =sum (early_death_counts )/len (early_death_counts )
        # AWARD FULL POINTS IF ON AVERAGE < 0.5 EARLY DEATHS PER SESSION
        passes =avg_early_deaths <0.5 
        pts =max_pts if passes else 0.0 
        total_pts +=pts 
        breakdown [sig ]={
        "avg_early_deaths":round (avg_early_deaths ,2 ),
        "threshold":0.5 ,
        "passes":passes ,
        "points":pts ,
        "max_points":max_pts ,
        }

        # ── SUB-SIGNAL 3: NEGATIVE HP SLOPE (UNDER PRESSURE OVER TIME) ───────────
    sig ="slope"
    max_pts =HP_POINTS [sig ]
    if slopes :
        avg_slope =sum (slopes )/len (slopes )
        # NEGATIVE SLOPE = HP DECREASING OVER TIME = PRESSURE EXISTS
        is_negative =avg_slope <0 
        pts =max_pts if is_negative else 0.0 
        total_pts +=pts 
        breakdown [sig ]={
        "avg_slope":round (avg_slope ,4 ),
        "is_negative":is_negative ,
        "points":pts ,
        "max_points":max_pts ,
        }

        # ── SUB-SIGNAL 4: NATURAL ESCALATION (EARLY HP - LATE HP IN [5, 35]) ─────
    sig ="escalation"
    max_pts =HP_POINTS [sig ]
    if escalations :
        avg_drop =sum (escalations )/len (escalations )
        in_range =ESCALATION_MIN <=avg_drop <=ESCALATION_MAX 
        pts =max_pts if in_range else 0.0 
        total_pts +=pts 
        breakdown [sig ]={
        "avg_hp_drop":round (avg_drop ,1 ),
        "target_min":ESCALATION_MIN ,
        "target_max":ESCALATION_MAX ,
        "in_range":in_range ,
        "points":pts ,
        "max_points":max_pts ,
        }

    hp_score =round (total_pts ,1 )
    return hp_score ,breakdown 


    # ════════════════════════════════════════════════════════════════════════════════
    # ENDPOINT
    # ════════════════════════════════════════════════════════════════════════════════

@config_score_bp .route ('/api/wormhole/config-score',methods =['GET'])
def get_config_score ():
    """
    GET /api/wormhole/config-score?config=<hash>

    Response shape:
    {
        "success": true,
        "config": "<hash>",
        "session_count": 12,
        "scores": {
            "ttk":     { "score": 80.0,  "breakdown": { ... } },
            "density": { "score": 60.0,  "breakdown": { ... } },
            "hp":      { "score": 75.0,  "breakdown": { ... } }
        },
        "weights": { "ttk": 0.4, "density": 0.3, "hp": 0.3 },
        "final_score": 72.5,
        "data_quality": "good"   // "good" | "limited" | "insufficient"
    }
    """
    config_hash =request .args .get ("config")
    if not config_hash :
        return jsonify ({"success":False ,"error":"Missing config param"}),400 

    try :
        with psycopg .connect (DB_URL )as conn :
            with conn .cursor ()as cur :
                sessions =_get_config_sessions (cur ,config_hash )

                if not sessions :
                    return jsonify ({"success":False ,"error":"No sessions found for this config"}),404 

                ttk_score ,ttk_breakdown =_score_ttk (cur ,sessions )
                density_score ,density_breakdown =_score_density (cur ,sessions )
                hp_score ,hp_breakdown =_score_hp (cur ,sessions )

        n =len (sessions )

        # ── FINAL WEIGHTED SCORE ──────────────────────────────────────────────
        # ONLY INCLUDE PILLARS THAT RETURNED A SCORE (NOT NONE / INSUFFICIENT DATA)
        pillar_scores =[]
        pillar_weights =[]

        for score ,weight in [
        (ttk_score ,TTK_WEIGHT ),
        (density_score ,DENSITY_WEIGHT ),
        (hp_score ,HP_WEIGHT ),
        ]:
            if score is not None :
                pillar_scores .append (score )
                pillar_weights .append (weight )

        if pillar_scores and pillar_weights :
            total_weight =sum (pillar_weights )
            final_score =sum (s *w for s ,w in zip (pillar_scores ,pillar_weights ))/total_weight 
            final_score =round (final_score ,1 )
        else :
            final_score =None 

        data_quality =(
        "insufficient"if n <MIN_SESSIONS_FOR_SCORE 
        else "limited"if n <3 
        else "good"
        )

        return jsonify ({
        "success":True ,
        "config":config_hash ,
        "session_count":n ,
        "scores":{
        "ttk":{
        "score":ttk_score ,
        "breakdown":ttk_breakdown ,
        },
        "density":{
        "score":density_score ,
        "breakdown":density_breakdown ,
        },
        "hp":{
        "score":hp_score ,
        "breakdown":hp_breakdown ,
        },
        },
        "weights":{
        "ttk":TTK_WEIGHT ,
        "density":DENSITY_WEIGHT ,
        "hp":HP_WEIGHT ,
        },
        "final_score":final_score ,
        "data_quality":data_quality ,
        })

    except Exception as e :
        return jsonify ({"success":False ,"error":str (e )}),500 