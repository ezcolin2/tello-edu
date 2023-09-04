from module.ai_model.NumberModel import *
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


def match_color_and_number(tello: Tello, brightness=0):
    """
    R, G, B에 대해서 아래에 있는 숫자를 매치하고 오름차순으로 정렬하고 사각형의 x 좌표와 함께 반환
    :param tello: Tello 객체
    :param brightness: 이미지 밝기
    :return: [(숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상)], {'red':128...}
    """
    global number_handler
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    red=-1
    green=-1
    blue=-1

    # 색깔별로 매칭되는 값 구하기
    red, (r_x, r_y, r_w, r_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
    green, (g_x, g_y, g_w, g_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=False)
    blue, (b_x, b_y, b_w, b_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=False)



    print(f'숫자 인식 : {[(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)]}')

    # 만약 인지를 못했다면
    if red==-1 or green==-1 or blue==-1:
        #뒤로 가서 한 번 더 체크
        tello.move_back(20)

        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame + brightness, (cam_width, cam_height))

        # 색깔별로 매칭되는 값 구하기
        red, (r_x, r_y, r_w, r_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.RED,
                                                                                                               save=True,
                                                                                                               rectangle_contour=False)
        green, (g_x, g_y, g_w, g_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.GREEN,
                                                                                                                 save=True,
                                                                                                                 rectangle_contour=False)
        blue, (b_x, b_y, b_w, b_h) = rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, Color.BLUE,
                                                                                                                save=True,
                                                                                                                rectangle_contour=False)

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


tello = Tello()

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# img+=30
# n=number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
# print(n)
#
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.1, 0.1, 0])
range_params = RangeParams([100000, 150000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.01, 0.01, 0.3)
number_handler = NumberHandler(model)
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params, range_params, number_handler)


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
# tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
# tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
print('이륙')
time.sleep(2)
# 도형들이 위치한 높이까지 올라간다.
tello.move_up(30)
print('위로 이동')
time.sleep(2)

# 오름차순 정렬
result, rectangle_x = match_color_and_number(tello, brightness=30)
tello.land()
print(result)

# 현재 위치
# 1은 왼쪽 사각형, 2는 가운데 사각형, 3은 오른쪽 사각형
current_location=2
# 순서대로 미션 진행
for i, color in enumerate(Color):

    """
    from zone 1 to zone 2
    """
    # 찾을 사각형의 위치를 알아냄
    location = rectangle_x[result[i][1]]

    # 현재 위치와 찾을 위치가 동일하지 않은 경우에만 이동
    if location != current_location:
        # 왼쪽 이동
        if location<current_location:
            # 숫자에 매치되는 색상을 찾음
            rectangle_ring_detection.move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.LEFT, brightness=30)

        # 오른쪽 이동
        else:
            rectangle_ring_detection.move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.RIGHT, brightness=30)

    # 해당 위치로 이동했으면 해당 사각형 아래의 숫자 bounding rectangle 그려서 저장
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+30, (cam_width, cam_height))
    rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, result[i][1], save=True, rectangle_contour=False)

    # 해당 색상이 가운데로 오게 함
    rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(tello, result[i][1], Figure.ANY, brightness=30)

    # 링 통과
    tello.move_down(20)
    tello.move_forward(100)

    # 180도 회전
    tello.rotate_clockwise(180)

    """
    from zone 2 to zone 1
    """
    # 찾을 사각형의 위치를 알아냄
    location = rectangle_x[result[i][1]]

    # 현재 위치와 찾을 위치가 동일하지 않은 경우에만 이동
    if location != current_location:
        # 왼쪽 이동
        if location > current_location:
            # 숫자에 매치되는 색상을 찾음
            rectangle_ring_detection.move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.LEFT,
                                                            brightness=30)

        # 오른쪽 이동
        else:
            rectangle_ring_detection.move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.RIGHT,
                                                            brightness=30)
    # 해당 위치로 이동했으면 해당 사각형 아래의 숫자 bounding rectangle 그려서 저장
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+30, (cam_width, cam_height))
    rectangle_ring_detection.find_number_and_contour_info_with_color_rectangle(img, result[i][1], save=True, rectangle_contour=False)

    # 해당 색상이 가운데로 오게 함
    rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(tello, result[i][1], Figure.ANY, brightness=30, save=True)

    # 링 통과
    tello.move_down(20)
    tello.move_forward(100)

    # 180도 회전
    tello.rotate_clockwise(180)

