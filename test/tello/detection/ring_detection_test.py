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
range_params_2 = RangeParams([10000, 40000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.05, 1.0, 0.35)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params_2, range_params_2, number_handler)

pid_params_3 = PIDParams([0.1, 0.1, 0], [0.1, 0.1, 0], [0.0003, 0.0003, 0])
range_params_3 = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.05, 0.05, 0.3)
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
tello.move_up(50)
print('상승 완료')
time.sleep(2)




next = 9


# 첫 번째 색 찾을 때까지 회전
rectangle_ring_detection.move_until_find(Color.RED_REC, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)
# rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED, Figure.ANY, brightness=30)

# 회전하면서 정면을 봄
rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.RED_REC, Figure.RECTANGLE, brightness=30,
                                                                              save=False, console=False)

print('중심 맞춤')

# 중심 맞추고 사진 저장
rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY, brightness=30,
                                                                              save=True)

# 링 통과
tello.move_down(30)
tello.move_forward(270)
tello.move_up(30)
tello.rotate_clockwise(180)
time.sleep(1)

# 숫자 판단
frame_read = tello.get_frame_read()
my_frame = frame_read.frame
img = cv2.resize(my_frame + 30, (cam_width, cam_height))

# 숫자 찾을 때는 파란색 제거하지 않기
# 가끔 검은색 숫자가 사라질 때가 있음
find_num, contour_info = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
a, b, c, d = contour_info
img_temp = img.copy()
cv2.putText(img_temp, str(find_num), (a+c//2, b-10), cv2.FONT_ITALIC, 1.5, (0, 255, 255), 2)
cv2.imwrite("temp.png", img_temp)
print(f'blue number : {find_num}')
# 바로 앞에 있는 것이 찾는 숫자가 아닐 때
if next!=find_num:
    # 다른 애 찾기
    rectangle_ring_detection.move_until_find(Color.BLUE, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

    # 정면 보도록 회전
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.BLUE, Figure.RECTANGLE,
                                                                                  brightness=30,
                                                                                  save=True, console=False)
    print('중심 맞춤')
    # 숫자 판단
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (cam_width, cam_height))
    find_num, _ = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE, save=True,
                                                                                             rectangle_contour=False)

    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY, brightness=30,
                                                                                  save=False)
    # 링 통과
    tello.move_down(30)
    tello.move_forward(270)
    tello.move_up(30)
    tello.rotate_clockwise(180)
    # 그 다음 마지막으로 통과하기
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY, brightness=30,
                                                                                  save=True)

# 찾는 숫자가 맞다면 회전 안하고 바로 통과
else:
    x, y, w, h = contour_info
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
    cv2.putText(img, str(find_num), (x+w//2, y-10), cv2.FONT_ITALIC, 1.5, (0, 255, 255), thickness=2)
    cv2.imwrite("number.png", img)

    # 회전 안하고 중심 맞춤
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY, brightness=30,
                                                                                  save=False)
    # 링 통과
    tello.move_down(30)
    tello.move_forward(270)
    tello.move_up(30)
    tello.rotate_clockwise(180)

    # 다른 애 찾기
    rectangle_ring_detection.move_until_find(Color.BLUE, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

    # 정면 보도록 회전
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.BLUE, Figure.RECTANGLE,
                                                                                  brightness=30,
                                                                                  save=False, console=False)
    print('중심 맞춤')


    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                  brightness=30,
                                                                                  save=True)
    # 링 통과
    tello.move_down(30)
    tello.move_forward(270)
    tello.move_up(30)
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