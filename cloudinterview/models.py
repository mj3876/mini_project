from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column('question', db.Text, nullable=False) 
    model_answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class SessionResult(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column('answer', db.Text) 
    feedback = db.Column(db.Text)
    round_number = db.Column('session_no', db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)