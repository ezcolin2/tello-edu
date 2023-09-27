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
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()


device = "cuda" if torch.cuda.is_available() else "cpu"
yolo_model = YOLO("yolo.pt", task = "segment")
yolo_model = yolo_model.to('cuda')
yolo_handler = YoloHandler(yolo_model)
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
while True:
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame + 30, (640, 480))
    yolo_handler.get_object_xyxy(img, draw_rectangle=True)
    cv2.imshow("asdf", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break