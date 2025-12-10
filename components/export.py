"""
데이터 다운로드 컴포넌트
"""
import streamlit as st
from datetime import datetime
import pandas as pd


def render_download_buttons(df, analysis_results=None, prefix=""):
    """
    데이터 다운로드 버튼 렌더링

    Args:
        df (pd.DataFrame): 원본 데이터프레임
        analysis_results (pd.DataFrame, optional): 분석 결과 데이터프레임
        prefix (str): 파일명 접두사
    """
    if df.empty:
        st.warning("다운로드할 데이터가 없습니다.")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    col1, col2 = st.columns(2)

    with col1:
        # 원본 데이터 CSV 다운로드
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        filename = f"{prefix}raw_data_{timestamp}.csv" if prefix else f"communication_data_{timestamp}.csv"

        st.download_button(
            label="📥 원본 데이터 다운로드 (CSV)",
            data=csv,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # 분석 결과 다운로드
        if analysis_results is not None and not analysis_results.empty:
            analysis_csv = analysis_results.to_csv(index=False, encoding='utf-8-sig')
            analysis_filename = f"{prefix}analysis_results_{timestamp}.csv" if prefix else f"analysis_results_{timestamp}.csv"

            st.download_button(
                label="📥 분석 결과 다운로드 (CSV)",
                data=analysis_csv,
                file_name=analysis_filename,
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("분석 결과가 없습니다", icon="ℹ️")


def render_excel_download_button(df, sheet_name="Sheet1", filename=None):
    """
    Excel 다운로드 버튼

    Args:
        df (pd.DataFrame): 데이터프레임
        sheet_name (str): 시트명
        filename (str, optional): 파일명
    """
    if df.empty:
        st.warning("다운로드할 데이터가 없습니다.")
        return

    try:
        import io
        from openpyxl import Workbook

        # Excel 파일 생성
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        output.seek(0)
        excel_data = output.getvalue()

        # 파일명 생성
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"communication_data_{timestamp}.xlsx"

        st.download_button(
            label="📥 Excel 다운로드",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Excel 다운로드 중 오류 발생: {str(e)}")


def render_json_download_button(data, filename=None):
    """
    JSON 다운로드 버튼

    Args:
        data (dict or pd.DataFrame): 데이터
        filename (str, optional): 파일명
    """
    try:
        import json

        if isinstance(data, pd.DataFrame):
            json_str = data.to_json(orient='records', force_ascii=False, indent=2)
        else:
            json_str = json.dumps(data, ensure_ascii=False, indent=2)

        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data_{timestamp}.json"

        st.download_button(
            label="📥 JSON 다운로드",
            data=json_str,
            file_name=filename,
            mime="application/json",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"JSON 다운로드 중 오류 발생: {str(e)}")
