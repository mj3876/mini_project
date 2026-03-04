from flask import Flask
from config import Config
from models import db
from routes.main import main_bp
from routes.quiz import quiz_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)