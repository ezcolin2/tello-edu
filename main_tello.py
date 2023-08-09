
from module.tello_detection_module import *
from module.config import *
from djitellopy import Tello
import time

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
# detection_qr(tello)
tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
time.sleep(2)

# 도형들이 위치한 높이까지 올라간다.
tello.move_up(60)
# detection_figure(tello, Color.RED, Figure.TRI)

"""
    Flag 1 수행
"""

# 원하는 도형을 발견할 때까지 회전
rotate_until_find(tello, Color.RED, Figure.TRI)

# 도형이 중간에 오도록 드론을 이동시킨 후 contour를 그려서 사진 촬영
tello_detection_figure(tello, Color.RED, Figure.TRI)

# qr이 잘 보이도록 아래로 조금 가서 qr 인식
tello.move_down(30)
time.sleep(1)
tello_detection_qr(tello)

# 도형들이 있는 높이로 이동
tello.move_up(60)
time.sleep(1)

"""
    Flag 2 수행
"""

# 원하는 도형을 발견할 때까지 회전
rotate_until_find(tello, Color.GREEN, Figure.CIRCLE)

# 도형이 중간에 오도록 드론을 이동시킨 후 contour를 그려서 사진 촬영
tello_detection_figure(tello, Color.GREEN, Figure.CIRCLE)

# qr이 잘 보이도록 아래로 조금 가서 qr 인식
tello.move_down(60)
time.sleep(1)
tello_detection_qr(tello)

# 도형들이 있는 높이로 이동
tello.move_up(60)
time.sleep(1)

"""
    Flag 3 수행
"""

# 원하는 도형을 발견할 때까지 회전
rotate_until_find(tello, Color.RED, Figure.CIRCLE)

# 도형이 중간에 오도록 드론을 이동시킨 후 contour를 그려서 사진 촬영
tello_detection_figure(tello, Color.RED, Figure.CIRCLE)

# qr이 잘 보이도록 아래로 조금 가서 qr 인식
tello.move_down(30)
time.sleep(1)

# 도형들이 있는 높이로 이동
tello.land()