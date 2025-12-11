"""
데이터 관리 페이지
"""
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.loader import get_cached_data, clear_cache
from data.updater import create_backup, log_change
import config

st.set_page_config(page_title="데이터 관리", page_icon="📋", layout="wide")

st.title("📋 데이터 관리")
st.markdown("전체 데이터를 확인하고 직접 수정할 수 있습니다.")
st.markdown("---")

# 안내 메시지
st.warning("""
⚠️ **주의사항**
- 데이터 수정 시 자동으로 TSV 파일에 반영됩니다
- 모든 변경사항은 로그로 기록되며 백업 파일이 생성됩니다
- 삭제된 데이터는 복구할 수 없으니 신중하게 수정하세요
""")

# 데이터 로딩
try:
    data_info = get_cached_data()
    df_original = data_info['data'].copy()

    if df_original.empty:
        st.warning("데이터가 없습니다.")
        st.stop()

    # 필터 옵션
    with st.expander("🔍 필터 옵션"):
        col1, col2, col3 = st.columns(3)

        with col1:
            # 날짜 필터
            if '발행 일자' in df_original.columns:
                df_original['발행 일자'] = pd.to_datetime(df_original['발행 일자'])
                min_date = df_original['발행 일자'].min().date()
                max_date = df_original['발행 일자'].max().date()

                date_range = st.date_input(
                    "날짜 범위",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

        with col2:
            # 배포 방식 필터
            if '배포 방식' in df_original.columns:
                channels = st.multiselect(
                    "배포 방식",
                    options=df_original['배포 방식'].unique(),
                    default=df_original['배포 방식'].unique()
                )

        with col3:
            # 주제 필터
            if '주제 분류' in df_original.columns:
                topics = st.multiselect(
                    "주제 분류",
                    options=df_original['주제 분류'].unique(),
                    default=df_original['주제 분류'].unique()
                )

    # 필터 적용
    df_filtered = df_original.copy()
    if len(date_range) == 2:
        df_filtered = df_filtered[
            (df_filtered['발행 일자'] >= pd.Timestamp(date_range[0])) &
            (df_filtered['발행 일자'] <= pd.Timestamp(date_range[1]))
        ]
    if channels:
        df_filtered = df_filtered[df_filtered['배포 방식'].isin(channels)]
    if topics:
        df_filtered = df_filtered[df_filtered['주제 분류'].isin(topics)]

    st.info(f"총 **{len(df_filtered):,}개** 행 표시 중 (전체: {len(df_original):,}개)")

    st.markdown("---")

    # 편집 가능한 데이터 테이블
    st.subheader("📊 데이터 편집")

    # 편집할 컬럼 설정
    column_config = {
        "발행 일자": st.column_config.DateColumn(
            "발행 일자",
            format="YYYY-MM-DD",
            required=True
        ),
        "조회수": st.column_config.NumberColumn(
            "조회수",
            min_value=0,
            format="%d"
        ),
        "댓글수": st.column_config.NumberColumn(
            "댓글수",
            min_value=0,
            format="%d"
        ),
        "좋아요수": st.column_config.NumberColumn(
            "좋아요수",
            min_value=0,
            format="%d"
        ),
        "AI포털 방문자수": st.column_config.NumberColumn(
            "AI포털 방문자수",
            min_value=0,
            format="%d"
        ),
        "콘텐츠 링크": st.column_config.LinkColumn(
            "콘텐츠 링크"
        )
    }

    # 데이터 편집기
    edited_df = st.data_editor(
        df_filtered,
        use_container_width=True,
        num_rows="dynamic",  # 행 추가/삭제 가능
        column_config=column_config,
        hide_index=False,
        key="data_editor"
    )

    st.markdown("---")

    # 변경사항 저장 버튼
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("💾 변경사항 저장", type="primary", use_container_width=True):
            # 변경사항 감지
            if not df_filtered.equals(edited_df):
                # 백업 생성
                backup_path = create_backup()
                if backup_path:
                    st.success(f"✅ 백업 생성: {os.path.basename(backup_path)}")

                # TSV 파일 업데이트
                try:
                    # 전체 데이터에 변경사항 반영 (간단한 방법: 전체 데이터 교체)
                    edited_df.to_csv(config.DATA_PATH, sep='\t', index=False, encoding='cp949')

                    # 변경 로그 기록
                    log_file = log_change(df_filtered, edited_df)
                    if log_file:
                        st.success(f"✅ 변경 로그 생성: {os.path.basename(log_file)}")

                    # 캐시 무효화
                    clear_cache()

                    st.success("✅ 변경사항이 저장되었습니다!")
                    st.balloons()

                    # 페이지 새로고침
                    if st.button("🔄 페이지 새로고침"):
                        st.rerun()

                except Exception as e:
                    st.error(f"❌ 저장 중 오류 발생: {str(e)}")
            else:
                st.info("변경사항이 없습니다.")

    with col2:
        if st.button("🔄 초기화", use_container_width=True):
            st.rerun()

except Exception as e:
    st.error(f"오류 발생: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
