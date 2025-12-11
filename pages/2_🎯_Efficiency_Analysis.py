"""
효율성 분석 페이지
"""
import streamlit as st
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import get_cached_data
from data.processor import preprocess_data
from analysis.efficiency import calculate_channel_efficiency, calculate_topic_performance, calculate_event_impact
from visualization.charts import create_efficiency_scatter, create_topic_distribution_box, create_bar_chart
from visualization.color_schemes import get_color_palette
from components.filters import render_date_filter, render_multiselect_filters, apply_filters

st.set_page_config(page_title="효율성 분석", page_icon="🎯", layout="wide")

# 색상 팔레트 선택 (사이드바)
with st.sidebar:
    st.markdown("### 🎨 차트 색상 설정")
    color_scheme = st.selectbox(
        "색상 팔레트 선택",
        options=[
            "기본 (Plotly)",
            "파스텔",
            "선명한 색상",
            "차분한 색상",
            "무지개",
            "단색 (파랑)",
            "단색 (녹색)"
        ],
        index=0
    )

# 색상 팔레트 가져오기 (Matplotlib/Seaborn)
selected_colors = get_color_palette(color_scheme, n_colors=10)

st.title("🎯 채널 효율성 분석")
st.markdown("배포 방식별, 주제별 성과를 분석합니다.")
st.markdown("---")

try:
    # 데이터 로딩
    data_info = get_cached_data()
    df = preprocess_data(data_info['data'])

    if df.empty:
        st.warning("데이터가 없습니다.")
        st.stop()

    # 필터
    with st.expander("🔍 필터 설정"):
        start_date, end_date = render_date_filter(df)
        channels, topics, events = render_multiselect_filters(df)

    filtered_df = apply_filters(df, start_date, end_date, channels, topics, events)
    st.info(f"필터 적용 결과: **{len(filtered_df):,}개** 게시물")
    st.markdown("---")

    # Views vs Comments 스캐터플롯
    st.subheader("📊 조회수 vs 댓글수 (채널 효율성)")
    scatter_fig = create_efficiency_scatter(filtered_df, color_discrete_sequence=selected_colors)
    st.pyplot(scatter_fig, use_container_width=True)
    plt.close(scatter_fig)
    st.caption("💡 **원의 크기**: 좋아요수를 나타냅니다. 크기가 클수록 좋아요가 많습니다.")

    # 호버 툴팁 대체: 상세 데이터 표시
    with st.expander("📊 상세 데이터 보기"):
        st.dataframe(filtered_df[['제목', '배포 방식', '조회수', '댓글수', '좋아요수']], use_container_width=True)

    st.markdown("---")

    # 채널별 효율성
    st.subheader("📡 배포 방식별 효율성")
    channel_eff = calculate_channel_efficiency(filtered_df)

    if not channel_eff.empty:
        col1, col2 = st.columns(2)

        with col1:
            bar1_fig = create_bar_chart(
                channel_eff,
                '배포_방식',
                '평균_조회수',
                '배포 방식별 평균 조회수',
                color_col='배포_방식',
                color_discrete_sequence=selected_colors
            )
            st.pyplot(bar1_fig, use_container_width=True)
            plt.close(bar1_fig)

        with col2:
            bar2_fig = create_bar_chart(
                channel_eff,
                '배포_방식',
                '댓글_전환율',
                '배포 방식별 댓글 전환율 (%)',
                color_col='배포_방식',
                color_discrete_sequence=selected_colors
            )
            st.pyplot(bar2_fig, use_container_width=True)
            plt.close(bar2_fig)

        with st.expander("배포 방식별 상세 데이터"):
            st.dataframe(channel_eff, use_container_width=True)

    st.markdown("---")

    # 주제별 성과
    st.subheader("📚 주제별 조회수 분포")
    topic_box_fig = create_topic_distribution_box(filtered_df, color_discrete_sequence=selected_colors)
    st.pyplot(topic_box_fig, use_container_width=True)
    plt.close(topic_box_fig)

    topic_perf = calculate_topic_performance(filtered_df)
    if not topic_perf.empty:
        with st.expander("주제별 상세 데이터"):
            st.dataframe(topic_perf, use_container_width=True)

    st.markdown("---")

    # 이벤트 영향 분석
    st.subheader("🎉 이벤트 유무별 영향 분석")
    event_impact = calculate_event_impact(filtered_df)

    if not event_impact.empty:
        col1, col2, col3 = st.columns(3)

        for idx, row in event_impact.iterrows():
            with [col1, col2, col3][idx % 3]:
                st.metric(
                    label=f"{row['이벤트_유무']}",
                    value=f"{row['평균_조회수']:.0f}",
                    delta=f"{row['게시물_수']}개"
                )

        with st.expander("이벤트 영향 상세 데이터"):
            st.dataframe(event_impact, use_container_width=True)

except Exception as e:
    st.error(f"오류 발생: {str(e)}")
