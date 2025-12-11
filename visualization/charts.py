"""
차트 생성 모듈 - Matplotlib/Seaborn 버전
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import config


def create_monthly_trend_chart(monthly_data):
    """
    월별 트렌드 라인차트

    Args:
        monthly_data (pd.DataFrame): 월별 집계 데이터

    Returns:
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if monthly_data.empty:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))

    # 라인 플롯
    ax.plot(monthly_data['월'], monthly_data['조회수'],
            marker='o', linewidth=2.5, label='조회수',
            color=config.COLOR_PALETTE['primary'], markersize=8)
    ax.plot(monthly_data['월'], monthly_data['댓글수'],
            marker='s', linewidth=2.5, label='댓글수',
            color=config.COLOR_PALETTE['secondary'], markersize=8)
    ax.plot(monthly_data['월'], monthly_data['좋아요수'],
            marker='^', linewidth=2.5, label='좋아요수',
            color=config.COLOR_PALETTE['tertiary'], markersize=8)

    # 스타일링
    ax.set_title('월별 참여도 추이', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('월', fontsize=11)
    ax.set_ylabel('건수', fontsize=11)
    ax.legend(loc='upper left', ncol=3, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)

    # X축 라벨 회전
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig


def create_efficiency_scatter(df, color_discrete_sequence=None):
    """
    Views vs Comments 스캐터플롯 (채널 효율성)

    Args:
        df (pd.DataFrame): 데이터프레임
        color_discrete_sequence (list, optional): 색상 팔레트

    Returns:
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 8))

    # 색상 팔레트 설정
    if color_discrete_sequence:
        colors = color_discrete_sequence
    else:
        colors = sns.color_palette('Set2', n_colors=len(df['배포 방식'].unique()))

    # 배포 방식별로 그룹화하여 플롯
    for idx, (channel, group) in enumerate(df.groupby('배포 방식')):
        scatter = ax.scatter(
            group['조회수'],
            group['댓글수'],
            s=group['좋아요수'] * 10 if '좋아요수' in group.columns else 100,  # 버블 크기 조정
            alpha=0.7,
            color=colors[idx % len(colors)],
            edgecolors='white',
            linewidth=1,
            label=channel
        )

    ax.set_title('채널 효율성: 조회수 vs 댓글수', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('조회수', fontsize=11)
    ax.set_ylabel('댓글수', fontsize=11)
    ax.legend(title='배포 방식', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)

    # Y축 0부터 시작
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    return fig


def create_topic_distribution_box(df, color_discrete_sequence=None):
    """
    주제별 조회수 분포 박스플롯

    Args:
        df (pd.DataFrame): 데이터프레임
        color_discrete_sequence (list, optional): 색상 팔레트

    Returns:
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty or '주제 분류' not in df.columns:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))

    # Seaborn boxplot
    sns.boxplot(
        data=df,
        x='주제 분류',
        y='조회수',
        palette=color_discrete_sequence if color_discrete_sequence else 'Set2',
        ax=ax
    )

    ax.set_title('주제별 조회수 분포', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('주제', fontsize=11)
    ax.set_ylabel('조회수', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


def create_impact_matrix(df, color_by='콘텐츠 분류'):
    """
    Z-Score 기반 Impact Matrix

    Args:
        df (pd.DataFrame): Z-Score가 포함된 데이터프레임
        color_by (str): 색상 구분 기준 컬럼명

    Returns:
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty or '조회수_zscore' not in df.columns:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 8))

    # 색상 매핑 (사분면인 경우만 특수 색상)
    if color_by == '사분면':
        color_map = {
            '높은 영향력': '#2ca02c',
            '높은 도달, 낮은 참여': '#1f77b4',
            '낮은 도달, 높은 참여': '#ff7f0e',
            '낮은 영향력': '#d62728'
        }
        for quadrant, color in color_map.items():
            mask = df['quadrant'] == quadrant
            if mask.any():
                ax.scatter(
                    df.loc[mask, '조회수_zscore'],
                    df.loc[mask, '댓글수_zscore'],
                    c=color,
                    label=quadrant,
                    alpha=0.7,
                    s=100,
                    edgecolors='white',
                    linewidth=1
                )
    else:
        # 다른 컬럼으로 색상 구분
        if color_by in df.columns:
            categories = df[color_by].unique()
            colors = sns.color_palette('Set2', n_colors=len(categories))
            for idx, category in enumerate(categories):
                mask = df[color_by] == category
                if mask.any():
                    ax.scatter(
                        df.loc[mask, '조회수_zscore'],
                        df.loc[mask, '댓글수_zscore'],
                        c=[colors[idx]],
                        label=category,
                        alpha=0.7,
                        s=100,
                        edgecolors='white',
                        linewidth=1
                    )

    # 기준선 추가
    ax.axhline(y=0, linestyle='--', color='gray', alpha=0.5, linewidth=1.5)
    ax.axvline(x=0, linestyle='--', color='gray', alpha=0.5, linewidth=1.5)

    ax.set_title(f'Impact Matrix (색상: {color_by})', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('조회수 (Z-Score)', fontsize=11)
    ax.set_ylabel('댓글수 (Z-Score)', fontsize=11)
    ax.legend(title=color_by, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(10, 6))

    if color_col and color_col in df.columns:
        # 색상 구분이 있는 경우
        categories = df[color_col].unique()
        colors = color_discrete_sequence if color_discrete_sequence else sns.color_palette('Set2', n_colors=len(categories))

        # 그룹별로 막대 그리기
        x_positions = range(len(df))
        for idx, category in enumerate(categories):
            mask = df[color_col] == category
            if mask.any():
                ax.bar(
                    [x for x, m in zip(x_positions, mask) if m],
                    df.loc[mask, y_col],
                    color=colors[idx % len(colors)],
                    label=category,
                    alpha=0.8
                )
    else:
        # 단일 색상
        bars = ax.bar(range(len(df)), df[y_col], color=config.COLOR_PALETTE['primary'], alpha=0.8)

    # 값 레이블 추가
    for idx, row in df.iterrows():
        value = row[y_col]
        x_pos = list(df.index).index(idx) if idx in df.index else idx
        # 값이 숫자인 경우에만 표시
        if pd.notna(value):
            ax.text(x_pos, value, f'{value:.0f}',
                    ha='center', va='bottom', fontsize=9)

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel(y_col, fontsize=11)

    # X축 레이블 설정
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df[x_col], rotation=45, ha='right')

    if color_col:
        ax.legend(frameon=True, shadow=True)

    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(8, 8))

    colors = sns.color_palette('Set2', n_colors=len(df))

    wedges, texts, autotexts = ax.pie(
        df[values_col],
        labels=df[names_col],
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 10}
    )

    # 퍼센트 텍스트 스타일
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    plt.tight_layout()
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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty:
        fig, ax = plt.subplots()
        return fig

    # 피벗 테이블 생성
    pivot_table = df.pivot_table(values=z_col, index=y_col, columns=x_col, aggfunc='sum')

    fig, ax = plt.subplots(figsize=(12, 8))

    sns.heatmap(
        pivot_table,
        cmap='Blues',
        annot=True,
        fmt='.0f',
        linewidths=0.5,
        cbar_kws={'label': z_col},
        ax=ax
    )

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel(y_col, fontsize=11)

    plt.tight_layout()
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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))

    colors = list(config.COLOR_PALETTE.values())
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p']

    for idx, y_col in enumerate(y_cols):
        if y_col in df.columns:
            ax.plot(
                df[x_col],
                df[y_col],
                marker=markers[idx % len(markers)],
                linewidth=2,
                label=y_col,
                color=colors[idx % len(colors)],
                markersize=8
            )

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel('값', fontsize=11)
    ax.legend(loc='upper left', ncol=3, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if df.empty or y_col not in df.columns:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 6))

    # 영역 차트
    ax.fill_between(
        range(len(df)),
        df[y_col],
        alpha=0.3,
        color=config.COLOR_PALETTE['primary']
    )
    ax.plot(
        range(len(df)),
        df[y_col],
        marker='o',
        linewidth=2,
        color=config.COLOR_PALETTE['primary'],
        markersize=8
    )

    # 최고/최저 주석
    max_idx = df[y_col].idxmax()
    min_idx = df[y_col].idxmin()

    max_x_pos = list(df.index).index(max_idx)
    max_y = df.loc[max_idx, y_col]
    min_x_pos = list(df.index).index(min_idx)
    min_y = df.loc[min_idx, y_col]

    # 최고점 주석
    ax.annotate(
        f'최고: {max_y:,.0f}',
        xy=(max_x_pos, max_y),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.8),
        arrowprops=dict(arrowstyle='->', color='green', lw=1.5)
    )

    # 최저점 주석
    ax.annotate(
        f'최저: {min_y:,.0f}',
        xy=(min_x_pos, min_y),
        xytext=(10, -20),
        textcoords='offset points',
        fontsize=10,
        bbox=dict(boxstyle='round,pad=0.5', fc='lightcoral', alpha=0.8),
        arrowprops=dict(arrowstyle='->', color='red', lw=1.5)
    )

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(x_col, fontsize=11)
    ax.set_ylabel(y_col, fontsize=11)
    ax.grid(True, alpha=0.3)

    # X축 레이블 설정
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df[x_col], rotation=45, ha='right')

    plt.tight_layout()
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
        matplotlib.figure.Figure: Matplotlib Figure 객체
    """
    if historical_df.empty or metric not in historical_df.columns:
        fig, ax = plt.subplots()
        return fig

    fig, ax = plt.subplots(figsize=(12, 5))

    # 히스토그램
    ax.hist(
        historical_df[metric],
        bins=30,
        color='lightblue',
        alpha=0.7,
        edgecolor='white',
        label='전체 데이터 분포'
    )

    # 현재 게시물 위치 (빨간 선)
    ax.axvline(
        selected_value,
        color='red',
        linestyle='--',
        linewidth=2.5,
        label=f'현재 게시물: {selected_value:,}'
    )

    # 백분위수 선들
    p25 = historical_df[metric].quantile(0.25)
    p50 = historical_df[metric].quantile(0.50)
    p75 = historical_df[metric].quantile(0.75)

    ax.axvline(p25, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.axvline(p50, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.axvline(p75, color='gray', linestyle=':', linewidth=1, alpha=0.7)

    # 백분위수 텍스트 주석
    y_max = ax.get_ylim()[1]
    ax.text(p25, y_max * 0.95, '25%', ha='center', fontsize=9, color='gray')
    ax.text(p50, y_max * 0.95, '50%', ha='center', fontsize=9, color='gray')
    ax.text(p75, y_max * 0.95, '75%', ha='center', fontsize=9, color='gray')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(metric, fontsize=11)
    ax.set_ylabel('빈도', fontsize=11)
    ax.legend(frameon=True, shadow=True)
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    return fig
