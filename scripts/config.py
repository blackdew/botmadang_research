"""봇마당 API 설정"""

API_BASE_URL = "https://botmadang.org/api/v1"
RATE_LIMIT_PER_MINUTE = 100
REQUEST_INTERVAL = 60.0 / RATE_LIMIT_PER_MINUTE  # ~0.6초

# API 엔드포인트
ENDPOINTS = {
    "posts": "/posts",
    "stats": "/stats",
    "agent_posts": "/agents/{agent_id}/posts",
    "agent_comments": "/agents/{agent_id}/comments",
    "post_comments": "/posts/{post_id}/comments",  # 인증 필요
    "submadangs": "/submadangs",  # 인증 필요
}

# 수집 기본값
DEFAULT_PAGE_SIZE = 50
MAX_RETRIES = 3
RETRY_DELAY = 5.0  # 초

# 데이터 경로
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
SAMPLES_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "samples")
