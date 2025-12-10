"""
차트 생성 모듈
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import config


def create_monthly_trend_chart(monthly_data):
    """
    월별 트렌드 라인차트

    Args:
        monthly_data (pd.DataFrame): 월별 집계 데이터

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if monthly_data.empty:
        return go.Figure()

    fig = go.Figure()

    # 조회수
    fig.add_trace(go.Scatter(
        x=monthly_data['월'],
        y=monthly_data['조회수'],
        name='조회수',
        line=dict(color=config.COLOR_PALETTE['primary'], width=3),
        mode='lines+markers'
    ))

    # 댓글수
    fig.add_trace(go.Scatter(
        x=monthly_data['월'],
        y=monthly_data['댓글수'],
        name='댓글수',
        line=dict(color=config.COLOR_PALETTE['secondary'], width=3),
        mode='lines+markers'
    ))

    # 좋아요수
    fig.add_trace(go.Scatter(
        x=monthly_data['월'],
        y=monthly_data['좋아요수'],
        name='좋아요수',
        line=dict(color=config.COLOR_PALETTE['tertiary'], width=3),
        mode='lines+markers'
    ))

    fig.update_layout(
        title='월별 참여도 추이',
        xaxis_title='월',
        yaxis_title='건수',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_efficiency_scatter(df, color_discrete_sequence=None):
    """
    Views vs Comments 스캐터플롯 (채널 효율성)

    Args:
        df (pd.DataFrame): 데이터프레임
        color_discrete_sequence (list, optional): 색상 팔레트

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x='조회수',
        y='댓글수',
        color='배포 방식' if '배포 방식' in df.columns else None,
        size='좋아요수' if '좋아요수' in df.columns else None,
        hover_data=['제목', '주제 분류'] if '제목' in df.columns else None,
        title='채널 효율성: 조회수 vs 댓글수',
        labels={'조회수': '조회수', '댓글수': '댓글수'},
        color_discrete_sequence=color_discrete_sequence
    )

    fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='white')))
    fig.update_layout(
        template='plotly_white',
        height=700  # 높이 증가
    )

    # Y축 범위 조정 (0부터 시작)
    if '댓글수' in df.columns:
        fig.update_yaxes(range=[0, df['댓글수'].max() * 1.1])

    return fig


def create_topic_distribution_box(df, color_discrete_sequence=None):
    """
    주제별 조회수 분포 박스플롯

    Args:
        df (pd.DataFrame): 데이터프레임
        color_discrete_sequence (list, optional): 색상 팔레트

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty or '주제 분류' not in df.columns:
        return go.Figure()

    fig = px.box(
        df,
        x='주제 분류',
        y='조회수',
        color='주제 분류',
        title='주제별 조회수 분포',
        labels={'주제 분류': '주제', '조회수': '조회수'},
        color_discrete_sequence=color_discrete_sequence
    )

    fig.update_layout(
        showlegend=False,
        template='plotly_white'
    )

    return fig


def create_impact_matrix(df, color_by='콘텐츠 분류'):
    """
    Z-Score 기반 Impact Matrix

    Args:
        df (pd.DataFrame): Z-Score가 포함된 데이터프레임
        color_by (str): 색상 구분 기준 컬럼명

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty or '조회수_zscore' not in df.columns:
        return go.Figure()

    # 색상 매핑 (사분면인 경우만 특수 색상)
    if color_by == '사분면':
        color_discrete_map = {
            '높은 영향력': '#2ca02c',
            '높은 도달, 낮은 참여': '#1f77b4',
            '낮은 도달, 높은 참여': '#ff7f0e',
            '낮은 영향력': '#d62728'
        }
    else:
        color_discrete_map = None  # Plotly 기본 색상 사용

    fig = px.scatter(
        df,
        x='조회수_zscore',
        y='댓글수_zscore',
        color=color_by if color_by in df.columns or color_by == '사분면' else 'quadrant',
        hover_data=['제목', '배포 방식', '주제 분류', '콘텐츠 분류'] if '제목' in df.columns else None,
        title=f'Impact Matrix (색상: {color_by})',
        labels={
            '조회수_zscore': '조회수 (Z-Score)',
            '댓글수_zscore': '댓글수 (Z-Score)'
        },
        color_discrete_map=color_discrete_map
    )

    # 기준선 추가
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)

    fig.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color='white')))
    fig.update_layout(
        template='plotly_white',
        height=700  # 높이 증가
    )

    return fig


def create_bar_chart(df, x_col, y_col, title, color_col=None, color_discrete_sequence=None):
    """
    범용 막대 차트

    Args:
        df (pd.DataFrame): 데이터프레임
        x_col (str): X축 컬럼
        y_col (str): Y축 컬럼
        title (str): 차트 제목
        color_col (str, optional): 색상 구분 컬럼
        color_discrete_sequence (list, optional): 색상 팔레트

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty:
        return go.Figure()

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        text=y_col,
        color_discrete_sequence=color_discrete_sequence
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        template='plotly_white',
        showlegend=True if color_col else False
    )

    return fig


def create_pie_chart(df, names_col, values_col, title):
    """
    파이 차트

    Args:
        df (pd.DataFrame): 데이터프레임
        names_col (str): 라벨 컬럼
        values_col (str): 값 컬럼
        title (str): 차트 제목

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty:
        return go.Figure()

    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(template='plotly_white')

    return fig


def create_heatmap(df, x_col, y_col, z_col, title):
    """
    히트맵

    Args:
        df (pd.DataFrame): 데이터프레임
        x_col (str): X축 컬럼
        y_col (str): Y축 컬럼
        z_col (str): 값 컬럼
        title (str): 차트 제목

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty:
        return go.Figure()

    # 피벗 테이블 생성
    pivot_table = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='sum')

    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Blues',
        text=pivot_table.values,
        texttemplate='%{text:.0f}',
        textfont={"size": 10}
    ))

    fig.update_layout(
        title=title,
        template='plotly_white'
    )

    return fig


def create_line_chart_with_markers(df, x_col, y_cols, title):
    """
    여러 라인을 가진 라인 차트

    Args:
        df (pd.DataFrame): 데이터프레임
        x_col (str): X축 컬럼
        y_cols (list): Y축 컬럼 리스트
        title (str): 차트 제목

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty:
        return go.Figure()

    fig = go.Figure()

    colors = list(config.COLOR_PALETTE.values())

    for idx, y_col in enumerate(y_cols):
        if y_col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[y_col],
                name=y_col,
                line=dict(color=colors[idx % len(colors)], width=2),
                mode='lines+markers'
            ))

    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title='값',
        hovermode='x unified',
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def create_time_series_area_chart(df, x_col, y_col, title):
    """
    시계열 영역 차트 (라인 + 영역)

    Args:
        df (pd.DataFrame): 데이터프레임
        x_col (str): X축 컬럼 (월)
        y_col (str): Y축 컬럼 (조회수, 댓글수 등)
        title (str): 차트 제목

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if df.empty or y_col not in df.columns:
        return go.Figure()

    fig = go.Figure()

    # 영역 차트
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        name=y_col,
        fill='tozeroy',
        line=dict(color=config.COLOR_PALETTE['primary'], width=2),
        fillcolor='rgba(31, 119, 180, 0.3)',
        mode='lines+markers'
    ))

    # 최고/최저 표시
    max_idx = df[y_col].idxmax()
    min_idx = df[y_col].idxmin()

    fig.add_annotation(
        x=df.loc[max_idx, x_col],
        y=df.loc[max_idx, y_col],
        text=f"최고: {df.loc[max_idx, y_col]:,.0f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="green",
        bgcolor="lightgreen",
        opacity=0.8
    )

    fig.add_annotation(
        x=df.loc[min_idx, x_col],
        y=df.loc[min_idx, y_col],
        text=f"최저: {df.loc[min_idx, y_col]:,.0f}",
        showarrow=True,
        arrowhead=2,
        arrowcolor="red",
        bgcolor="lightcoral",
        opacity=0.8
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title=y_col,
        hovermode='x unified',
        template='plotly_white',
        showlegend=False
    )

    return fig


def create_benchmark_position_chart(historical_df, selected_value, metric, title):
    """
    벤치마킹 위치 차트 (히스토그램 + 현재 위치)

    Args:
        historical_df (pd.DataFrame): 과거 전체 데이터
        selected_value (float): 선택된 게시물의 값
        metric (str): 지표명 (조회수, 댓글수 등)
        title (str): 차트 제목

    Returns:
        go.Figure: Plotly 차트 객체
    """
    if historical_df.empty or metric not in historical_df.columns:
        return go.Figure()

    fig = go.Figure()

    # 히스토그램 (전체 데이터 분포)
    fig.add_trace(go.Histogram(
        x=historical_df[metric],
        name='전체 데이터 분포',
        marker_color='lightblue',
        opacity=0.7,
        nbinsx=30
    ))

    # 현재 게시물 위치 (수직선)
    fig.add_vline(
        x=selected_value,
        line_dash="dash",
        line_color="red",
        line_width=3,
        annotation_text=f"현재 게시물: {selected_value:,}",
        annotation_position="top"
    )

    # 백분위수 선들 (25th, 50th, 75th)
    p25 = historical_df[metric].quantile(0.25)
    p50 = historical_df[metric].quantile(0.50)
    p75 = historical_df[metric].quantile(0.75)

    fig.add_vline(x=p25, line_dash="dot", line_color="gray", opacity=0.5,
                  annotation_text="25%", annotation_position="bottom left")
    fig.add_vline(x=p50, line_dash="dot", line_color="gray", opacity=0.5,
                  annotation_text="50%", annotation_position="bottom left")
    fig.add_vline(x=p75, line_dash="dot", line_color="gray", opacity=0.5,
                  annotation_text="75%", annotation_position="bottom left")

    fig.update_layout(
        title=title,
        xaxis_title=metric,
        yaxis_title='빈도',
        template='plotly_white',
        height=400,
        showlegend=True
    )

    return fig
