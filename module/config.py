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
red = [0, 105, 0, 24, 255, 255]  # 빨강
green = [57, 27, 0, 90, 255, 255]  # 초록
blue = [107, 44, 0, 129, 255, 255]  # 파랑
myColors = [
    red,
    green,
    blue
]
# 도형 점의 개수
count = [
    [3, 4], # 삼각형
    [7, 9]  # 원
]

# PID 제어 관련 설정
fb_range = [20000, 24000]
ud_range = [0.3 * cam_height, 0.7 * cam_height]
pid = [0.1, 0.1, 0] # proportional, integrate, deriative