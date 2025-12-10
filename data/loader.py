"""
데이터 로딩 및 캐싱 모듈
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import config


@st.cache_data(ttl=config.CACHE_TTL)
def load_data():
    """
    Excel 파일을 읽어 DataFrame 반환

    Returns:
        pd.DataFrame: 로드된 데이터프레임
    """
    try:
        df = pd.read_excel(config.DATA_PATH)
        return df
    except FileNotFoundError:
        st.error(f"데이터 파일을 찾을 수 없습니다: {config.DATA_PATH}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {str(e)}")
        return pd.DataFrame()


def get_cached_data():
    """
    캐시된 데이터 반환 + 메타 정보

    Returns:
        dict: 데이터, 최종 업데이트 시간, 총 행 수
    """
    df = load_data()

    return {
        'data': df,
        'last_updated': datetime.now(),
        'total_rows': len(df)
    }


def clear_cache():
    """캐시 무효화"""
    st.cache_data.clear()
