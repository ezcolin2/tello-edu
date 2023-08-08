
from web_cam_detection_module import *
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
# detection_figure(tello, Color.RED, Figure.TRI)
"""
    처음 빨간색 원을 감지할 때까지 회전하면서 올라온다.
    빨간색 원을 감지한 횟수가 일정 횟수 이상이면 빨간색 원을 감지했다고 판단하고 움직임을 멈춘다.
"""

cnt = 0
while cnt<4:
    frame_read = tello.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (cam_width, cam_height))
    cv2.imshow("asdf", img)
    contour_info ,figureType = find_color(img, Color.RED, Figure.TRI)
    print(contour_info, figureType)
    x, y, w, h = contour_info
    if cam_width*0.2 <= x+w//2 <= cam_width*0.8 and cam_height*0.2 <= y+h//2 <= cam_height*0.8 and figureType >=0 and w*h>5000:
        cnt+=1
        tello.send_rc_control(0,0,0,0)
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    tello.send_rc_control(0, 0, 20, 0)
print("감지 ")
cv2.destroyAllWindows()
# tello.land()
"""
    Flag 1 미션 수행 
"""

tello_detection_figure(tello, Color.RED, Figure.TRI)
cv2.destroyAllWindows()
# 만약 qr을 잘 인식 못하면 아래로 조금 감
# tello.move_down(10)
# Flag 1 qr 코드 인식
tello.send_rc_control(0, 0, 0, 0)

# 아래로 조금 가서 qr 인식
tello.move_down(30)
tello_detection_qr(tello)
cv2.destroyAllWindows()
# 다음 인식을 위해 뒤로 조금 감
tello.move_back(60)
time.sleep(2)
tello.move_up(60)
tello.send_rc_control(0, 0, 0, 0)