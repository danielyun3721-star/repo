"""
벤치마킹 및 비교 분석 모듈
"""
import pandas as pd
import numpy as np
from scipy.stats import zscore, percentileofscore


def calculate_zscore_matrix(df):
    """
    Z-Score로 정규화한 Impact Matrix 생성

    Args:
        df (pd.DataFrame): 데이터프레임

    Returns:
        pd.DataFrame: Z-Score가 추가된 데이터프레임
    """
    if df.empty or '조회수' not in df.columns or '댓글수' not in df.columns:
        return df

    df = df.copy()

    # Z-Score 계산 (0이 아닌 값들만 사용)
    views_data = df[df['조회수'] > 0]['조회수']
    comments_data = df[df['댓글수'] >= 0]['댓글수']

    if len(views_data) > 1:
        df['조회수_zscore'] = zscore(df['조회수'])
    else:
        df['조회수_zscore'] = 0

    if len(comments_data) > 1:
        df['댓글수_zscore'] = zscore(df['댓글수'])
    else:
        df['댓글수_zscore'] = 0

    # NaN, Inf 처리
    df['조회수_zscore'] = df['조회수_zscore'].replace([np.inf, -np.inf], 0).fillna(0)
    df['댓글수_zscore'] = df['댓글수_zscore'].replace([np.inf, -np.inf], 0).fillna(0)

    # Impact Score 계산 (Z-score 평균)
    df['impact_score'] = (df['조회수_zscore'] + df['댓글수_zscore']) / 2

    # 사분면 분류
    def classify_quadrant(row):
        if row['조회수_zscore'] > 0 and row['댓글수_zscore'] > 0:
            return '높은 영향력'
        elif row['조회수_zscore'] > 0 and row['댓글수_zscore'] <= 0:
            return '높은 도달, 낮은 참여'
        elif row['조회수_zscore'] <= 0 and row['댓글수_zscore'] > 0:
            return '낮은 도달, 높은 참여'
        else:
            return '낮은 영향력'

    df['quadrant'] = df.apply(classify_quadrant, axis=1)

    return df


def benchmark_against_history(new_data, historical_df, metric='조회수'):
    """
    신규 데이터를 과거 데이터 대비 벤치마킹

    Args:
        new_data (pd.Series or dict): 신규 데이터
        historical_df (pd.DataFrame): 과거 데이터
        metric (str): 비교할 지표

    Returns:
        dict: 벤치마킹 결과
    """
    if historical_df.empty or metric not in historical_df.columns:
        return {
            'metric': metric,
            'value': 0,
            'percentile': 0,
            'z_score': 0,
            'rank': 0,
            'total': 0,
            'category': '데이터 부족',
            'mean': 0,
            'median': 0,
            'std': 0
        }

    # 새 데이터 값 추출
    if isinstance(new_data, dict):
        value = new_data.get(metric, 0)
    else:
        value = new_data[metric] if metric in new_data.index else 0

    # 통계 계산
    mean = historical_df[metric].mean()
    median = historical_df[metric].median()
    std = historical_df[metric].std()

    # 백분위수 계산
    percentile = percentileofscore(historical_df[metric], value, kind='rank')

    # Z-Score 계산
    z_score = (value - mean) / std if std > 0 else 0

    # 순위 계산
    rank = (historical_df[metric] < value).sum() + 1
    total = len(historical_df) + 1

    # 카테고리 분류
    if percentile >= 90:
        category = "상위 10% (매우 우수)"
    elif percentile >= 75:
        category = "상위 25% (우수)"
    elif percentile >= 50:
        category = "상위 50% (평균 이상)"
    elif percentile >= 25:
        category = "하위 50% (평균 이하)"
    else:
        category = "하위 25% (개선 필요)"

    return {
        'metric': metric,
        'value': value,
        'percentile': percentile,
        'z_score': z_score,
        'rank': rank,
        'total': total,
        'category': category,
        'mean': mean,
        'median': median,
        'std': std
    }


def compare_period_performance(df, period_type='월'):
    """
    기간별 성과 비교

    Args:
        df (pd.DataFrame): 데이터프레임
        period_type (str): '월', '분기', '연도'

    Returns:
        pd.DataFrame: 기간별 비교 결과
    """
    if df.empty:
        return pd.DataFrame()

    # 기간 컬럼 선택
    if period_type == '월' and '년월' in df.columns:
        period_col = '년월'
    elif period_type == '분기' and '분기' in df.columns:
        period_col = '분기'
    elif period_type == '연도' and '연도' in df.columns:
        period_col = '연도'
    else:
        return pd.DataFrame()

    # 기간별 집계
    comparison = df.groupby(period_col).agg({
        '조회수': ['mean', 'sum', 'count'],
        '댓글수': ['mean', 'sum'],
        '좋아요수': ['mean', 'sum']
    }).reset_index()

    # 컬럼명 정리
    comparison.columns = [
        period_type,
        '평균_조회수', '총_조회수', '게시물_수',
        '평균_댓글수', '총_댓글수',
        '평균_좋아요수', '총_좋아요수'
    ]

    # 기간을 문자열로 변환
    comparison[period_type] = comparison[period_type].astype(str)

    return comparison


def identify_top_performers(df, metric='조회수', top_n=10):
    """
    상위 성과 게시물 식별

    Args:
        df (pd.DataFrame): 데이터프레임
        metric (str): 순위 기준 지표
        top_n (int): 상위 N개

    Returns:
        pd.DataFrame: 상위 성과 게시물
    """
    if df.empty or metric not in df.columns:
        return pd.DataFrame()

    # 지표 기준 내림차순 정렬
    top_df = df.nlargest(top_n, metric)

    # 필요한 컬럼만 선택
    columns_to_show = ['제목', '발행 일자', metric]
    if '배포 방식' in df.columns:
        columns_to_show.append('배포 방식')
    if '주제 분류' in df.columns:
        columns_to_show.append('주제 분류')
    if '댓글수' in df.columns and metric != '댓글수':
        columns_to_show.append('댓글수')
    if '좋아요수' in df.columns and metric != '좋아요수':
        columns_to_show.append('좋아요수')

    return top_df[columns_to_show].reset_index(drop=True)


def calculate_percentile_ranges(df, metric='조회수'):
    """
    백분위수 범위 계산

    Args:
        df (pd.DataFrame): 데이터프레임
        metric (str): 분석할 지표

    Returns:
        dict: 백분위수 범위
    """
    if df.empty or metric not in df.columns:
        return {}

    percentiles = [10, 25, 50, 75, 90, 95]
    ranges = {}

    for p in percentiles:
        ranges[f'p{p}'] = df[metric].quantile(p / 100)

    ranges['min'] = df[metric].min()
    ranges['max'] = df[metric].max()
    ranges['mean'] = df[metric].mean()
    ranges['median'] = df[metric].median()
    ranges['std'] = df[metric].std()

    return ranges
