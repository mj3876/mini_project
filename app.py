from flask import Flask#플라스크 프레임워크에서 flask클래스 가져와서 웹 앱 객체 만듦
from config import Config#config.py파일에서 Config클래스 가져옴 DB주소,API키 설정값 담긴 클래스
from models import db#model.py에서 db객체 가져옴
from routes.main import main_bp
from routes.quiz import quiz_bp
#class Config:
    #SECRET_KEY ='abc123'
    #DB_URL='mysql://'키값과 url값들을 담음
def create_app():
    app = Flask(__name__)
    #Flask 클라스에서 (__name__)이라는 변수 app.import했을때 이 함수를 실행해라
    app.config.from_object(Config)
    #.config:속성
    #app.config:Flask의 설정값을 담는 딕셔너리
    #app.config['SECRET_KEY']이렇게 쓸 수 있음
    #.from_object(Config)Config에 있는 설정값들을 app.config에 한번에 복사
    db.init_app(app)
    # 블루프린트 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(quiz_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)