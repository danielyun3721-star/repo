"""
유틸리티 함수 모듈
"""
import pandas as pd
from datetime import datetime


def format_number(number):
    """
    숫자를 천 단위 구분자로 포맷팅

    Args:
        number: 숫자

    Returns:
        str: 포맷팅된 문자열
    """
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return str(number)


def format_percentage(value, decimals=1):
    """
    백분율 포맷팅

    Args:
        value: 값
        decimals (int): 소수점 자리수

    Returns:
        str: 포맷팅된 백분율 문자열
    """
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return str(value)


def safe_divide(numerator, denominator, default=0):
    """
    안전한 나눗셈 (0으로 나누기 방지)

    Args:
        numerator: 분자
        denominator: 분모
        default: 분모가 0일 때 반환값

    Returns:
        float: 나눗셈 결과
    """
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (ValueError, TypeError, ZeroDivisionError):
        return default


def get_period_label(period):
    """
    기간 객체를 문자열 라벨로 변환

    Args:
        period: pd.Period 객체

    Returns:
        str: 기간 문자열
    """
    if pd.isna(period):
        return ""

    return str(period)


def calculate_days_diff(date1, date2):
    """
    두 날짜 간의 일수 차이 계산

    Args:
        date1: 첫 번째 날짜
        date2: 두 번째 날짜

    Returns:
        int: 일수 차이
    """
    try:
        if isinstance(date1, str):
            date1 = pd.to_datetime(date1)
        if isinstance(date2, str):
            date2 = pd.to_datetime(date2)

        delta = abs((date2 - date1).days)
        return delta
    except Exception:
        return 0


def get_unique_options(df, column, include_other=True):
    """
    데이터프레임에서 특정 컬럼의 고유값 추출

    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 컬럼명
        include_other (bool): '기타' 옵션 포함 여부

    Returns:
        list: 정렬된 고유값 리스트
    """
    if df.empty or column not in df.columns:
        return ['기타'] if include_other else []

    # 고유값 추출 (NaN 제외)
    unique_values = df[column].dropna().unique().tolist()

    # '미분류' 제외
    unique_values = [v for v in unique_values if v != '미분류']

    # 정렬
    unique_values = sorted(unique_values)

    # '기타' 추가
    if include_other and '기타' not in unique_values:
        unique_values.append('기타')

    return unique_values
