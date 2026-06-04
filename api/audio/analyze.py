#!/usr/bin/env python3
"""
meowREMIX Music Pattern Analyzer v4.0  (DB-backed Flask Blueprint)
==================================================================
Replaces the old file-based analyze.py.  All inputs are read from
Neon (written by ingest.py) and all outputs are written back to Neon.

Flask routes exposed:
  POST /api/audio/analyze/<int:song_id>   — run full analysis for a song
  GET  /api/audio/analyze/<int:song_id>   — fetch stored analysis summary
  GET  /api/audio/analyze/<int:song_id>/full — fetch full_json blob

Heavy analytical imports (numpy, collections, etc.) are deferred to inside
the route handler so Vercel's import-time scan never touches them.
pandas / matplotlib / scipy / music21 / tkinter are NOT imported here at all.

DB tables written by this module:
  audio_analyses            — per-song summary + full hierarchical JSON
  audio_pitch_transitions   — pitch → next_pitch probabilities
  audio_interval_distribution
  audio_phrase_analysis
  audio_section_analysis
  audio_motif_results
"""

import os
import json
import logging
import warnings

from flask import Blueprint, jsonify
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format="  %(message)s")
logger = logging.getLogger(__name__)

DB_URL = os.environ.get("DATABASE_URL")

audio_analyze_bp = Blueprint("audio_analyze", __name__)


# ── DB HELPERS ────────────────────────────────────────────────────────────────
def _connect():
    import psycopg
    if not DB_URL:
        raise RuntimeError("DATABASE_URL not set.")
    return psycopg.connect(DB_URL)


def _rows_as_dicts(cur):
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _safe_float(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _safe_int(v):
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


# ── LOAD EVENTS FROM DB ───────────────────────────────────────────────────────

def _load_events(conn, song_id: int) -> list[dict]:
    """
    Pull all note events for song_id from audio_note_events.
    Returns a list of plain dicts — no pandas involved.
    Numeric fields are coerced to Python float/int so downstream
    analysis code can treat them like DataFrame values.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                event_index, voice_index,
                measure_number, beat_position,
                absolute_offset_quarters, absolute_offset_seconds,
                bar_progress, song_progress,
                is_measure_start, is_measure_end, is_section_candidate,
                pitch, pitch_class, octave, scale_degree, pitch_class_int,
                chromatic_offset, distance_from_tonic, distance_from_dominant,
                duration_quarter_length, duration_type, duration_sec, tempo_bpm,
                note_length_bucket, note_name, audio_file,
                beat_strength, metrical_strength, is_syncopated,
                duration_ratio_previous, duration_ratio_next,
                is_rest, tension_score, tension_delta, tension_smoothness,
                melodic_smoothness, interval_smoothness, connection_score,
                interval_from_previous, interval_to_next,
                interval_direction, interval_size_class,
                is_step, is_leap, is_large_leap,
                previous_pitch, next_pitch,
                previous_duration_type, next_duration_type,
                phrase_candidate_start, phrase_candidate_end, phrase_candidate_id,
                cadence_authentic, cadence_half, cadence_plagal,
                local_chord, local_chord_root, local_chord_quality, harmonic_function,
                relative_interval_pattern, relative_rhythm_pattern, sequence_window_id,
                simultaneous_note_count, vertical_interval_from_bass
            FROM audio_note_events
            WHERE song_id = %s
            ORDER BY absolute_offset_quarters, voice_index
        """, (song_id,))
        rows = _rows_as_dicts(cur)

    # COERCE DECIMAL / None SAFELY
    float_cols = {
        "beat_position", "absolute_offset_quarters", "absolute_offset_seconds",
        "bar_progress", "song_progress", "metrical_strength",
        "duration_quarter_length", "duration_sec", "tempo_bpm",
        "duration_ratio_previous", "duration_ratio_next",
        "tension_score", "tension_delta", "tension_smoothness",
        "melodic_smoothness", "interval_smoothness", "connection_score",
        "vertical_interval_from_bass",
    }
    int_cols = {
        "event_index", "voice_index", "measure_number", "octave",
        "scale_degree", "pitch_class_int", "chromatic_offset",
        "distance_from_tonic", "distance_from_dominant",
        "interval_from_previous", "interval_to_next",
        "simultaneous_note_count", "phrase_candidate_id", "sequence_window_id",
    }
    bool_cols = {
        "is_measure_start", "is_measure_end", "is_section_candidate",
        "is_syncopated", "is_rest", "is_step", "is_leap", "is_large_leap",
        "phrase_candidate_start", "phrase_candidate_end",
        "cadence_authentic", "cadence_half", "cadence_plagal",
    }
    for row in rows:
        for c in float_cols:
            if c in row:
                row[c] = _safe_float(row[c])
        for c in int_cols:
            if c in row:
                row[c] = _safe_int(row[c])
        for c in bool_cols:
            if c in row:
                row[c] = bool(row[c]) if row[c] is not None else False
    return rows



# ANALYSIS ENGINE - ALL FUNCTIONS RECEIVE A LIST OF DICTS EVENTS AND RETURN PLAIN PYTHON STRUCTURES 
def _notes_only(events: list[dict]) -> list[dict]:
    return [e for e in events if not e.get("is_rest")]


# ── HELPERS ───────────────────────────────────────────────────────────────────

def _strip_octave(pitch_str):
    if not pitch_str or pitch_str == "REST":
        return pitch_str
    return "".join(c for c in str(pitch_str) if not c.isdigit() and c != "-")


def _pitch_to_midi(pitch_str):
    import re
    if not pitch_str or pitch_str == "REST":
        return None
    m = re.match(r"^([A-G][#b\-]?)(\d+)$", str(pitch_str))
    if not m:
        return None
    note_name, octave = m.groups()
    note_name = (note_name.replace("Db", "C#").replace("Eb", "D#")
                 .replace("Gb", "F#").replace("Ab", "G#").replace("Bb", "A#")
                 .replace("B-", "A#"))
    semitone_map = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
                    "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    if note_name not in semitone_map:
        return None
    return semitone_map[note_name] + 12 * (int(octave) + 1)


def _get_ngrams(seq, n):
    return [tuple(seq[i:i + n]) for i in range(len(seq) - n + 1)]


DUR_QL = {
    "whole": 4.0, "half": 2.0, "quarter": 1.0, "eighth": 0.5,
    "sixteenth": 0.25, "thirty-second": 0.125,
    "dotted-half": 3.0, "dotted-quarter": 1.5, "dotted-eighth": 0.75,
    "other": 1.0,
}


def _ql_sum(pattern):
    return sum(DUR_QL.get(d, 1.0) for d in pattern)


def _is_measure_valid(pattern, beats=4):
    total = _ql_sum(pattern)
    if total <= 0:
        return False
    ratio = total / beats
    return abs(ratio - round(ratio)) < 0.02


# ── Contextual tension ────────────────────────────────────────────────────────

def _apply_contextual_tension(events: list[dict]) -> list[dict]:
    """
    Add 'contextual_tension' to each event (mirrors original compute_contextual_tension).
    Also ensures tension_delta and tension_smoothness exist.
    """
    metric_factor = {"strong": 0.9, "medium": 1.0, "weak": 1.1, "pickup": 1.15}
    total = len(events)
    for i, ev in enumerate(events):
        base = ev.get("tension_score") or 0.5
        mf   = metric_factor.get(ev.get("beat_strength"), 1.0)
        pf   = 0.85 + 0.3 * (i / total) if total > 1 else 1.0
        ev["contextual_tension"] = max(0.0, min(1.0, base * mf * pf))
        if ev.get("tension_delta") is None and i > 0:
            prev_t = events[i - 1].get("tension_score") or 0.0
            ev["tension_delta"] = (ev.get("tension_score") or 0.0) - prev_t
        if ev.get("tension_smoothness") is None and ev.get("tension_delta") is not None:
            ev["tension_smoothness"] = 1.0 / (1.0 + 3.0 * abs(ev["tension_delta"]))
    return events



def _assign_phrases(events: list[dict]) -> list[dict]:
    """
    Use phrase_candidate_id already stored by converter.py.
    If missing, fall back to a simple boundary heuristic.
    Also computes phrase_position (0→1 within each phrase).
    """
    if events and events[0].get("phrase_candidate_id") is not None:
        from collections import defaultdict
        phrase_groups = defaultdict(list)
        for ev in events:
            phrase_groups[ev["phrase_candidate_id"]].append(ev)
        for pid, group in phrase_groups.items():
            n = len(group)
            for j, ev in enumerate(group):
                ev["phrase_id"]       = pid
                ev["phrase_position"] = j / n if n > 1 else 0.0
        return events

    phrase_id  = 0
    beat_acc   = 0.0
    for i, ev in enumerate(events):
        ql = ev.get("duration_quarter_length") or 1.0
        beat_acc += ql
        ev["phrase_id"] = phrase_id
        if ev.get("is_rest") and ql >= 2.0 and beat_acc >= 16.0:
            phrase_id += 1
            beat_acc   = 0.0
        elif beat_acc >= 16.0 and ev.get("is_measure_start"):
            phrase_id += 1
            beat_acc   = 0.0

    from collections import defaultdict
    phrase_groups = defaultdict(list)
    for ev in events:
        phrase_groups[ev["phrase_id"]].append(ev)
    for pid, group in phrase_groups.items():
        n = len(group)
        for j, ev in enumerate(group):
            ev["phrase_position"] = j / n if n > 1 else 0.0
    return events



def _analyze_transitions(events: list[dict]) -> list[dict]:
    """
    Returns list of {from_pitch, to_pitch, count, probability} dicts.
    """
    from collections import Counter, defaultdict
    notes = [e for e in events if not e.get("is_rest") and e.get("pitch") and e.get("next_pitch")]
    pair_counts = Counter((e["pitch"], e["next_pitch"]) for e in notes)

    by_from = defaultdict(int)
    for (fp, tp), cnt in pair_counts.items():
        by_from[fp] += cnt

    tension_map = {}
    for e in notes:
        p = e["pitch"]
        t = e.get("contextual_tension") or e.get("tension_score") or 0.5
        tension_map.setdefault(p, []).append(t)
    avg_tension = {p: sum(vs) / len(vs) for p, vs in tension_map.items()}

    rows = []
    for (fp, tp), cnt in pair_counts.items():
        total = by_from[fp]
        rows.append({
            "from_pitch":  fp,
            "to_pitch":    tp,
            "count":       cnt,
            "probability": round(cnt / total, 6) if total else 0.0,
            "dest_tension": round(avg_tension.get(tp, 0.5), 4),
        })
    rows.sort(key=lambda r: (r["from_pitch"], -r["probability"]))
    return rows



def _analyze_intervals(events: list[dict]) -> list[dict]:
    from collections import Counter
    notes = [e for e in events if not e.get("is_rest") and e.get("interval_from_previous") is not None]
    counts = Counter(int(e["interval_from_previous"]) for e in notes)
    total  = sum(counts.values()) or 1
    return [
        {"interval": iv, "frequency": cnt, "percentage": round(cnt / total * 100, 4)}
        for iv, cnt in sorted(counts.items())
    ]



def _classify_tension_curve(tensions: list) -> str:
    if len(tensions) < 2:
        return "flat"
    x = tensions
    peaks, troughs = [], []
    for i in range(1, len(x) - 1):
        if x[i] > x[i - 1] and x[i] > x[i + 1]:
            peaks.append(i)
        elif x[i] < x[i - 1] and x[i] < x[i + 1]:
            troughs.append(i)
    if not peaks and not troughs:
        if x[-1] > x[0] + 0.1:    return "rise"
        if x[0] > x[-1] + 0.1:    return "fall"
        return "plateau"
    if len(peaks) >= 2:            return "multiple_peak"
    if len(peaks) == 1:
        pi = peaks[0]
        if not troughs or pi < troughs[0]: return "rise-fall"
        return "fall-rise"
    if troughs:
        ti = troughs[0]
        return "fall-rise" if ti < len(x) // 2 else "rise-fall"
    return "complex"



def _detect_cadences(events: list[dict]) -> list[dict]:
    from collections import defaultdict
    by_phrase = defaultdict(list)
    for e in events:
        if not e.get("is_rest"):
            by_phrase[e.get("phrase_id", 0)].append(e)

    cadences = []
    for pid, notes in by_phrase.items():
        if len(notes) < 2:
            continue
        last = notes[-1]
        pen  = notes[-2]

        l_sd  = _safe_int(last.get("scale_degree"))
        p_sd  = _safe_int(pen.get("scale_degree"))
        l_pc  = last.get("pitch_class") or ""
        p_pc  = pen.get("pitch_class") or ""

        ctype = None
        if l_sd is not None and p_sd is not None:
            if p_sd in (5, 7) and l_sd == 1:   ctype = "perfect_authentic"
            elif p_sd == 4 and l_sd == 1:        ctype = "plagal"
            elif p_sd == 5 and l_sd == 6:        ctype = "deceptive"
            elif l_sd == 5:                      ctype = "half"
        else:
            if p_pc in ("D", "F#") and l_pc == "G":   ctype = "perfect_authentic"
            elif p_pc in ("C", "E") and l_pc == "G":   ctype = "plagal"
            elif p_pc == "D" and l_pc == "E":          ctype = "deceptive"
            elif l_pc == "D":                          ctype = "half"

        if ctype:
            cadences.append({
                "phrase_id":         pid,
                "cadence_type":      ctype,
                "final_pitch":       last.get("pitch"),
                "penultimate_pitch": pen.get("pitch"),
                "measure":           last.get("measure_number"),
            })
    return cadences



def _analyze_phrases_detailed(events: list[dict], cadences: list[dict]) -> tuple[list, dict]:
    from collections import Counter, defaultdict
    by_phrase = defaultdict(list)
    for e in events:
        by_phrase[e.get("phrase_id", 0)].append(e)

    cad_by_phrase = {c["phrase_id"]: c for c in cadences}
    phrases = []

    for pid, group in sorted(by_phrase.items()):
        notes = [e for e in group if not e.get("is_rest")]
        if not notes:
            continue

        first, last = notes[0], notes[-1]
        start_meas = _safe_int(first.get("measure_number"))
        end_meas   = _safe_int(last.get("measure_number"))

        beat_positions = [e.get("beat_position") or 0.0 for e in group]
        last_ql = last.get("duration_quarter_length") or 1.0
        length_beats = round(
            (beat_positions[-1] if beat_positions else 0.0) -
            (beat_positions[0]  if beat_positions else 0.0) + last_ql, 2
        )

        tensions = [
            e.get("contextual_tension") or e.get("tension_score") or 0.0
            for e in notes
            if (e.get("contextual_tension") or e.get("tension_score")) is not None
        ]
        curve_type  = _classify_tension_curve(tensions)
        cad         = cad_by_phrase.get(pid)
        cadence_type = cad["cadence_type"] if cad else None

        avg_t  = sum(tensions) / len(tensions) if tensions else 0.0
        peak_t = max(tensions) if tensions else 0.0

        phrases.append({
            "phrase_id":           int(pid),
            "start_measure":       start_meas,
            "end_measure":         end_meas,
            "length_beats":        float(length_beats),
            "length_measures":     (end_meas - start_meas + 1) if (start_meas and end_meas) else None,
            "phrase_start_degree": _safe_int(first.get("scale_degree")),
            "phrase_end_degree":   _safe_int(last.get("scale_degree")),
            "destination_scale_degree": _safe_int(last.get("scale_degree")),
            "tension_curve":       tensions,
            "curve_type":          curve_type,
            "cadence_type":        cadence_type,
            "avg_tension":         round(float(avg_t), 4),
            "peak_tension":        round(float(peak_t), 4),
        })

    dest_counts = {}
    for p in phrases:
        d = p.get("destination_scale_degree")
        if d is not None:
            dest_counts[d] = dest_counts.get(d, 0) + 1
    total_d = sum(dest_counts.values()) or 1
    dest_probs = {str(k): round(v / total_d, 4) for k, v in dest_counts.items()}

    return phrases, dest_probs


def _analyze_motifs_detailed(events: list[dict]) -> list[dict]:
    from collections import defaultdict
    notes  = [e for e in events if not e.get("is_rest") and e.get("pitch")]
    if len(notes) < 2:
        return []

    pitch_seq    = [e["pitch"] for e in notes]
    measure_seq  = [e.get("measure_number", 0) for e in notes]
    iv_seq       = [e.get("interval_from_previous") for e in notes]

    phrase_seq   = [e.get("phrase_id", 0) for e in notes]
    motifs_raw   = defaultdict(list) 

    for n in (2, 3, 4):
        for i in range(len(pitch_seq) - n + 1):
            if len(set(phrase_seq[i:i + n])) > 1:
                continue   
            gram = " ".join(pitch_seq[i:i + n])
            motifs_raw[gram].append((i, measure_seq[i]))

    motif_list = []
    for motif_str, occs in motifs_raw.items():
        if len(occs) < 2:
            continue
        occs.sort(key=lambda x: x[0])
        start_measures = [o[1] for o in occs]
        diffs = [start_measures[j] - start_measures[j - 1]
                 for j in range(1, len(start_measures))]
        avg_ret = round(sum(diffs) / len(diffs), 2) if diffs else 0.0

        n_notes = len(motif_str.split())
        occ_patterns = []
        for idx, _ in occs:
            pat = tuple(iv_seq[idx + 1: idx + n_notes] if idx + 1 < len(iv_seq) else [])
            occ_patterns.append(pat)
        is_exact = len(set(occ_patterns)) == 1 if all(p for p in occ_patterns) else False
        variant  = "exact" if is_exact else "varied"

        motif_list.append({
            "motif_id":                    motif_str,
            "length":                      n_notes,
            "occurrences":                 start_measures,
            "first_occurrence":            start_measures[0],
            "reuse_count":                 len(occs),
            "average_return_distance_bars": avg_ret,
            "variation_rate":              0.0 if is_exact else 0.5,
            "variation_types":             [variant],
        })

    motif_list.sort(key=lambda m: m["reuse_count"], reverse=True)
    return motif_list


def _discover_sections(events: list[dict], phrases: list[dict]) -> list[dict]:
    if not phrases:
        return []

    sections = []
    current  = {
        "section_id": "A",
        "phrases": [phrases[0]["phrase_id"]],
        "start_bar": phrases[0]["start_measure"],
        "end_bar":   phrases[0]["end_measure"],
        "cadences":  [],
        "tensions":  phrases[0]["tension_curve"][:],
    }
    sec_counter = 0

    for i in range(1, len(phrases)):
        prev, curr = phrases[i - 1], phrases[i]
        split = (
            prev.get("cadence_type") == "half" and
            curr.get("cadence_type") == "perfect_authentic"
        )
        if split:
            sections.append(current)
            sec_counter += 1
            current = {
                "section_id": chr(65 + sec_counter),
                "phrases":    [],
                "start_bar":  curr["start_measure"],
                "end_bar":    curr["end_measure"],
                "cadences":   [],
                "tensions":   [],
            }
        current["phrases"].append(curr["phrase_id"])
        current["end_bar"] = curr["end_measure"]
        if curr.get("cadence_type"):
            current["cadences"].append(curr["cadence_type"])
        current["tensions"].extend(curr["tension_curve"])

    sections.append(current)

    result = []
    for sec in sections:
        if not sec["phrases"]:
            continue
        ts  = sec["tensions"]
        avg = round(sum(ts) / len(ts), 4) if ts else 0.0
        pk  = round(max(ts), 4) if ts else 0.0
        n   = len(sec["phrases"])
        cad = round(len(sec["cadences"]) / n, 4) if n else 0.0

        total_bars = max((p["end_measure"] or 0) for p in phrases) or 1
        start_r = (sec["start_bar"] or 0) / total_bars
        end_r   = (sec["end_bar"]   or 0) / total_bars
        center  = (start_r + end_r) / 2
        if center < 0.2:    role = "setup"
        elif center < 0.6:  role = "development"
        elif center < 0.85: role = "climax"
        else:               role = "resolution"

        result.append({
            "section_id":      sec["section_id"],
            "start_bar":       sec["start_bar"],
            "end_bar":         sec["end_bar"],
            "average_tension": avg,
            "peak_tension":    pk,
            "cadence_density": cad,
            "structural_role": role,
        })
    return result



def _detect_expectation_delays(phrases: list[dict]) -> list[dict]:
    events = []
    for i in range(len(phrases) - 1):
        cur, nxt = phrases[i], phrases[i + 1]
        if cur.get("cadence_type") == "half" and nxt.get("phrase_start_degree") != 1:
            delay = (nxt.get("start_measure") or 0) - (cur.get("end_measure") or 0)
            events.append({
                "type":             "deferred_resolution",
                "delay_length_bars": delay,
                "from_phrase":      cur["phrase_id"],
                "to_phrase":        nxt["phrase_id"],
            })
    return events



def _extract_emotional_features(events: list[dict]) -> dict:
    notes = [e for e in events if not e.get("is_rest")]
    if not notes:
        return {}
    n = len(notes)

    steps     = sum(1 for e in notes if e.get("is_step"))
    tension_v = [e.get("contextual_tension") or e.get("tension_score") or 0.0 for e in notes]
    smooth_v  = [e.get("melodic_smoothness") or 0.5 for e in notes]
    leaps     = sum(1 for e in notes if e.get("is_large_leap"))

    buckets = {}
    for e in notes:
        b = e.get("note_length_bucket")
        if b:
            buckets[b] = buckets.get(b, 0) + 1
    total_b = sum(buckets.values()) or 1

    return {
        "stepwise_motion_ratio":   round(steps / n, 4) if n else 0.0,
        "tension_variance":        round(
            sum((t - sum(tension_v) / n) ** 2 for t in tension_v) / n, 4
        ) if n else 0.0,
        "average_melodic_smoothness": round(sum(smooth_v) / len(smooth_v), 4) if smooth_v else 0.5,
        "large_leap_ratio":        round(leaps / n, 4) if n else 0.0,
        "note_bucket_distribution": {k: round(v / total_b, 4) for k, v in buckets.items()},
    }



def _compute_familiarity_novelty(motif_detailed: list[dict]) -> dict:
    if not motif_detailed:
        return {"familiarity_score": 0.0, "novelty_score": 1.0}
    total    = sum(m["reuse_count"] for m in motif_detailed) or 1
    returns  = sum(m["reuse_count"] - 1 for m in motif_detailed if m["reuse_count"] > 1)
    fam      = round(returns / total, 4)
    return {"familiarity_score": fam, "novelty_score": round(1.0 - fam, 4)}


def _compute_return_to_familiarity(motif_detailed: list[dict]) -> dict:
    if not motif_detailed:
        return {"motif_return_rate": 0.0, "average_return_distance": 0.0}
    total = len(motif_detailed) or 1
    with_returns = [m for m in motif_detailed if m["reuse_count"] > 1]
    rate = round(len(with_returns) / total, 4)
    dists = [m["average_return_distance_bars"] for m in with_returns if m["average_return_distance_bars"] > 0]
    avg_d = round(sum(dists) / len(dists), 2) if dists else 0.0
    return {"motif_return_rate": rate, "average_return_distance": avg_d}



def _analyze_song_trajectory(phrases: list[dict], sections: list[dict]) -> dict:
    if not sections:
        return {}
    total_bars = max((s.get("end_bar") or 0) for s in sections) or 1
    climax_sec = max(sections, key=lambda s: s["peak_tension"])
    cc = ((climax_sec.get("start_bar") or 0) + (climax_sec.get("end_bar") or 0)) / 2
    return {
        "intro_region":       {"start_bar": sections[0]["start_bar"],  "end_bar": sections[0]["end_bar"]},
        "climax_region":      {"start_bar": climax_sec["start_bar"],   "end_bar": climax_sec["end_bar"]},
        "resolution_region":  {"start_bar": sections[-1]["start_bar"], "end_bar": sections[-1]["end_bar"]},
        "climax_location":    round(cc / total_bars, 4),
    }



def _smoothness_stats(events: list[dict]) -> dict:
    """Summary stats used in audio_analyses summary columns."""
    notes = [e for e in events if not e.get("is_rest")]
    if not notes:
        return {}
    smooth_vals = [e["melodic_smoothness"] for e in notes if e.get("melodic_smoothness") is not None]
    avg_smooth  = round(sum(smooth_vals) / len(smooth_vals), 4) if smooth_vals else None
    return {"avg_melodic_smoothness": avg_smooth}



def _build_full_json(events, phrases, dest_probs, motif_detailed,
                     sections, expectation_events, emotional_features,
                     familiarity_data, return_fam_data, trajectory) -> dict:
    source = ""
    for e in events:
        if e.get("pitch"):
            source = str(e.get("pitch", ""))
            break

    return {
        "schema_version": "4.0",
        "song_analysis": {
            "cadence_frequency": (
                len([p for p in phrases if p.get("cadence_type")]) / len(phrases)
                if phrases else 0.0
            ),
            "emotional_features":         emotional_features,
            "familiarity_novelty_balance": familiarity_data,
            "return_to_familiarity":       return_fam_data,
            "phrase_destination_distribution": dest_probs,
        },
        "section_analysis":  sections,
        "phrase_analysis":   phrases,
        "motif_analysis":    motif_detailed,
        "expectation_events": expectation_events,
        "trajectory_analysis": trajectory,
    }


# DB WRITERS
def _write_to_db(conn, song_id: int,
                 transitions, intervals, phrases, sections, motifs,
                 full_json, dest_probs, summary_stats) -> int:
    """
    Upsert all analysis tables.  Returns the analysis_id created/updated.
    """
    import json as _json

    emotional = full_json.get("song_analysis", {}).get("emotional_features", {})
    fam       = full_json.get("song_analysis", {}).get("familiarity_novelty_balance", {})
    ret_fam   = full_json.get("song_analysis", {}).get("return_to_familiarity", {})
    traj      = full_json.get("trajectory_analysis", {})

    tensions       = [p["avg_tension"]  for p in phrases if p.get("avg_tension")  is not None]
    peak_tensions  = [p["peak_tension"] for p in phrases if p.get("peak_tension") is not None]
    avg_tension    = round(sum(tensions) / len(tensions), 4)         if tensions      else None
    peak_tension   = round(max(peak_tensions), 4)                    if peak_tensions else None
    phrase_lengths = [p["length_beats"]  for p in phrases if p.get("length_beats") is not None]
    avg_phrase_len = round(sum(phrase_lengths) / len(phrase_lengths), 2) if phrase_lengths else None

    cad_freq = full_json["song_analysis"].get("cadence_frequency", 0.0)

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM audio_analyses WHERE song_id = %s", (song_id,))
        existing = cur.fetchone()
        if existing:
            cur.execute("DELETE FROM audio_analyses WHERE song_id = %s", (song_id,))

        cur.execute("""
            INSERT INTO audio_analyses (
                song_id,
                avg_interval_size, stepwise_motion_ratio, motif_density,
                cadence_density, tension_variance, phrase_length_average,
                familiarity_score, novelty_score, motif_return_rate,
                avg_return_distance, cadence_frequency, climax_location,
                full_json, dest_probs_json, sections_json, trajectory_json
            ) VALUES (
                %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s
            ) RETURNING id
        """, (
            song_id,
            _safe_float(summary_stats.get("avg_melodic_smoothness")),
            _safe_float(emotional.get("stepwise_motion_ratio")),
            _safe_float(len(motifs) / max(len(phrases), 1)),
            _safe_float(cad_freq),
            _safe_float(emotional.get("tension_variance")),
            _safe_float(avg_phrase_len),
            _safe_float(fam.get("familiarity_score")),
            _safe_float(fam.get("novelty_score")),
            _safe_float(ret_fam.get("motif_return_rate")),
            _safe_float(ret_fam.get("average_return_distance")),
            _safe_float(cad_freq),
            _safe_float(traj.get("climax_location")),
            _json.dumps(full_json),
            _json.dumps(dest_probs),
            _json.dumps(sections),
            _json.dumps(traj),
        ))
        analysis_id = cur.fetchone()[0]

        cur.execute("DELETE FROM audio_pitch_transitions WHERE song_id = %s", (song_id,))
        if transitions:
            cur.executemany("""
                INSERT INTO audio_pitch_transitions
                    (song_id, analysis_id, from_pitch, to_pitch, count, probability)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [
                (song_id, analysis_id,
                 t["from_pitch"], t["to_pitch"], t["count"], t["probability"])
                for t in transitions
            ])

        cur.execute("DELETE FROM audio_interval_distribution WHERE song_id = %s", (song_id,))
        if intervals:
            cur.executemany("""
                INSERT INTO audio_interval_distribution
                    (song_id, analysis_id, interval, frequency, percentage)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                (song_id, analysis_id, iv["interval"], iv["frequency"], iv["percentage"])
                for iv in intervals
            ])

        cur.execute("DELETE FROM audio_phrase_analysis WHERE song_id = %s", (song_id,))
        if phrases:
            cur.executemany("""
                INSERT INTO audio_phrase_analysis (
                    song_id, analysis_id,
                    phrase_id, start_measure, end_measure,
                    length_beats, length_measures,
                    phrase_start_degree, phrase_end_degree,
                    curve_type, cadence_type,
                    avg_tension, peak_tension
                ) VALUES (
                    %s, %s,
                    %s, %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s,
                    %s, %s
                )
            """, [
                (
                    song_id, analysis_id,
                    p["phrase_id"], p["start_measure"], p["end_measure"],
                    p["length_beats"], p.get("length_measures"),
                    p.get("phrase_start_degree"), p.get("phrase_end_degree"),
                    p["curve_type"], p.get("cadence_type"),
                    p["avg_tension"], p["peak_tension"],
                )
                for p in phrases
            ])

        cur.execute("DELETE FROM audio_section_analysis WHERE song_id = %s", (song_id,))
        if sections:
            cur.executemany("""
                INSERT INTO audio_section_analysis (
                    song_id, analysis_id,
                    section_id, start_bar, end_bar,
                    average_tension, peak_tension,
                    cadence_density, structural_role
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                (
                    song_id, analysis_id,
                    s["section_id"], s["start_bar"], s["end_bar"],
                    s["average_tension"], s["peak_tension"],
                    s["cadence_density"], s["structural_role"],
                )
                for s in sections
            ])

        cur.execute("DELETE FROM audio_motif_results WHERE song_id = %s", (song_id,))
        if motifs:
            cur.executemany("""
                INSERT INTO audio_motif_results (
                    song_id, analysis_id,
                    motif_str, motif_length, reuse_count,
                    first_occurrence_measure, avg_return_distance,
                    variation_type
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [
                (
                    song_id, analysis_id,
                    m["motif_id"], m["length"], m["reuse_count"],
                    m["first_occurrence"], m["average_return_distance_bars"],
                    m["variation_types"][0] if m["variation_types"] else "exact",
                )
                for m in motifs
            ])

    conn.commit()
    return analysis_id


# FLASK ROUTES
@audio_analyze_bp.route("/api/audio/analyze/<int:song_id>", methods=["POST"])
def run_analysis(song_id: int):
    """
    Run the full analysis pipeline for a song already in Neon.
    Reads from audio_note_events, writes all results back to DB.
    """
    try:
        conn = _connect()

        with conn.cursor() as cur:
            cur.execute("SELECT song_name FROM audio_songs WHERE id = %s", (song_id,))
            row = cur.fetchone()
            if not row:
                conn.close()
                return jsonify({"success": False, "error": f"Song {song_id} not found"}), 404
            song_name = row[0]

        logger.info(f"[analyze] Starting analysis for '{song_name}' (id={song_id})")

        logger.info("  [1] Loading events from DB...")
        events = _load_events(conn, song_id)
        if not events:
            conn.close()
            return jsonify({"success": False, "error": "No events found for this song"}), 400
        logger.info(f"      {len(events)} events loaded")

        logger.info("  [2] Computing contextual tension...")
        events = _apply_contextual_tension(events)

        logger.info("  [3] Assigning phrase IDs...")
        events = _assign_phrases(events)

        logger.info("  [4] Pitch transitions...")
        transitions = _analyze_transitions(events)

        logger.info("  [5] Interval distribution...")
        intervals = _analyze_intervals(events)

        logger.info("  [6] Cadence detection...")
        cadences = _detect_cadences(events)

        logger.info("  [7] Phrase detailed analysis...")
        phrases, dest_probs = _analyze_phrases_detailed(events, cadences)

        logger.info("  [8] Motif analysis...")
        motifs = _analyze_motifs_detailed(events)

        logger.info("  [9] Section discovery...")
        sections = _discover_sections(events, phrases)

        logger.info("  [10] Expectation events...")
        expectation_events = _detect_expectation_delays(phrases)

        logger.info("  [11] Emotional features...")
        emotional = _extract_emotional_features(events)

        logger.info("  [12] Familiarity / novelty...")
        fam_data     = _compute_familiarity_novelty(motifs)
        ret_fam_data = _compute_return_to_familiarity(motifs)

        logger.info("  [13] Song trajectory...")
        trajectory = _analyze_song_trajectory(phrases, sections)

        logger.info("  [14] Smoothness stats...")
        smooth_stats = _smoothness_stats(events)

        full_json = _build_full_json(
            events, phrases, dest_probs, motifs,
            sections, expectation_events, emotional,
            fam_data, ret_fam_data, trajectory
        )

        logger.info("  [15] Writing results to DB...")
        analysis_id = _write_to_db(
            conn, song_id,
            transitions, intervals, phrases, sections, motifs,
            full_json, dest_probs, smooth_stats
        )

        conn.close()
        logger.info(f"  ✓ Analysis complete — analysis_id={analysis_id}")

        return jsonify({
            "success":        True,
            "song_id":        song_id,
            "song_name":      song_name,
            "analysis_id":    analysis_id,
            "events_analyzed": len(events),
            "transitions":    len(transitions),
            "phrases":        len(phrases),
            "sections":       len(sections),
            "motifs":         len(motifs),
            "cadences":       len(cadences),
        }), 201

    except Exception as e:
        logger.exception(f"Analysis failed for song_id={song_id}")
        return jsonify({"success": False, "error": str(e)}), 500


@audio_analyze_bp.route("/api/audio/analyze/<int:song_id>", methods=["GET"])
def get_analysis_summary(song_id: int):
    """Return the stored analysis summary row (no full_json blob)."""
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, song_id, created_at,
                        avg_interval_size, stepwise_motion_ratio, motif_density,
                        cadence_density, tension_variance, phrase_length_average,
                        familiarity_score, novelty_score, motif_return_rate,
                        avg_return_distance, cadence_frequency, climax_location
                    FROM audio_analyses
                    WHERE song_id = %s
                    ORDER BY created_at DESC LIMIT 1
                """, (song_id,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": f"No analysis for song {song_id}"}), 404
                cols = [d[0] for d in cur.description]
                d = dict(zip(cols, row))
                if d.get("created_at") and hasattr(d["created_at"], "isoformat"):
                    d["created_at"] = d["created_at"].isoformat()
                for k, v in d.items():
                    if hasattr(v, "__float__") and not isinstance(v, (bool, int)):
                        d[k] = float(v) if v is not None else None
        return jsonify({"success": True, "analysis": d})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@audio_analyze_bp.route("/api/audio/analyze/<int:song_id>/full", methods=["GET"])
def get_analysis_full(song_id: int):
    """Return the full hierarchical JSON blob for a song."""
    try:
        with _connect() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT full_json FROM audio_analyses
                    WHERE song_id = %s
                    ORDER BY created_at DESC LIMIT 1
                """, (song_id,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": f"No analysis for song {song_id}"}), 404
                full = row[0]  # psycopg RETURNS JSONB AS DICT ALREADY
        return jsonify({"success": True, "song_id": song_id, "analysis": full})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500