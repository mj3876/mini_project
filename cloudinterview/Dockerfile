# 1. 가벼운 Alpine 리눅스 기반의 파이썬 이미지 사용
FROM python:3.11-alpine

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 빌드 패키지 설치 (경량화 전략)
# --no-cache를 써야 설치 후 찌꺼기 파일이 남지 않아 용량이 줄어듭니다.
RUN apk add --no-cache gcc musl-dev linux-headers

# 4. 의존성 파일 먼저 복사 (캐시 효율화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 소스 코드 복사
COPY . .

# 6. Flask 앱이 사용할 포트 명시
EXPOSE 5000

# 7. 컨테이너 실행 시 실행할 명령어
CMD ["python", "app.py"]
