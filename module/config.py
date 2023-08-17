from enum import Enum
cam_width = 640 # 웹캠 너비
cam_height = 480 # 웹캠 높이
detect_min = 100 # 색을 탐지하는 최소 면적
determin_min = 500 # 모양을 탐지하기 위한 최소 면적
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2
    BLACK = 3
class Figure(Enum):
    TRI = 0
    CIRCLE = 1
    RECTANGLE = 2
    NUMBER = 3

class Direction(Enum):
    """
    Tello 객체의 send_rc_control 메소드의 인자로 들어갈 값.
    홀수라면 음수이고 짝수라면 양수임.
    """
    RIGHT = 0
    LEFT = 1
    FORWARD = 2
    BACKWARD = 3
    UP = 4
    DOWN = 5
    CLOCKWISE = 6
    COUNTERCLOCKWISE = 7
# h_min, s_min, v_min, h_max, s_max, v_max 순서
red = [0, 22, 0, 12, 255, 255]  # 빨강
green = [58, 79, 0, 105, 255, 255]  # 초록
blue = [102, 44, 59, 130, 255, 209]  # 파랑
black = [0, 0, 0, 100, 88, 58] # 검정
myColors = [
    red,
    green,
    blue,
    black
]
# 도형 점의 개수
count = [
    [3, 4], # 삼각형
    [7, 9], # 원
    [4, 5],  # 사각형
    [1, 255] # 숫자
]

# PID 제어 관련 설정
fb_range = [24000, 28000]
ud_range = [0.4 * cam_height, 0.6 * cam_height]
pid = [0.1, 0.1, 0] # proportional, integrate, deriative

min_find_area = 3000 # 찾기 위한 최소 면적
find_range = 0.3 # 찾기 위한 contour의 중심 좌표의 범위
find_range_qr = 0.45 # qr을 찾기 위한 contour의 중심 좌표의 범위

center_range = 0.3 # 중심에 있다고 판단하기 위한 중심 좌표의 범위

aspect_ratio_range = 0.1 # 정면에 있다고 판단할 가로세로비율