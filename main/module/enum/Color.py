from enum import Enum


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


# h_min, s_min, v_min, h_max, s_max, v_max 순서
red = [0, 170, 0, 179, 255, 255]  # 빨강
green = [10, 100, 0, 80, 190, 255]  # 초록
blue = [100, 130, 0, 120, 255, 255]  # 파랑
myColors = [
    red,
    green,
    blue
    # black
]