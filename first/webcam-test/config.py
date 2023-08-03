from enum import Enum
cam_width = 640 # 웹캠 너비
cam_height = 480 # 웹캠 높이
detect_min = 100 # 색을 탐지하는 최소 면적
determin_min = 500 # 모양을 탐지하기 위한 최소 면적
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
class Figure(Enum):
    TRI = 0
    CIRCLE = 1

# h_min, s_min, v_min, h_max, s_max, v_max 순서
red = [4, 117, 112, 9, 255, 255]  # 빨강
green = [50, 39, 40, 120, 172, 177]  # 초록
blue = [23, 89, 17, 167, 255, 106]  # 파랑
myColors = [
    red,
    green,
    blue
]
# 도형 점의 개수
count = [
    3, # 삼각형
    8  # 원
]
