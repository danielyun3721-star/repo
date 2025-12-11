"""
설정 파일
"""
import os

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'raw_data.txt')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# 컬럼 매핑 (원본 → 사용)
COLUMN_MAPPING = {
    '발행 일자': '발행_일자',
    '콘텐츠 분류': '콘텐츠_분류',
    '배포 방식': '배포_방식',
    '대상': '대상',
    '주제 분류': '주제_분류',
    '제목': '제목',
    '담당자': '담당자',
    '콘텐츠 링크': '콘텐츠_링크',
    '이벤트 유무': '이벤트_유무',
    '조회수': '조회수',
    '댓글수': '댓글수',
    '좋아요수': '좋아요수',
    '댓글 리스트': '댓글_리스트',
    'AI포털 방문자수': 'AI포털_방문자수'
}

# 역방향 매핑 (사용 → 원본) - Excel 저장 시 사용
REVERSE_COLUMN_MAPPING = {v: k for k, v in COLUMN_MAPPING.items()}

# 선택 옵션 (실제 데이터 확인 후 업데이트 가능)
CONTENT_TYPES = ['공지', '뉴스레터', '블로그', '동영상', '인포그래픽', '기타']
DISTRIBUTION_CHANNELS = ['이메일', '인트라넷', 'MS Teams', 'Slack', '기타']
TOPIC_CATEGORIES = ['HR', 'IT', '마케팅', '재무', '일반', '기타']

# 차트 색상 팔레트
COLOR_PALETTE = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'tertiary': '#2ca02c',
    'quaternary': '#d62728',
    'quinary': '#9467bd',
    'senary': '#8c564b',
    'septenary': '#e377c2',
    'octonary': '#7f7f7f'
}

# 기타 설정
CACHE_TTL = 3600  # 캐시 TTL: 1시간 (초 단위)
