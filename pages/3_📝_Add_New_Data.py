"""
신규 데이터 추가 페이지
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.data_input import render_input_form
from data.loader import get_cached_data
from data.processor import preprocess_data

st.set_page_config(page_title="데이터 추가", page_icon="📝", layout="wide")

st.title("📝 신규 커뮤니케이션 데이터 추가")
st.markdown("새로운 커뮤니케이션 제작물 데이터를 입력하세요.")
st.markdown("---")

# 안내 메시지
st.info("""
💡 **안내사항**
- 필수 항목(*)은 반드시 입력해야 합니다
- 데이터 추가 시 자동으로 Excel 파일에 저장됩니다
- 백업 파일이 자동으로 생성됩니다
- 데이터 추가 후 페이지를 새로고침하면 업데이트된 결과를 확인할 수 있습니다
""")

st.markdown("---")

# 데이터 로딩
try:
    data_info = get_cached_data()
    df = preprocess_data(data_info['data'])

    # 입력 폼 렌더링 (df 전달)
    render_input_form(df)

except Exception as e:
    st.error(f"오류 발생: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
