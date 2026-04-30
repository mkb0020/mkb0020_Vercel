import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

load_dotenv()

score_bp = Blueprint('score', __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'weights', 'reward_model.pt')

_model    = None
_embedder = None


def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            return None
        from models.reward_model import load_model
        _model = load_model(MODEL_PATH)
    return _model


def get_embedder():
    global _embedder
    if _embedder is None:
        from models.embeddings import get_embedder as _get_embedder
        _embedder = _get_embedder()
    return _embedder


@score_bp.route('/api/score', methods=['POST'])
def score_responses():
    model = get_model()
    if model is None:
        return jsonify({
            "success": False,
            "error": "No trained model found. Run train.py first."
        }), 503

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data received"}), 400

    prompt    = data.get("prompt", "").strip()
    responses = data.get("responses", [])

    if not prompt:
        return jsonify({"success": False, "error": "prompt is required"}), 400
    if not responses or not isinstance(responses, list):
        return jsonify({"success": False, "error": "responses must be a non-empty list"}), 400
    if len(responses) > 10:
        return jsonify({"success": False, "error": "Max 10 responses per request"}), 400

    responses = [r.strip() for r in responses if r.strip()]
    if not responses:
        return jsonify({"success": False, "error": "All responses were empty"}), 400

    try:
        import torch
        import numpy as np

        embedder = get_embedder()
        prompts_repeated = [prompt] * len(responses)
        prompt_vecs   = embedder.encode(prompts_repeated, convert_to_numpy=True, show_progress_bar=False)
        response_vecs = embedder.encode(responses,         convert_to_numpy=True, show_progress_bar=False)
        combined      = np.concatenate([prompt_vecs, response_vecs], axis=1)

        input_tensor = torch.tensor(combined, dtype=torch.float32)
        scores = model.score(input_tensor).numpy().tolist()

        if len(scores) > 1:
            min_s, max_s = min(scores), max(scores)
            spread = max_s - min_s if max_s != min_s else 1.0
            normalized = [(s - min_s) / spread for s in scores]
        else:
            normalized = [float(1 / (1 + np.exp(-scores[0])))]

        results = sorted([
            {
                "response":  responses[i],
                "raw_score": round(scores[i], 4),
                "score":     round(normalized[i], 4),
                "rank":      None
            }
            for i in range(len(responses))
        ], key=lambda x: x["score"], reverse=True)

        for rank, item in enumerate(results, 1):
            item["rank"] = rank

        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@score_bp.route('/api/score/status', methods=['GET'])
def model_status():
    model_exists = os.path.exists(MODEL_PATH)
    model_loaded = _model is not None

    return jsonify({
        "success":      True,
        "model_ready":  model_exists,
        "model_loaded": model_loaded,
    })