"""
필터링 UI 컴포넌트
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_date_filter(df):
    """
    날짜 범위 필터

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        tuple: (start_date, end_date)
    """
    if df.empty or '발행 일자' not in df.columns:
        return None, None

    min_date = df['발행 일자'].min()
    max_date = df['발행 일자'].max()

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "시작 날짜",
            value=min_date,
            min_value=min_date,
            max_value=max_date
        )

    with col2:
        end_date = st.date_input(
            "종료 날짜",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )

    return start_date, end_date


def render_multiselect_filters(df):
    """
    다중 선택 필터

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        tuple: (selected_channels, selected_topics, selected_events)
    """
    if df.empty:
        return [], [], []

    col1, col2, col3 = st.columns(3)

    with col1:
        if '배포 방식' in df.columns:
            channels = sorted(df['배포 방식'].unique().tolist())
            selected_channels = st.multiselect(
                "배포 방식",
                options=channels,
                default=channels
            )
        else:
            selected_channels = []

    with col2:
        if '주제 분류' in df.columns:
            topics = sorted(df['주제 분류'].unique().tolist())
            selected_topics = st.multiselect(
                "주제 분류",
                options=topics,
                default=topics
            )
        else:
            selected_topics = []

    with col3:
        if '이벤트 유무' in df.columns:
            events = sorted(df['이벤트 유무'].unique().tolist())
            selected_events = st.multiselect(
                "이벤트 유무",
                options=events,
                default=events
            )
        else:
            selected_events = []

    return selected_channels, selected_topics, selected_events


def render_content_type_filter(df):
    """
    콘텐츠 분류 필터

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        list: 선택된 콘텐츠 분류
    """
    if df.empty or '콘텐츠 분류' not in df.columns:
        return []

    content_types = sorted(df['콘텐츠 분류'].unique().tolist())
    selected = st.multiselect(
        "콘텐츠 분류",
        options=content_types,
        default=content_types
    )

    return selected


def apply_filters(df, start_date=None, end_date=None, channels=None, topics=None, events=None, content_types=None):
    """
    필터 적용

    Args:
        df (pd.DataFrame): 원본 데이터프레임
        start_date: 시작 날짜
        end_date: 종료 날짜
        channels (list): 배포 방식 필터
        topics (list): 주제 분류 필터
        events (list): 이벤트 유무 필터
        content_types (list): 콘텐츠 분류 필터

    Returns:
        pd.DataFrame: 필터링된 데이터프레임
    """
    if df.empty:
        return df

    filtered = df.copy()

    # 날짜 필터
    if start_date and end_date and '발행 일자' in filtered.columns:
        filtered = filtered[
            (filtered['발행 일자'] >= pd.to_datetime(start_date)) &
            (filtered['발행 일자'] <= pd.to_datetime(end_date))
        ]

    # 배포 방식 필터
    if channels and '배포 방식' in filtered.columns:
        filtered = filtered[filtered['배포 방식'].isin(channels)]

    # 주제 분류 필터
    if topics and '주제 분류' in filtered.columns:
        filtered = filtered[filtered['주제 분류'].isin(topics)]

    # 이벤트 유무 필터
    if events and '이벤트 유무' in filtered.columns:
        filtered = filtered[filtered['이벤트 유무'].isin(events)]

    # 콘텐츠 분류 필터
    if content_types and '콘텐츠 분류' in filtered.columns:
        filtered = filtered[filtered['콘텐츠 분류'].isin(content_types)]

    return filtered


def render_metric_filter(metric_options):
    """
    지표 선택 필터

    Args:
        metric_options (list): 지표 옵션 리스트

    Returns:
        str: 선택된 지표
    """
    selected_metric = st.selectbox(
        "분석 지표 선택",
        options=metric_options,
        index=0
    )

    return selected_metric


def render_quick_filters():
    """
    빠른 필터 (기간 프리셋)

    Returns:
        tuple: (start_date, end_date) 또는 None
    """
    quick_filter = st.radio(
        "빠른 필터",
        options=["전체", "최근 1개월", "최근 3개월", "최근 6개월", "최근 1년", "사용자 지정"],
        horizontal=True,
        index=0
    )

    today = datetime.today()

    if quick_filter == "전체":
        return None, None
    elif quick_filter == "최근 1개월":
        return today - timedelta(days=30), today
    elif quick_filter == "최근 3개월":
        return today - timedelta(days=90), today
    elif quick_filter == "최근 6개월":
        return today - timedelta(days=180), today
    elif quick_filter == "최근 1년":
        return today - timedelta(days=365), today
    else:  # 사용자 지정
        return "custom", "custom"
