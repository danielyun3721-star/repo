"""
색상 팔레트 매핑 - Plotly 색상 스킴을 Matplotlib/Seaborn으로 변환
"""
import matplotlib.pyplot as plt
import seaborn as sns
import config


# Plotly 색상 스킴을 Matplotlib/Seaborn으로 매핑
COLOR_SCHEME_MAPPING = {
    "기본 (Plotly)": {
        'type': 'custom',
        'colors': list(config.COLOR_PALETTE.values())
    },
    "파스텔": {
        'type': 'seaborn',
        'palette': 'pastel'
    },
    "선명한 색상": {
        'type': 'matplotlib',
        'palette': 'Set1'
    },
    "차분한 색상": {
        'type': 'matplotlib',
        'palette': 'Set2'
    },
    "무지개": {
        'type': 'matplotlib',
        'palette': 'rainbow',
        'n_colors': 10
    },
    "단색 (파랑)": {
        'type': 'matplotlib',
        'palette': 'Blues',
        'sequential': True
    },
    "단색 (녹색)": {
        'type': 'matplotlib',
        'palette': 'Greens',
        'sequential': True
    }
}


def get_color_palette(scheme_name, n_colors=10):
    """
    색상 팔레트 반환

    Args:
        scheme_name (str): 색상 스킴 이름
        n_colors (int): 필요한 색상 개수

    Returns:
        list: 색상 리스트
    """
    scheme = COLOR_SCHEME_MAPPING.get(scheme_name)

    if not scheme:
        # 스킴을 찾지 못하면 기본 팔레트 반환
        return list(config.COLOR_PALETTE.values())[:n_colors]

    if scheme['type'] == 'custom':
        colors = scheme['colors']
        # 색상이 부족하면 반복
        while len(colors) < n_colors:
            colors = colors + scheme['colors']
        return colors[:n_colors]

    elif scheme['type'] == 'seaborn':
        return sns.color_palette(scheme['palette'], n_colors=n_colors)

    elif scheme['type'] == 'matplotlib':
        if scheme.get('sequential'):
            # Sequential colormap (Blues, Greens 등)
            cmap = plt.cm.get_cmap(scheme['palette'])
            # 0.3부터 0.9까지 사용 (너무 연한 색과 너무 진한 색 제외)
            return [cmap(0.3 + 0.6 * i / (n_colors - 1)) for i in range(n_colors)]
        else:
            # Qualitative colormap (Set1, Set2 등)
            cmap = plt.cm.get_cmap(scheme['palette'])
            if hasattr(cmap, 'colors'):
                colors = list(cmap.colors)
            else:
                # colormap에서 색상 추출
                colors = [cmap(i) for i in range(cmap.N)]

            # 색상이 부족하면 반복
            while len(colors) < n_colors:
                colors = colors + colors
            return colors[:n_colors]

    # 기본값
    return list(config.COLOR_PALETTE.values())[:n_colors]
