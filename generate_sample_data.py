"""
샘플 데이터 생성 스크립트
raw_data.txt와 동일한 구조의 샘플 파일을 랜덤 데이터로 생성
"""
import pandas as pd
import random
from datetime import datetime, timedelta
import sys

# UTF-8 출력 설정
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("raw_data.txt 읽는 중...")
# raw_data.txt 읽기 (실제 컬럼 구조 확인)
df_original = pd.read_csv('raw_data.txt', sep='\t', encoding='cp949')

print(f"원본 파일 로드 완료: {len(df_original)}개 행, {len(df_original.columns)}개 컬럼")
print(f"컬럼 목록: {list(df_original.columns)}")

# 원본 컬럼 이름 저장
columns = df_original.columns.tolist()

# 샘플 데이터 개수 설정
n_samples = 15

print(f"\n{n_samples}개의 샘플 데이터 생성 중...")

# 각 컬럼의 유니크 값 추출 (범주형 데이터에 사용)
unique_values = {}
for col in columns:
    if df_original[col].dtype == 'object' and col not in ['제목', '콘텐츠 링크', '댓글 리스트']:
        # NaN이 아닌 유니크 값만 추출
        values = df_original[col].dropna().unique()
        if len(values) > 0:
            unique_values[col] = values.tolist()

# 샘플 데이터 생성
sample_data = []

for i in range(n_samples):
    row = {}

    for col in columns:
        if '발행' in col and '일자' in col:
            # 날짜 컬럼
            row[col] = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))

        elif '제목' in col:
            # 제목 컬럼
            row[col] = f'샘플 콘텐츠 제목 {i+1}'

        elif '링크' in col:
            # 링크 컬럼
            row[col] = f'https://example.com/content{i+1}'

        elif '조회수' in col:
            # 조회수
            row[col] = random.randint(100, 10000)

        elif '댓글수' in col or '댓글 수' in col:
            # 댓글수
            row[col] = random.randint(0, 100)

        elif '좋아요' in col:
            # 좋아요수
            row[col] = random.randint(0, 500)

        elif 'AI포털' in col or '방문자' in col:
            # AI포털 방문자수
            row[col] = random.randint(50, 2000)

        elif '댓글 리스트' in col or '댓글리스트' in col:
            # 댓글 리스트 (빈 값)
            row[col] = ''

        elif col in unique_values:
            # 범주형 데이터 (원본에서 추출한 값 사용)
            row[col] = random.choice(unique_values[col])

        else:
            # 기타 (빈 값)
            row[col] = ''

    sample_data.append(row)

# DataFrame 생성
df_sample = pd.DataFrame(sample_data)

# 샘플 파일 저장
output_file = 'sample_data.txt'
df_sample.to_csv(output_file, sep='\t', index=False, encoding='cp949')

print(f"\n{output_file} 생성 완료!")
print(f"   - {len(df_sample)}개 행")
print(f"   - {len(df_sample.columns)}개 컬럼")
print(f"\n생성된 샘플 데이터:")
print(df_sample.head())
