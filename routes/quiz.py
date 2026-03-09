#app.py파일을 실행할건데 그 파일에서 라우트해서 실행될 인자들 설정 모음
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
#request: 클라이언트가 보낸 요청 데이터 접근(form,args등),session:브라우저 세션에 데이터 저장/읽기(로그인상태등),redirect:다른 url로 접근
#url_for:함수이름으로 url자동생성 current_app:현재 실행 중인 Flask앱 자체에 접근
from sqlalchemy.sql.expression import func
#SQLAlchemy의 SQL함수 모음 DB에서 정렬할 때 사용
from models import db, Question, SessioonResult
#db: SQLalchemy의 db객체 Question:질문 테이블 SessionResult: 사용자 답변/피드백 테이블
from services.gemini_service import GeminiService
from services.voice_service import VoiceService
quiz_bp=Blueprint('quiz',__name__,url_prefix='/quiz')
#quiz_bp는 blueprint모듈사용해서 /quiz로 접속할 것임
voice_service=VoiceService()#변수 선언
def get_gemini():
    return GeminiService(current_app.config.get('GEMINI_API_KEY'))
#current_app.config 딕셔너리에서 get()방식으로 Geminiapi가져옴
@quiz_bp.route('/start',methods=['GET','POST'])
#route했을 때 GET과 POST라는 변수를 method라는 인자(속성)의 리스트 원소로 받음
def start():
    #GET:페이지 접속 POST(폼제출)처리
    if request.method=='POST':
        category=request.form.get('category')
        #form이라는 요청데이터에서 'category'값을 추출 
        if category:#catagory가 참이면
            session['category']=category#세션에 카테고리 저장
        session['round_number']=1#라운드를 1로 초기화
    return redirect(url_for('quiz.question'))#/quiz/question으로 이동
#request.form은 이요청에서 보낸 데이터만
@quiz_bp.route('/question')
def question():
    category=session.get('category')
    #/quiz/start에서 session['category']='CS'저장->Flask가 응답할 때 쿠키에 세션 데이터를 담아서 브라우저에 전송->브라우저가 쿠키 저장->브라우저가 /quiz/question요청하고 쿠키를 같이 보냄->Flask가 쿠키에서 세션꺼냄
    if not category:
        return redirect(url_for('main.index'))#없으면 main(홈)페이지로
    q=Question.query.filter_by(category=category).order_by(func.random()).first()
    #DB에서 catagory 필터해서 무작위로 첫번째 결과 가져옴
    if not q:
        return "질문이 없습니다.",404
    session['current_q_id']=q.id#현재 질문 ID를 세션에 저장->버그 currnet_id로 오타발생->
    audio_url= voice_service.text_to_speech(q.content)#질문을 음성 파일로 변환
    return render_template('quiz.html',question=q,round_num=session.get('round_number',1),audio_url=audio_url)
    #quiz.html에 질문 객체,session중 라운드번호,오디오 url 전달
@quiz_bp.route('/submit',methods=['POST'])
#BLUEPRINT로 submit로 라우팅할거고 Post데이터 받을 거야(폼제출로만 접근가능)
def submit():
    user_answer=request.form.get('user_answer')
    q_id=session.get('current_q_id')#->버그 currnet_id로 오타발생->qusestion_obj이 홈으로 redirect
    round_num=session.get('round_number',1)
    question_obj=Question.query.get(q_id)#질문한 DB객체를 조회
    if not question_obj:
        return redirect(url_for('main.index'))#질문 없으면 홈으로
    gemini=get_gemini()
    eval_result=gemini.evaluate_answer(
        question=question_obj.content,#질문내용
        model_answer=question_obj.model_answer,#모범답안
        user_answer=user_answer#사용자 답변
    )#제미나이 API에 질문/모범답안/사용자답변을 보내서 채점 결과 받음
    result_record=SessioonResult(
        question_id=q_id,
        user_answer=user_answer,
        feedback=eval_result.get('feedback',''),
        round_number=round_num
    )
    db.session.add(result_record)#session응답을 db에 추가
    db.session.commit()#저장 확정
    session['round_number']=round_num+1#다음 라운드로 증가
    return render_template('feedback.html',question=question_obj,user_answer=user_answer, eval_result=eval_result)
    #제미나이에게 응답받은 내용을 feedback.html에 저장
    #홈(/) → 카테고리 선택→ POST /quiz/start → 세션에 카테고리/라운드 저장→ /quiz/question → DB에서 랜덤 질문 + TTS 음성 생성→ /quiz/submit → Gemini 채점 → DB 저장→ feedback.html 결과 표시