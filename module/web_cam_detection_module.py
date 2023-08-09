from module.image_processing_module import *
from module.tello_tracking_module import *

import time
def web_cam_detection_figure(webcam_cap, color, figure):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param webcam_cap : VideoCapture
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    while True:
        # success는 성공 여부, img는 이미지
        _, img = webcam_cap.read()
        contour_info, figureType = find_color(img, color, figure)
        print(contour_info, figureType)
        cv2.imshow("Video", img)


        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def web_cam_detection_qr(webcam_cap):
    """
    VideoCatprue를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
    :param webcam_cap : VideoCapture
    :return: 없음
    """
    while True:
        success, img = webcam_cap.read()
        barcode_info, img = read_img(img)
        img = cv2.resize(img, (cam_width, cam_height))
        cv2.imshow("QR", img)

        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

