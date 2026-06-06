#!/usr/bin/env python3
"""
meowREMIX Rule Compiler v6.0  (DB-backed)
==========================================
Reads all analysis data from Neon (written by api/audio/analyze.py) and
generates forms/rules.js — a single ES-module file consumed directly by
meowREMIX.html.

Changes from v5.0
-----------------
BUG FIXES
  • build_bar_center_rules: keys now include octave (e.g. "G4" not "G") so the
    engine's getSmoothBarCandidate() finds real matches instead of always falling
    back to defaults.  Pass 1 derives centres from real event durations; Pass 2
    falls back to structural-role mapping only when no event data exists.
  • build_compositional_rules: structural role-transitions are now derived from
    the section_rows already loaded from audio_section_analysis (which has a
    structural_role column) instead of the missing "structural_roles" key that
    v5.0 tried to read from full_json.
  • JSON safety pass in write_rules_js: NaN / Infinity values are replaced with
    0.0 before serialisation so the browser never receives invalid JSON.

ENHANCEMENTS
  • --all-songs flag: blend rules from every analysed song in the DB,
    count-weighted, so the more songs you ingest the richer the output.
  • build_bucket_transition_rules (NEW): encodes which bucket naturally follows
    which (long→medium, short→medium arcs etc.) so the engine picks note lengths
    that feel musically coherent rather than random.
  • build_bucket_rhythm_bias (NEW): maps each bucket to duration-type
    probabilities so the engine pairs long notes with slow rhythms and short
    notes with fast ones automatically.
  • build_bucket_tension_map (NEW): per-bucket tension statistics so the engine
    can bias toward calm pitches on long notes and expressive pitches on short
    staccato ones.
  • --minify flag: write compact JS for production builds.

Audio asset paths (relative to forms/ dir):
  projects/audio/notes/long/{note}.m4a
  projects/audio/notes/medium/{note}.m4a
  projects/audio/notes/short/{note}.m4a
"""

import os
import re
import math
import json
import logging
import warnings
import psycopg
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# ── LOGGING ───────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format='  %(message)s')
logger = logging.getLogger(__name__)

# ── PATHS ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)

DB_URL = os.environ.get("DATABASE_URL")
OUTPUT_JS = PROJECT_ROOT / "forms" / "rules.js"

print(f"ENV_PATH : {ENV_PATH}  (exists={ENV_PATH.exists()})")
print(f"DB_URL   : {bool(DB_URL)}")

# NOTE SAMPLE NAMES — ORDER MATTERS, MUST MATCH MEOWREMIX.HTML SAMPLE_NAMES
SAMPLE_NAMES = ["g", "a", "b", "c", "d", "e", "f", "g2"]

# AUDIO PATH ROOTS FOR EACH BUCKET (RELATIVE TO THE HTML FILE IN FORMS/)
AUDIO_PATHS = {
    "long": "../projects/audio/notes/long",
    "medium": "../projects/audio/notes/medium",
    "short": "../projects/audio/notes/short",
}

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 1 — Replace BUCKET_SEQUENCE_PRIOR (lines ~88-94 in rules.py)
# Much heavier bias toward long/medium to prevent staccato chaining
# ══════════════════════════════════════════════════════════════════════════════
BUCKET_SEQUENCE_PRIOR = {
    "long":   [("long", 0.55), ("medium", 0.38), ("short", 0.07)],
    "medium": [("long", 0.30), ("medium", 0.50), ("short", 0.20)],
    "short":  [("long", 0.15), ("medium", 0.60), ("short", 0.25)],
}

# ══════════════════════════════════════════════════════════════════════════════
# PATCH 2 — Replace BUCKET_RHYTHM_PRIOR (lines ~96-101 in rules.py)
# Long notes now strongly prefer whole/dotted-half — no quarters at all
# Short notes capped at eighth — no sixteenth spam
# ══════════════════════════════════════════════════════════════════════════════
BUCKET_RHYTHM_PRIOR = {
    "long":   {"whole": 8, "dotted-half": 6, "half": 4},
    "medium": {"half": 3, "dotted-quarter": 4, "quarter": 5, "dotted-eighth": 2},
    "short":  {"dotted-quarter": 2, "quarter": 4, "dotted-eighth": 3, "eighth": 4},
}

# PER-BUCKET TARGET TENSION (USED TO COMPUTE PITCH-BIAS MULTIPLIERS)
BUCKET_TENSION_TARGET = {"long": 0.15, "medium": 0.30, "short": 0.55}


# ══════════════════════════════════════════════════════════════════════════════
# DB HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _connect():
    from dotenv import load_dotenv
    load_dotenv(ENV_PATH, override=True)
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set.")
    return psycopg.connect(db_url)


def _rows_as_dicts(cur):
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def build_rules_js_string(song_name, music_rules, comp_library, meta, minify=False):
    """
    Return the rules.js content as a string (no file I/O).
    This is the pure version used by both main() and save_to_neon().
    """
    music_rules  = _clean_json(music_rules)
    comp_library = _clean_json(comp_library)
    meta         = _clean_json(meta)
    indent = None if minify else 2
    return (
        f"// Auto-generated — meowREMIX Rule Engine v6.0\n"
        f"// Source song  : {song_name}\n"
        f"// Generated at : {meta['generatedAt']}\n"
        f"// DO NOT EDIT — regenerate via: POST /api/audio/rebuild-rules\n\n"
        f"export const metadata = {json.dumps(meta, indent=indent)};\n\n"
        f"export const musicRules = {json.dumps(music_rules, indent=indent)};\n\n"
        f"export const ruleLibrary = {json.dumps(comp_library, indent=indent)};\n"
    )


def save_to_neon(rules_js_content: str, song_name: str):
    """
    Upsert the compiled rules.js string into audio_rules_cache (single row).
    Creates the table if it doesn't exist yet.
    """
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audio_rules_cache (
                    id          INTEGER PRIMARY KEY DEFAULT 1,
                    rules_js    TEXT NOT NULL,
                    compiled_at TIMESTAMPTZ DEFAULT NOW(),
                    song_names  TEXT,
                    CHECK (id = 1)
                )
            """)
            cur.execute("""
                INSERT INTO audio_rules_cache (id, rules_js, compiled_at, song_names)
                VALUES (1, %s, NOW(), %s)
                ON CONFLICT (id) DO UPDATE
                    SET rules_js    = EXCLUDED.rules_js,
                        compiled_at = EXCLUDED.compiled_at,
                        song_names  = EXCLUDED.song_names
            """, (rules_js_content, song_name))
        conn.commit()
        logger.info(f"  ✓ rules.js saved to Neon audio_rules_cache ({len(rules_js_content)//1024} KB)")
    finally:
        conn.close()


import requests

BASE_URL = os.environ.get("INGEST_URL", "").rstrip("/")

def _fetch_rules_data(all_songs=False, song_id=None):
    """Fetch all rules data from Vercel instead of connecting to Neon directly."""
    if not BASE_URL:
        raise RuntimeError(
            "INGEST_URL not set in .env\n"
            "  Add: INGEST_URL=https://mkb0020.vercel.app"
        )
    params = {}
    if all_songs:  params["all_songs"] = "true"
    if song_id:    params["song_id"]   = str(song_id)

    logger.info(f"  Fetching rules data from {BASE_URL}/api/audio/rules-data ...")
    r = requests.get(f"{BASE_URL}/api/audio/rules-data", params=params, timeout=120)
    r.raise_for_status()
    return r.json()


def _coerce(row):
    out = {}
    for k, v in row.items():
        if k.endswith('_json') and isinstance(v, str):
            try:    v = json.loads(v)
            except: pass
        if hasattr(v, '__float__') and not isinstance(v, (bool, int)):
            out[k] = float(v) if v is not None else None
        else:
            out[k] = v
    return out

def _safe(v, fallback=0.0):
    """Return v if finite float, else fallback."""
    if v is None:
        return fallback
    try:
        f = float(v)
        return f if math.isfinite(f) else fallback
    except (TypeError, ValueError):
        return fallback


def _clean_json(obj):
    """Recursively replace NaN / Infinity so the browser gets valid JSON."""
    if isinstance(obj, float):
        return 0.0 if (math.isnan(obj) or math.isinf(obj)) else obj
    if isinstance(obj, dict):
        return {k: _clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_json(i) for i in obj]
    return obj


# ══════════════════════════════════════════════════════════════════════════════
# SONG SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def pick_song(conn, song_id=None, all_songs=False):
    """
    Returns a list of (song_id, song_name) tuples.
    - song_id given  → single entry
    - all_songs=True → every analysed song
    - default        → most recent analysed song
    """
    with conn.cursor() as cur:
        if song_id is not None:
            cur.execute("SELECT id, song_name FROM audio_songs WHERE id = %s", (song_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Song id={song_id} not found.")
            return [row]

        cur.execute("""
            SELECT DISTINCT s.id, s.song_name
            FROM audio_songs s
            JOIN audio_analyses a ON a.song_id = s.id
            ORDER BY s.id
        """)
        rows = cur.fetchall()

    if not rows:
        raise RuntimeError(
            "No analysed songs found in DB.\n"
            "  Run: python scripts/converter.py\n"
            "  Then POST /api/audio/analyze/<id>"
        )

    if all_songs:
        return list(rows)

    if len(rows) > 1:
        logger.info(
            f"  Multiple analysed songs found. Using most recent: "
            f"'{rows[-1][1]}' (id={rows[-1][0]}).  "
            f"Pass --all-songs to blend all."
        )
    return [rows[-1]]


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════════════════════

def load_transitions(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.from_pitch, t.to_pitch, t.count, t.probability
            FROM audio_pitch_transitions t
            JOIN audio_analyses a ON a.id = t.analysis_id
            WHERE t.song_id = %s
            ORDER BY a.created_at DESC, t.count DESC
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


def load_intervals(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT i.interval, i.frequency, i.percentage
            FROM audio_interval_distribution i
            JOIN audio_analyses a ON a.id = i.analysis_id
            WHERE i.song_id = %s
            ORDER BY a.created_at DESC, i.interval
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


def load_phrases(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT p.phrase_id, p.start_measure, p.end_measure,
                   p.length_beats, p.length_measures, p.phrase_start_degree,
                   p.phrase_end_degree, p.curve_type, p.cadence_type,
                   p.avg_tension, p.peak_tension
            FROM audio_phrase_analysis p
            JOIN audio_analyses a ON a.id = p.analysis_id
            WHERE p.song_id = %s
            ORDER BY a.created_at DESC, p.phrase_id
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


def load_sections(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT s.section_id, s.start_bar, s.end_bar,
                   s.average_tension, s.peak_tension,
                   s.cadence_density, s.structural_role
            FROM audio_section_analysis s
            JOIN audio_analyses a ON a.id = s.analysis_id
            WHERE s.song_id = %s
            ORDER BY a.created_at DESC, s.start_bar
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


def load_motifs(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT m.motif_str, m.motif_length, m.reuse_count,
                   m.first_occurrence_measure, m.avg_return_distance,
                   m.variation_type
            FROM audio_motif_results m
            JOIN audio_analyses a ON a.id = m.analysis_id
            WHERE m.song_id = %s
            ORDER BY a.created_at DESC, m.reuse_count DESC
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


def load_summary(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT avg_interval_size, stepwise_motion_ratio, motif_density,
                   cadence_density, tension_variance, phrase_length_average,
                   familiarity_score, novelty_score, motif_return_rate,
                   avg_return_distance, cadence_frequency, climax_location,
                   full_json, dest_probs_json, sections_json, trajectory_json
            FROM audio_analyses
            WHERE song_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (song_id,))
        row = cur.fetchone()
        if not row:
            raise RuntimeError(f"No analysis found for song_id={song_id}")
        cols = [d[0] for d in cur.description]
        d = dict(zip(cols, row))
        for k, v in d.items():
            if k.endswith('_json'):
                continue
            if hasattr(v, '__float__') and not isinstance(v, (bool, int)):
                d[k] = float(v) if v is not None else None
        return d


def load_note_events_aggregated(conn, song_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT event_index, measure_number, beat_position,
                   pitch, pitch_class, octave, scale_degree,
                   duration_quarter_length, duration_type, duration_sec,
                   tempo_bpm, tension_score, beat_strength,
                   is_rest, is_measure_start,
                   note_length_bucket, note_name, audio_file,
                   interval_from_previous, interval_to_next,
                   melodic_smoothness, connection_score,
                   previous_pitch, next_pitch,
                   previous_duration_type, next_duration_type,
                   absolute_offset_quarters, voice_index,
                   local_chord, local_chord_root, local_chord_quality,
                   harmonic_function
            FROM audio_note_events
            WHERE song_id = %s
            ORDER BY absolute_offset_quarters, voice_index
        """, (song_id,))
        return [_coerce(r) for r in _rows_as_dicts(cur)]


# ══════════════════════════════════════════════════════════════════════════════
# MULTI-SONG BLENDING HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _merge_transitions(all_rows):
    """Count-weighted merge of transition rows from multiple songs."""
    pair_counts = Counter()
    for rows in all_rows:
        for r in rows:
            pair_counts[(r['from_pitch'], r['to_pitch'])] += int(r['count'] or 1)
    by_from = defaultdict(int)
    for (fp, _), cnt in pair_counts.items():
        by_from[fp] += cnt
    merged = []
    for (fp, tp), cnt in pair_counts.items():
        total = by_from[fp]
        merged.append({
            'from_pitch': fp,
            'to_pitch': tp,
            'count': cnt,
            'probability': round(cnt / total, 6) if total else 0.0,
        })
    return merged


def _merge_intervals(all_rows):
    freq_map = Counter()
    for rows in all_rows:
        for r in rows:
            freq_map[int(r['interval'])] += int(r['frequency'] or 0)
    total = sum(freq_map.values()) or 1
    return [
        {'interval': iv, 'frequency': cnt, 'percentage': round(cnt / total * 100, 4)}
        for iv, cnt in sorted(freq_map.items())
    ]


# ══════════════════════════════════════════════════════════════════════════════
# GENERAL HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def filter_low_frequency(items, count_key='count', bottom_percent=10):
    if not items:
        return items
    counts = [r[count_key] for r in items if r.get(count_key) is not None]
    if not counts:
        return items
    counts_sorted = sorted(counts)
    idx = max(0, int(len(counts_sorted) * bottom_percent / 100) - 1)
    threshold = counts_sorted[idx]
    return [r for r in items if (r.get(count_key) or 0) > threshold]


def normalize_weights(items, weight_key='weight'):
    total = sum(r.get(weight_key, 0) for r in items)
    if total > 0:
        for r in items:
            r[weight_key] = round(r.get(weight_key, 0) / total, 6)
    return items


def is_degenerate_motif(pattern_list):
    return not pattern_list or all(p == pattern_list[0] for p in pattern_list)


def repair_split_pitch_tokens(tokens):
    repaired, i = [], 0
    while i < len(tokens):
        t = tokens[i].strip()
        if (len(t) == 1 and t.isalpha() and i + 1 < len(tokens)
                and tokens[i + 1].strip().isdigit()):
            repaired.append(t + tokens[i + 1].strip())
            i += 2
        else:
            repaired.append(t)
            i += 1
    return repaired


def parse_motif_robust(motif_str):
    raw = repair_split_pitch_tokens(motif_str.split())
    valid = [p for p in raw if re.match(r'^[A-G][#\-]?\d*$', p) or p == 'REST']
    return valid if len(valid) == len(raw) else []


def pitch_to_midi(pitch_str):
    if not pitch_str or pitch_str == 'REST':
        return None
    m = re.match(r'^([A-G][#b\-]?)(\d+)$', str(pitch_str))
    if not m:
        return None
    note_name, octave = m.groups()
    note_name = (note_name.replace('Db', 'C#').replace('Eb', 'D#')
                 .replace('Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')
                 .replace('B-', 'A#'))
    semitone_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5,
                    'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    if note_name not in semitone_map:
        return None
    return semitone_map[note_name] + 12 * (int(octave) + 1)


def voice_leading_penalty(melody_note, harmony_note):
    midi_mel = pitch_to_midi(melody_note)
    midi_harm = pitch_to_midi(harmony_note)
    if midi_mel is None or midi_harm is None:
        return 1.0
    ivl = abs(midi_mel - midi_harm) % 12
    penalty = 1.0
    if ivl > 5: penalty *= 0.6
    if ivl in (1, 2): penalty *= 1.2
    return min(1.5, max(0.3, penalty))


# ══════════════════════════════════════════════════════════════════════════════
# LOW-LEVEL RULE BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def build_transition_rules(transition_rows):
    rows = filter_low_frequency(transition_rows, 'count', bottom_percent=10)
    by_pitch = defaultdict(list)
    for r in rows:
        by_pitch[r['from_pitch']].append(r)
    rules = {}
    for pitch, group in by_pitch.items():
        candidates = []
        for r in group:
            w = r['probability']
            if r['to_pitch'] == pitch:
                w *= 0.5   # SAME-NOTE PENALTY
            candidates.append({'note': r['to_pitch'], 'weight': w})
        rules[pitch] = normalize_weights(candidates)
    return rules


def build_interval_bias(interval_rows):
    rows = filter_low_frequency(interval_rows, 'frequency', bottom_percent=10)
    result = {}
    for r in rows:
        iv = r.get('interval')
        if iv is None:
            continue
        iv = int(iv)
        key = f"+{iv}" if iv > 0 else str(iv)
        result[key] = round(_safe(r.get('percentage')) / 100.0, 6)
    total = sum(result.values())
    if total > 0:
        result = {k: round(v / total, 6) for k, v in result.items()}
    return result


def build_motif_bank(motif_rows):
    rows = [r for r in motif_rows if _safe(r.get('reuse_count')) >= 2]
    rows = filter_low_frequency(rows, 'reuse_count', bottom_percent=10)
    if not rows:
        return [], {}
    total = sum(r['reuse_count'] for r in rows)
    motifs = []
    by_entry = {}
    for r in rows:
        pattern = parse_motif_robust(r['motif_str'])
        if not pattern or is_degenerate_motif(pattern):
            continue
        weight = round(r['reuse_count'] / total, 6)
        obj = {"pattern": pattern, "weight": weight}
        motifs.append(obj)
        by_entry.setdefault(pattern[0], []).append(obj)
    return motifs, by_entry


def build_rhythm_patterns(events):
    DUR_QL = {
        'whole': 4.0, 'half': 2.0, 'quarter': 1.0, 'eighth': 0.5,
        'sixteenth': 0.25, 'thirty-second': 0.125,
        'dotted-half': 3.0, 'dotted-quarter': 1.5, 'dotted-eighth': 0.75,
        'other': 1.0,
    }
    beats_per_measure = 4
    dur_seq = [e['duration_type'] for e in events if not e['is_rest'] and e.get('duration_type')]

    def ql_sum(pat):
        return sum(DUR_QL.get(d, 1.0) for d in pat)

    def valid(pat):
        total = ql_sum(pat)
        if total <= 0:
            return False
        ratio = total / beats_per_measure
        return abs(ratio - round(ratio)) < 0.02

    pair_counts = Counter()
    triple_counts = Counter()
    single_counts = Counter(dur_seq)

    for i in range(len(dur_seq) - 1):
        gram = (dur_seq[i], dur_seq[i + 1])
        if valid(gram):
            pair_counts[gram] += 1
    for i in range(len(dur_seq) - 2):
        gram = (dur_seq[i], dur_seq[i + 1], dur_seq[i + 2])
        if valid(gram):
            triple_counts[gram] += 1

    pattern_items = []
    total_pat = sum(pair_counts.values()) + sum(triple_counts.values())
    for gram, cnt in pair_counts.items():
        pattern_items.append({'pattern': list(gram), 'weight': cnt / total_pat if total_pat else 0})
    for gram, cnt in triple_counts.items():
        pattern_items.append({'pattern': list(gram), 'weight': cnt / total_pat if total_pat else 0})

    total_single = sum(single_counts.values())
    singles = {
        dur: round(cnt / total_single, 6)
        for dur, cnt in single_counts.items()
        if cnt / total_single > 0.02
    }
    return pattern_items, singles


def build_beat_duration_rules(events):
    DUR_QL = {
        'whole': 4.0, 'half': 2.0, 'quarter': 1.0, 'eighth': 0.5,
        'sixteenth': 0.25, 'thirty-second': 0.125,
        'dotted-half': 3.0, 'dotted-quarter': 1.5, 'dotted-eighth': 0.75,
        'other': 1.0,
    }
    beats_per_measure = 4
    beat_counts = defaultdict(Counter)
    for e in events:
        bp = e.get('beat_position')
        dt = e.get('duration_type')
        if bp is None or not dt or e['is_rest']:
            continue
        bp_rounded = round(float(bp), 2)
        ql = DUR_QL.get(dt, 1.0)
        remaining = beats_per_measure - ((bp_rounded - 1) % beats_per_measure)
        if ql <= remaining + 0.02:
            beat_counts[bp_rounded][dt] += 1
    rules = {}
    for bp, counter in beat_counts.items():
        total = sum(counter.values())
        rules[str(bp)] = [
            {"duration": dur, "weight": round(cnt / total, 6)}
            for dur, cnt in sorted(counter.items(), key=lambda x: -x[1])
        ]
    return rules


def build_contour_rules(events):
    def to_contour(iv):
        if iv is None:
            return None
        return 'UP' if iv > 0 else ('DOWN' if iv < 0 else 'SAME')

    notes = [e for e in events if not e['is_rest'] and e.get('interval_from_previous') is not None]
    contours = [to_contour(e['interval_from_previous']) for e in notes]
    contours = [c for c in contours if c]

    counts = Counter()
    for n in (2, 3, 4):
        for i in range(len(contours) - n + 1):
            counts[tuple(contours[i:i + n])] += 1

    items = filter_low_frequency(
        [{'pattern': list(k), 'count': v} for k, v in counts.items()],
        'count', bottom_percent=10
    )
    total = sum(r['count'] for r in items)
    return [
        {"pattern": r['pattern'], "weight": round(r['count'] / total, 6)}
        for r in items
    ] if total else []


def build_suspension_rules(events):
    notes = [e for e in events
             if not e['is_rest']
             and e.get('tension_score') is not None
             and e.get('interval_to_next') is not None]
    susp_pairs = Counter()
    for e in notes:
        tension = _safe(e.get('tension_score'))
        iv_next = e.get('interval_to_next')
        if tension >= 0.4 and iv_next is not None and -3 <= int(iv_next) <= -1:
            p = e.get('pitch', '')
            np_ = e.get('next_pitch', '')
            if p and np_ and p != 'REST' and np_ != 'REST':
                susp_pairs[(p, np_)] += 1
    items = [{'pitch': k[0], 'next_pitch': k[1], 'count': v}
             for k, v in susp_pairs.items()]
    items = filter_low_frequency(items, 'count', bottom_percent=5)
    total = sum(r['count'] for r in items)
    if not total:
        return []
    return [
        {"from": r['pitch'], "to": r['next_pitch'],
         "weight": round(r['count'] / total, 6)}
        for r in items
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PATCH 3 — Replace build_harmony_rules entirely
# ══════════════════════════════════════════════════════════════════════════════

def build_harmony_rules(events):
    # Consonance weight by interval class (semitones mod 12)
    CONSONANCE = {
        0: 0.5,   # unison — boring
        1: 0.1,   # minor 2nd — very dissonant
        2: 0.2,   # major 2nd — dissonant
        3: 0.9,   # minor 3rd — consonant
        4: 1.0,   # major 3rd — very consonant
        5: 0.85,  # perfect 4th — consonant
        6: 0.1,   # tritone — very dissonant
        7: 1.0,   # perfect 5th — very consonant
        8: 0.75,  # minor 6th — consonant
        9: 0.80,  # major 6th — consonant
        10: 0.3,  # minor 7th — mildly dissonant
        11: 0.15, # major 7th — dissonant
    }

    # Group by (song_id, measure_number, offset) — FIX for multi-song blend
    by_beat = defaultdict(list)
    for e in events:
        if e.get('is_rest') or not e.get('pitch'):
            continue
        sid = e.get('voice_index', 0)   # voice_index proxies song separation
        meas = e.get('measure_number', 0)
        offset = round(float(e.get('absolute_offset_quarters') or 0), 3)
        by_beat[(sid, meas, offset)].append(e)

    pair_counts = defaultdict(int)
    pair_consonance = defaultdict(list)
    pair_vert = defaultdict(list)

    for key, group in by_beat.items():
        if len(group) < 2:
            continue
        # Sort highest pitch first → highest = melody
        sorted_g = sorted(
            group,
            key=lambda e: -(pitch_to_midi(e.get('pitch', '')) or 0)
        )
        melody = sorted_g[0]
        mel_p = melody.get('pitch')
        mel_midi = pitch_to_midi(mel_p)
        if not mel_p or mel_midi is None:
            continue

        for other in sorted_g[1:]:
            hp = other.get('pitch')
            if not hp or hp == 'REST':
                continue
            harm_midi = pitch_to_midi(hp)
            if harm_midi is None:
                continue

            # Interval class consonance
            iv_class = abs(mel_midi - harm_midi) % 12
            cons = CONSONANCE.get(iv_class, 0.3)

            # Vertical interval from bass (from analyzer data)
            vert = _safe(other.get('vertical_interval_from_bass'), None)

            pair_counts[(mel_p, hp)] += 1
            pair_consonance[(mel_p, hp)].append(cons)
            if vert is not None:
                pair_vert[(mel_p, hp)].append(vert)

    # Build melody → harmony candidates weighted by consonance
    by_melody = defaultdict(list)
    for (mel, harm), cnt in pair_counts.items():
        avg_cons = float(np.mean(pair_consonance[(mel, harm)]))
        vl = voice_leading_penalty(mel, harm)
        # Down-weight if avg vertical interval is very wide (>9 semitones)
        avg_vert = float(np.mean(pair_vert[(mel, harm)])) if pair_vert[(mel, harm)] else 5.0
        width_penalty = 1.0 if avg_vert <= 9 else max(0.3, 1.0 - (avg_vert - 9) * 0.1)
        raw = cnt * avg_cons * vl * width_penalty
        by_melody[mel].append({'note': harm, 'raw': raw, 'consonance': avg_cons})

    harmony_rules = {}
    for mel, candidates in by_melody.items():
        # Only keep consonant candidates (consonance >= 0.5)
        filtered = [c for c in candidates if c['consonance'] >= 0.5]
        if not filtered:
            filtered = candidates  # fallback: keep all if nothing passes filter
        total = sum(c['raw'] for c in filtered)
        if total > 0:
            harmony_rules[mel] = [
                {'note': c['note'], 'weight': round(c['raw'] / total, 6)}
                for c in sorted(filtered, key=lambda x: -x['raw'])
            ]

    # Pitch-class rules — weighted by avg consonance score
    pc_counts = defaultdict(lambda: defaultdict(float))
    pc_cons_sums = defaultdict(lambda: defaultdict(float))
    for (mel, harm), cnt in pair_counts.items():
        mel_pc = re.sub(r'\d', '', mel) if mel else None
        harm_pc = re.sub(r'\d', '', harm) if harm else None
        if mel_pc and harm_pc:
            avg_cons = float(np.mean(pair_consonance[(mel, harm)]))
            pc_counts[mel_pc][harm_pc] += cnt
            pc_cons_sums[mel_pc][harm_pc] += avg_cons * cnt

    pc_rules = {}
    for mel_pc, harm_map in pc_counts.items():
        weighted = {
            h: pc_cons_sums[mel_pc][h] / cnt
            for h, cnt in harm_map.items()
        }
        total = sum(weighted.values())
        if total > 0:
            pc_rules[mel_pc] = [
                {"note": h, "weight": round(w / total, 6)}
                for h, w in sorted(weighted.items(), key=lambda x: -x[1])
                if w / total > 0.01  # drop negligible candidates
            ]

    return harmony_rules, pc_rules


# ══════════════════════════════════════════════════════════════════════════════
# PATCH 4 — New helper: build_vertical_harmony_rules
# ══════════════════════════════════════════════════════════════════════════════

def build_vertical_harmony_rules(events):
    """
    Build a pitch-class → preferred vertical interval table from
    vertical_interval_from_bass data captured by the analyzer.

    Returns:
    {
        "preferredIntervals": {
            "G": [{"interval": 4, "weight": 0.35}, ...],  # major 3rd above G
            ...
        },
        "consonanceThreshold": 0.5,   # engine should reject pairs below this
        "preferredIntervalClasses": [3, 4, 5, 7, 8, 9]  # globally safe ivs
    }
    """
    CONSONANCE = {
        0: 0.5, 1: 0.1, 2: 0.2, 3: 0.9, 4: 1.0,
        5: 0.85, 6: 0.1, 7: 1.0, 8: 0.75, 9: 0.80,
        10: 0.3, 11: 0.15,
    }

    pc_iv_counts = defaultdict(Counter)
    for e in events:
        if e.get('is_rest') or not e.get('pitch_class'):
            continue
        vert = e.get('vertical_interval_from_bass')
        if vert is None:
            continue
        try:
            iv_class = int(round(float(vert))) % 12
            pc = e.get('pitch_class', '')
            if pc:
                pc_iv_counts[pc][iv_class] += 1
        except (TypeError, ValueError):
            continue

    preferred = {}
    for pc, iv_counter in pc_iv_counts.items():
        total = sum(iv_counter.values())
        if not total:
            continue
        # Weight by both frequency AND consonance
        weighted = {
            iv: (cnt / total) * CONSONANCE.get(iv, 0.3)
            for iv, cnt in iv_counter.items()
        }
        w_total = sum(weighted.values())
        if w_total > 0:
            preferred[pc] = [
                {"interval": iv, "weight": round(w / w_total, 4)}
                for iv, w in sorted(weighted.items(), key=lambda x: -x[1])
                if w / w_total > 0.02
            ]

    return {
        "preferredIntervals": preferred,
        "consonanceThreshold": 0.5,
        "preferredIntervalClasses": [3, 4, 5, 7, 8, 9],
    }


def build_phrase_templates(phrase_rows):
    if not phrase_rows:
        return {}
    lengths = [_safe(r.get('length_beats')) for r in phrase_rows]
    length_counter = Counter(round(l) for l in lengths)
    total = sum(length_counter.values())
    length_dist = {int(k): round(v / total, 4) for k, v in length_counter.items()}

    tensions = [_safe(r.get('avg_tension')) for r in phrase_rows]
    low = [t for t in tensions if t < 0.3]
    med = [t for t in tensions if 0.3 <= t < 0.6]
    high = [t for t in tensions if t >= 0.6]
    arcs = []
    if low: arcs.append({'type': 'low', 'mean_tension': round(float(np.mean(low)), 4)})
    if med: arcs.append({'type': 'medium', 'mean_tension': round(float(np.mean(med)), 4)})
    if high: arcs.append({'type': 'high', 'mean_tension': round(float(np.mean(high)), 4)})

    curve_counts = Counter(r.get('curve_type', 'flat') for r in phrase_rows)
    ct_total = sum(curve_counts.values())
    shapes = (
        [{"shape": k, "probability": round(v / ct_total, 4)} for k, v in curve_counts.most_common()]
        if ct_total else
        [{"shape": "arch", "probability": 0.40}, {"shape": "wave", "probability": 0.30}]
    )
    return {
        'length_distribution': length_dist,
        'typical_tension_arcs': arcs,
        'typical_contour_shapes': shapes,
    }


def build_contour_arcs_from_phrases(phrase_rows):
    ARC_DEFS = [
        ("arch", ["UP", "UP", "DOWN"], 0.25),
        ("rise_plateau", ["UP", "SAME", "DOWN"], 0.20),
        ("wave", ["UP", "DOWN", "UP"], 0.15),
        ("ascending", ["UP", "UP", "UP"], 0.15),
        ("descending", ["DOWN", "DOWN", "DOWN"], 0.15),
        ("stasis", ["SAME", "SAME"], 0.10),
    ]
    arc_map = {
        'rise': 'ascending', 'fall': 'descending', 'rise-fall': 'arch',
        'fall-rise': 'wave', 'plateau': 'stasis', 'flat': 'stasis',
        'multiple_peak': 'wave', 'complex': 'arch',
    }
    arc_counts = {name: 0 for name, _, _ in ARC_DEFS}
    for p in phrase_rows:
        mapped = arc_map.get(p.get('curve_type', 'flat'), 'arch')
        if mapped in arc_counts:
            arc_counts[mapped] += 1

    total_obs = sum(arc_counts.values())
    arcs = []
    for name, pattern, default_w in ARC_DEFS:
        weight = arc_counts[name] / total_obs if total_obs > 0 else default_w
        arcs.append({"name": name, "pattern": pattern, "weight": weight})
    total = sum(a['weight'] for a in arcs)
    if total > 0:
        for a in arcs:
            a['weight'] = round(a['weight'] / total, 4)
    return arcs


def build_style_biases():
    return {
        "ruleBiases": {
            'transition': 0.3, 'harmony': 0.6, 'rhythm': 0.2,
            'motif': 0.4, 'suspension': 0.5, 'contour': 0.3,
        },
        "styleInterpolationDefaults": {
            "Hallelujah": 0.40,
            "Greensleeves": 0.35,
            "ItIsWell": 0.25,
        },
    }


# ── FIX: BAR CENTER RULES NOW PRODUCE FULL PITCH STRINGS E.G. "G4" ────────────

def build_bar_center_rules(section_rows, events):
    """
    Build bar-center transition rules where keys AND values are full pitch
    strings (e.g. "G4", "C4", "D4") so the engine's getSmoothBarCandidate()
    can call pitchToMidi() on them.

    BUG FIX from v5.0: the old version produced pitch-class-only keys ("G",
    "C") which pitchToMidi() cannot parse, so the engine always fell through
    to its hardcoded defaults.

    Strategy (two-pass):
      Pass 1 — derive measure-level tonal centres from real event data:
               the pitch with the longest cumulative duration in each measure.
      Pass 2 — fall back to a structural-role mapping only when Pass 1
               produces no transitions (e.g. song has a single measure).
    """
    # PASS 1: MEASURE → DOMINANT PITCH BY CUMULATIVE DURATION
    dur_by_measure = defaultdict(lambda: defaultdict(float))
    for e in events:
        if e.get('is_rest') or not e.get('pitch'):
            continue
        m = e.get('measure_number')
        ql = _safe(e.get('duration_quarter_length'), 1.0)
        if m is not None:
            dur_by_measure[int(m)][e['pitch']] += ql

    measure_centers = {
        m: max(pitch_durs, key=pitch_durs.get)
        for m, pitch_durs in dur_by_measure.items()
    }

    transitions = Counter()
    for m in sorted(measure_centers)[:-1]:
        transitions[(measure_centers[m], measure_centers[m + 1])] += 1

    # PASS 2: SECTION-ROLE FALLBACK WHEN EVENT DATA IS SPARSE
    if not transitions and section_rows:
        role_pitch = {
            'setup': 'G3',
            'development': 'C4',
            'climax': 'D4',
            'resolution': 'G3',
        }
        centres = [role_pitch.get(s.get('structural_role', 'resolution'), 'G3')
                   for s in section_rows]
        for i in range(len(centres) - 1):
            transitions[(centres[i], centres[i + 1])] += 1

    if not transitions:
        return {
            'G3': [{'note': 'C4', 'weight': 0.50}, {'note': 'D4', 'weight': 0.50}],
            'C4': [{'note': 'G3', 'weight': 0.40}, {'note': 'D4', 'weight': 0.60}],
            'D4': [{'note': 'G3', 'weight': 0.70}, {'note': 'C4', 'weight': 0.30}],
        }

    by_from = defaultdict(list)
    for (prev_p, next_p), cnt in transitions.items():
        by_from[prev_p].append({'note': next_p, 'count': cnt})

    rules = {}
    for prev_p, candidates in by_from.items():
        total = sum(c['count'] for c in candidates)
        rules[prev_p] = [
            {"note": c['note'], "weight": round(c['count'] / total, 6)}
            for c in sorted(candidates, key=lambda x: -x['count'])
        ]
    return rules


def build_smoothness_rules(events):
    smooth_map = defaultdict(lambda: defaultdict(list))
    for e in events:
        pp = e.get('previous_pitch')
        cp = e.get('pitch')
        ms = e.get('melodic_smoothness')
        if pp and cp and pp != 'REST' and cp != 'REST' and ms is not None:
            try:
                smooth_map[pp][cp].append(float(ms))  # force float
            except (TypeError, ValueError):
                pass

    trans_smooth = {
        pp: {cp: round(float(np.mean(vals)), 6) for cp, vals in targets.items()}
        for pp, targets in smooth_map.items()
    }

    rhythm_flow_map = defaultdict(lambda: defaultdict(list))
    for e in events:
        pd_ = e.get('previous_duration_type')
        cd = e.get('duration_type')
        cs = e.get('connection_score')
        if pd_ and cd and cs is not None:
            try:
                rhythm_flow_map[pd_][cd].append(float(cs))  # force float
            except (TypeError, ValueError):
                pass

    rhythm_flow = [
        {"from": fd, "to": td, "smoothness": round(float(np.mean(vals)), 6)}
        for fd, targets in rhythm_flow_map.items()
        for td, vals in targets.items()
    ]
    return trans_smooth, rhythm_flow


def build_note_length_rules(events):
    bucket_counts = Counter()
    pc_bucket_note = defaultdict(lambda: defaultdict(Counter))
    for e in events:
        if e.get('is_rest'):
            continue
        bucket = e.get('note_length_bucket')
        pc = e.get('pitch_class')
        name = e.get('note_name')
        if bucket and pc and name:
            bucket_counts[bucket] += 1
            pc_bucket_note[pc][bucket][name] += 1

    total = sum(bucket_counts.values())
    bucket_weights = (
        {b: round(cnt / total, 4) for b, cnt in bucket_counts.items()}
        if total else {"long": 0.33, "medium": 0.34, "short": 0.33}
    )
    bucket_by_pitch = {
        pc: {bucket: nc.most_common(1)[0][0] for bucket, nc in buckets.items()}
        for pc, buckets in pc_bucket_note.items()
    }
    return bucket_weights, bucket_by_pitch, AUDIO_PATHS


# ══════════════════════════════════════════════════════════════════════════════
# NEW: BUCKET-LEVEL RULES (THREE ADDITIONS THAT THE ENGINE CAN USE)
# ══════════════════════════════════════════════════════════════════════════════

def build_bucket_transition_rules(events):
    """
    Encode how note-length buckets naturally sequence one after another.
    Data from real events is blended with BUCKET_SEQUENCE_PRIOR so even a
    sparse dataset produces musically sensible behaviour.

    Returns: {bucket: [{next, weight}]}
    """
    observed = defaultdict(Counter)
    prev_bucket = None
    for e in sorted(events, key=lambda x: _safe(x.get('absolute_offset_quarters'))):
        if e.get('is_rest'):
            continue
        cur = e.get('note_length_bucket')
        if cur and prev_bucket:
            observed[prev_bucket][cur] += 1
        if cur:
            prev_bucket = cur

    rules = {}
    for bucket, prior_list in BUCKET_SEQUENCE_PRIOR.items():
        blended = {nb: w * 5 for nb, w in prior_list}  # PRIOR WEIGHT = 5 PSEUDO-COUNTS
        for next_b, cnt in observed.get(bucket, {}).items():
            blended[next_b] = blended.get(next_b, 0) + cnt
        total = sum(blended.values())
        rules[bucket] = [
            {"next": nb, "weight": round(w / total, 4)}
            for nb, w in sorted(blended.items(), key=lambda x: -x[1])
        ]
    return rules


def build_bucket_rhythm_bias(events):
    """
    Per-bucket duration-type probability table.
    Blends BUCKET_RHYTHM_PRIOR with observed data.

    Returns: {bucket: {duration_type: weight}}
    """
    observed = defaultdict(Counter)
    for e in events:
        if e.get('is_rest'):
            continue
        bucket = e.get('note_length_bucket')
        dt = e.get('duration_type')
        if bucket and dt:
            observed[bucket][dt] += 1

    result = {}
    for bucket, prior in BUCKET_RHYTHM_PRIOR.items():
        blended = dict(prior)
        for dt, cnt in observed.get(bucket, {}).items():
            blended[dt] = blended.get(dt, 0) + cnt
        total = sum(blended.values())
        result[bucket] = {
            dt: round(cnt / total, 4)
            for dt, cnt in sorted(blended.items(), key=lambda x: -x[1])
            if cnt / total > 0.01
        }
    return result


def build_bucket_tension_map(events):
    """
    Compute tension statistics per bucket and per (bucket, pitch_class).
    The engine uses this to bias toward stable pitches on long notes and
    expressive pitches on short staccato ones.

    Returns:
      {
        "avgTensionByBucket": {"long": float, "medium": float, "short": float},
        "pitchBias": {
          "long":   {"G": multiplier, ...},   # > 1 = preferred, < 1 = avoid
          "medium": {...},
          "short":  {...},
        }
      }
    """
    bucket_tensions = defaultdict(list)
    pc_bucket_t = defaultdict(lambda: defaultdict(list))
    for e in events:
        if e.get('is_rest'):
            continue
        bucket = e.get('note_length_bucket')
        pc = e.get('pitch_class')
        tension = e.get('tension_score')
        if bucket and tension is not None:
            bucket_tensions[bucket].append(_safe(tension))
            if pc:
                pc_bucket_t[bucket][pc].append(_safe(tension))

    avg_by_bucket = {
        b: round(float(np.mean(vs)), 4) if vs else BUCKET_TENSION_TARGET[b]
        for b, vs in bucket_tensions.items()
    }
    for b in ("long", "medium", "short"):
        avg_by_bucket.setdefault(b, BUCKET_TENSION_TARGET[b])

    pitch_bias = {}
    for bucket in ("long", "medium", "short"):
        t_target = BUCKET_TENSION_TARGET[bucket]
        bias = {}
        for pc, vals in pc_bucket_t.get(bucket, {}).items():
            avg_t = float(np.mean(vals)) if vals else 0.3
            diff = abs(avg_t - t_target)
            bias[pc] = round(max(0.4, 1.5 - diff * 2), 3)
        pitch_bias[bucket] = bias

    return {"avgTensionByBucket": avg_by_bucket, "pitchBias": pitch_bias}


# ══════════════════════════════════════════════════════════════════════════════
# COMPOSITIONAL RULE LIBRARY
# ══════════════════════════════════════════════════════════════════════════════

def build_compositional_rules(summary, section_rows):
    """
    Build the high-level compositional rule library from full_json + section_rows.

    BUG FIX from v5.0: role_transitions are now derived from section_rows
    (structural_role column) instead of the missing "structural_roles" key
    in full_json that v5.0 tried to read.
    """
    analysis = summary.get('full_json') or {}
    if not analysis:
        logger.warning("  full_json missing — compositional rules will use defaults.")

    meta = {
        "schema_version": "6.0",
        "generated_at": datetime.now().isoformat(),
        "tempo_independent": True,
        "description": "Compositional rule library – meowREMIX v6.0.",
    }

    song_analysis = analysis.get("song_analysis", {})
    phrases = analysis.get("phrase_analysis", [])
    sections = analysis.get("section_analysis", [])
    motifs = analysis.get("motif_analysis", [])
    events_list = analysis.get("expectation_events", [])
    traj = analysis.get("trajectory_analysis", {})
    emotional = song_analysis.get("emotional_features", {})
    total_phrases = len(phrases) or 1

    rules = {}

    # PHRASE DESTINATIONS
    dest_probs = song_analysis.get("phrase_destination_distribution", {})
    rules["phrase_destination_rules"] = {"4_bar_phrase": dest_probs}

    # TENSION ARC TEMPLATES
    arc_counts = Counter(p.get("curve_type", "flat") for p in phrases)
    tension_arcs = []
    for shape, cnt in arc_counts.items():
        sp = [p for p in phrases if p.get("curve_type") == shape]
        tensions = [_safe(p.get("avg_tension")) for p in sp]
        avg_dur = float(np.mean([_safe(p.get("length_beats", 4)) for p in sp])) if sp else 4.0
        avg_peak = float(np.mean(tensions)) if tensions else 0.5
        tension_arcs.append({
            "type": shape,
            "frequency": round(cnt / total_phrases, 4),
            "average_duration_beats": round(avg_dur, 2),
            "average_peak_location": round(avg_peak, 4),
        })
    rules["tension_arc_templates"] = tension_arcs

    # MOTIF REUSE
    if motifs:
        ret_dists = [
            _safe(m.get("average_return_distance_bars") or m.get("avg_return_distance"))
            for m in motifs
            if _safe(m.get("average_return_distance_bars") or m.get("avg_return_distance")) > 0
        ]
        avg_return = float(np.mean(ret_dists)) if ret_dists else 8.0
        exact_flags = [
            1 if "exact" in (m.get("variation_types") or [m.get("variation_type", "varied")]) else 0
            for m in motifs
        ]
        exact_rate = float(np.mean(exact_flags)) if exact_flags else 0.27
        var_rate = 1.0 - exact_rate
    else:
        avg_return, exact_rate, var_rate = 8.0, 0.27, 0.34

    rules["motif_rules"] = {
        "average_return_distance": round(avg_return, 1),
        "variation_probability": round(var_rate, 4),
        "exact_repeat_probability": round(exact_rate, 4),
    }

    # FAMILIARITY MODEL
    fam = song_analysis.get("return_to_familiarity", {})
    fam_bl = song_analysis.get("familiarity_novelty_balance", {})
    mr = _safe(fam.get("motif_return_rate"), 0.5)
    rules["familiarity_model"] = {
        "reuse_probability": round(mr, 4),
        "variation_probability": round(1.0 - mr, 4),
        "familiarity_score": round(_safe(fam_bl.get("familiarity_score"), 0.5), 4),
        "novelty_score": round(_safe(fam_bl.get("novelty_score"), 0.5), 4),
    }

    # SECTION TEMPLATES
    section_templates = []
    for sec in sections:
        bar_length = max(1, _safe(sec.get("end_bar")) - _safe(sec.get("start_bar")) + 1)
        section_templates.append({
            "section_id": sec.get("section_id", "?"),
            "average_length_bars": bar_length,
            "cadence_density": _safe(sec.get("cadence_density")),
            "tension_profile": {
                "average": _safe(sec.get("average_tension"), 0.5),
                "peak": _safe(sec.get("peak_tension"), 0.7),
            },
            "structural_role": sec.get("structural_role", "development"),
        })
    rules["section_templates"] = section_templates

    # CADENCE RULES
    cad_counts = Counter(p.get("cadence_type") for p in phrases if p.get("cadence_type"))
    total_cad = sum(cad_counts.values())
    rules["cadence_rules"] = (
        {k: round(v / total_cad, 4) for k, v in cad_counts.items()}
        if total_cad else
        {"authentic": 0.48, "half": 0.22, "plagal": 0.18, "deceptive": 0.12}
    )

    # EXPECTATION / DELAY RULES
    delay_events = [e for e in events_list if e.get("type") == "deferred_resolution"]
    if delay_events:
        avg_delay = float(np.mean([_safe(e.get("delay_length_bars"), 1) for e in delay_events]))
        delay_prob = len(delay_events) / total_phrases
    else:
        delay_prob, avg_delay = 0.18, 1.0
    rules["expectation_rules"] = {
        "delay_probability": round(delay_prob, 4),
        "average_delay_length": round(avg_delay, 1),
    }

    # ── FIX: ROLE TRANSITIONS FROM SECTION_ROWS (NOT MISSING FULL_JSON KEY) ──
    trans_counts = defaultdict(Counter)
    for i in range(len(section_rows) - 1):
        from_role = section_rows[i].get("structural_role", "development")
        to_role = section_rows[i + 1].get("structural_role", "development")
        trans_counts[from_role][to_role] += 1

    role_transitions = {}
    for from_role, nexts in trans_counts.items():
        total = sum(nexts.values())
        role_transitions[from_role] = {k: round(v / total, 4) for k, v in nexts.items()}

    if not role_transitions:
        role_transitions = {
            "setup": {"development": 0.72, "climax": 0.28},
            "development": {"climax": 0.55, "development": 0.30, "resolution": 0.15},
            "climax": {"resolution": 0.80, "development": 0.20},
            "resolution": {"setup": 0.60, "development": 0.40},
        }
    rules["role_transitions"] = role_transitions

    # SCALE-DEGREE PATTERNS
    degree_seqs = []
    for p in phrases:
        try:
            s_val = int(float(p.get("phrase_start_degree") or 0))
            e_val = int(float(p.get("phrase_end_degree") or 0))
            if s_val and e_val:
                degree_seqs.append((s_val, e_val))
        except (ValueError, TypeError):
            continue
    seq_counts = Counter(degree_seqs)
    total_seq = sum(seq_counts.values())
    rules["scale_degree_patterns"] = (
        [{"pattern": list(p), "frequency": round(c / total_seq, 4)}
         for p, c in seq_counts.most_common(20)]
        if total_seq else
        [{"pattern": [1, 2, 3], "frequency": 0.20},
         {"pattern": [5, 4, 3], "frequency": 0.15}]
    )

    # SONG TRAJECTORY
    rules["song_trajectory_templates"] = {
        "climax_position_average": _safe(traj.get("climax_location"), 0.78),
        "resolution_position_average": 0.93,
    }

    # EMOTIONAL PROFILES
    profile = {}
    if _safe(emotional.get("tension_variance")) > 0.1:
        profile["high_tension"] = True
    if _safe(emotional.get("stepwise_motion_ratio"), 1.0) > 0.5:
        profile["stepwise"] = True
    rules["emotional_profiles"] = {"profile_A": profile}

    # RULE PRIORITY WEIGHTS (NOTE_LENGTH_BUCKET ADDED)
    rules["rule_priority"] = {
        "motif_reuse": 0.95,
        "cadence_behavior": 0.88,
        "phrase_destination": 0.85,
        "familiarity": 0.82,
        "tension_arc": 0.80,
        "note_length_bucket": 0.75,
        "trajectory": 0.75,
        "structural_role": 0.70,
        "scale_degree_attraction": 0.60,
        "interval_choice": 0.52,
    }

    # RULE PACKS (CONVENIENCE GROUPINGS FOR THE ENGINE)
    rules["rule_sets"] = {
        "motif_rules": rules["motif_rules"],
        "phrase_rules": rules["phrase_destination_rules"],
        "cadence_rules": rules["cadence_rules"],
        "tension_rules": rules["tension_arc_templates"],
        "section_rules": rules["section_templates"],
        "familiarity_rules": rules["familiarity_model"],
        "role_rules": rules["role_transitions"],
        "scale_degree_rules": rules["scale_degree_patterns"],
        "trajectory_rules": rules["song_trajectory_templates"],
        "emotional_profiles": rules["emotional_profiles"],
    }

    rules["gravity_model"] = {
        "tonic_pull": 0.81,
        "dominant_pull": 0.63,
        "mediant_pull": 0.41,
    }

    rules["emotional_memory_rules"] = {
        "average_motif_return_distance": rules["motif_rules"]["average_return_distance"],
        "return_variation_rate": rules["motif_rules"]["variation_probability"],
        "recognition_strength": _safe(fam_bl.get("familiarity_score"), 0.5),
    }

    rules["confidence_notes"] = {
        "phrase_destinations": len(dest_probs) / 5,
        "tension_arcs": len(tension_arcs) / 5,
        "cadences": len(rules["cadence_rules"]) / 4,
        "motifs": len(motifs) / 100,
    }

    return {**meta, "rule_library": rules}


# ══════════════════════════════════════════════════════════════════════════════
# JS WRITER
# ══════════════════════════════════════════════════════════════════════════════

def write_rules_js(output_path, song_name, music_rules, comp_library, meta,
                   minify=False, save_neon=True):
    """
    Build the rules.js string, write it to disk (for local runs), and
    optionally upsert to Neon so Vercel can serve it dynamically.
    """
    js = build_rules_js_string(song_name, music_rules, comp_library, meta, minify)

    # Always write to disk when called locally
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(js, encoding='utf-8')
        size_kb = output_path.stat().st_size / 1024
        logger.info(f"  ✓ {output_path}  ({size_kb:.1f} KB)")

    # Also push to Neon so /api/audio/rules.js can serve it on Vercel
    if save_neon:
        try:
            save_to_neon(js, song_name)
        except Exception as e:
            logger.warning(f"  ⚠ Neon save failed (rules still written to disk): {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PATCH 5 — Updated main() with vertical harmony integration
# ══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="meowREMIX Rule Compiler v6.0 — fetches from Vercel, writes forms/rules.js"
    )
    parser.add_argument("--song-id", type=int, default=None,
                        help="Song ID to compile rules for (default: most recent).")
    parser.add_argument("--all-songs", action="store_true",
                        help="Blend rules from every analysed song in the DB.")
    parser.add_argument("--minify", action="store_true",
                        help="Write compact (minified) JS output.")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("meowREMIX Rule Compiler v6.0")
    logger.info("=" * 60)
    logger.info(f"Project Root : {PROJECT_ROOT}")
    logger.info(f"Output       : {OUTPUT_JS}")
    logger.info(f"Source URL   : {BASE_URL or '(not set — check INGEST_URL in .env)'}")

    if not BASE_URL:
        logger.error(
            "INGEST_URL is not set.\n"
            "  Add to vercel_app/.env:  INGEST_URL=https://mkb0020.vercel.app"
        )
        import sys; sys.exit(1)

    stats = compile_rules(all_songs=args.all_songs, song_id=args.song_id,
                          minify=args.minify, write_file=True)

    logger.info(f"\n{'─' * 60}")
    logger.info("Rule Compiler v6.0 complete.")
    logger.info(f"  rules.js      → {OUTPUT_JS}")
    logger.info(f"  Transitions   : {stats['transitions']}")
    logger.info(f"  Motifs        : {stats['motifs']}")
    logger.info(f"  Suspensions   : {stats['suspensions']}")
    logger.info(f"  Smoothness    : {stats['smoothness_pairs']}")
    logger.info(f"  Bar centers   : {stats['bar_centers']}")
    logger.info(f"  Note buckets  : {stats['bucket_weights']}")
    logger.info(f"  Bucket trans  : {stats['bucket_transitions']}")
    logger.info(f"  Vertical iv   : {stats['vertical_intervals']}")
    logger.info('─' * 60)


def _fetch_preference_signals() -> dict:
    """
    Fetch the RLHF preference signal summary from the Vercel API.
    Uses /api/audio/analyze/0/preferences which returns the global corpus
    (song_id=0 triggers the fallback that reads all rows).
    Returns empty dict on any failure so compile_rules degrades gracefully.
    """
    if not BASE_URL:
        return {}
    try:
        r = requests.get(f"{BASE_URL}/api/audio/analyze/1/preferences", timeout=30)
        r.raise_for_status()
        data = r.json()
        return data.get("preferences", {})
    except Exception as e:
        logger.warning(f"  ⚠ Could not fetch preference signals: {e}")
        return {}


def _apply_transition_boosts(transitions: dict, pref: dict) -> dict:
    """
    Boost / penalise transition rule weights using merged RLHF signals
    (phrase-derived transitions + sequence panel direct ratings, sequence 2x).

    transition_rules shape: { "G4": [{"note":"A4","weight":0.3}, ...], ... }
    We strip octaves from signal keys to match pitch-class level.
    """
    top_liked    = pref.get("note_transition_signals", {}).get("top_liked",    [])
    top_disliked = pref.get("note_transition_signals", {}).get("top_disliked", [])

    if not top_liked and not top_disliked:
        return transitions

    BOOST_STRENGTH = 2.0   # liked transitions get up to 2× weight
    PEN_STRENGTH   = 0.35  # disliked transitions get down to 0.35× weight

    # Build pc→pc lookup: (from_pc, to_pc) → multiplier
    boost_map = {}
    for sig in top_liked:
        score = sig.get("preference_score", 0)
        if score > 0:
            boost_map[(sig["from"], sig["to"])] = 1 + (BOOST_STRENGTH - 1) * score
    for sig in top_disliked:
        score = sig.get("preference_score", 0)
        if score < 0:
            # score is negative; penalty scales with abs value
            boost_map[(sig["from"], sig["to"])] = PEN_STRENGTH + (1 - PEN_STRENGTH) * (1 + score)

    if not boost_map:
        return transitions

    import re
    def _pc(p): return re.sub(r'\d', '', p) if p else p

    boosted = {}
    for from_note, candidates in transitions.items():
        from_pc = _pc(from_note)
        new_cands = []
        for c in candidates:
            to_pc = _pc(c.get("note", ""))
            mult  = boost_map.get((from_pc, to_pc), 1.0)
            new_cands.append({**c, "weight": round(c.get("weight", 1.0) * mult, 6)})
        boosted[from_note] = new_cands

    return boosted


def _apply_harmony_boosts(harmony_rules: dict, pref: dict) -> dict:
    """
    Boost / penalise harmony rule weights using harmony panel RLHF signals.

    harmony_rules shape: { "G4": [{"note":"B4","weight":0.4}, ...], ... }
    harmony_signals are pitch-class level: {"note_a":"G","note_b":"B", ...}
    """
    harm_sig = pref.get("harmony_signals", {})
    top_liked    = harm_sig.get("top_liked",    [])
    top_disliked = harm_sig.get("top_disliked", [])

    if not top_liked and not top_disliked:
        return harmony_rules

    BOOST_STRENGTH = 2.5
    PEN_STRENGTH   = 0.3

    pair_map = {}
    for sig in top_liked:
        score = sig.get("preference_score", 0)
        if score > 0:
            pair_map[(sig["note_a"], sig["note_b"])] = 1 + (BOOST_STRENGTH - 1) * score
            pair_map[(sig["note_b"], sig["note_a"])] = 1 + (BOOST_STRENGTH - 1) * score  # symmetric
    for sig in top_disliked:
        score = sig.get("preference_score", 0)
        if score < 0:
            mult = PEN_STRENGTH + (1 - PEN_STRENGTH) * (1 + score)
            pair_map[(sig["note_a"], sig["note_b"])] = mult
            pair_map[(sig["note_b"], sig["note_a"])] = mult

    if not pair_map:
        return harmony_rules

    import re
    def _pc(p): return re.sub(r'\d', '', p) if p else p

    boosted = {}
    for from_note, candidates in harmony_rules.items():
        from_pc = _pc(from_note)
        new_cands = []
        for c in candidates:
            to_pc = _pc(c.get("note", ""))
            mult  = pair_map.get((from_pc, to_pc), 1.0)
            new_cands.append({**c, "weight": round(c.get("weight", 1.0) * mult, 6)})
        boosted[from_note] = new_cands

    return boosted


def compile_rules(all_songs=True, song_id=None, minify=False, write_file=False) -> dict:
    """
    Full pipeline: fetch data from Vercel → build all rule structures →
    save rules.js string to Neon (always) → optionally write to disk.

    Returns a stats dict so callers (Flask endpoint, main()) can log results.
    Called by:
      - main()                         (local manual run, write_file=True)
      - /api/audio/rebuild-rules       (Vercel trigger, write_file=False)
    """
    if not BASE_URL:
        raise RuntimeError(
            "INGEST_URL not set in environment.\n"
            "  Add: INGEST_URL=https://mkb0020.vercel.app"
        )

    # ── FETCH ALL DATA FROM VERCEL ────────────────────────────────────────────
    logger.info("\nFetching rules data from Vercel API...")
    payload    = _fetch_rules_data(all_songs=all_songs, song_id=song_id)
    song_ids   = payload["song_ids"]
    songs_map  = {s["id"]: s["song_name"] for s in payload["songs"]}
    blend_mode = len(song_ids) > 1
    song_name  = (
        "+".join(songs_map[sid] for sid in song_ids)
        if blend_mode else
        songs_map[song_ids[0]]
    )

    if blend_mode:
        logger.info(f"  Blending {len(song_ids)} songs: {song_name}")
    else:
        logger.info(f"  Compiling rules for: '{song_name}'  (id={song_ids[0]})")

    # ── UNPACK PAYLOAD ────────────────────────────────────────────────────────
    all_data = payload["data"]

    def get(sid, key):
        """Pull a table for a given song_id, coercing all rows."""
        rows = all_data.get(str(sid), {}).get(key, [])
        return [_coerce(r) for r in rows]

    if blend_mode:
        logger.info("[1-7] Blending data from all songs...")
        trans_rows    = _merge_transitions([get(sid, "transitions") for sid in song_ids])
        interval_rows = _merge_intervals([get(sid, "intervals")    for sid in song_ids])
        primary_id    = song_ids[-1]    # most recent song for structural data
        phrase_rows   = get(primary_id, "phrases")
        section_rows  = get(primary_id, "sections")
        motif_rows    = get(primary_id, "motifs")
        raw_summary   = get(primary_id, "summary")
        summary       = raw_summary[0] if raw_summary else {}
        events        = [e for sid in song_ids for e in get(sid, "events")]
        logger.info(f"    {len(events)} total events across {len(song_ids)} songs")
    else:
        sid = song_ids[0]
        logger.info("[1] Transitions...")
        trans_rows    = get(sid, "transitions")
        logger.info(f"    {len(trans_rows)} rows")
        logger.info("[2] Intervals...")
        interval_rows = get(sid, "intervals")
        logger.info(f"    {len(interval_rows)} rows")
        logger.info("[3] Phrases...")
        phrase_rows   = get(sid, "phrases")
        logger.info(f"    {len(phrase_rows)} phrases")
        logger.info("[4] Sections...")
        section_rows  = get(sid, "sections")
        logger.info(f"    {len(section_rows)} sections")
        logger.info("[5] Motifs...")
        motif_rows    = get(sid, "motifs")
        logger.info(f"    {len(motif_rows)} motifs")
        logger.info("[6] Summary...")
        raw_summary   = get(sid, "summary")
        summary       = raw_summary[0] if raw_summary else {}
        logger.info("[7] Events...")
        events        = get(sid, "events")
        logger.info(f"    {len(events)} events")

    # ── BUILD LOW-LEVEL MUSICRULES ────────────────────────────────────────────
    logger.info("\n--- Building low-level musicRules ---")

    logger.info("[A] Transition rules...")
    transitions = build_transition_rules(trans_rows)

    logger.info("[B] Interval bias...")
    interval_bias = build_interval_bias(interval_rows)

    logger.info("[C] Motif bank...")
    motifs, motifs_by_entry = build_motif_bank(motif_rows)
    logger.info(f"    {len(motifs)} motifs, {len(motifs_by_entry)} entry points")

    logger.info("[D] Rhythm patterns + single durations...")
    rhythm_patterns, single_durations = build_rhythm_patterns(events)

    logger.info("[E] Beat duration rules...")
    beat_dur = build_beat_duration_rules(events)

    logger.info("[F] Contour rules...")
    contours = build_contour_rules(events)

    logger.info("[G] Suspension rules...")
    suspensions = build_suspension_rules(events)

    logger.info("[H] Harmony rules...")
    harmony_rules, pc_harmony = build_harmony_rules(events)

    logger.info("[I] Phrase templates + contour arcs...")
    phrase_templates = build_phrase_templates(phrase_rows)
    contour_arcs     = build_contour_arcs_from_phrases(phrase_rows)
    style_biases     = build_style_biases()

    logger.info("[J] Bar center rules (full pitch strings)...")
    bar_rules = build_bar_center_rules(section_rows, events)
    logger.info(f"    {len(bar_rules)} bar-center pitch anchors")

    logger.info("[K] Smoothness rules...")
    trans_smooth, rhythm_flow = build_smoothness_rules(events)

    logger.info("[L] Note-length bucket rules (long / medium / short)...")
    bucket_weights, bucket_by_pitch, audio_paths = build_note_length_rules(events)
    logger.info(f"    Bucket weights: {bucket_weights}")

    logger.info("[M] Bucket transition rules...")
    bucket_transitions = build_bucket_transition_rules(events)

    logger.info("[N] Bucket × rhythm bias...")
    bucket_rhythm_bias = build_bucket_rhythm_bias(events)

    logger.info("[O] Bucket × tension map...")
    bucket_tension_map = build_bucket_tension_map(events)

    logger.info("[P] Vertical harmony rules...")
    vertical_harmony = build_vertical_harmony_rules(events)
    logger.info(f"    {len(vertical_harmony.get('preferredIntervals', {}))} pitch classes mapped")

    logger.info("[Q] Fetching RLHF preference signals...")
    pref_signals = _fetch_preference_signals()
    if pref_signals.get("total_ratings", 0) > 0:
        by_type = pref_signals.get("by_type", {})
        logger.info(f"    {pref_signals['total_ratings']} total ratings — "
                    f"phrase={by_type.get('phrase',0)}, "
                    f"harmony={by_type.get('harmony',0)}, "
                    f"sequence={by_type.get('sequence',0)}")
        logger.info("[R] Applying RLHF boosts to transition + harmony rules...")
        transitions   = _apply_transition_boosts(transitions,   pref_signals)
        harmony_rules = _apply_harmony_boosts(harmony_rules,    pref_signals)
        logger.info("    ✓ Preference boosts applied")
    else:
        logger.info("    No preference data yet — skipping boosts")

    # ── ASSEMBLE MUSICRULES ───────────────────────────────────────────────────
    total_trans = sum(len(v) for v in transitions.values())
    meta = {
        "source":            song_name,
        "generatedAt":       datetime.now().isoformat(),
        "totalMotifs":       len(motifs),
        "totalTransitions":  total_trans,
        "totalSuspensions":  len(suspensions),
        "voiceLeadingEnabled": True,
        "totalTransitionSmoothnessPairs": sum(len(v) for v in trans_smooth.values()),
        "totalRhythmFlowRules": len(rhythm_flow),
        "engineVersion":     "6.0",
        "blendMode":         blend_mode,
        "noteBuckets":       list(audio_paths.keys()),
        "sampleNames":       SAMPLE_NAMES,
    }

    music_rules = {
        "transitionRules":        transitions,
        "intervalBias":           interval_bias,
        "motifs":                 motifs,
        "motifsByEntry":          motifs_by_entry,
        "rhythmPatterns":         rhythm_patterns,
        "singleDurations":        single_durations,
        "beatDurationRules":      beat_dur,
        "contourRules":           contours,
        "contourArcs":            contour_arcs,
        "harmonyRules":           harmony_rules,
        "pitchClassHarmonyRules": pc_harmony,
        "suspensionRules":        suspensions,
        "phraseTemplates":        phrase_templates,
        "barCenterRules":         bar_rules,
        "styleBiases":            style_biases,
        "smoothnessRules": {
            "transitionSmoothness": trans_smooth,
            "rhythmFlowRules":      rhythm_flow,
            "smoothnessBias":       0.85,
        },
        "verticalHarmonyRules":    vertical_harmony,
        "noteLengthBuckets": {
            "bucketWeights":     bucket_weights,
            "bucketByPitch":     bucket_by_pitch,
            "audioPaths":        audio_paths,
            "sampleNames":       SAMPLE_NAMES,
            "bucketTransitions": bucket_transitions,
            "bucketRhythmBias":  bucket_rhythm_bias,
            "bucketTensionMap":  bucket_tension_map,
        },
        "preferenceSignals": pref_signals,  # RLHF — read by audioTraining.html + meowREMIX.html
    }

    # ── BUILD COMPOSITIONAL RULE LIBRARY ──────────────────────────────────────
    logger.info("\n--- Building compositional rule library ---")
    comp_library = build_compositional_rules(summary, section_rows)
    logger.info(f"    {len(comp_library.get('rule_library', {}))} rule families")

    # ── WRITE / SAVE ──────────────────────────────────────────────────────────
    logger.info("\n--- Saving output ---")
    out_path = OUTPUT_JS if write_file else None
    write_rules_js(out_path, song_name, music_rules, comp_library, meta,
                   minify=minify, save_neon=True)

    return {
        "song_name":          song_name,
        "transitions":        total_trans,
        "motifs":             len(motifs),
        "suspensions":        len(suspensions),
        "smoothness_pairs":   sum(len(v) for v in trans_smooth.values()),
        "bar_centers":        len(bar_rules),
        "bucket_weights":     list(bucket_weights.keys()),
        "bucket_transitions": list(bucket_transitions.keys()),
        "vertical_intervals": len(vertical_harmony.get("preferredIntervals", {})),
    }


if __name__ == "__main__":
    main()