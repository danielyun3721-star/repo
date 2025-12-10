"""
채널 효율성 분석 모듈
"""
import pandas as pd


def calculate_channel_efficiency(df):
    """
    배포 방식별 효율성 분석

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 배포 방식별 효율성 지표
    """
    if df.empty or '배포 방식' not in df.columns:
        return pd.DataFrame()

    efficiency = df.groupby('배포 방식').agg({
        '조회수': ['mean', 'sum', 'count'],
        '댓글수': ['mean', 'sum'],
        '좋아요수': ['mean', 'sum']
    }).reset_index()

    # 컬럼명 정리
    efficiency.columns = [
        '배포_방식',
        '평균_조회수', '총_조회수', '게시물_수',
        '평균_댓글수', '총_댓글수',
        '평균_좋아요수', '총_좋아요수'
    ]

    # 댓글 전환율 계산
    efficiency['댓글_전환율'] = (efficiency['평균_댓글수'] / efficiency['평균_조회수'] * 100).fillna(0)

    # 참여율 계산
    efficiency['참여율'] = ((efficiency['평균_댓글수'] + efficiency['평균_좋아요수']) / efficiency['평균_조회수'] * 100).fillna(0)

    # 내림차순 정렬 (평균 조회수 기준)
    efficiency = efficiency.sort_values('평균_조회수', ascending=False)

    return efficiency


def calculate_topic_performance(df):
    """
    주제별 성과 분석

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 주제별 성과 지표
    """
    if df.empty or '주제 분류' not in df.columns:
        return pd.DataFrame()

    topic_perf = df.groupby('주제 분류').agg({
        '조회수': ['mean', 'sum', 'median', 'count'],
        '댓글수': ['mean', 'sum'],
        '좋아요수': ['mean', 'sum']
    }).reset_index()

    # 컬럼명 정리
    topic_perf.columns = [
        '주제_분류',
        '평균_조회수', '총_조회수', '중앙값_조회수', '게시물_수',
        '평균_댓글수', '총_댓글수',
        '평균_좋아요수', '총_좋아요수'
    ]

    # 내림차순 정렬
    topic_perf = topic_perf.sort_values('총_조회수', ascending=False)

    return topic_perf


def calculate_content_type_performance(df):
    """
    콘텐츠 분류별 성과 분석

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 콘텐츠 분류별 성과 지표
    """
    if df.empty or '콘텐츠 분류' not in df.columns:
        return pd.DataFrame()

    content_perf = df.groupby('콘텐츠 분류').agg({
        '조회수': ['mean', 'sum', 'count'],
        '댓글수': ['mean', 'sum'],
        '좋아요수': ['mean', 'sum']
    }).reset_index()

    # 컬럼명 정리
    content_perf.columns = [
        '콘텐츠_분류',
        '평균_조회수', '총_조회수', '게시물_수',
        '평균_댓글수', '총_댓글수',
        '평균_좋아요수', '총_좋아요수'
    ]

    # 참여율 계산
    content_perf['참여율'] = (
        (content_perf['평균_댓글수'] + content_perf['평균_좋아요수']) /
        content_perf['평균_조회수'] * 100
    ).fillna(0)

    # 내림차순 정렬
    content_perf = content_perf.sort_values('총_조회수', ascending=False)

    return content_perf


def calculate_event_impact(df):
    """
    이벤트 유무별 영향 분석

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: 이벤트 유무별 성과 비교
    """
    if df.empty or '이벤트 유무' not in df.columns:
        return pd.DataFrame()

    event_impact = df.groupby('이벤트 유무').agg({
        '조회수': ['mean', 'median', 'count'],
        '댓글수': 'mean',
        '좋아요수': 'mean'
    }).reset_index()

    # 컬럼명 정리
    event_impact.columns = [
        '이벤트_유무',
        '평균_조회수', '중앙값_조회수', '게시물_수',
        '평균_댓글수',
        '평균_좋아요수'
    ]

    return event_impact
