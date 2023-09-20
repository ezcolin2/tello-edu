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
pid_params = PIDParams([0.08, 0.08, 0], [0.2, 0.2, 0], [0.0003, 0.0003, 0])
range_params = RangeParams([20000, 60000], [0.45 * cam_params.width, 0.55 * cam_params.height], 1000, 0.1, 0.01, 0.3)
number_handler = NumberHandler(model)

pid_params_2 = PIDParams([0.13, 0.13, 0], [0.13, 0.13, 0], [0.0003, 0.0003, 0])
range_params_2 = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 1000, 0.05, 0.01, 0.3)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params_2, range_params_2, number_handler)

figure_detection = FigureAndNumberDetectionTello(tello, cam_params, pid_params, range_params, number_handler)

number_detection = NumberDetectionTello(tello, cam_params, pid_params, range_params, model)
def first(right, forward, color):
    # 일단 아무거나 찾음
    figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)

    # 중심 맞춤
    figure_detection.tello_detection_with_rotate(color, brightness=30)
    print('정면 바라보는 중')

    while True:
        figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)

        print('중심 맞추기 완료')

        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame + 30, (cam_width, cam_height))
        contour_info, figure_type, = figure_detection.figure_handler.find_color_except_ring(img, color, Figure.RECTANGLE, 500, draw_contour=True)
        if figure_type==4:
            cv2.imwrite(f'{Color(color.value).name}_rectangle.png', img)
            break
        elif figure_type==3:
            tello.move_up(40)
            tello.move_forward(120)
            tello.move_down(40)
            tello.rotate_clockwise(180)
            continue


        # 옆으로 이동
        tello.move_right(right)
        tello.move_forward(forward)

        # 회전
        tello.rotate_counter_clockwise(90)

        # 일단 아무거나 찾음
        figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)

    # 반복문이 끝났다는 것은 사각형을 찾은 것
    # 숫자를 찾을 때까지 아래로 이동

    # predicted = number_detection.move_until_find_number(Direction.DOWN, brightness=30)

    # 숫자 예측
    tello.move_back(40)
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (cam_width, cam_height))
    predicted = figure_detection.find_number_and_contour_info_with_color(img, color, save=True, rectangle_contour=True)
    # _, predicted = number_detection.number_handler.find_biggest_number(img, 500)
    print(f'예측값 : {predicted}')


    # # 일단 아무거나 찾음
    # figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)
    #
    # # 중심 맞춤
    # # figure_detection.tello_detection_with_rotate(color, brightness=30)
    # figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)
    #
    # # 옆으로 이동
    # tello.move_right(right)
    # tello.move_forward(forward)
    #
    # # 일단 아무거나 찾음
    # figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)
    #
    # # 중심 맞춤
    # # figure_detection.tello_detection_with_rotate(color, brightness=30)
    # figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)
    #
    # # 옆으로 이동
    # tello.move_right(right)
    # tello.move_forward(forward)
    #
    # # 일단 아무거나 찾음
    # figure_detection.move_until_find_figure(color, Direction.COUNTERCLOCKWISE, brightness=30)
    #
    # # 중심 맞춤
    # # figure_detection.tello_detection_with_rotate(color, brightness=30)
    # figure_detection.tello_detection_with_no_rotate(color, Figure.ANY, brightness=30)

def second(color):
    # 가로세로비율 맞춰서 찾음
    rectangle_ring_detection.move_until_find(color, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)
    # rectangle_ring_detection.tello_detection_rectangle_ring_with_rotate(color, Figure.RECTANGLE, brightness=30, save=False, console=False)

    # 중심 맞춤
    rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(color, Figure.ANY, brightness=30, save=True)

    # 링 통과
    tello.move_down(40)
    tello.move_forward(260)
    tello.move_up(40)

    # 180도 회전
    tello.rotate_clockwise(180)


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

# first(90, 90, Color.BLUE)
# first(90, 90, Color.GREEN)
# first(90, 90, Color.RED)

second(Color.BLUE)
tello.land()