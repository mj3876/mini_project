from flask import Blueprint, render_template
#Blueprint는 app에 붙일 인자 묶어놓는 모듈,render_template는 html과 연결
main_bp = Blueprint('main',__name__)
#Blueprint 클래스에 main이라는 인자로 이름 붙이고
#main.py파일을 import해서불러올때 __name__이 routes.main으로 파일의 경로를 찾아 전달해줌
#blueprint 내부에는 
#def __int__(self,name,import_name,url_prefic=Non)이라는 내용이 담김
#self.name=main저장 self.import_name=routes.main저장 self.deferred_functions = []저장
@main_bp.route('/')
#main_bp.deferred_functions에 경로='/' 등록
#나중에 app.register_blueprint(main_bp)
#->deferred_functions을 순회하며 app에 실제 라우트 등록
def index():
    return render_template('index.html')#웹페이지를 접속하면 html파일을 연결해라