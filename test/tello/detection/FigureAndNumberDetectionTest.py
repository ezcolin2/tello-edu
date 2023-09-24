from main.module.ai_model.NumberModel import *
import time
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.detection.NumberDetectionTello import NumberDetectionTello
from main.module.tello.detection.FigureAndNumberDetectionTello import FigureAndNumberDetectionTello

from main.module.enum.Color import *
from main.module.enum.Direction import *
from main.module.enum.Figure import *
from main.module.handler.NumberHandler import NumberHandler
import logging
from djitellopy import Tello

model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../../../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# NumberHandler 인스턴스 생성
number_handler = NumberHandler(model)
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.07, 0.07, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
range_params = RangeParams([60000, 140000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.1, 0.1, 0.3)
number_handler = NumberHandler(model)

figure_detection = FigureAndNumberDetectionTello(None, cam_params, pid_params, range_params, number_handler)


cv2.waitKey()
# (x, y, w, h), predicted = number_handler.find_biggest_number(one_img, 500)
# cv2.rectangle(one_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
# cv2.putText(one_img, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)