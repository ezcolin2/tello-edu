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
    RECTANGLE = 2
    NUMBER = 3
    ANY = 4

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
red = [0, 50, 0, 10, 255, 230]  # 빨강
# green = [42, 99, 0, 67, 255, 255]  # 초록
green = [35, 49, 0, 87, 255, 255]  # 초록
blue = [85, 50, 0, 126, 255, 255]  # 파랑
# black = [0, 0, 0, 100, 88, 58] # 검정
myColors = [
    red,
    green,
    blue
    # black
]
# 도형 점의 개수
count = [
    [3, 4], # 삼각형
    [7, 9], # 원
    [3, 5],  # 사각형
    [1, 255], # 숫자
    [1, 1000] # 아무거나
]


# 숫자는 크기가 작기 때문에 범위 줄임
fb_range_number = [6000, 10000]
min_find_area = 3000 # 찾기 위한 최소 면적
find_range = 0.3 # 찾기 위한 contour의 중심 좌표의 범위
find_range_qr = 0.45 # qr을 찾기 위한 contour의 중심 좌표의 범위

center_range = 0.3 # 중심에 있다고 판단하기 위한 중심 좌표의 범위

aspect_ratio_range = 0.1 # 정면에 있다고 판단할 가로세로비율