"""
트렌드 분석 모듈
"""
import pandas as pd


def calculate_monthly_engagement(df):
    """
    월별 참여 지표 집계

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 월별 집계 데이터
    """
    if df.empty or '년월' not in df.columns:
        return pd.DataFrame()

    monthly = df.groupby('년월').agg({
        '조회수': 'sum',
        '댓글수': 'sum',
        '좋아요수': 'sum',
        '제목': 'count'  # 게시물 수
    }).reset_index()

    monthly.columns = ['월', '조회수', '댓글수', '좋아요수', '게시물_수']

    # 월 컬럼을 문자열로 변환
    monthly['월'] = monthly['월'].astype(str)

    # 총 참여수 계산
    monthly['총_참여수'] = monthly['댓글수'] + monthly['좋아요수']

    # 게시물당 평균 지표
    monthly['평균_조회수'] = monthly['조회수'] / monthly['게시물_수']
    monthly['평균_댓글수'] = monthly['댓글수'] / monthly['게시물_수']
    monthly['평균_좋아요수'] = monthly['좋아요수'] / monthly['게시물_수']

    return monthly


def calculate_quarterly_engagement(df):
    """
    분기별 참여 지표 집계

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 분기별 집계 데이터
    """
    if df.empty or '분기' not in df.columns:
        return pd.DataFrame()

    quarterly = df.groupby('분기').agg({
        '조회수': 'sum',
        '댓글수': 'sum',
        '좋아요수': 'sum',
        '제목': 'count'
    }).reset_index()

    quarterly.columns = ['분기', '조회수', '댓글수', '좋아요수', '게시물_수']

    # 분기 컬럼을 문자열로 변환
    quarterly['분기'] = quarterly['분기'].astype(str)

    # 총 참여수 계산
    quarterly['총_참여수'] = quarterly['댓글수'] + quarterly['좋아요수']

    return quarterly


def calculate_growth_rate(df, period='월'):
    """
    기간별 성장률 계산

    Args:
        df (pd.DataFrame): 시계열 데이터프레임
        period (str): 기간 타입 ('월' 또는 '분기')

    Returns:
        pd.DataFrame: 성장률이 추가된 데이터프레임
    """
    if df.empty:
        return df

    df = df.copy()

    # 조회수 성장률
    df['조회수_성장률'] = df['조회수'].pct_change() * 100

    # 댓글수 성장률
    df['댓글수_성장률'] = df['댓글수'].pct_change() * 100

    # 좋아요수 성장률
    df['좋아요수_성장률'] = df['좋아요수'].pct_change() * 100

    # 무한값과 NaN 처리
    df = df.replace([float('inf'), float('-inf')], 0)
    df = df.fillna(0)

    return df


def calculate_moving_average(df, column, window=3):
    """
    이동 평균 계산

    Args:
        df (pd.DataFrame): 데이터프레임
        column (str): 계산할 컬럼명
        window (int): 윈도우 크기

    Returns:
        pd.Series: 이동 평균 시리즈
    """
    if df.empty or column not in df.columns:
        return pd.Series()

    return df[column].rolling(window=window, min_periods=1).mean()
