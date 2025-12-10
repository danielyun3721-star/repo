"""
사내 커뮤니케이션 데이터 분석 Streamlit 앱 - 메인 페이지
"""
import streamlit as st
from data.loader import get_cached_data
from data.processor import preprocess_data

# 페이지 설정
st.set_page_config(
    page_title="사내 커뮤니케이션 분석 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바
with st.sidebar:
    st.title("📊 커뮤니케이션 분석")
    st.markdown("---")

    # 데이터 정보
    try:
        data_info = get_cached_data()
        df = preprocess_data(data_info['data'])

        st.metric(
            label="총 게시물 수",
            value=f"{data_info['total_rows']:,}개"
        )

        st.caption(f"최종 업데이트: {data_info['last_updated'].strftime('%Y-%m-%d %H:%M')}")

        # 기간 정보
        if not df.empty and '발행 일자' in df.columns:
            min_date = df['발행 일자'].min()
            max_date = df['발행 일자'].max()

            st.markdown("---")
            st.markdown("**데이터 기간**")
            st.caption(f"{min_date.strftime('%Y-%m-%d')} ~ {max_date.strftime('%Y-%m-%d')}")

    except Exception as e:
        st.error(f"데이터 로딩 오류: {str(e)}")

    st.markdown("---")
    st.info("👈 왼쪽 메뉴에서 원하는 분석을 선택하세요")

# 메인 페이지
st.title("📊 사내 커뮤니케이션 데이터 분석 대시보드")

st.markdown("""
### 환영합니다!

이 대시보드는 2025년 사내 커뮤니케이션 성과를 분석하고 모니터링합니다.

---

### 주요 기능

#### 📈 **Dashboard**
- 전체 데이터 개요 및 기본 통계
- 주요 지표 요약 (조회수, 댓글수, 좋아요수)
- 월별 참여도 추이

#### 📊 **Trend Analysis**
- 월별/분기별 트렌드 분석
- 성장률 계산
- 시계열 패턴 분석

#### 🎯 **Efficiency Analysis**
- 채널별 효율성 분석 (Views vs Comments)
- 주제별 조회수 분포
- 콘텐츠 유형별 성과
- 이벤트 영향 분석

#### 📝 **Add New Data**
- 신규 커뮤니케이션 데이터 입력
- 실시간 Excel 파일 업데이트
- 자동 백업 생성

#### 🔍 **Comparison**
- 과거 데이터 대비 벤치마킹
- Z-Score 기반 Impact Matrix
- 백분위수 및 순위 계산
- 기간별 성과 비교

---

### 사용 방법

1. **왼쪽 사이드바**에서 원하는 메뉴를 선택하세요
2. 각 페이지에서 **필터**를 사용하여 데이터를 조정할 수 있습니다
3. **그래프와 차트**는 인터랙티브하게 탐색 가능합니다
4. **다운로드 버튼**을 통해 데이터와 분석 결과를 다운로드할 수 있습니다

---

### 데이터 구조

현재 분석 중인 데이터는 다음 정보를 포함합니다:

- **발행 일자**: 게시물 발행 날짜
- **콘텐츠 분류**: 콘텐츠 유형 (공지, 뉴스레터, 블로그 등)
- **배포 방식**: 배포 채널 (이메일, 인트라넷, Teams 등)
- **주제 분류**: 주제 카테고리 (HR, IT, 마케팅 등)
- **성과 지표**: 조회수, 댓글수, 좋아요수, AI포털 방문자수

---

### 문의 및 피드백

대시보드 사용 중 문의사항이나 개선 제안이 있으시면 담당자에게 연락해주세요.
""")

# 푸터
st.markdown("---")
st.caption("🤖 Powered by Streamlit | 📊 사내 커뮤니케이션 분석 대시보드 v1.0")
