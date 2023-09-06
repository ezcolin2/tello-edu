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

# Tello 객체 생성
tello = Tello()

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../../../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# img+=30
# 연결
tello.connect()
# 초기 세팅
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0
# 배터리 출력
print(tello.get_battery())

# stream 끔
tello.streamoff()
# detection_qr(tello)
tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
tello.move_up(50)
cam_params = CamParams(640, 480)
pid_params = PIDParams([0.13, 0.13, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
range_params = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.2, 0.01, 0.3)
number_handler = NumberHandler(model)

rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params, range_params, number_handler)
# 원하는 색상 도형 찾아서 가운데로
# rectangle_ring_detection.move_until_find_figure(Color.BLUE, Figure.RECTANGLE, Direction.RIGHT, brightness=30)
# rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.RECTANGLE, brightness=30, save=True)
# tello.move_down(40)
# tello.move_forward(200)
# tello.move_up(40)
# tello.rotate_clockwise(180)
# rectangle_ring_detection.move_until_find_figure(Color.GREEN, Figure.RECTANGLE, Direction.RIGHT, brightness=30)
# rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.GREEN, Figure.RECTANGLE, brightness=30, save=True)
# tello.move_down(40)
# tello.move_forward(200)

rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.GREEN, Figure.RECTANGLE, brightness=30, save=True)

tello.land()