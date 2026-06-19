# Updated 6/15/26
import os
from flask import Flask, send_from_directory
from api.comments import comments_bp                           # GENERAL
from api.submitGameFeedback import feedback_bp                 # CATASTROPHE 2
from api.support import support_bp                              # GENERAL
from api.testerSignup import tester_signup_bp                  # GENERAL
from api.wormholeFeedback import wormhole_feedback_bp          # WORMHOLES ALL THE WAY DOWN
from api.leaderboard import leaderboard_bp                     # WORMHOLES ALL THE WAY DOWN
from api.wormhole_analysis import wormhole_analysis_bp         # WORMHOLES ALL THE WAY DOWN
from api.config_score import config_score_bp                       # WORMHOLES ALL THE WAY DOWN
from api.scores import scores_bp                               # WORMHOLES ALL THE WAY DOWN
from api.blog import blog_bp                                   # GENERAL
from api.responses import responses_bp                         # AI DOPAMINE: A/B RESPONSE PAIRS
from api.compare import compare_bp                             # AI DOPAMINE: PREFERENCE VOTES 
from api.AI_score import score_bp                              # AI DOPAMINE
from api.trueDelta import truedelta_bp                         # TRUE DELTA
from api.audio.ingest       import audio_ingest_bp             # meowREMIX
from api.audio.analyze      import audio_analyze_bp            # meowREMIX
from api.audio.rules_serve  import rules_serve_bp              # meowREMIX — serves rules.js from Neon
from api.audio_training     import audio_training_bp           # meowREMIX
from api.memories import memories_bp                           # LIGHTHOUSE
from api.catforce import catforce_bp                           # CATFORCE CONTENT SCHEDULER
from api.tiktok import tiktok_bp                               # CATFORCE TIK TOK BLUEPRINT

from api.projects import projects_bp

from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='forms')
CORS(app)

app.register_blueprint(comments_bp)             # GENERAL
app.register_blueprint(feedback_bp)             # CATastrophe2
app.register_blueprint(support_bp)              # GENERAL
app.register_blueprint(tester_signup_bp)        # CATastrophe2
app.register_blueprint(wormhole_feedback_bp)    # WORMHOLES ALL THE WAY DOWN
app.register_blueprint(leaderboard_bp)          # WORMHOLES ALL THE WAY DOWN
app.register_blueprint(scores_bp)               # WORMHOLES ALL THE WAY DOWN
app.register_blueprint(wormhole_analysis_bp)    # WORMHOLES ALL THE WAY DOWN
app.register_blueprint(config_score_bp)         # WORMHOLES ALL THE WAY DOWN
app.register_blueprint(blog_bp)                 # BLOG
app.register_blueprint(responses_bp)            # AI DOPAMINE
app.register_blueprint(compare_bp)              # AI DOPAMINE
app.register_blueprint(score_bp)                # AI DOPAMINE
app.register_blueprint(truedelta_bp)
app.register_blueprint(audio_ingest_bp)         # meowREMIX
app.register_blueprint(audio_analyze_bp)        # meowREMIX
app.register_blueprint(rules_serve_bp)          # meowREMIX — rules.js from Neon
app.register_blueprint(audio_training_bp)       # meowREMIX
app.register_blueprint(memories_bp)             # LIGHTHOUSE
app.register_blueprint(catforce_bp)             # CATFORCE CONTENT SCHEDULER
app.register_blueprint(tiktok_bp)               # CATFORCE TIK TOK BP
app.register_blueprint(projects_bp)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/catforce')
def catforce_page():
    return send_from_directory('forms', 'catforce.html')

# === NEW: PROJECT INGEST HTML serving PAGE ROUTE ===
@app.route('/project-submit')
def project_submit_page():
    return send_from_directory('forms', 'projectSubmit.html')

@app.route('/comments')
def comments_page():
    return send_from_directory('forms', 'comments.html')

@app.route('/game-testing')
def game_testing_page():
    return send_from_directory('forms', 'GameTesting.html')

@app.route('/support')
def support_page():
    return send_from_directory('forms', 'support.html')

@app.route('/tester-signup')
def tester_signup_page():
    return send_from_directory('forms', 'testerSignup.html')

@app.route('/dashboard')
def dashboard_page():
    return send_from_directory('forms', 'dashboard.html')

@app.route('/wormhole-feedback')
def wormhole_feedback_page():
    return send_from_directory('forms', 'wormholeFeedback.html')

@app.route('/leaderboard')
def leaderboard_page():
    return send_from_directory('forms', 'leaderboard.html')

@app.route('/wormhole-analysis')
def wormhole_analysis_page():
    return send_from_directory('forms', 'wormhole-analysis.html')

@app.route('/blog')
def blog_page():
    return send_from_directory('forms', 'blog.html')

@app.route('/admin/new')
def admin_new_post_page():
    return send_from_directory('forms', 'admin_new_post.html')

@app.route('/response-input')
def response_input_page():
    return send_from_directory('forms', 'response_input.html')

@app.route('/arena')
def arena_page():
    return send_from_directory('forms', 'arena.html')

@app.route('/ai-dopamine')
def ai_dopamine_page():
    return send_from_directory('forms', 'ai-dopamine.html')

@app.route('/scorer')
def scorer_page():
    return send_from_directory('forms', 'scorer.html')

@app.route('/steam-analysis')
def steam_analysis_page():
    return send_from_directory('forms', 'steam-analysis.html')

@app.route('/true-delta')
def trueDelta_page():
    return send_from_directory('forms', 'true-delta.html')

@app.route('/true-delta/template')
def trueDelta_template():
    return send_from_directory('static/templates', 'true-up_template.xlsx',
                               as_attachment=True,
                               download_name='TrueDelta_Template.xlsx')


@app.route('/meowREMIX')
@app.route('/meowREMIX.html')
def meow_remix():
    return send_from_directory('forms', 'meowREMIX.html')

@app.route('/forms/rules.js')
def rules_js():
    return send_from_directory('forms', 'rules.js', mimetype='application/javascript')

@app.route('/audioTraining')
@app.route('/audioTraining.html')
def audio_training_page():
    return send_from_directory('forms', 'audioTraining.html')

@app.route('/memories')
def memories_page():
    return send_from_directory('forms', 'memories.html')

FORMS_DIR = os.path.join(os.path.dirname(__file__), "forms")
 
@app.route("/terms")
def terms():
    return send_from_directory(FORMS_DIR, "terms.html")
 
@app.route("/privacy")
def privacy():
    return send_from_directory(FORMS_DIR, "privacy.html")

if __name__ == '__main__':
    app.run()