"""
데이터 전처리 모듈
"""
import pandas as pd
import numpy as np
import config


def preprocess_data(df):
    """
    데이터 전처리 및 파생 변수 생성

    Args:
        df (pd.DataFrame): 원본 데이터프레임

    Returns:
        pd.DataFrame: 전처리된 데이터프레임
    """
    if df.empty:
        return df

    # 데이터 복사
    df = df.copy()

    # 컬럼명 정규화 (옵션: 사용자가 원본 컬럼명 유지를 원할 수 있으므로 주석 처리)
    # df = df.rename(columns=config.COLUMN_MAPPING)

    # 날짜 파싱
    if '발행 일자' in df.columns:
        df['발행 일자'] = pd.to_datetime(df['발행 일자'], errors='coerce')

        # 파생 변수: 년월, 분기
        df['년월'] = df['발행 일자'].dt.to_period('M')
        df['분기'] = df['발행 일자'].dt.to_period('Q')
        df['연도'] = df['발행 일자'].dt.year
        df['월'] = df['발행 일자'].dt.month

    # 숫자형 변환
    numeric_cols = ['조회수', '댓글수', '좋아요수', 'AI포털 방문자수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 파생 변수 계산
    if '댓글수' in df.columns and '좋아요수' in df.columns:
        df['총_참여수'] = df['댓글수'] + df['좋아요수']

    if '조회수' in df.columns and '총_참여수' in df.columns:
        # 참여율 계산 (0으로 나누기 방지)
        df['참여율'] = df.apply(
            lambda row: (row['총_참여수'] / row['조회수'] * 100) if row['조회수'] > 0 else 0,
            axis=1
        )

    if '댓글수' in df.columns and '조회수' in df.columns:
        # 댓글 전환율
        df['댓글_전환율'] = df.apply(
            lambda row: (row['댓글수'] / row['조회수'] * 100) if row['조회수'] > 0 else 0,
            axis=1
        )

    # 결측값 처리
    text_cols = ['콘텐츠 분류', '배포 방식', '대상', '주제 분류', '제목', '담당자', '이벤트 유무']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna('미분류')

    return df
