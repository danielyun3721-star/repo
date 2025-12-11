"""
비교 분석 및 벤치마킹 페이지
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import get_cached_data
from data.processor import preprocess_data
from analysis.benchmarking import (
    calculate_zscore_matrix, benchmark_against_history,
    compare_period_performance, identify_top_performers, calculate_percentile_ranges
)
from visualization.charts import create_impact_matrix, create_benchmark_position_chart
from components.filters import render_date_filter, render_multiselect_filters, apply_filters
import matplotlib.pyplot as plt

st.set_page_config(page_title="비교 분석", page_icon="🔍", layout="wide")

st.title("🔍 비교 분석 및 벤치마킹")
st.markdown("과거 데이터 대비 성과를 비교하고 벤치마킹합니다.")
st.markdown("---")

try:
    # 데이터 로딩
    data_info = get_cached_data()
    df = preprocess_data(data_info['data'])

    if df.empty:
        st.warning("데이터가 없습니다.")
        st.stop()

    # Z-Score Impact Matrix
    st.subheader("📊 Impact Matrix (Z-Score Scaled)")
    st.markdown("조회수와 댓글수를 Z-Score로 정규화하여 4개 사분면으로 분류합니다.")

    # 색상 구분 기준 선택
    color_by = st.selectbox(
        "색상 구분 기준",
        options=['콘텐츠 분류', '배포 방식', '대상', '주제 분류', '담당자', '사분면'],
        index=0,
        help="선택한 기준에 따라 데이터 포인트의 색상이 달라집니다"
    )

    df_with_zscore = calculate_zscore_matrix(df)
    impact_fig = create_impact_matrix(df_with_zscore, color_by=color_by)
    st.pyplot(impact_fig, use_container_width=True)
    plt.close(impact_fig)

    # 사분면 통계
    col1, col2, col3, col4 = st.columns(4)
    quadrant_counts = df_with_zscore['quadrant'].value_counts()

    with col1:
        count = quadrant_counts.get('높은 영향력', 0)
        st.metric("높은 영향력", f"{count}개")

    with col2:
        count = quadrant_counts.get('높은 도달, 낮은 참여', 0)
        st.metric("높은 도달, 낮은 참여", f"{count}개")

    with col3:
        count = quadrant_counts.get('낮은 도달, 높은 참여', 0)
        st.metric("낮은 도달, 높은 참여", f"{count}개")

    with col4:
        count = quadrant_counts.get('낮은 영향력', 0)
        st.metric("낮은 영향력", f"{count}개")

    st.markdown("---")

    # 전체 데이터 대비 게시물 위치 비교
    st.subheader("🎯 전체 데이터 대비 게시물 위치 비교")
    st.markdown("특정 게시물을 선택하여 과거 전체 데이터 대비 위치를 확인하세요.")

    if '제목' in df.columns:
        selected_title = st.selectbox(
            "분석할 게시물 선택",
            options=df['제목'].unique(),
            index=0
        )

        if selected_title:
            selected_post = df[df['제목'] == selected_title].iloc[0]
            historical_df = df[df['제목'] != selected_title]

            # 조회수 벤치마킹
            views_benchmark = benchmark_against_history(selected_post, historical_df, '조회수')

            st.markdown("#### 조회수 분석")

            # 히스토그램 + 위치 표시
            views_fig = create_benchmark_position_chart(
                historical_df,
                views_benchmark['value'],
                '조회수',
                '조회수 분포 및 현재 게시물 위치'
            )
            st.pyplot(views_fig, use_container_width=True)
            plt.close(views_fig)

            # 메트릭 표시
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "조회수",
                    f"{views_benchmark['value']:,}",
                    delta=f"상위 {100 - views_benchmark['percentile']:.1f}%"
                )
                st.caption(f"평균: {views_benchmark['mean']:.0f} | 중앙값: {views_benchmark['median']:.0f}")

            with col2:
                st.metric(
                    "백분위수",
                    f"{views_benchmark['percentile']:.1f}%"
                )
                st.caption(f"순위: {views_benchmark['rank']}/{views_benchmark['total']}")

            with col3:
                st.metric(
                    "Z-Score",
                    f"{views_benchmark['z_score']:.2f}"
                )
                st.caption(views_benchmark['category'])

            # 댓글수 벤치마킹
            comments_benchmark = benchmark_against_history(selected_post, historical_df, '댓글수')

            st.markdown("#### 댓글수 분석")

            # 히스토그램 + 위치 표시
            comments_fig = create_benchmark_position_chart(
                historical_df,
                comments_benchmark['value'],
                '댓글수',
                '댓글수 분포 및 현재 게시물 위치'
            )
            st.pyplot(comments_fig, use_container_width=True)
            plt.close(comments_fig)

            # 메트릭 표시
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "댓글수",
                    f"{comments_benchmark['value']:,}",
                    delta=f"상위 {100 - comments_benchmark['percentile']:.1f}%"
                )

            with col2:
                st.metric(
                    "백분위수",
                    f"{comments_benchmark['percentile']:.1f}%"
                )

            with col3:
                st.metric(
                    "Z-Score",
                    f"{comments_benchmark['z_score']:.2f}"
                )
                st.caption(comments_benchmark['category'])

    st.markdown("---")

    # 기간별 비교
    st.subheader("📅 기간별 성과 비교")

    period_type = st.radio(
        "기간 선택",
        options=["월별", "분기별", "연도별"],
        horizontal=True
    )

    comparison = compare_period_performance(df, period_type)

    if not comparison.empty:
        st.dataframe(comparison, use_container_width=True)
    else:
        st.info("비교할 데이터가 없습니다.")

    st.markdown("---")

    # 상위 성과 게시물
    st.subheader("🏆 상위 성과 게시물")

    metric_choice = st.selectbox(
        "기준 지표 선택",
        options=['조회수', '댓글수', '좋아요수']
    )

    top_n = st.slider("표시할 개수", min_value=5, max_value=50, value=10, step=5)

    top_performers = identify_top_performers(df, metric=metric_choice, top_n=top_n)

    if not top_performers.empty:
        st.dataframe(top_performers, use_container_width=True)
    else:
        st.info("데이터가 없습니다.")

except Exception as e:
    st.error(f"오류 발생: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
