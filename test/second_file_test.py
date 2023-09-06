from main.module.ai_model.NumberModel import *
import time
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.detection.RectangleRingDetection import RectangleRingDetection
from main.module.enum.Color import *
from main.module.enum.Direction import *
from main.module.enum.Figure import *
from main.module.handler.NumberHandler import NumberHandler
import logging
from djitellopy import Tello
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)
def match_color_and_number(frame, brightness=0):
    """
    R, G, B에 대해서 아래에 있는 숫자를 매치하고 오름차순으로 정렬하고 사각형의 x 좌표와 함께 반환
    :param tello: Tello 객체
    :param brightness: 이미지 밝기
    :return: [(숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상)], {'red':128...}
    """
    global number_handler
    img = cv2.resize(frame+brightness, (cam_width, cam_height))

    red=-1
    green=-1
    blue=-1

    # 색깔별로 매칭되는 값 구하기
    red, (r_x, r_y, r_w, r_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=True)
    green, (g_x, g_y, g_w, g_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
    blue, (b_x, b_y, b_w, b_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=True)




    # RGB 순서로 값 반환
    result = [(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)]
    result.sort()

    # 각 사각형들의 x 좌표 반환
    rectangle_x = {
        Color.RED : r_x,
        Color.GREEN : g_x,
        Color.BLUE : b_x
    }
    print(f'최종 숫자 : {result}')

    return result, rectangle_x

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.13, 0.13, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
range_params = RangeParams([100000, 150000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.01, 0.01, 0.3)
number_handler = NumberHandler(model)

img = cv2.imread("3_6_9.png")

rectangle_ring_detection = RectangleRingDetection(img, cam_params, pid_params, range_params, number_handler)
a, b = match_color_and_number(img, brightness=0)
print(a, b)