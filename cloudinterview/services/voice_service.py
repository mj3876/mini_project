import os
from gtts import gTTS

class VoiceService:
    def __init__(self):
        # 음성 파일을 저장할 폴더 생성
        self.save_path = "static/audio"
        os.makedirs(self.save_path, exist_ok=True)

    def text_to_speech(self, text, filename="question.mp3"):
        """텍스트를 한국어 음성(mp3)으로 변환하여 저장"""
        try:
            tts = gTTS(text=text, lang='ko')
            file_full_path = os.path.join(self.save_path, filename)
            tts.save(file_full_path)
            # 브라우저에서 접근 가능한 URL 경로 반환
            return f"/static/audio/{filename}"
        except Exception as e:
            print(f"TTS 생성 오류: {e}")
            return None