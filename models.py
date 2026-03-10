from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
#DB객체 껍데기만 만든 상태
#db.init_app(app)실제 플라스크 앱이랑 연결
class Question(db.Model):
#db.Model은 SQLAlchemy가 미리 만들어둔 부모클래스 db테이블과 연결되는 자식클래스를 만들수 있음
    __tablename__='questions'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    #id라는 열을 새로운 테이블에 생성
    #db.Colmn(타입,옵션들..)
    #열이름=db.Column(정수타입,기본키,자동으로 1씩 증가(회수))
    content=db.Column('question',db.Text,nullable=False)
    #얜 db의 question이라는 실제 컬럼을 갖고 와서 열로 구성
    model_answer=db.Column(db.Text,nullable=False)
    category=db.Column(db.String(50),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.now)
class SessioonResult(db.Model):
    __tablename__='answers'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    question_id=db.Column(db.Integer,db.ForeignKey('questions.id'),nullable=False)
    #questionid:답변이 왔을 때 연결할 질문
    #questions 테이블          answers 테이블
    #┌────┬──────────┐        ┌────┬─────────────┬────────┐
    #│ id │ content  │        │ id │ question_id │ answer │
    #├────┼──────────┤        ├────┼─────────────┼────────┤
    #│  1 │ OOP란?   │◄───────│  1 │      1      │ 캡슐화 │
    #│  2 │ REST란?  │        │  2 │      1      │ 상속   │
    #└────┴──────────┘        └────┴─────────────┴────────┘
    user_answer=db.Column('answer',db.Text)
    #사용자가 입력한 답변 db의 answer에 저장,읽을 때 db.answer에서 가져와서 user_answer로 읽음
    feedback=db.Column(db.Text)
    round_number=db.Column('session_no',db.Integer,nullable=False,default=1)
    #db컬럼명은 sesseion_no
    created_at=db.Column(db.DateTime,default=datetime.now)