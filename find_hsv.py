import time
from module.params import *
from module.tello_detection_module import *
from djitellopy import Tello
import logging
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

while True:
    frame_read = tello.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame + 30, (cam_width, cam_height))
    cv2.imshow("abc", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
