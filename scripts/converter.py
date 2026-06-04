#!/usr/bin/env python3
"""
meowREMIX Converter v1.0
========================
Reads .mxl files from  projects/audio/source-files/
Transposes everything to G major (or G minor if the source is minor)
Extracts a rich per-note event payload
POSTs to  POST /api/audio/ingest  on your Vercel app

Dependencies (all local-only, never on Vercel):
    music21   pip install music21
    requests  pip install requests
    python-dotenv

Usage:
    # convert all .mxl files in source-files/
    python scripts/converter.py

    # convert a single file
    python scripts/converter.py --file "projects/audio/source-files/hallelujah.mxl"

    # dry-run (parse + print, don't POST)
    python scripts/converter.py --dry-run

    # set a custom ingest URL (overrides .env)
    python scripts/converter.py --url https://my-app.vercel.app
"""

import os
import re
import sys
import json
import math
import logging
import argparse
import warnings
import requests
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv

warnings.filterwarnings('ignore')

# ── MUSIC21 IS LOCAL ONLY ───────────────────────────────────────────────────
try:
    import music21
    from music21 import converter as m21converter, key, pitch, interval, stream
    from music21 import note as m21note, chord as m21chord, tempo as m21tempo
    from music21 import meter, harmony
except ImportError:
    print("ERROR: music21 is not installed.  Run:  pip install music21")
    sys.exit(1)

# ── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="  %(message)s")
logger = logging.getLogger(__name__)

# ── PATHS ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent   # VERCEL_APP/SCRIPTS/
PROJECT_ROOT = SCRIPT_DIR.parent                 # VERCEL_APP/
SOURCE_DIR   = PROJECT_ROOT / "projects" / "audio" / "source-files"

load_dotenv(PROJECT_ROOT / ".env")

INGEST_URL = os.environ.get("INGEST_URL", "").rstrip("/")   # E.G. HTTPS://MYAPP.VERCEL.APP

# ── KEY / TRANSPOSITION CONSTANTS ───────────────────────────────────────────
TARGET_MAJOR = key.Key("G", "major")
TARGET_MINOR = key.Key("G", "minor")

# G MAJOR SCALE DEGREES (PITCH CLASS → DEGREE 1-7)
G_MAJOR_DEGREES = {
    "G": 1, "A": 2, "B": 3, "C": 4,
    "D": 5, "E": 6, "F#": 7,
}
G_MINOR_DEGREES = {
    "G": 1, "A": 2, "B-": 3, "C": 4,
    "D": 5, "E-": 6, "F": 7,
}

# TENSION SCORES PER SCALE DEGREE (1=STABLE, 7=MOST TENSE)
DEGREE_TENSION = {1: 0.0, 2: 0.2, 3: 0.1, 4: 0.3, 5: 0.1, 6: 0.2, 7: 0.5, None: 0.3}

# ── NOTE-LENGTH BUCKET MAPPING ───────────────────────────────────────────────
# EACH BUCKET CORRESPONDS TO AN AUDIO FILE FOLDER: LONG / MEDIUM / SHORT
# THRESHOLDS ARE IN QUARTER-NOTE LENGTHS
def duration_to_bucket(quarter_length: float) -> str:
    """Map a note's quarter-length duration to long / medium / short."""
    if quarter_length >= 2.0:      # HALF NOTE OR LONGER  → LONG  (HELD FOR A FULL BAR OR MORE)
        return "long"
    elif quarter_length >= 0.75:   # DOTTED-EIGHTH TO DOTTED-QUARTER → MEDIUM (HALF-BAR FEEL)
        return "medium"
    else:                           # EIGHTH AND SHORTER → SHORT (STACCATO)
        return "short"

# CANONICAL NOTE NAME USED TO LOOK UP THE AUDIO FILE
# WE HAVE: G  A  B  C  D  E  F  G2
# G2 = HIGH G (OCTAVE 5).  EVERYTHING ELSE MAPS TO ITS LETTER.
def pitch_to_note_name(p: pitch.Pitch) -> str:
    pc = p.pitchClass          # 0-11
    # G=7, A=9, B=11, C=0, D=2, E=4, F#=6 (G MAJOR)
    # MAP PITCHCLASS → CLOSEST SAMPLE LETTER
    PC_TO_LETTER = {
        0: "c", 1: "c",
        2: "d", 3: "d",
        4: "e",
        5: "f", 6: "f",
        7: "g", 8: "g",
        9: "a", 10: "a",
        11: "b",
    }
    letter = PC_TO_LETTER.get(pc, "g")
    # HIGH G = G2 (OCTAVE 5+)
    if letter == "g" and p.octave >= 5:
        letter = "g2"
    return letter

def audio_file_path(bucket: str, note_name: str) -> str:
    """Return the relative URL path for the audio file."""
    return f"projects/audio/notes/{bucket}/{note_name}.m4a"

# ── DURATION TYPE HELPERS ────────────────────────────────────────────────────
def quarter_to_dur_type(ql: float) -> str:
    mapping = [
        (4.0, "whole"),
        (3.0, "dotted-half"),
        (2.0, "half"),
        (1.5, "dotted-quarter"),
        (1.0, "quarter"),
        (0.75, "dotted-eighth"),
        (0.5,  "eighth"),
        (0.25, "sixteenth"),
        (0.125, "thirty-second"),
    ]
    for threshold, name in mapping:
        if abs(ql - threshold) < 0.01:
            return name
    return "other"

# ── HARMONIC CONTEXT HELPERS ─────────────────────────────────────────────────
def get_harmonic_function(degree: int, mode: str) -> str:
    if mode == "major":
        return {1: "tonic", 2: "supertonic", 3: "mediant", 4: "subdominant",
                5: "dominant", 6: "submediant", 7: "leading-tone"}.get(degree, "chromatic")
    else:  # MINOR
        return {1: "tonic", 2: "supertonic", 3: "mediant", 4: "subdominant",
                5: "dominant", 6: "submediant", 7: "subtonic"}.get(degree, "chromatic")

def get_local_chord(notes_at_offset: list) -> tuple:
    """Given a list of concurrent pitches, return (chord_str, root, quality)."""
    if not notes_at_offset:
        return None, None, None
    try:
        c = m21chord.Chord(notes_at_offset)
        root = c.root().name if c.root() else None
        quality = c.quality
        chord_str = f"{root} {quality}" if root else None
        return chord_str, root, quality
    except Exception:
        return None, None, None

# ── BEAT STRENGTH ─────────────────────────────────────────────────────────────
def beat_strength_label(beat_pos: float, time_sig_num: int = 4) -> tuple:
    """Return (label, metrical_strength) for a beat position (1-based)."""
    beat_1based = ((beat_pos - 1) % time_sig_num) + 1
    if abs(beat_1based - 1.0) < 0.01:
        return "strong", 1.0
    elif abs(beat_1based - 3.0) < 0.01 and time_sig_num == 4:
        return "medium", 0.75
    elif beat_1based % 1.0 == 0:
        return "weak", 0.5
    else:
        return "pickup", 0.25

# ── TENSION HELPERS ──────────────────────────────────────────────────────────
def pitch_tension(p: pitch.Pitch, degree_map: dict) -> float:
    pc_name = p.name  # E.G. "F#"
    degree = degree_map.get(pc_name)
    if degree is None:
        # CHROMATIC NOTE — HIGH TENSION
        return 0.7
    return DEGREE_TENSION.get(degree, 0.3)

# ── INTERVAL HELPERS ─────────────────────────────────────────────────────────
def interval_semitones(p1: pitch.Pitch, p2: pitch.Pitch) -> int:
    try:
        return int(interval.Interval(p1, p2).semitones)
    except Exception:
        return 0

def interval_direction(semitones: int) -> str:
    if semitones > 0:   return "ascending"
    if semitones < 0:   return "descending"
    return "same"

def interval_size_class(semitones: int) -> str:
    abs_semi = abs(semitones)
    if abs_semi == 0:   return "unison"
    if abs_semi <= 2:   return "step"
    if abs_semi <= 4:   return "small-leap"
    if abs_semi <= 7:   return "leap"
    return "large-leap"

def melodic_smoothness(semitones: int) -> float:
    """0=jagged, 1=stepwise."""
    abs_s = abs(semitones)
    if abs_s == 0:   return 1.0
    if abs_s <= 2:   return 0.95
    if abs_s <= 4:   return 0.70
    if abs_s <= 7:   return 0.40
    return 0.15

def interval_smoothness(semitones: int) -> float:
    return melodic_smoothness(semitones)

def connection_score(prev_ql: float, cur_ql: float) -> float:
    """How smoothly does the rhythm flow? 1=very smooth."""
    ratio = cur_ql / prev_ql if prev_ql else 1.0
    if 0.5 <= ratio <= 2.0:   return 0.9
    if 0.25 <= ratio <= 4.0:  return 0.6
    return 0.3

# ── PHRASE DETECTION (SIMPLE BOUNDARY HEURISTIC) ─────────────────────────────
def detect_phrase_boundaries(events: list, beats_per_measure: int = 4) -> list:
    """
    Simple phrase boundary: a rest at a strong beat OR a long note (whole/dotted-half)
    after at least 4 beats of content.
    Returns a list of event_index values that start a new phrase.
    """
    boundaries = [0]
    beat_accumulator = 0.0
    for i, ev in enumerate(events):
        if ev["is_rest"]:
            continue
        beat_accumulator += ev["duration_quarter_length"]
        if beat_accumulator >= (beats_per_measure * 4):   # 4 BARS MINIMUM
            # CHECK IF NEXT NON-REST IS AT MEASURE START OR THIS IS A LONG NOTE
            if ev.get("is_measure_start") or ev["duration_quarter_length"] >= 3.0:
                boundaries.append(i)
                beat_accumulator = 0.0
    return boundaries

# ── MAIN MXL PARSING FUNCTION ─────────────────────────────────────────────────
def parse_mxl(path: Path) -> dict:
    """
    Parse a single .mxl file and return the ingest payload dict.
    Transposes to G major/minor.
    """
    logger.info(f"  Parsing: {path.name}")
    score = m21converter.parse(str(path))

    # ── DETECT KEY & MODE ────────────────────────────────────────────────────
    detected_key = score.analyze("key")
    source_mode  = detected_key.mode if detected_key else "major"
    target_key   = TARGET_MAJOR if source_mode == "major" else TARGET_MINOR
    degree_map   = G_MAJOR_DEGREES if source_mode == "major" else G_MINOR_DEGREES

    logger.info(f"    Detected key : {detected_key}  ({source_mode})")
    logger.info(f"    Target key   : {target_key}")

    # ── TRANSPOSE ────────────────────────────────────────────────────────────
    if detected_key:
        transp_interval = interval.Interval(detected_key.tonic, target_key.tonic)
        score = score.transpose(transp_interval)
    else:
        logger.warning("    Could not detect key — skipping transposition.")

    # ── GLOBAL METADATA ──────────────────────────────────────────────────────
    tempo_bpm   = 120.0
    time_sig    = "4/4"
    sig_num     = 4
    sig_denom   = 4

    for el in score.flatten():
        if isinstance(el, m21tempo.MetronomeMark) and el.number:
            tempo_bpm = float(el.number)
            break

    for el in score.flatten():
        if isinstance(el, meter.TimeSignature):
            time_sig  = el.ratioString
            sig_num   = el.numerator
            sig_denom = el.denominator
            break

    beat_sec          = 60.0 / tempo_bpm
    measure_sec       = beat_sec * sig_num
    total_measures    = 0

    for part in score.parts:
        meas = list(part.getElementsByClass("Measure"))
        if meas:
            total_measures = max(total_measures, meas[-1].number or len(meas))

    song_name = path.stem.lower().replace(" ", "_").replace("-", "_")

    # ── BUILD CONCURRENT-NOTE LOOKUP (OFFSET → PITCHES) FOR VERTICAL HARMONY ─
    # FLATTEN ALL SOUNDING NOTES BY ABSOLUTE QUARTER OFFSET
    offset_pitches: dict[float, list] = defaultdict(list)
    for part in score.parts:
        for el in part.flatten().notesAndRests:
            if isinstance(el, (m21note.Note, m21chord.Chord)):
                pitches = el.pitches if isinstance(el, m21chord.Chord) else [el.pitch]
                for p in pitches:
                    offset_pitches[float(el.offset)].append(p)

    # ── WALK EVERY PART / VOICE AND COLLECT EVENTS ───────────────────────────
    events     = []
    event_idx  = 0

    for voice_idx, part in enumerate(score.parts):
        flat_notes = list(part.flatten().notesAndRests)

        # PRE-COLLECT PITCHES LIST FOR CONTEXT (PREV/NEXT)
        pitch_seq  = []  # (ABSOLUTE_OFFSET_QUARTERS, PITCH_OBJ_OR_NONE, QL, DUR_TYPE)
        for el in flat_notes:
            abs_off = float(el.offset)
            ql      = float(el.duration.quarterLength) if el.duration.quarterLength else 1.0
            if isinstance(el, m21note.Rest):
                pitch_seq.append((abs_off, None, ql, quarter_to_dur_type(ql)))
            elif isinstance(el, m21note.Note):
                pitch_seq.append((abs_off, el.pitch, ql, quarter_to_dur_type(ql)))
            elif isinstance(el, m21chord.Chord):
                # TREAT THE HIGHEST NOTE AS THE MELODY NOTE FOR THIS VOICE
                top = sorted(el.pitches, key=lambda p: p.ps)[-1]
                pitch_seq.append((abs_off, top, ql, quarter_to_dur_type(ql)))

        total_quarters = sum(ps[2] for ps in pitch_seq) if pitch_seq else 1.0
        running_offset = 0.0

        for seq_idx, (abs_off, p_obj, ql, dur_type) in enumerate(pitch_seq):
            is_rest = (p_obj is None)

            # ── NEIGHBOURING CONTEXT ─────────────────────────────────────────
            prev_entry = pitch_seq[seq_idx - 1] if seq_idx > 0 else None
            next_entry = pitch_seq[seq_idx + 1] if seq_idx < len(pitch_seq) - 1 else None

            prev_pitch_obj = prev_entry[1] if prev_entry else None
            next_pitch_obj = next_entry[1] if next_entry else None
            prev_ql        = prev_entry[2] if prev_entry else None
            next_ql        = next_entry[2] if next_entry else None
            prev_dur_type  = prev_entry[3] if prev_entry else None
            next_dur_type  = next_entry[3] if next_entry else None

            # ── PITCH FIELDS ─────────────────────────────────────────────────
            if not is_rest:
                pc_name   = p_obj.name          # E.G. "F#"
                pc_int    = p_obj.pitchClass     # 0-11
                octave    = p_obj.octave
                pitch_str = f"{pc_name}{octave}"   # E.G. "F#4"

                degree    = degree_map.get(pc_name)
                tension   = pitch_tension(p_obj, degree_map)
                harm_func = get_harmonic_function(degree, source_mode) if degree else "chromatic"

                # CHROMATIC OFFSET: 0 = IN KEY, ±1 = ONE SEMITONE OUTSIDE
                chrom_off = 0
                if degree is None:
                    chrom_off = 1  # NON-DIATONIC

                # DISTANCE FROM TONIC (G=0) IN SEMITONES
                tonic_p   = pitch.Pitch("G4")
                dist_tonic = abs(interval_semitones(tonic_p, p_obj)) % 12
                # DISTANCE FROM DOMINANT (D=7 SEMITONES ABOVE G)
                dominant_p = pitch.Pitch("D4")
                dist_dom   = abs(interval_semitones(dominant_p, p_obj)) % 12
            else:
                pc_name = pitch_str = harm_func = None
                pc_int = octave = degree = chrom_off = dist_tonic = dist_dom = None
                tension = 0.0

            # ── DURATION & BUCKET ────────────────────────────────────────────
            bucket    = duration_to_bucket(ql) if not is_rest else None
            note_name = pitch_to_note_name(p_obj) if not is_rest else None
            af        = audio_file_path(bucket, note_name) if not is_rest else None
            dur_sec   = ql * beat_sec

            # ── POSITION FIELDS ──────────────────────────────────────────────
            abs_off_sec   = abs_off * beat_sec
            measure_num   = int(abs_off // sig_num) + 1
            beat_in_meas  = (abs_off % sig_num) + 1.0   # 1-BASED
            bar_progress  = (abs_off % sig_num) / sig_num
            song_progress = abs_off / total_quarters if total_quarters else 0.0

            is_measure_start = abs(beat_in_meas - 1.0) < 0.01
            is_measure_end   = abs(beat_in_meas + ql - (sig_num + 1)) < 0.05

            bs_label, metrical_str = beat_strength_label(beat_in_meas, sig_num)

            # SECTION CANDIDATE: DOWNBEAT OF A MEASURE DIVISIBLE BY 4
            is_section_cand = is_measure_start and (measure_num % 4 == 1)

            # ── INTERVAL / SMOOTHNESS FIELDS ─────────────────────────────────
            if not is_rest and prev_pitch_obj is not None:
                iv_from_prev = interval_semitones(prev_pitch_obj, p_obj)
                iv_dir       = interval_direction(iv_from_prev)
                iv_sz        = interval_size_class(iv_from_prev)
                mel_smooth   = melodic_smoothness(iv_from_prev)
                iv_smooth    = interval_smoothness(iv_from_prev)
                is_step      = abs(iv_from_prev) <= 2
                is_leap      = 3 <= abs(iv_from_prev) <= 7
                is_large_lp  = abs(iv_from_prev) > 7
                prev_p_str   = f"{prev_pitch_obj.name}{prev_pitch_obj.octave}"
            else:
                iv_from_prev = iv_dir = iv_sz = None
                mel_smooth = iv_smooth = None
                is_step = is_leap = is_large_lp = False
                prev_p_str = None

            if not is_rest and next_pitch_obj is not None:
                iv_to_next   = interval_semitones(p_obj, next_pitch_obj)
                next_p_str   = f"{next_pitch_obj.name}{next_pitch_obj.octave}"
            else:
                iv_to_next   = None
                next_p_str   = None

            conn_sc = None
            if prev_ql is not None and not is_rest:
                conn_sc = connection_score(prev_ql, ql)

            # ── TENSION DELTA + SMOOTHNESS ────────────────────────────────────
            if prev_entry and prev_entry[1] is not None and not is_rest:
                prev_tension = pitch_tension(prev_entry[1], degree_map)
                t_delta      = tension - prev_tension
                t_smooth     = 1.0 / (1.0 + 3.0 * abs(t_delta))
            else:
                t_delta = t_smooth = None

            # ── DURATION RATIOS ───────────────────────────────────────────────
            dur_ratio_prev = (ql / prev_ql) if prev_ql else None
            dur_ratio_next = (ql / next_ql) if next_ql else None

            # ── SYNCOPATION: NOTE STARTS OFF-BEAT AND LASTS INTO A STRONG BEAT ─
            is_sync = False
            if not is_rest and beat_in_meas % 1.0 != 0.0:
                end_beat = beat_in_meas + ql
                if int(end_beat) > int(beat_in_meas):
                    is_sync = True

            # ── PHRASE CANDIDATE MARKERS (SIMPLE ACCUMULATOR) ─────────────────
            # MARKED IN POST-PROCESSING BELOW — PLACEHOLDER
            phrase_cand_start = False
            phrase_cand_end   = False
            phrase_cand_id    = None

            # ── CADENCE DETECTION (SIMPLIFIED: LEADING-TONE RESOLVING TO TONIC) ─
            cad_authentic = False
            cad_half      = False
            cad_plagal    = False
            if not is_rest and degree == 1 and prev_pitch_obj is not None:
                prev_degree = degree_map.get(prev_pitch_obj.name)
                if prev_degree == 5:
                    cad_authentic = True
                elif prev_degree == 4:
                    cad_plagal = True
            if not is_rest and degree == 5 and is_measure_end:
                cad_half = True

            # ── VERTICAL (HARMONIC) CONTEXT ───────────────────────────────────
            concurrent_pitches = offset_pitches.get(abs_off, [])
            local_chord_str, chord_root, chord_quality = get_local_chord(concurrent_pitches)
            sim_note_count = len(concurrent_pitches)

            # VERTICAL INTERVAL FROM BASS (LOWEST CONCURRENT PITCH)
            vert_iv = None
            if not is_rest and concurrent_pitches:
                bass = min(concurrent_pitches, key=lambda pp: pp.ps)
                if bass != p_obj:
                    vert_iv = float(abs(p_obj.ps - bass.ps) % 12)

            # ── RELATIVE INTERVAL / RHYTHM PATTERN (3-NOTE WINDOW) ────────────
            rel_iv_pat   = None
            rel_rhy_pat  = None
            seq_win_id   = None
            if seq_idx >= 2:
                win = pitch_seq[seq_idx - 2 : seq_idx + 1]
                ivs = []
                rhy = []
                ok  = True
                for wi in range(1, len(win)):
                    if win[wi][1] is None or win[wi-1][1] is None:
                        ok = False; break
                    ivs.append(str(interval_semitones(win[wi-1][1], win[wi][1])))
                    rhy.append(win[wi][3])
                if ok:
                    rel_iv_pat  = " ".join(ivs)
                    rel_rhy_pat = " ".join(rhy)
                    seq_win_id  = seq_idx - 2

            # ── BUILD EVENT DICT ──────────────────────────────────────────────
            ev = {
                "event_index":               event_idx,
                "voice_index":               voice_idx,
                # POSITION
                "measure_number":            measure_num,
                "beat_position":             round(beat_in_meas, 4),
                "absolute_offset_quarters":  round(abs_off, 6),
                "absolute_offset_seconds":   round(abs_off_sec, 6),
                "bar_progress":              round(bar_progress, 6),
                "song_progress":             round(song_progress, 6),
                "is_measure_start":          is_measure_start,
                "is_measure_end":            is_measure_end,
                "is_section_candidate":      is_section_cand,
                # PITCH
                "pitch":                     pitch_str,
                "pitch_class":               pc_name,
                "octave":                    octave,
                "scale_degree":              degree,
                "pitch_class_int":           pc_int,
                "chromatic_offset":          chrom_off,
                "distance_from_tonic":       dist_tonic,
                "distance_from_dominant":    dist_dom,
                # DURATION
                "duration_quarter_length":   round(ql, 6),
                "duration_type":             dur_type,
                "duration_sec":              round(dur_sec, 6),
                "tempo_bpm":                 tempo_bpm,
                # AUDIO FILE MAPPING  ← NEW BUCKET SYSTEM
                "note_length_bucket":        bucket,
                "note_name":                 note_name,
                "audio_file":                af,
                # RHYTHM
                "beat_strength":             bs_label,
                "metrical_strength":         metrical_str,
                "is_syncopated":             is_sync,
                "duration_ratio_previous":   round(dur_ratio_prev, 6) if dur_ratio_prev is not None else None,
                "duration_ratio_next":       round(dur_ratio_next, 6) if dur_ratio_next is not None else None,
                # MELODY CONTEXT
                "is_rest":                   is_rest,
                "tension_score":             round(tension, 6),
                "tension_delta":             round(t_delta, 6) if t_delta is not None else None,
                "tension_smoothness":        round(t_smooth, 6) if t_smooth is not None else None,
                "melodic_smoothness":        round(mel_smooth, 6) if mel_smooth is not None else None,
                "interval_smoothness":       round(iv_smooth, 6) if iv_smooth is not None else None,
                "connection_score":          round(conn_sc, 6) if conn_sc is not None else None,
                "interval_from_previous":    iv_from_prev,
                "interval_to_next":          iv_to_next,
                "interval_direction":        iv_dir,
                "interval_size_class":       iv_sz,
                "is_step":                   is_step,
                "is_leap":                   is_leap,
                "is_large_leap":             is_large_lp,
                "previous_pitch":            prev_p_str,
                "next_pitch":                next_p_str,
                "previous_duration_type":    prev_dur_type,
                "next_duration_type":        next_dur_type,
                # PHRASE / CADENCE
                "phrase_candidate_start":    phrase_cand_start,
                "phrase_candidate_end":      phrase_cand_end,
                "phrase_candidate_id":       phrase_cand_id,
                "cadence_authentic":         cad_authentic,
                "cadence_half":              cad_half,
                "cadence_plagal":            cad_plagal,
                # HARMONIC
                "local_chord":               local_chord_str,
                "local_chord_root":          chord_root,
                "local_chord_quality":       chord_quality,
                "harmonic_function":         harm_func,
                # MOTIF
                "relative_interval_pattern": rel_iv_pat,
                "relative_rhythm_pattern":   rel_rhy_pat,
                "sequence_window_id":        seq_win_id,
                # MULTI-VOICE
                "simultaneous_note_count":   sim_note_count,
                "vertical_interval_from_bass": vert_iv,
            }

            events.append(ev)
            event_idx += 1
            running_offset += ql

    # ── POST-PROCESS: ASSIGN PHRASE IDS ──────────────────────────────────────
    phrase_starts = detect_phrase_boundaries(events)
    phrase_id     = 0
    next_start_set = set(phrase_starts)

    for i, ev in enumerate(events):
        if i in next_start_set:
            phrase_id += 1
            ev["phrase_candidate_start"] = True
        ev["phrase_candidate_id"] = phrase_id
        # MARK PHRASE END: LAST EVENT BEFORE NEXT BOUNDARY
        if (i + 1) in next_start_set or (i == len(events) - 1):
            ev["phrase_candidate_end"] = True

    logger.info(f"    Events extracted : {len(events)}")
    logger.info(f"    Tempo            : {tempo_bpm} BPM")
    logger.info(f"    Time signature   : {time_sig}")
    logger.info(f"    Measures         : {total_measures}")
    logger.info(f"    Phrases detected : {phrase_id}")

    # ── ASSEMBLE PAYLOAD ──────────────────────────────────────────────────────
    payload = {
        "song_name":       song_name,
        "original_key":    str(detected_key) if detected_key else "Unknown",
        "transposed_key":  str(target_key),
        "tempo_bpm":       tempo_bpm,
        "time_signature":  time_sig,
        "total_measures":  total_measures,
        "total_events":    len(events),
        "mode":            source_mode,
        "events":          events,
    }
    return payload


# ── POST TO VERCEL ─────────────────────────────────────────────────────────
def post_to_ingest(payload: dict, base_url: str, dry_run: bool = False) -> dict | None:
    if dry_run:
        sample = json.dumps(payload["events"][0], indent=2) if payload["events"] else "{}"
        logger.info(f"  [DRY RUN] Would POST {len(payload['events'])} events for '{payload['song_name']}'")
        logger.info(f"  First event sample:\n{sample}")
        return None

    url = f"{base_url}/api/audio/ingest"
    logger.info(f"  POSTing {len(payload['events'])} events → {url}")
    try:
        resp = requests.post(
            url,
            json=payload,
            timeout=120,   # LARGE PAYLOADS MAY TAKE A MOMENT
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info(f"  ✓ Ingest success: song_id={result.get('song_id')}  "
                    f"events={result.get('events_inserted')}")
        return result
    except requests.HTTPError as e:
        logger.error(f"  ✗ HTTP error: {e.response.status_code} — {e.response.text[:400]}")
    except requests.RequestException as e:
        logger.error(f"  ✗ Request failed: {e}")
    return None


# ── ENTRY POINT ───────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="meowREMIX Converter v1.0 — parse .mxl files → Neon DB via Vercel ingest"
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to a single .mxl file (default: all .mxl in projects/audio/source-files/)"
    )
    parser.add_argument(
        "--url",
        default=INGEST_URL,
        help="Base URL of your Vercel app (default: INGEST_URL from .env)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Parse and print without POSTing to Vercel"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("meowREMIX Converter v1.0")
    logger.info("=" * 60)
    logger.info(f"Project root : {PROJECT_ROOT}")
    logger.info(f"Source dir   : {SOURCE_DIR}")
    logger.info(f"Ingest URL   : {args.url or '(not set — use --dry-run or set INGEST_URL in .env)'}")

    if not args.dry_run and not args.url:
        logger.error(
            "INGEST_URL is not set.  Add it to vercel_app/.env  or pass --url.\n"
            "  Example:  INGEST_URL=https://my-app.vercel.app\n"
            "  Or run with --dry-run to test without posting."
        )
        sys.exit(1)

    # COLLECT FILES
    if args.file:
        files = [Path(args.file).resolve()]
        if not files[0].exists():
            logger.error(f"File not found: {files[0]}")
            sys.exit(1)
    else:
        if not SOURCE_DIR.is_dir():
            logger.error(f"Source directory not found: {SOURCE_DIR}")
            sys.exit(1)
        files = sorted(SOURCE_DIR.glob("*.mxl"))
        if not files:
            logger.error(f"No .mxl files found in {SOURCE_DIR}")
            sys.exit(1)

    logger.info(f"Files found  : {len(files)}")
    logger.info("")

    results = []
    for mxl_path in files:
        logger.info(f"[{mxl_path.name}]")
        try:
            payload = parse_mxl(mxl_path)
            result  = post_to_ingest(payload, args.url, dry_run=args.dry_run)
            results.append((mxl_path.name, "ok", result))
        except Exception as e:
            logger.error(f"  ✗ Failed to process {mxl_path.name}: {e}")
            results.append((mxl_path.name, "error", str(e)))
        logger.info("")

    # ── SUMMARY ───────────────────────────────────────────────────────────────
    logger.info("─" * 60)
    logger.info("Conversion summary:")
    ok_count  = sum(1 for _, status, _ in results if status == "ok")
    err_count = len(results) - ok_count
    for name, status, detail in results:
        icon = "✓" if status == "ok" else "✗"
        song_id = detail.get("song_id") if isinstance(detail, dict) else "—"
        events  = detail.get("events_inserted") if isinstance(detail, dict) else "—"
        logger.info(f"  {icon} {name:<40} song_id={song_id}  events={events}")
    logger.info(f"\n  {ok_count} succeeded  ·  {err_count} failed")
    logger.info("─" * 60)

    if err_count:
        sys.exit(1)


if __name__ == "__main__":
    main()