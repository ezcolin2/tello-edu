from main.module.ai_model.NumberModel import *
import time
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.detection.RectangleRingDetection import RectangleRingDetection
from main.module.tello.detection.FigureAndNumberDetectionTello import FigureAndNumberDetectionTello
from main.module.enum.Color import *
from main.module.enum.Direction import *
from main.module.enum.Figure import *
from main.module.handler.NumberHandler import NumberHandler
import logging
from djitellopy import Tello
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# img+=30
# n=number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
# print(n)
#
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.1, 0.1, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
range_params = RangeParams([60000, 140000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.1, 0.1, 0.3)
number_handler = NumberHandler(model)

figure_detection = FigureAndNumberDetectionTello(tello, cam_params, pid_params, range_params, number_handler)
def first(right, forward, color):
    # 일단 아무거나 찾음
    figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)

    # 중심 맞춤
    figure_detection.tello_detection_with_rotate(color, brightness=30)
    print('정면 바라보는 중')
    figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)

    # 옆으로 이동
    tello.move_right(right)
    tello.move_forward(forward)

    # 일단 아무거나 찾음
    figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)

    # 중심 맞춤
    # figure_detection.tello_detection_with_rotate(color, brightness=30)
    figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)

    # 옆으로 이동
    tello.move_right(right)
    tello.move_forward(forward)

    # 일단 아무거나 찾음
    figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)

    # 중심 맞춤
    # figure_detection.tello_detection_with_rotate(color, brightness=30)
    figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)

    # 옆으로 이동
    tello.move_right(right)
    tello.move_forward(forward)


# 연결
tello.connect()
print("연결 완료")
# 초기 세팅
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0
# 배터리 출력
print(f'남은 배터리 : {tello.get_battery()}')

# stream 끔
tello.streamoff()
# stream 킴
tello.streamon()
# 이륙
tello.send_rc_control(0, 0, 0, 0)
tello.takeoff()
print('이륙')
tello.move_up(60)
time.sleep(2)

first(80, 60, Color.RED)
tello.land()