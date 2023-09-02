from enum import Enum


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


# h_min, s_min, v_min, h_max, s_max, v_max 순서
red = [0, 50, 0, 10, 255, 230]  # 빨강
green = [35, 49, 0, 87, 255, 255]  # 초록
blue = [85, 50, 0, 126, 255, 255]  # 파랑
myColors = [
    red,
    green,
    blue
    # black
]