import json
import re
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def evaluate_answer(self, question: str, model_answer: str, user_answer: str) -> dict:
        prompt = f"""
당신은 IT 기술 면접관입니다. 아래 지원자의 답변을 평가해주세요.

[면접 질문]: {question}
[모범 답안]: {model_answer}
[지원자 답변]: {user_answer}

규칙:
- 모범 답안의 핵심 키워드가 포함되었는지 확인하세요.
- 피드백은 200자 이내로 부드럽지만 핵심을 짚어주세요.
- 반드시 아래 JSON 형식으로만 응답하세요.

{{
    "score": 85,
    "feedback": "잘 답변하셨습니다. 다만 [핵심 개념] 부분이 누락되어 아쉽습니다."
}}
"""
        try:
            response = self.model.generate_content(prompt)
            cleaned = re.sub(r'```(?:json)?\s*', '', response.text).replace('```', '').strip()
            return json.loads(cleaned)
        except Exception as e:
            return {"score": 0, "feedback": f"평가 중 오류가 발생했습니다: {str(e)}"}