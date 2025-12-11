"""
데이터 검증 모듈
"""
from datetime import datetime, date


def validate_input(data):
    """
    입력 데이터 유효성 검증

    Args:
        data (dict): 입력 데이터

    Returns:
        tuple: (is_valid, error_message)
    """
    # 필수 필드 확인
    required_fields = ['발행 일자', '콘텐츠 분류', '배포 방식', '주제 분류', '제목', '이벤트 유무']

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"필수 항목이 누락되었습니다: {field}"

    # 제목 길이 확인
    if len(str(data.get('제목', ''))) < 2:
        return False, "제목은 최소 2자 이상이어야 합니다"

    # 숫자 필드 검증
    numeric_fields = ['조회수', '댓글수', '좋아요수', 'AI포털 방문자수']
    for field in numeric_fields:
        if field in data:
            try:
                value = int(data[field])
                if value < 0:
                    return False, f"{field}는 0 이상이어야 합니다"
            except (ValueError, TypeError):
                return False, f"{field}는 숫자여야 합니다"

    # 날짜 검증
    if '발행 일자' in data:
        발행_일자 = data['발행 일자']
        if isinstance(발행_일자, str):
            try:
                # 두 가지 형식 모두 지원: 'YYYY-MM-DD' 또는 'YYYY-MM-DD HH:MM:SS'
                if len(발행_일자) == 10:  # 'YYYY-MM-DD'
                    발행_일자 = datetime.strptime(발행_일자, '%Y-%m-%d').date()
                else:  # 'YYYY-MM-DD HH:MM:SS'
                    발행_일자 = datetime.strptime(발행_일자, '%Y-%m-%d %H:%M:%S').date()
            except ValueError:
                return False, "발행 일자 형식이 올바르지 않습니다"

        if isinstance(발행_일자, (datetime, date)):
            # 미래 날짜 확인
            if 발행_일자 > date.today():
                return False, "발행 일자는 미래 날짜일 수 없습니다"

    # URL 형식 검증 (선택사항)
    if data.get('콘텐츠 링크'):
        url = data['콘텐츠 링크']
        if not url.startswith(('http://', 'https://')):
            # 경고만 표시, 검증 실패는 아님
            pass

    return True, ""


def validate_date_range(start_date, end_date):
    """
    날짜 범위 유효성 검증

    Args:
        start_date: 시작 날짜
        end_date: 종료 날짜

    Returns:
        tuple: (is_valid, error_message)
    """
    if not start_date or not end_date:
        return False, "날짜를 선택해주세요"

    if start_date > end_date:
        return False, "시작 날짜는 종료 날짜보다 이전이어야 합니다"

    return True, ""


def validate_file_upload(file):
    """
    업로드 파일 유효성 검증

    Args:
        file: 업로드된 파일 객체

    Returns:
        tuple: (is_valid, error_message)
    """
    if file is None:
        return False, "파일이 업로드되지 않았습니다"

    # 파일 확장자 검증
    allowed_extensions = ['.xlsx', '.xls', '.csv']
    file_extension = file.name.split('.')[-1].lower()

    if f".{file_extension}" not in allowed_extensions:
        return False, f"지원하지 않는 파일 형식입니다. 허용: {', '.join(allowed_extensions)}"

    # 파일 크기 검증 (예: 10MB)
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if hasattr(file, 'size') and file.size > max_size:
        return False, "파일 크기는 10MB 이하여야 합니다"

    return True, ""


def sanitize_input(text):
    """
    입력 텍스트 정제

    Args:
        text (str): 입력 텍스트

    Returns:
        str: 정제된 텍스트
    """
    if not text:
        return ""

    # 앞뒤 공백 제거
    text = text.strip()

    # 여러 공백을 하나로
    text = ' '.join(text.split())

    return text
