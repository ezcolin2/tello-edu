import colorama

from detection import *


webcam_cap = cv2.VideoCapture(0)
webcam_cap.set(3, cam_width) # width 세팅
webcam_cap.set(4, cam_height) # height 세팅

detection_figure(webcam_cap, Color.RED, Figure.TRI)
detection_qr(webcam_cap)