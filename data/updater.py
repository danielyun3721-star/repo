"""
Excel 파일 업데이트 모듈
"""
import pandas as pd
import streamlit as st
from datetime import datetime
import os
import shutil
import config


def create_backup():
    """
    현재 Excel 파일 백업

    Returns:
        str: 백업 파일 경로
    """
    try:
        if not os.path.exists(config.BACKUP_DIR):
            os.makedirs(config.BACKUP_DIR)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"raw_data_backup_{timestamp}.txt"
        backup_path = os.path.join(config.BACKUP_DIR, backup_filename)

        shutil.copy2(config.DATA_PATH, backup_path)
        return backup_path
    except Exception as e:
        st.warning(f"백업 생성 중 오류 발생: {str(e)}")
        return None


def append_new_data(new_data):
    """
    신규 데이터를 Excel 파일에 추가

    Args:
        new_data (dict): 신규 데이터 딕셔너리

    Returns:
        bool: 성공 여부
    """
    try:
        # 백업 생성
        backup_path = create_backup()
        if backup_path:
            st.info(f"백업 파일 생성: {os.path.basename(backup_path)}")

        # 기존 데이터 읽기
        df = pd.read_csv(config.DATA_PATH, sep='\t', encoding='cp949')

        # 새 행 추가
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)

        # TSV 저장
        df.to_csv(config.DATA_PATH, sep='\t', index=False, encoding='cp949')

        return True
    except Exception as e:
        st.error(f"데이터 추가 중 오류 발생: {str(e)}")
        return False


def update_existing_data(index, updated_data):
    """
    기존 데이터 수정

    Args:
        index (int): 수정할 행 인덱스
        updated_data (dict): 업데이트할 데이터

    Returns:
        bool: 성공 여부
    """
    try:
        # 백업 생성
        create_backup()

        # 기존 데이터 읽기
        df = pd.read_csv(config.DATA_PATH, sep='\t', encoding='cp949')

        # 데이터 수정
        for key, value in updated_data.items():
            if key in df.columns:
                df.loc[index, key] = value

        # TSV 저장
        df.to_csv(config.DATA_PATH, sep='\t', index=False, encoding='cp949')

        return True
    except Exception as e:
        st.error(f"데이터 수정 중 오류 발생: {str(e)}")
        return False


def delete_data(index):
    """
    데이터 삭제

    Args:
        index (int): 삭제할 행 인덱스

    Returns:
        bool: 성공 여부
    """
    try:
        # 백업 생성
        create_backup()

        # 기존 데이터 읽기
        df = pd.read_csv(config.DATA_PATH, sep='\t', encoding='cp949')

        # 데이터 삭제
        df = df.drop(index)
        df = df.reset_index(drop=True)

        # TSV 저장
        df.to_csv(config.DATA_PATH, sep='\t', index=False, encoding='cp949')

        return True
    except Exception as e:
        st.error(f"데이터 삭제 중 오류 발생: {str(e)}")
        return False


def log_change(original_df, edited_df):
    """
    데이터 변경 로그 기록

    Args:
        original_df (pd.DataFrame): 원본 데이터프레임
        edited_df (pd.DataFrame): 수정된 데이터프레임

    Returns:
        str: 로그 파일 경로
    """
    try:
        log_dir = os.path.join(config.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'change_log_{timestamp}.txt')

        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"변경 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"변경 전 행 수: {len(original_df)}\n")
            f.write(f"변경 후 행 수: {len(edited_df)}\n")
            f.write("\n=== 변경 내역 ===\n")

            # 행 수 차이 계산
            row_diff = len(edited_df) - len(original_df)
            if row_diff > 0:
                f.write(f"\n[추가된 행: {row_diff}개]\n")
            elif row_diff < 0:
                f.write(f"\n[삭제된 행: {abs(row_diff)}개]\n")

            f.write("\n\n[수정 사항은 백업 파일과 비교하세요]\n")

        return log_file
    except Exception as e:
        st.warning(f"로그 기록 중 오류 발생: {str(e)}")
        return None
