# 커뮤니케이션 분석 대시보드

Streamlit 기반 커뮤니케이션 제작물 성과 분석 및 벤치마킹 대시보드

사내 커뮤니케이션 결과 데이터를 분석하고, 신규 데이터 추가 시 과거 데이터 대비 위치/수준을 실시간 모니터링할 수 있습니다.

## 주요 기능

- 📊 **전체 성과 분석**: 월별 트렌드, 채널 효율성, 주제별 분포 분석
- 🎯 **효율성 분석**: 조회수 vs 댓글수 스캐터플롯, 참여율 분석
- 🔍 **비교 분석**: Z-Score 기반 Impact Matrix, 과거 데이터 대비 벤치마킹
- 📝 **신규 데이터 추가**: 웹 인터페이스를 통한 데이터 입력
- 📋 **데이터 관리**: 전체 데이터 조회 및 편집

## 설치 방법

### 1. 저장소 클론

```bash
git clone https://github.com/danielyun3721-star/repo.git
cd repo
```

### 2. 필수 패키지 설치

```bash
python -m pip install -r requirements.txt
```

### 3. 데이터 파일 준비

1. `sample_data.xlsx` 파일을 `raw_data.xlsx`로 이름 변경하거나
2. 동일한 구조의 실제 데이터를 `raw_data.xlsx` 파일로 준비하세요

**필수 컬럼**:
- 발행 일자
- 콘텐츠 분류
- 배포 방식
- 대상
- 주제 분류
- 제목
- 담당자
- 콘텐츠 링크
- 이벤트 유무
- 조회수
- 댓글수
- 좋아요수
- 댓글 리스트
- AI포털 방문자수

## 실행 방법

```bash
python -m streamlit run app.py
```

브라우저에서 `http://localhost:8501` 자동 실행됩니다.

## 프로젝트 구조

```
.
├── app.py                  # 메인 애플리케이션
├── config.py              # 설정 파일
├── requirements.txt       # 패키지 의존성
├── sample_data.xlsx       # 샘플 데이터 (참고용)
├── analysis/             # 분석 모듈
├── components/           # UI 컴포넌트
├── data/                 # 데이터 처리 모듈
├── pages/                # Streamlit 페이지
├── utils/                # 유틸리티 함수
└── visualization/        # 차트 생성 모듈
```

## 사용 방법

### 데이터 조회 및 분석

1. 왼쪽 사이드바에서 원하는 메뉴 선택
2. 필터를 사용하여 데이터 범위 조정 (날짜, 배포 방식, 주제 등)
3. 인터랙티브 차트 탐색 (확대/축소, 호버, 다운로드)
4. 다운로드 버튼으로 분석 결과 저장

### 신규 데이터 추가

1. "Add New Data" 페이지 선택
2. 폼에 데이터 입력 (필수 항목 *표시)
3. "데이터 추가" 버튼 클릭
4. 자동으로 Excel 파일에 저장 및 백업 생성
5. 페이지 새로고침하여 업데이트된 데이터 확인

### 벤치마킹

1. "Comparison" 페이지 선택
2. Impact Matrix에서 전체 게시물의 위치 확인
3. 개별 게시물 선택하여 상세 벤치마킹
4. 백분위수, Z-Score, 순위 등 확인

## 주요 설정 변경

`config.py` 파일에서 다음 설정을 변경할 수 있습니다:

- `DATA_PATH`: 데이터 파일 경로
- `CONTENT_TYPES`: 콘텐츠 분류 옵션
- `DISTRIBUTION_CHANNELS`: 배포 방식 옵션
- `TOPIC_CATEGORIES`: 주제 분류 옵션
- `COLOR_PALETTE`: 차트 색상
- `CACHE_TTL`: 캐시 유효 시간

## 백업 관리

- 데이터 추가/수정 시 자동으로 `backups/` 폴더에 백업 파일 생성
- 백업 파일명 형식: `raw_data_backup_YYYYMMDD_HHMMSS.xlsx`
- 정기적으로 오래된 백업 파일 정리 권장

## 문제 해결

### 데이터가 표시되지 않을 때
- `raw_data.xlsx` 파일이 프로젝트 루트에 있는지 확인
- 파일 형식이 올바른지 확인 (Excel .xlsx)
- 필수 컬럼이 모두 포함되어 있는지 확인

### 성능이 느릴 때
- 브라우저 캐시 삭제
- Streamlit 앱 재시작
- `config.py`에서 `CACHE_TTL` 값 조정

### 신규 데이터 추가가 안 될 때
- 필수 항목이 모두 입력되었는지 확인
- Excel 파일이 다른 프로그램에서 열려있지 않은지 확인
- 쓰기 권한이 있는지 확인

## 기술 스택

- **Python 3.x**
- **Streamlit**: 웹 애플리케이션 프레임워크
- **Pandas**: 데이터 처리
- **Plotly**: 인터랙티브 차트
- **OpenPyXL**: Excel 파일 처리
