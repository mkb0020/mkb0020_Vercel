# /api/audio_training.py
from flask import Blueprint, request, jsonify
import json
import os
import psycopg2

audio_training_bp = Blueprint('audio_training', __name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

@audio_training_bp.route('/api/audio/preferences', methods=['POST'])
def submit_preference():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    rating = data.get('rating')
    if rating not in ('like', 'dislike'):
        return jsonify({'error': 'Rating must be like or dislike'}), 400

    training_type = data.get('trainingType', 'phrase')  # phrase | harmony | sequence
    source        = data.get('source', 'audioTraining')
    phrase_id     = data.get('phraseId')
    bpm           = int(data.get('bpm', 90))
    measures      = int(data.get('measures', 2))
    phrase_json   = json.dumps(data.get('phrase', {}))

    slider = data.get('sliderState', {})
    susp = float(slider.get('suspensionRisk', 0))
    lvol = float(slider.get('longVolume',     0))
    mvol = float(slider.get('mediumVolume',   0))
    svol = float(slider.get('shortVolume',    0))

    # harmony / sequence panels send note_a + note_b instead of a full phrase
    note_a = data.get('noteA')   # harmony: lower/first note;  sequence: first note
    note_b = data.get('noteB')   # harmony: upper note;        sequence: second note

    # phrase panel still requires these
    if training_type == 'phrase':
        for field in ['phraseId', 'phrase']:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

    # harmony / sequence panels require note_a + note_b
    if training_type in ('harmony', 'sequence'):
        if not note_a or not note_b:
            return jsonify({'error': 'noteA and noteB required for harmony/sequence'}), 400

    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute(
            """INSERT INTO audio_preferences
               (phrase_id, rating, bpm, measures, phrase_json,
                suspension_risk, long_volume, medium_volume, short_volume,
                source, training_type, note_a, note_b)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (phrase_id, rating, bpm, measures, phrase_json,
             susp, lvol, mvol, svol,
             source, training_type, note_a, note_b)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500