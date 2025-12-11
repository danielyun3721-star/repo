"""
신규 데이터 입력 폼 컴포넌트
"""
import streamlit as st
from datetime import datetime, date
import config
from data.updater import append_new_data
from data.loader import clear_cache
from utils.validation import validate_input
from utils.helpers import get_unique_options


def render_input_form(df):
    """
    신규 데이터 입력 폼 렌더링

    Args:
        df (pd.DataFrame): 기존 데이터프레임
    """

    st.subheader("신규 커뮤니케이션 데이터 추가")
    st.markdown("---")

    with st.form("new_data_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            발행_일자 = st.date_input(
                "발행 일자 *",
                value=date.today(),
                help="게시물 발행 날짜"
            )

            # 콘텐츠 분류 (동적)
            existing_content_types = get_unique_options(df, '콘텐츠 분류', include_other=True)
            콘텐츠_분류 = st.selectbox(
                "콘텐츠 분류 *",
                options=existing_content_types,
                help="기존 콘텐츠 분류 또는 '기타' 선택"
            )

            # '기타' 선택 시 신규 입력 필드 표시
            if 콘텐츠_분류 == '기타':
                콘텐츠_분류_신규 = st.text_input(
                    "신규 콘텐츠 분류 입력",
                    placeholder="예: 웨비나, 팟캐스트 등",
                    help="새로운 콘텐츠 분류를 입력하세요"
                )
                if 콘텐츠_분류_신규:
                    콘텐츠_분류 = 콘텐츠_분류_신규

            # 배포 방식 (동적)
            existing_channels = get_unique_options(df, '배포 방식', include_other=True)
            배포_방식 = st.selectbox(
                "배포 방식 *",
                options=existing_channels,
                help="기존 배포 방식 또는 '기타' 선택"
            )

            # '기타' 선택 시 신규 입력 필드 표시
            if 배포_방식 == '기타':
                배포_방식_신규 = st.text_input(
                    "신규 배포 방식 입력",
                    placeholder="예: Notion, Confluence 등",
                    help="새로운 배포 방식을 입력하세요"
                )
                if 배포_방식_신규:
                    배포_방식 = 배포_방식_신규

            # 대상 (동적)
            existing_targets = get_unique_options(df, '대상', include_other=True)
            대상 = st.selectbox(
                "대상",
                options=existing_targets,
                help="기존 대상 또는 '기타' 선택"
            )

            # '기타' 선택 시 신규 입력 필드 표시
            if 대상 == '기타':
                대상_신규 = st.text_input(
                    "신규 대상 입력",
                    placeholder="예: 전사, 개발팀, 디자인팀 등",
                    help="새로운 대상을 입력하세요"
                )
                if 대상_신규:
                    대상 = 대상_신규

            # 주제 분류 (동적)
            existing_topics = get_unique_options(df, '주제 분류', include_other=True)
            주제_분류 = st.selectbox(
                "주제 분류 *",
                options=existing_topics,
                help="기존 주제 분류 또는 '기타' 선택"
            )

            # '기타' 선택 시 신규 입력 필드 표시
            if 주제_분류 == '기타':
                주제_분류_신규 = st.text_input(
                    "신규 주제 분류 입력",
                    placeholder="예: AI/ML, 데이터 분석 등",
                    help="새로운 주제 분류를 입력하세요"
                )
                if 주제_분류_신규:
                    주제_분류 = 주제_분류_신규

            제목 = st.text_input(
                "제목 *",
                placeholder="게시물 제목을 입력하세요",
                help="게시물 제목"
            )

        with col2:
            담당자 = st.text_input(
                "담당자",
                placeholder="담당자명",
                help="작성 담당자"
            )

            콘텐츠_링크 = st.text_input(
                "콘텐츠 링크",
                placeholder="https://...",
                help="게시물 링크 URL"
            )

            이벤트_유무 = st.selectbox(
                "이벤트 유무 *",
                options=["없음", "있음"],
                help="이벤트 진행 여부"
            )

            조회수 = st.number_input(
                "조회수 *",
                min_value=0,
                value=0,
                step=1,
                help="총 조회수"
            )

            댓글수 = st.number_input(
                "댓글수 *",
                min_value=0,
                value=0,
                step=1,
                help="총 댓글수"
            )

            좋아요수 = st.number_input(
                "좋아요수 *",
                min_value=0,
                value=0,
                step=1,
                help="총 좋아요수"
            )

        # 추가 필드
        st.markdown("### 추가 정보")
        col3, col4 = st.columns(2)

        with col3:
            AI포털_방문자수 = st.number_input(
                "AI포털 방문자수",
                min_value=0,
                value=0,
                step=1,
                help="AI포털 방문자 수 (해당 시)"
            )

        with col4:
            댓글_리스트 = st.text_area(
                "댓글 리스트 (선택사항)",
                placeholder="주요 댓글 내용을 입력하세요",
                help="댓글 내용 (선택사항)",
                height=100
            )

        st.markdown("---")
        st.caption("* 표시는 필수 입력 항목입니다")

        # 버튼 배치
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])

        with col_btn1:
            submitted = st.form_submit_button(
                "데이터 추가",
                type="primary",
                use_container_width=True
            )

        with col_btn2:
            cancelled = st.form_submit_button(
                "취소",
                use_container_width=True
            )

        if submitted:
            # 데이터 구성
            new_data = {
                '발행 일자': datetime.combine(발행_일자, datetime.min.time()).strftime('%Y-%m-%d %H:%M:%S'),
                '콘텐츠 분류': 콘텐츠_분류,
                '배포 방식': 배포_방식,
                '대상': 대상 if 대상 else '',
                '주제 분류': 주제_분류,
                '제목': 제목,
                '담당자': 담당자 if 담당자 else '',
                '콘텐츠 링크': 콘텐츠_링크 if 콘텐츠_링크 else '',
                '이벤트 유무': 이벤트_유무,
                '조회수': int(조회수),
                '댓글수': int(댓글수),
                '좋아요수': int(좋아요수),
                '댓글 리스트': 댓글_리스트 if 댓글_리스트 else '',
                'AI포털 방문자수': int(AI포털_방문자수)
            }

            # 유효성 검증
            is_valid, error_message = validate_input(new_data)

            if is_valid:
                # 데이터 추가
                with st.spinner('데이터를 추가하는 중...'):
                    success = append_new_data(new_data)

                if success:
                    st.success("데이터가 성공적으로 추가되었습니다!")
                    st.balloons()

                    # 캐시 무효화
                    clear_cache()

                    # 추가 정보 표시
                    with st.expander("추가된 데이터 확인"):
                        st.json(new_data)

                    st.info("페이지가 자동으로 새로고침됩니다...")

                    # 자동으로 페이지 새로고침
                    st.rerun()
                else:
                    st.error("데이터 추가 중 오류가 발생했습니다. 다시 시도해주세요.")
            else:
                st.error(f"입력 데이터 오류: {error_message}")

        if cancelled:
            st.info("입력이 취소되었습니다.")
