from main.module.ai_model.NumberModel import *
import time
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.detection.NumberDetectionTello import NumberDetectionTello
from main.module.tello.detection.FigureAndNumberDetectionTello import FigureAndNumberDetectionTello
from main.module.tello.detection.RectangleRingDetection import RectangleRingDetection

from main.module.enum.Color import *
from main.module.enum.Direction import *
from main.module.enum.Figure import *
from main.module.handler.NumberHandler import NumberHandler
import logging
from djitellopy import Tello
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()



# img+=30
# n=number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
# print(n)
#
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경

model.load_state_dict(torch.load("../../../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

number_handler = NumberHandler(model)

pid_params_2 = PIDParams([0.1, 0.1, 0], [0.13, 0.13, 0], [0.0003, 0.0003, 0])
range_params_2 = RangeParams([10000, 40000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.1, 1.0, 0.35)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params_2, range_params_2, number_handler)

pid_params_3 = PIDParams([0.1, 0.1, 0], [0.1, 0.1, 0], [0.0003, 0.0003, 0])
range_params_3 = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.05, 0.04, 0.3)
rectangle_ring_rotate_detection = RectangleRingDetection(tello, cam_params, pid_params_3, range_params_3, number_handler)



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
# tello.move_up(50)
print('상승 완료')
time.sleep(2)

# 첫 번째 색 찾을 때까지 회전
rectangle_ring_detection.move_until_find(Color.RED_REC, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

# 회전하면서 정면을 봄
p_aspect_ratio = rectangle_ring_detection.tello_detection_square_ring_with_no_rotate(Color.RED_REC, Figure.ANY,
                                                                                     brightness=30)
rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.RED_REC, Figure.RECTANGLE,
                                                                              p_aspect_ratio, brightness=30,
                                                                              save=False, console=False)
rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY,
                                                                              brightness=30,
                                                                              save=True)
# 링 통과
tello.move_down(35)
tello.move_forward(220)
tello.move_up(35)
tello.rotate_clockwise(180)
tello.land()


# 정면 보면 숫자 판단
# frame_read = tello.get_frame_read()
# my_frame = frame_read.frame
# img = cv2.resize(my_frame + 30, (cam_width, cam_height))
# num, _ = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE,
#                                                                            save=True,
#                                                                            rectangle_contour=False)
#
# # 숫자 저장
# if save_number:
#     tello.move_down(30)
#     frame_read = tello.get_frame_read()
#     my_frame = frame_read.frame
#     img = cv2.resize(my_frame + 30, (cam_width, cam_height))
#     rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, color,
#                                                                                save=True,
#                                                                                rectangle_contour=False)
#     tello.move_up(30)