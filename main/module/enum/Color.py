from enum import Enum


class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    RED_REC = 3


# h_min, s_min, v_min, h_max, s_max, v_max 순서
# red = [0, 170, 0, 179, 255, 255]  # 빨강 2차 예선
# red = [0, 130, 0, 179, 255, 255]  # 빨강 강의실
# red = [0, 130, 0, 10, 255, 255]  # 빨강 강의실
# red_rec = [0, 170, 0, 179, 255, 255] # 빨강 링
red_rec = [0, 160, 0, 179, 255, 160] # 빨강 링 최신
# red_rec = [0, 130, 0, 179, 255, 100] # 빨강 링 전 103
red = [1, 130, 0, 10, 255, 255] # 빨간 플래그 본선
# red = [0, 130, 0, 179, 255, 255]  # 빨강 전 104
# green = [10, 100, 0, 80, 190, 255]  # 초록 2차 예선
# green = [50, 70, 0, 80, 190, 255]  # 초록 강의실
green = [45, 50, 0, 75, 255, 255] # 초록 본선
# blue = [100, 130, 0, 120, 255, 255]  # 파랑 2차 예선
# blue = [0, 130, 0, 179, 255, 255]  # 파랑 집
# blue = [90, 100, 0, 160, 255, 255] # 파랑 본선. 링과 도형 둘 다 감지하는 범위
blue = [90, 60, 0, 160, 255, 255] # 파랑 본선 최신. 링과 도형 둘 다 감지하는 범위
# blue = [0, 80, 0, 179, 255, 255] # 파랑 강의실
# blue = [90, 90, 0, 130, 255, 255] # 파랑 강의실

myColors = [
    red,
    green,
    blue,
    red_rec
    # black
]