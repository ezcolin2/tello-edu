from enum import Enum


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


# h_min, s_min, v_min, h_max, s_max, v_max 순서
# red = [0, 170, 0, 179, 255, 255]  # 빨강 2차 예선
red = [0, 130, 0, 179, 255, 255]  # 빨강 강의실
# green = [10, 100, 0, 80, 190, 255]  # 초록 2차 예선
green = [50, 70, 0, 80, 190, 255]  # 초록 강의실
# blue = [100, 130, 0, 120, 255, 255]  # 파랑 2차 예선
# blue = [90, 100, 0, 160, 255, 255] # 파랑 본선. 링과 도형 둘 다 감지하는 범위
blue = [80, 90, 0, 150, 255, 255] # 파랑 강의실

myColors = [
    red,
    green,
    blue
    # black
]