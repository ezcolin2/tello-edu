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

# number handler 생성
number_handler = NumberHandler(model)

# # rectangle ring detection 생성
cam_params = CamParams(640, 480)
# pid_params = PIDParams([0.13, 0.13, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
# range_params = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.2, 0.01, 0.3)
# rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params, range_params, number_handler)
#
# # ring detection rotate 생성
# range_params_rotate = RangeParams([80000, 120000], [0.4 * cam_params.width, 0.6 * cam_params.height], 1000, 0.2, 0.1, 0.4)
# ring_detection_rotate = RectangleRingDetection(tello, cam_params, pid_params, range_params_rotate, number_handler)

pid_params_2 = PIDParams([0.1, 0.1, 0], [0.13, 0.13, 0], [0.0003, 0.0003, 0])
range_params_2 = RangeParams([10000, 40000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.03, 1.0, 0.35)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params_2, range_params_2, number_handler)

pid_params_3 = PIDParams([0.1, 0.1, 0], [0.1, 0.1, 0], [0.0003, 0.0003, 0])
range_params_3 = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.05, 0.05, 0.3)
rectangle_ring_rotate_detection = RectangleRingDetection(tello, cam_params, pid_params_3, range_params_3, number_handler)



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
tello.move_up(90)
# 첫 번째 색 찾을 때까지 회전
p_aspect_ratio = rectangle_ring_detection.move_until_find(Color.RED_REC, Figure.ANY, Direction.COUNTERCLOCKWISE,
                                                          brightness=30)

# 회전하면서 정면을 봄
# p_aspect_ratio = rectangle_ring_detection.tello_detection_square_ring_with_no_rotate(Color.RED_REC, Figure.ANY, brightness=30)
rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.RED_REC, Figure.RECTANGLE,
                                                                              p_aspect_ratio, brightness=30,
                                                                              save=False, console=False)
print('완료')
tello.land()