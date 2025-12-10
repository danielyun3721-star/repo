"""
메인 대시보드 페이지
"""
import streamlit as st
import sys
import os

# 부모 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import get_cached_data
from data.processor import preprocess_data
from analysis.statistics import calculate_basic_stats
from analysis.trends import calculate_monthly_engagement, calculate_quarterly_engagement, calculate_growth_rate
from visualization.charts import create_monthly_trend_chart, create_bar_chart, create_pie_chart, create_line_chart_with_markers, create_time_series_area_chart
from components.filters import render_date_filter, render_multiselect_filters, apply_filters
from components.export import render_download_buttons

st.set_page_config(page_title="대시보드", page_icon="📊", layout="wide")

st.title("📊 전체 대시보드")
st.markdown("사내 AI 커뮤니케이션 데이터의 전체 개요 및 주요 지표 확인")
st.markdown("---")

# 데이터 로딩
try:
    data_info = get_cached_data()
    df = preprocess_data(data_info['data'])

    if df.empty:
        st.warning("데이터가 없습니다. raw_data.xlsx 파일을 확인해주세요.")
        st.stop()

    # 필터 섹션
    with st.expander("🔍 필터 설정", expanded=False):
        start_date, end_date = render_date_filter(df)
        channels, topics, events = render_multiselect_filters(df)

    # 필터 적용
    filtered_df = apply_filters(df, start_date, end_date, channels, topics, events)

    st.info(f"📌 필터 적용 결과: **{len(filtered_df):,}개** 게시물")
    st.markdown("---")

    # 기본 통계
    stats = calculate_basic_stats(filtered_df)

    st.subheader("📈 주요 지표")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="전체 게시물",
            value=f"{stats['전체_게시물_수']:,}개"
        )

    with col2:
        st.metric(
            label="평균 조회수",
            value=f"{stats['평균_조회수']:.0f}"
        )

    with col3:
        st.metric(
            label="평균 댓글수",
            value=f"{stats['평균_댓글수']:.1f}"
        )

    with col4:
        st.metric(
            label="평균 좋아요수",
            value=f"{stats['평균_좋아요수']:.1f}"
        )

    # 두 번째 줄 지표
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="총 조회수",
            value=f"{stats['총_조회수']:,}"
        )

    with col6:
        st.metric(
            label="총 댓글수",
            value=f"{stats['총_댓글수']:,}"
        )

    with col7:
        st.metric(
            label="총 좋아요수",
            value=f"{stats['총_좋아요수']:,}"
        )

    with col8:
        if '평균_참여율' in stats:
            st.metric(
                label="평균 참여율",
                value=f"{stats['평균_참여율']:.2f}%"
            )

    st.markdown("---")

    # 트렌드 분석 (Trend Analysis 페이지에서 통합)
    st.subheader("📈 트렌드 분석")

    # 기간 단위 선택
    period_type = st.radio(
        "기간 단위 선택",
        options=["월별", "분기별"],
        horizontal=True
    )

    # 월별 트렌드
    if period_type == "월별":
        st.markdown("#### 📅 월별 참여도 추이")
        monthly_data = calculate_monthly_engagement(filtered_df)

        if not monthly_data.empty:
            chart = create_monthly_trend_chart(monthly_data)
            st.plotly_chart(chart, use_container_width=True)

            # 성장률 분석
            with st.expander("📊 월별 성장률 분석"):
                monthly_with_growth = calculate_growth_rate(monthly_data, '월')

                growth_chart = create_line_chart_with_markers(
                    monthly_with_growth,
                    '월',
                    ['조회수_성장률', '댓글수_성장률', '좋아요수_성장률'],
                    '월별 성장률 (%)'
                )
                st.plotly_chart(growth_chart, use_container_width=True)

                # 상세 데이터 테이블
                st.dataframe(monthly_with_growth, use_container_width=True)
        else:
            st.info("월별 데이터를 생성할 수 없습니다.")

    # 분기별 트렌드
    else:
        st.markdown("#### 📅 분기별 참여도 추이")
        quarterly_data = calculate_quarterly_engagement(filtered_df)

        if not quarterly_data.empty:
            chart = create_line_chart_with_markers(
                quarterly_data,
                '분기',
                ['조회수', '댓글수', '좋아요수'],
                '분기별 참여도 추이'
            )
            st.plotly_chart(chart, use_container_width=True)

            with st.expander("분기별 상세 데이터"):
                st.dataframe(quarterly_data, use_container_width=True)
        else:
            st.info("분기별 데이터를 생성할 수 없습니다.")

    st.markdown("---")

    # 카테고리별 분석
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 배포 방식별 게시물 수")
        if '배포 방식' in filtered_df.columns:
            channel_counts = filtered_df['배포 방식'].value_counts().reset_index()
            channel_counts.columns = ['배포 방식', '게시물 수']

            chart = create_pie_chart(channel_counts, '배포 방식', '게시물 수', '배포 방식별 게시물 분포')
            st.plotly_chart(chart, use_container_width=True)

    with col_right:
        st.subheader("📊 주제별 게시물 수")
        if '주제 분류' in filtered_df.columns:
            topic_counts = filtered_df['주제 분류'].value_counts().reset_index()
            topic_counts.columns = ['주제 분류', '게시물 수']

            chart = create_pie_chart(topic_counts, '주제 분류', '게시물 수', '주제별 게시물 분포')
            st.plotly_chart(chart, use_container_width=True)

    st.markdown("---")

    # 상세 통계 (시계열 차트로 변경)
    st.subheader("📋 상세 통계 시계열 분석")

    # 월별 데이터 집계 (이미 위에서 계산했으면 재사용)
    if period_type == "월별" and not monthly_data.empty:
        monthly_stats = monthly_data
    else:
        monthly_stats = calculate_monthly_engagement(filtered_df)

    if not monthly_stats.empty:
        col1, col2 = st.columns(2)

        with col1:
            # 조회수 시계열 차트
            views_chart = create_time_series_area_chart(
                monthly_stats,
                '월',
                '조회수',
                '월별 조회수 추이'
            )
            st.plotly_chart(views_chart, use_container_width=True)

        with col2:
            # 참여도 (댓글수 + 좋아요수) 시계열 차트
            if '댓글수' in monthly_stats.columns and '좋아요수' in monthly_stats.columns:
                monthly_stats_copy = monthly_stats.copy()
                monthly_stats_copy['참여도'] = monthly_stats_copy['댓글수'] + monthly_stats_copy['좋아요수']

                engagement_chart = create_time_series_area_chart(
                    monthly_stats_copy,
                    '월',
                    '참여도',
                    '월별 참여도 추이 (댓글+좋아요)'
                )
                st.plotly_chart(engagement_chart, use_container_width=True)
    else:
        # 차트를 그릴 수 없는 경우 기존 텍스트 통계 표시
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**조회수 통계**")
            st.write(f"- 총합: **{stats['총_조회수']:,}**")
            st.write(f"- 평균: **{stats['평균_조회수']:.0f}**")
            st.write(f"- 중앙값: **{stats['중앙값_조회수']:.0f}**")
            st.write(f"- 최고: **{stats['최고_조회수']:,}**")
            st.write(f"- 최저: **{stats['최저_조회수']:,}**")

        with col2:
            st.markdown("**참여도 통계**")
            st.write(f"- 총 댓글수: **{stats['총_댓글수']:,}**")
            st.write(f"- 총 좋아요수: **{stats['총_좋아요수']:,}**")
            if stats['평균_조회수'] > 0:
                engagement_rate = (stats['평균_댓글수'] + stats['평균_좋아요수']) / stats['평균_조회수'] * 100
                st.write(f"- 평균 참여율: **{engagement_rate:.2f}%**")

    st.markdown("---")

    # 데이터 다운로드
    st.subheader("📥 데이터 다운로드")
    render_download_buttons(filtered_df, monthly_data, prefix="dashboard_")

except Exception as e:
    st.error(f"오류 발생: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
