from flask import Flask, send_from_directory
from api.comments import comments_bp  
from api.submitGameFeedback import feedback_bp

app = Flask(__name__, static_folder='../static', template_folder='../forms')

app.register_blueprint(comments_bp)
app.register_blueprint(feedback_bp)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run()