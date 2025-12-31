from flask import Flask, send_from_directory
from api.comments import comments_bp
from api.submitGameFeedback import feedback_bp
from api.support import support_bp
from api.testerSignup import tester_signup_bp

app = Flask(__name__, static_folder='static', template_folder='forms')

app.register_blueprint(comments_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(support_bp)
app.register_blueprint(tester_signup_bp)

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

if __name__ == '__main__':
    app.run()