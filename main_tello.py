

from module.tello_detection_module import *
from module.config import *
import time
from djitellopy import Tello
import logging
logging.getLogger('djitellopy').setLevel(logging.WARNING)  # 또는 logging.ERROR 등


tello = Tello()
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
tello.move_up(30)
time.sleep(2)
move_until_find_figure(tello, Color.GREEN, Figure.RECTANGLE, Direction.RIGHT, brightness=30)
tello_detection_figure(tello, Color.GREEN, Figure.RECTANGLE, save=True, console=True)

tello.land()
