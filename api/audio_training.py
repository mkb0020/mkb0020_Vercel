# /blueprints/audio_training.py
from flask import Blueprint, request, jsonify
import json
import os
import psycopg2
from psycopg2.extras import Json

audio_training_bp = Blueprint('audio_training', __name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

@audio_training_bp.route('/api/audio/preferences', methods=['POST'])
def submit_preference():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    required = ['phraseId', 'rating', 'bpm', 'measures', 'phrase', 'sliderState']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    source = data.get('source', 'audioTraining')  # allow callers to tag origin

    rating = data['rating']
    if rating not in ('like', 'dislike'):
        return jsonify({'error': 'Rating must be like or dislike'}), 400

    phrase_id = data['phraseId']
    bpm = int(data['bpm'])
    measures = int(data['measures'])
    phrase_json = json.dumps(data['phrase'])  # ensure JSONB

    slider = data['sliderState']
    susp = float(slider.get('suspensionRisk', 0))
    lvol = float(slider.get('longVolume', 0))
    mvol = float(slider.get('mediumVolume', 0))
    svol = float(slider.get('shortVolume', 0))

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO audio_preferences
               (phrase_id, rating, bpm, measures, phrase_json,
                suspension_risk, long_volume, medium_volume, short_volume, source)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (phrase_id, rating, bpm, measures, phrase_json,
             susp, lvol, mvol, svol, source)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500