from color_qr_detection_module import *
from tello_module import *

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

def tello_detection_figure(tello, color, figure):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param tello : Tello
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    # 가장 먼저 해당 도형을 찾기 위해 회전한다.

    p_error = 0
    while True:
        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame, (cam_width, cam_height))
        contour_info, figure_type = find_color(img, color, figure)
        print(contour_info, figure_type)
        cv2.imshow("Video", img)

        # 이미지 이름 정하기
        image_name="" # 저장할 이미지 이름
        if color==Color.RED:
            image_name+="red"
        elif color==Color.GREEN:
            image_name+="green"
        elif color==Color.BLUE:
            image_name+="blue"
        if figure==Figure.TRI:
            image_name+=" triangle"
        elif figure==Figure.CIRCLE:
            image_name+=" circle"

        # 객체 가운데로
        success, p_error = track_figure(tello, contour_info,  pid, p_error)
        # print(success, p_error)
        if success:
            cv2.imwrite(f"./images/{image_name}.png", img)
            break
        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def tello_detection_qr(tello):
    """
    Tello를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
    :param tello : Tello 객체
    :return: 없음
    """
    p_error = 0

    while True:
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (cam_width, cam_height))
        barcode_info, img = read_img(img)
        cv2.imshow("QR detection", img)
        contour_info = barcode_info[:4]
        barcode = barcode_info[4]
        if barcode==None:
            continue
        # 객체 가운데로
        success, p_error = track_figure(tello, contour_info, pid, p_error)
        if success:
            barcode_info = barcode.data.decode('utf-8')
            print(barcode_info)
            break
        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break