
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
import time
from djitellopy import Tello
import logging
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
figure_detection.move_until_find_figure(Color.RED, Figure.RECTANGLE, Direction.RIGHT, brightness=30)
figure_detection.tello_detection_figure(Color.RED, Figure.RECTANGLE, save=True, console=True)

tello.land()
