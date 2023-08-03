import colorama

from detection import *
from djitellopy import Tello
import time


webcam_cap = cv2.VideoCapture(0)
webcam_cap.set(3, cam_width) # width 세팅
webcam_cap.set(4, cam_height) # height 세팅
decoder = cv2.QRCodeDetector()

# detection_figure(webcam_cap, Color.RED, Figure.TRI)
detection_qr(webcam_cap, decoder)