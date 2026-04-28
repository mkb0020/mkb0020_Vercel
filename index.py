# Updated 4/28/26
from flask import Flask, send_from_directory
from api.comments import comments_bp
from api.submitGameFeedback import feedback_bp
from api.support import support_bp
from api.testerSignup import tester_signup_bp
from api.wormholeFeedback import wormhole_feedback_bp
from api.leaderboard import leaderboard_bp  
from api.wormhole_analysis import wormhole_analysis_bp 
from api.scores import scores_bp
from flask_cors import CORS      
from api.blog import blog_bp       

app = Flask(__name__, static_folder='static', template_folder='forms')
CORS(app)

app.register_blueprint(comments_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(support_bp)
app.register_blueprint(tester_signup_bp)
app.register_blueprint(wormhole_feedback_bp)
app.register_blueprint(leaderboard_bp)        
app.register_blueprint(scores_bp)      
app.register_blueprint(wormhole_analysis_bp)   
app.register_blueprint(blog_bp)



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

if __name__ == '__main__':
    app.run()