import logging
import time
from djitellopy import Tello
from module.enum.Color import *
from module.enum.Direction import *
from module.enum.Figure import *
from module.params.PIDParams import PIDParams
from module.params.RangeParams import RangeParams
from module.params.CamParams import CamParams
from module.tello.detection.FigureDetectionTello import FigureDetectionTello
from module.tello.detection.QRDetectionTello import QRDetectionTello
cam_params = CamParams(640, 480)
pid_params = PIDParams([0.1, 0.1, 0])
range_params = RangeParams([6000, 10000], [0.4 * cam_params.width, 0.6 * cam_params.height], 3000, 0.3, 0.1, 0.3)


logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()
figure_detection = FigureDetectionTello(tello, cam_params, pid_params, range_params)
qr_detection = QRDetectionTello(tello, cam_params, range_params, pid_params)
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
time.sleep(2)
# 도형들이 위치한 높이까지 올라간다.
tello.move_up(30)
# detection_figure(tello, Color.RED, Figure.TRI)

def mission(tello, color, figure):
    """
    1. 원하는 색상, 모양의 도형을 찾을 때까지 회전
    2. qr을 감지할 때까지 아래로 이동해서 qr 감지 및 내용 출력
    3. 뒤로 조금 물러남
    4. 이전에 감지한 도형의 높이까지 올라옴
    참고로 qr 감지는 CIRCLE 일 때만 진행함
    :param tello: Tello 객체
    :param color: 색상
    :param figure: 도형
    :return:
    """
    # 원하는 도형을 발견할 때까지 회전
    figure_detection.move_until_find_figure(color, figure, Direction.COUNTERCLOCKWISE, brightness=30)

    # 도형이 중간에 오도록 드론을 이동시킨 후 contour를 그려서 사진 촬영
    figure_detection.tello_detection_figure(color, figure, brightness=30)

    # 도형이 원 일때만 qr 감지
    # qr이 잘 보이도록 아래로 조금 가서 qr 인식
    if figure == Figure.CIRCLE:
        qr_detection.move_until_find_qr(Direction.DOWN, brightness=30)
        time.sleep(1)
        qr_detection.tello_detection_qr(brightness=30)

        # 도형들이 있는 높이로 이동
        # tello.move_back(60)
        time.sleep(1)
        figure_detection.move_until_find_figure(color, figure, Direction.UP, brightness=30)
        time.sleep(1)
"""
    Flag 1 수행
"""
mission(tello, Color.RED, Figure.CIRCLE)

"""
    Flag 2 수행
"""
mission(tello, Color.GREEN, Figure.CIRCLE)
"""
    Flag 3 수행
"""
mission(tello, Color.BLUE, Figure.TRI)
tello.move_up(100)
tello.move_forward(200)
tello.move_down(100)
mission(tello, Color.BLUE, Figure.CIRCLE)

tello.land()