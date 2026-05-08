# Updated 4/29/26
from flask import Flask, send_from_directory
from api.comments import comments_bp
from api.submitGameFeedback import feedback_bp
from api.support import support_bp
from api.testerSignup import tester_signup_bp
from api.wormholeFeedback import wormhole_feedback_bp
from api.leaderboard import leaderboard_bp
from api.wormhole_analysis import wormhole_analysis_bp
from api.scores import scores_bp
from api.blog import blog_bp
from api.responses import responses_bp      # AI Dopamine: A/B response pairs
from api.compare import compare_bp          # AI Dopamine: preference votes
from api.AI_score import score_bp
from api.mkDelta import mkdelta_bp

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
app.register_blueprint(blog_bp)                 # BLOG
app.register_blueprint(responses_bp)            # AI DOPAMINE
app.register_blueprint(compare_bp)              # AI DOPAMINE
app.register_blueprint(score_bp)                # AI DOPAMINE
app.register_blueprint(mkdelta_bp) 
 


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

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

@app.route('/mkdelta')
def mkdelta_page():
    return send_from_directory('forms', 'mkdelta.html')

@app.route('/mkdelta/template')
def mkdelta_template():
    return send_from_directory('static/templates', 'true-up_template.xlsx',
                               as_attachment=True,
                               download_name='MKDelta_Template.xlsx')

if __name__ == '__main__':
    app.run()