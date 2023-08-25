

from module.tello_detection_module import *
from module.config import *
import time
from djitellopy import Tello
import logging
logging.getLogger('djitellopy').setLevel(logging.WARNING)  # 또는 logging.ERROR 등


tello = Tello()
decoder = cv2.QRCodeDetector()
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
tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
time.sleep(2)
# 도형들이 위치한 높이까지 올라간다.
tello.move_up(90)
def mission(tello, color, figure):
    """
    1. 원하는 색상, 모양의 도형을 찾을 때까지 회전
    2. qr을 감지할 때까지 아래로 이동해서 qr 감지 및 내용 출력
    3. 뒤로 조금 물러남
    4. 이전에 감지한 도형의 높이까지 올라옴
    :param tello: Tello 객체
    :param color: 색상
    :param figure: 도형
    :return:
    """
    # 원하는 도형을 발견할 때까지 회전
    # move_until_find_figure(tello, color, figure, Direction.CLOCKWISE)
    tello_detection_figure(tello, color, figure)
    # 숫자 검출
    move_until_find_number(tello, Figure.NUMBER, Direction.DOWN)
    # 도형이 중간에 오도록 드론을 이동시킨 후 contour를 그려서 사진 촬영


    # 숫자 가운데로
    tello_detection_number(tello)

tello.send_command('cw 180')
move_until_find_figure(tello, Color.GREEN, Figure.RECTANGLE, Direction.UP)
tello_detection_figure(tello, Color.GREEN, Figure.RECTANGLE)
tello.move_forward(150)

move_until_find_figure(tello, Color.RED, Figure.RECTANGLE, Direction.CLOCKWISE)
tello_detection_figure(tello, Color.RED, Figure.RECTANGLE)
tello.move_forward(150)
