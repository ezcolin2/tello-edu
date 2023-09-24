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
from main.module.handler.FigureHandler import FigureHandler
import logging
from djitellopy import Tello
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
print(f'남은 배터리 : {tello.get_battery()}')

# stream 끔
tello.streamoff()
# stream 킴
tello.streamon()
# 이륙
tello.send_rc_control(0, 0, 0, 0)
figure_handler = FigureHandler()
center_percentage = 0.1
# 사각형 링 감지 테스트
while True:

    print('중심 맞추기 완료')

    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (640, 480))
    contour_info, figure_type, = figure_handler.find_color(img, Color.BLUE, Figure.ANY, 500,
                                                                                        draw_contour=True)
    x, y, w, h = contour_info
    if x!=0 and y!=0 and w!=0 and h!=0:
        cv2.putText(img, f'area : {w*h}, aspect : {w/h}', (x, y),cv2.FONT_ITALIC, fontScale=0.5, color= (0,255,255))
        print(f'figure type : {figure_type}')
        cv2.rectangle(
            img,
            (int(320-640*center_percentage), int(240-480*center_percentage)),
            (int(320+640*center_percentage), int(240+480*center_percentage)),
            (0, 0, 0),
            2
        )
    cv2.imshow("video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


