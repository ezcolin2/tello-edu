import cv2
from module.enum.Color import *
from module.params.PIDParams import PIDParams
from module.params.RangeParams import RangeParams
from module.params.CamParams import CamParams
from module.handler.ImageHandler import ImageHandler
from module.handler.FigureHandler import FigureHandler
from module.handler.NumberHandler import NumberHandler
from module.ai_model.NumberModel import NumberModel
from module.tello.detection.FigureDetectionTello import FigureDetectionTello
from module.tello.detection.RectangleRingDetection import RectangleRingDetection
from module.enum.Color import *
from module.enum.Direction import *
from module.enum.Figure import *
import torch
import numpy as np
import logging
from djitellopy import Tello
import time

logging.getLogger('djitellopy').setLevel(logging.WARNING)

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
# detection_qr(tello)
tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
tello.move_up(50)
cam_params = CamParams(640, 480)
pid_params = PIDParams([0.1, 0.1, 0])
range_params = RangeParams([100000, 150000], [0.45 * cam_params.width, 0.55 * cam_params.height], 3000, 0.01, 0.01, 0.3)
# 원하는 색상 도형 찾아서 가운데로
rectangle_ring_detection = RectangleRingDetection(tello, cam_params, pid_params, range_params)
rectangle_ring_detection.move_until_find_rectangle_ring(Color.BLUE, Figure.RECTANGLE, Direction.RIGHT, brightness=30)
rectangle_ring_detection.tello_detection_rectangle_ring_with_no_rotate(Color.BLUE, Figure.RECTANGLE, brightness=30)