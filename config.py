import os

# 로컬 개발 환경에서만 .env 파일 사용
# 쿠버네티스에서는 YAML의 env 블록이 환경변수를 직접 주입하므로 load_dotenv() 불필요
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    # ── DB 접속 정보 ──────────────────────────────────────────────
    # 쿠버네티스: 웹서버 Deployment YAML의 env 블록에서 주입
    #   DB_HOST → mysql-service (DB파드를 가리키는 ClusterIP Service 이름)
    #   나머지   → Secret 또는 ConfigMap으로 주입 권장
    DB_USER     = os.getenv('DB_USER',     'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST     = os.getenv('DB_HOST',     'localhost')  # k8s: DB Service 이름
    DB_PORT     = os.getenv('DB_PORT',     '3306')
    DB_NAME     = os.getenv('DB_NAME',     'interview_db')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ── 웹서버 전용 설정 ──────────────────────────────────────────
    # 쿠버네티스: 웹서버 Deployment YAML의 env 블록에서 주입
    SECRET_KEY     = os.getenv('SECRET_KEY',     'dev-secret')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')