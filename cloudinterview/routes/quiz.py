from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from sqlalchemy.sql.expression import func
from models import db, Question, SessionResult
from services.gemini_service import GeminiService
from services.voice_service import VoiceService

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')
voice_service = VoiceService()

def get_gemini():
    return GeminiService(current_app.config.get('GEMINI_API_KEY'))
@quiz_bp.route('/start')
def start():
    # 세션 초기화 작업 (예: 라운드 번호 1로 세팅)
    session['round_number'] = 1
    # 카테고리 선택 페이지로 보내거나 바로 첫 질문으로 리다이렉트
    return redirect(url_for('quiz.question'))
@quiz_bp.route('/question')
def question():
    category = session.get('category')
    if not category:
        return redirect(url_for('main.index'))

    # DB에서 랜덤 질문 추출
    q = Question.query.filter_by(category=category).order_by(func.random()).first()
    if not q:
        return "질문이 없습니다.", 404

    session['current_q_id'] = q.id
    
    # ✅ gTTS로 질문 읽어주는 파일 생성
    audio_url = voice_service.text_to_speech(q.content)

    return render_template(
        'quiz.html', 
        question=q, 
        round_num=session.get('round_number', 1),
        audio_url=audio_url  # 생성된 음성 경로 전달
    )
# routes/quiz.py 파일 하단에 추가

@quiz_bp.route('/submit', methods=['POST'])
def submit():
    """유저가 입력한(또는 음성 인식된) 답변을 받아 제미나이에게 채점 맡김"""
    user_answer = request.form.get('user_answer')
    q_id = session.get('current_q_id')
    round_num = session.get('round_number', 1)
    
    # DB에서 원본 질문과 모범답안 가져오기
    from models import Question, SessionResult
    question_obj = Question.query.get(q_id)

    if not question_obj:
        return redirect(url_for('main.index'))

    # 1. 제미나이 평가 (API 호출)
    gemini = get_gemini()
    eval_result = gemini.evaluate_answer(
        question=question_obj.content,
        model_answer=question_obj.model_answer,
        user_answer=user_answer
    )

    # 2. 유저 답변과 피드백을 DB(answers 테이블)에 저장
    result_record = SessionResult(
        question_id=q_id,
        user_answer=user_answer,
        feedback=eval_result.get('feedback', ''),
        round_number=round_num
    )
    db.session.add(result_record)
    db.session.commit()

    # 다음 회차를 위해 라운드 번호 증가
    session['round_number'] = round_num + 1

    # 피드백 화면으로 이동 (feedback.html 필요)
    return render_template(
        'feedback.html', 
        question=question_obj,
        user_answer=user_answer,
        eval_result=eval_result
    )
# ... submit 라우트는 이전 텍스트 버전과 동일