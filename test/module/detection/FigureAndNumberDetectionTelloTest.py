from main.module.ai_model.NumberModel import *
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.enum.Color import *
from main.module.handler.NumberHandler import NumberHandler
from main.module.tello.detection.FigureAndNumberDetectionTello import FigureAndNumberDetectionTello
import logging
from djitellopy import Tello
# 로그 설정
logging.getLogger('djitellopy').setLevel(logging.WARNING)
tello = Tello()

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# img+=30
# n=number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
# print(n)
#
cam_width = 640
cam_height = 480
cam_params = CamParams(cam_width, cam_height)
pid_params = PIDParams([0.13, 0.13, 0], [0.13, 0.13, 0], [0.0001, 0.0001, 0])
range_params = RangeParams([80000, 120000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.1, 0.01, 0.3)
number_handler = NumberHandler(model)
figure_and_number_detection = FigureAndNumberDetectionTello(tello, cam_params, pid_params, range_params, number_handler)

img = cv2.imread("numbers.png")
read = figure_and_number_detection.find_number_and_contour_info_with_color(img, Color.BLUE, save=True, rectangle_contour=True)
print(read)

# img2 = cv2.imread("number2.png")
# read2 = figure_and_number_detection.find_number_and_contour_info_with_color_rectangle(img2, Color.GREEN, save=True, rectangle_contour=True)
# print(read2)
cv2.waitKey()
