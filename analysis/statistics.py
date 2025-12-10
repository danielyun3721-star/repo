"""
기본 통계 계산 모듈
"""
import pandas as pd


def calculate_basic_stats(df):
    """
    기본 통계 계산

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        dict: 기본 통계 딕셔너리
    """
    if df.empty:
        return {
            '전체_게시물_수': 0,
            '평균_조회수': 0,
            '평균_댓글수': 0,
            '평균_좋아요수': 0,
            '총_조회수': 0,
            '총_댓글수': 0,
            '총_좋아요수': 0,
            '중앙값_조회수': 0,
            '최고_조회수': 0,
            '최저_조회수': 0
        }

    stats = {
        '전체_게시물_수': len(df),
        '평균_조회수': df['조회수'].mean(),
        '평균_댓글수': df['댓글수'].mean(),
        '평균_좋아요수': df['좋아요수'].mean(),
        '총_조회수': df['조회수'].sum(),
        '총_댓글수': df['댓글수'].sum(),
        '총_좋아요수': df['좋아요수'].sum(),
        '중앙값_조회수': df['조회수'].median(),
        '최고_조회수': df['조회수'].max(),
        '최저_조회수': df['조회수'].min()
    }

    # AI포털 방문자수가 있는 경우
    if 'AI포털 방문자수' in df.columns:
        stats['평균_AI포털_방문자수'] = df['AI포털 방문자수'].mean()
        stats['총_AI포털_방문자수'] = df['AI포털 방문자수'].sum()

    # 참여율이 있는 경우
    if '참여율' in df.columns:
        stats['평균_참여율'] = df['참여율'].mean()

    return stats


def calculate_category_stats(df, category_column):
    """
    카테고리별 통계 계산

    Args:
        df (pd.DataFrame): 데이터프레임
        category_column (str): 카테고리 컬럼명

    Returns:
        pd.DataFrame: 카테고리별 통계
    """
    if df.empty or category_column not in df.columns:
        return pd.DataFrame()

    stats = df.groupby(category_column).agg({
        '조회수': ['count', 'sum', 'mean', 'median'],
        '댓글수': ['sum', 'mean'],
        '좋아요수': ['sum', 'mean']
    }).reset_index()

    # 컬럼명 정리
    stats.columns = [
        category_column,
        '게시물_수', '총_조회수', '평균_조회수', '중앙값_조회수',
        '총_댓글수', '평균_댓글수',
        '총_좋아요수', '평균_좋아요수'
    ]

    # 내림차순 정렬 (총 조회수 기준)
    stats = stats.sort_values('총_조회수', ascending=False)

    return stats


def calculate_time_series_stats(df, time_column='년월'):
    """
    시계열 통계 계산

    Args:
        df (pd.DataFrame): 데이터프레임
        time_column (str): 시간 컬럼명

    Returns:
        pd.DataFrame: 시계열 통계
    """
    if df.empty or time_column not in df.columns:
        return pd.DataFrame()

    stats = df.groupby(time_column).agg({
        '조회수': ['count', 'sum', 'mean'],
        '댓글수': ['sum', 'mean'],
        '좋아요수': ['sum', 'mean']
    }).reset_index()

    # 컬럼명 정리
    stats.columns = [
        time_column,
        '게시물_수', '총_조회수', '평균_조회수',
        '총_댓글수', '평균_댓글수',
        '총_좋아요수', '평균_좋아요수'
    ]

    return stats
