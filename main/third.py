from main.module.ai_model.NumberModel import *
from main.module.ai_model.NumberModelV2 import *
import time
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.detection.NumberDetectionTello import NumberDetectionTello
from main.module.tello.detection.FigureAndNumberDetectionTello import FigureAndNumberDetectionTello
from main.module.tello.detection.RectangleRingDetection import RectangleRingDetection
from main.module.tello.detection.YoloDetectionTello import YoloDetectionTello

from main.module.enum.Color import *
from main.module.enum.Direction import *
from main.module.enum.Figure import *
from main.module.handler.NumberHandler import NumberHandler
from main.module.handler.NumberHandlerV2 import NumberHandlerV2
from main.module.handler.YoloHandler import YoloHandler
import logging
from djitellopy import Tello
from ultralytics import YOLO


def load(root, fileName):
    import os

    state_dict = torch.load(os.path.abspath(os.path.join(root, fileName + '.pth')))
    model = state_dict['model_state_dict']
    optimizer = state_dict['optimizer_state_dict']

    return model, optimizer


# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정
number_handler = NumberHandler(model)

# 숫자 인식 모델 생성
# number_model = NumberModelV2()  # 모델 클래스 정의로 변경
# msd, _ = load('./module/ai_model/', 'classifier')
# number_model.load_state_dict(msd)
# number_model.eval()
# number_handler = NumberHandlerV2(number_model)

# yolo 모델 생성
device = "cuda" if torch.cuda.is_available() else "cpu"
yolo_model = YOLO("./module/ai_model/yolo.pt", task = "segment")
yolo_model = yolo_model.to('cpu')
yolo_handler = YoloHandler(yolo_model)

# zone 1 도형 탐색 객체
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.08, 0.08, 0], [0.2, 0.2, 0], [0.0003, 0.0003, 0])
range_params = RangeParams([20000, 60000], [0.45 * cam_params.width, 0.55 * cam_params.height], 1000, 0.1, 0.1, 0.4)
figure_detection = FigureAndNumberDetectionTello(tello, cam_params, pid_params, range_params, number_handler)

# zone 2 링 탐색 객체
pid_params_2 = PIDParams([0.1, 0.1, 0], [0.13, 0.13, 0], [0.0005, 0.0005, 0])
range_params_2 = RangeParams([10000, 40000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.1, 1.0, 0.35)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params_2, range_params_2, number_handler)

# zone 2 링 회전 및 통과 객체
pid_params_3 = PIDParams([0.1, 0.1, 0], [0.1, 0.1, 0], [0.0003, 0.0003, 0])
range_params_3 = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.05, 0.05,
                             0.4)
rectangle_ring_rotate_detection = RectangleRingDetection(tello, cam_params, pid_params_3, range_params_3,
                                                         number_handler)

# zone 3 기체 탐지 객체
yolo_detection = YoloDetectionTello(tello, cam_params, pid_params, range_params, yolo_handler)


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
        contour_info, figure_type, = figure_detection.figure_handler.find_color_except_ring(img, color, Figure.ANY,
                                                                                            range_params.min_area,
                                                                                            draw_contour=True,
                                                                                            show=True)
        print(f'figure type : {figure_type}')
        if figure_type == 4:
            cv2.imwrite(f'images/{Color(color.value).name}_rectangle.png', img)
            break
        elif figure_type == 3:
            tello.move_up(40)
            tello.move_forward(160)
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
    predicted, _ = figure_detection.find_number_and_contour_info_with_color(img, color, save=True,
                                                                            rectangle_contour=True)
    # _, predicted = number_detection.number_handler.find_biggest_number(img, 500)
    tello.move_forward(60)
    print(f'예측값 : {predicted}')
    return predicted


def second(next):
    # 첫 번째 색 찾을 때까지 회전
    rectangle_ring_detection.move_until_find(Color.RED_REC, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

    # 회전하면서 정면을 봄
    p_aspect_ratio = rectangle_ring_detection.tello_detection_square_ring_with_no_rotate(Color.RED_REC, Figure.ANY,
                                                                                         brightness=30)
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.RED_REC, Figure.RECTANGLE,
                                                                                  p_aspect_ratio, brightness=30,
                                                                                  save=False, console=False)

    print('중심 맞춤')

    # 중심 맞추고 사진 저장
    rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY,
                                                                                  brightness=30,
                                                                                  save=True)

    # 링 통과
    tello.move_down(30)
    tello.move_forward(260)
    tello.rotate_clockwise(180)
    tello.move_down(20)
    time.sleep(1)

    # 숫자 판단
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (cam_width, cam_height))

    # 숫자 찾을 때는 파란색 제거하지 않기
    # 가끔 검은색 숫자가 사라질 때가 있음
    find_num, contour_info = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img,
                                                                                                        Color.RED_REC,
                                                                                                        save=False,
                                                                                                        rectangle_contour=False)
    a, b, c, d = contour_info
    img_temp = img.copy()
    cv2.putText(img_temp, str(find_num), (a + c // 2, b - 10), cv2.FONT_ITALIC, 1.5, (0, 255, 255), 2)
    print(f'blue number : {find_num}')
    tello.move_up(30)
    # 바로 앞에 있는 것이 찾는 숫자가 아닐 때
    if next != find_num:
        # 다른 애 찾기
        if b_x < r_x:
            tello.move_right(40)
        else:
            tello.move_left(40)
        rectangle_ring_detection.move_until_find(Color.BLUE, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

        # 정면 보도록 회전
        p_aspect_ratio = rectangle_ring_detection.tello_detection_square_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                             brightness=30)
        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.BLUE, Figure.RECTANGLE,
                                                                                      p_aspect_ratio,
                                                                                      brightness=30,
                                                                                      save=False, console=False)
        print('중심 맞춤')
        # 숫자 판단
        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame + 30, (cam_width, cam_height))
        find_num, _ = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE,
                                                                                                 save=True,
                                                                                                 rectangle_contour=False)

        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                      brightness=30,
                                                                                      save=False)
        # 링 통과
        tello.move_down(30)
        tello.move_forward(220)
        tello.move_up(30)
        tello.rotate_clockwise(180)
        # 그 다음 마지막으로 통과하기
        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                      brightness=30,
                                                                                      save=True)

        # 링 통과
        tello.move_down(30)
        tello.move_forward(220)

    # 찾는 숫자가 맞다면 회전 안하고 바로 통과
    else:
        x, y, w, h = contour_info
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), thickness=2)
        cv2.putText(img, str(find_num), (x + w // 2, y - 10), cv2.FONT_ITALIC, 1.5, (0, 255, 255), thickness=2)
        cv2.imwrite("Red_ring_number.png", img)

        # 회전 안하고 중심 맞춤
        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY,
                                                                                      brightness=30,
                                                                                      save=False)
        # 링 통과
        tello.move_down(30)
        tello.move_forward(220)


        # 다른 애 찾기
        if b_x < r_x:
            tello.move_left(40)
        else:
            tello.move_right(40)
        rectangle_ring_detection.move_until_find(Color.BLUE, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)

        # 정면 보도록 회전
        p_aspect_ratio = rectangle_ring_detection.tello_detection_square_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                             brightness=30)
        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v3(Color.BLUE, Figure.RECTANGLE,
                                                                                      p_aspect_ratio,
                                                                                      brightness=30,
                                                                                      save=False, console=False)
        print('중심 맞춤')

        rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.ANY,
                                                                                      brightness=30,
                                                                                      save=True)
        # 링 통과
        tello.move_down(30)
        tello.move_forward(220)

def third(direction:Direction):
    # 기체 찾을 때까지 이동
    yolo_detection.move_until_find(direction, brightness=30, save=True)

    # 중심
    yolo_detection.tello_detection_yolo_with_no_rotate(brightness=30, save=False)



def get_ring_location():
    """
    빨간색 링과 파란색 링을 찾아서 위치를 알아내는 함수
    :return: r_x, b_x
    """
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (cam_width, cam_height))
    blue_contour_info, _, = rectangle_ring_detection.figure_handler.find_color_with_ring(img, Color.BLUE, Figure.ANY,
                                                                                         1000, draw_contour=True)
    red_contour_info, _, = rectangle_ring_detection.figure_handler.find_color_with_ring(img, Color.RED_REC, Figure.ANY,
                                                                                        1000, draw_contour=True)
    cv2.imwrite("temp_ring_test.png", img)
    r_x = red_contour_info[0]
    b_x = blue_contour_info[0]
    return r_x, b_x


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
tello.move_up(80)
print('상승 완료')
tello.rotate_clockwise(170)
# 파란 링, 빨간 링 위치 파악
time.sleep(2)
r_x, b_x = get_ring_location()
print(r_x, b_x)
tello.move_down(30)
tello.rotate_clockwise(10)

first_number = first(90, 90, Color.BLUE)
second_number = first(90, 90, Color.GREEN)
third_number = first(90, 90, Color.RED)
tello.move_up(40)
tello.move_forward(120)
tello.move_down(20)

# 숫자 정렬
num_list = [first_number, second_number, third_number]
num_list.sort()
next_number = third_number + third_number - second_number
next_number = next_number%10

# zone 2
second(next_number)

# zone 3
direction = Direction.RIGHT if b_x < r_x else Direction.LEFT
third(direction)

# tello.move_up(60)
# tello.move_forward(100)
# # second(Color.BLUE)
#
# rectangle_ring_detection.move_until_find(Color.RED_REC, Figure.ANY, Direction.COUNTERCLOCKWISE, brightness=30)
# rectangle_ring_rotate_detection.tello_detection_rectangle_ring_with_rotate_v2(Color.RED_REC, Figure.RECTANGLE, brightness=30, save=False, console=False)
# print('중심 맞춤')
#
# # 중심 맞추고 사진 저장
# rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.RED_REC, Figure.ANY, brightness=30, save=True)
#
# # 링 통과
# tello.move_down(40)
# tello.move_forward(240)
tello.land()

