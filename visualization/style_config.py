"""
Matplotlib 스타일 및 한글 폰트 설정
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import warnings


def setup_korean_font():
    """한글 폰트 자동 설정"""
    system = platform.system()

    # Windows
    if system == 'Windows':
        font_candidates = ['Malgun Gothic', 'NanumGothic', 'AppleGothic']
    # macOS
    elif system == 'Darwin':
        font_candidates = ['AppleGothic', 'Arial Unicode MS']
    # Linux
    else:
        font_candidates = ['NanumGothic', 'DejaVu Sans']

    # 사용 가능한 폰트 찾기
    available_fonts = [f.name for f in fm.fontManager.ttflist]

    for font in font_candidates:
        if font in available_fonts:
            plt.rcParams['font.family'] = font
            plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
            return font

    # 폰트를 찾지 못한 경우 경고
    warnings.warn("한글 폰트를 찾을 수 없습니다. 텍스트가 깨질 수 있습니다.")
    plt.rcParams['axes.unicode_minus'] = False
    return None


def apply_default_style():
    """기본 차트 스타일 적용"""
    try:
        plt.style.use('seaborn-v0_8-whitegrid')  # Plotly white와 유사
    except:
        # seaborn-v0_8 스타일이 없으면 기본 whitegrid 사용
        try:
            plt.style.use('seaborn-whitegrid')
        except:
            # 모두 실패하면 기본 스타일 유지
            pass

    # 글꼴 설정
    setup_korean_font()

    # 기타 스타일
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 13
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 14
