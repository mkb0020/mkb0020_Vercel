import os
import psycopg
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")

audio_ingest_bp = Blueprint('audio_ingest', __name__)


def _f(val):
    """Return float or None."""
    try:
        return float(val) if val is not None else None
    except (TypeError, ValueError):
        return None

def _i(val):
    """Return int or None."""
    try:
        return int(val) if val is not None else None
    except (TypeError, ValueError):
        return None

def _b(val):
    """Return bool, defaulting to False."""
    if val is None:
        return False
    return bool(val)

def _s(val, max_len: int = None):
    """Return stripped string or None."""
    if val is None:
        return None
    s = str(val).strip()
    if max_len:
        s = s[:max_len]
    return s or None


# POST /api/audio/ingest
@audio_ingest_bp.route('/api/audio/ingest', methods=['POST'])
def ingest_song():
    """
    Accepts a JSON payload from the local converter.py CLI and writes
    song metadata + all note events into Neon.

    Expected payload shape:
    {
        "song_name": "hallelujah",
        "original_key": "C major",
        "transposed_key": "G major",
        "tempo_bpm": 72.0,
        "time_signature": "4/4",
        "total_measures": 48,
        "total_events": 312,
        "mode": "major",
        "events": [ { ...note event dict... }, ... ]
    }

    Returns:
    {
        "success": true,
        "song_id": 7,
        "events_inserted": 312
    }
    """
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"success": False, "error": "No JSON body received"}), 400

        song_name = _s(data.get("song_name"), 255)
        if not song_name:
            return jsonify({"success": False, "error": "'song_name' is required"}), 400

        events = data.get("events")
        if not isinstance(events, list):
            return jsonify({"success": False, "error": "'events' must be a list"}), 400

        with psycopg.connect(DB_URL, autocommit=False) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM audio_songs WHERE song_name = %s",
                    (song_name,)
                )
                existing = cur.fetchone()
                if existing:
                    old_id = existing[0]
                    cur.execute("DELETE FROM audio_note_events WHERE song_id = %s", (old_id,))
                    cur.execute("DELETE FROM audio_songs WHERE id = %s", (old_id,))

                cur.execute("""
                    INSERT INTO audio_songs
                        (song_name, original_key, transposed_key, tempo_bpm,
                         time_signature, total_measures, total_events, mode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    song_name,
                    _s(data.get("original_key"), 50),
                    _s(data.get("transposed_key"), 50),
                    _f(data.get("tempo_bpm")),
                    _s(data.get("time_signature"), 20),
                    _i(data.get("total_measures")),
                    _i(data.get("total_events")),
                    _s(data.get("mode"), 20),
                ))
                song_id = cur.fetchone()[0]

                rows = []
                for ev in events:
                    rows.append((
                        song_id,
                        _i(ev.get("event_index")),
                        _i(ev.get("voice_index")),
                        _i(ev.get("measure_number")),
                        _f(ev.get("beat_position")),
                        _f(ev.get("absolute_offset_quarters")),
                        _f(ev.get("absolute_offset_seconds")),
                        _f(ev.get("bar_progress")),
                        _f(ev.get("song_progress")),
                        _b(ev.get("is_measure_start")),
                        _b(ev.get("is_measure_end")),
                        _b(ev.get("is_section_candidate")),
                        _s(ev.get("pitch"), 20),
                        _s(ev.get("pitch_class"), 10),
                        _i(ev.get("octave")),
                        _i(ev.get("scale_degree")),
                        _i(ev.get("pitch_class_int")),
                        _f(ev.get("chromatic_offset")),
                        _i(ev.get("distance_from_tonic")),
                        _i(ev.get("distance_from_dominant")),
                        _f(ev.get("duration_quarter_length")),
                        _s(ev.get("duration_type"), 30),
                        _f(ev.get("duration_sec")),
                        _f(ev.get("tempo_bpm")),
                        _s(ev.get("note_length_bucket"), 10),
                        _s(ev.get("note_name"), 10),
                        _s(ev.get("audio_file"), 60),
                        _s(ev.get("beat_strength"), 10),
                        _f(ev.get("metrical_strength")),
                        _b(ev.get("is_syncopated")),
                        _f(ev.get("duration_ratio_previous")),
                        _f(ev.get("duration_ratio_next")),
                        _b(ev.get("is_rest")),
                        _f(ev.get("tension_score")),
                        _f(ev.get("tension_delta")),
                        _f(ev.get("tension_smoothness")),
                        _f(ev.get("melodic_smoothness")),
                        _f(ev.get("interval_smoothness")),
                        _f(ev.get("connection_score")),
                        _i(ev.get("interval_from_previous")),
                        _i(ev.get("interval_to_next")),
                        _s(ev.get("interval_direction"), 15),
                        _s(ev.get("interval_size_class"), 10),
                        _b(ev.get("is_step")),
                        _b(ev.get("is_leap")),
                        _b(ev.get("is_large_leap")),
                        _s(ev.get("previous_pitch"), 20),
                        _s(ev.get("next_pitch"), 20),
                        _s(ev.get("previous_duration_type"), 30),
                        _s(ev.get("next_duration_type"), 30),
                        _b(ev.get("phrase_candidate_start")),
                        _b(ev.get("phrase_candidate_end")),
                        _i(ev.get("phrase_candidate_id")),
                        _b(ev.get("cadence_authentic")),
                        _b(ev.get("cadence_half")),
                        _b(ev.get("cadence_plagal")),
                        _s(ev.get("local_chord"), 60),
                        _s(ev.get("local_chord_root"), 10),
                        _s(ev.get("local_chord_quality"), 20),
                        _s(ev.get("harmonic_function"), 20),
                        _s(ev.get("relative_interval_pattern"), 40),
                        _s(ev.get("relative_rhythm_pattern"), 40),
                        _i(ev.get("sequence_window_id")),
                        _i(ev.get("simultaneous_note_count")),
                        _f(ev.get("vertical_interval_from_bass")),
                    ))

                cur.executemany("""
                    INSERT INTO audio_note_events (
                        song_id, event_index, voice_index,
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
                    ) VALUES (
                        %s, %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s
                    )
                """, rows)

            conn.commit()

        return jsonify({
            "success": True,
            "song_id": song_id,
            "events_inserted": len(rows),
            "song_name": song_name,
        }), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@audio_ingest_bp.route('/api/audio/songs', methods=['GET'])
def list_songs():
    """Return all songs with their metadata."""
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, song_name, original_key, transposed_key,
                           tempo_bpm, time_signature, total_measures, total_events,
                           mode, created_at
                    FROM audio_songs
                    ORDER BY created_at DESC
                """)
                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()

        songs = []
        for row in rows:
            d = dict(zip(cols, row))
            if d.get("created_at") and hasattr(d["created_at"], "isoformat"):
                d["created_at"] = d["created_at"].isoformat()
            if d.get("tempo_bpm") is not None:
                d["tempo_bpm"] = float(d["tempo_bpm"])
            songs.append(d)

        return jsonify({"success": True, "songs": songs, "count": len(songs)})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# GET /api/audio/songs/<int:song_id>/events  — fetch events for a song
@audio_ingest_bp.route('/api/audio/songs/<int:song_id>/events', methods=['GET'])
def get_song_events(song_id):
    """
    Return note events for a song.
    Optional query params:
      ?bucket=long|med|short   — filter by note_length_bucket
      ?note=g|a|b|...          — filter by note_name
      ?rests=false             — exclude rests (default: include)
      ?limit=500&offset=0      — pagination
    """
    try:
        bucket   = request.args.get('bucket')
        note     = request.args.get('note')
        rests    = request.args.get('rests', 'true').lower() != 'false'
        limit    = min(int(request.args.get('limit', 1000)), 5000)
        offset   = int(request.args.get('offset', 0))

        conditions = ["song_id = %s"]
        params: list = [song_id]

        if bucket:
            conditions.append("note_length_bucket = %s")
            params.append(bucket)
        if note:
            conditions.append("note_name = %s")
            params.append(note)
        if not rests:
            conditions.append("is_rest = FALSE")

        where = " AND ".join(conditions)

        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT song_name FROM audio_songs WHERE id = %s", (song_id,))
                song_row = cur.fetchone()
                if not song_row:
                    return jsonify({"success": False, "error": f"Song {song_id} not found"}), 404

                cur.execute(f"""
                    SELECT event_index, measure_number, beat_position, pitch, pitch_class,
                           octave, duration_quarter_length, duration_type,
                           note_length_bucket, note_name, audio_file,
                           tension_score, beat_strength, is_rest,
                           phrase_candidate_id, cadence_authentic, cadence_half, cadence_plagal,
                           absolute_offset_quarters, song_progress
                    FROM audio_note_events
                    WHERE {where}
                    ORDER BY absolute_offset_quarters, voice_index
                    LIMIT %s OFFSET %s
                """, params + [limit, offset])

                cols = [d[0] for d in cur.description]
                rows = cur.fetchall()

        events = [dict(zip(cols, row)) for row in rows]
        numeric_cols = {
            'beat_position', 'duration_quarter_length', 'tension_score',
            'metrical_strength', 'absolute_offset_quarters', 'song_progress'
        }
        for ev in events:
            for col in numeric_cols:
                if col in ev and ev[col] is not None:
                    ev[col] = float(ev[col])

        return jsonify({
            "success": True,
            "song_id": song_id,
            "song_name": song_row[0],
            "count": len(events),
            "events": events,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# DELETE /api/audio/songs/<int:song_id>  — remove a song and its events
@audio_ingest_bp.route('/api/audio/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    try:
        with psycopg.connect(DB_URL, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT song_name FROM audio_songs WHERE id = %s", (song_id,))
                row = cur.fetchone()
                if not row:
                    return jsonify({"success": False, "error": f"Song {song_id} not found"}), 404
                cur.execute("DELETE FROM audio_songs WHERE id = %s", (song_id,))

        return jsonify({"success": True, "deleted_song_id": song_id, "song_name": row[0]})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500