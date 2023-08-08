from color_detection_module import *
import pyzbar.pyzbar as pyzbar

import time
def detection_figure(webcam_cap, color, figure):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param webcam_cap : VideoCapture
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    # 가장 먼저 해당 도형을 찾기 위해 회전한다.

    p_error = 0
    while True:
        # success는 성공 여부, img는 이미지
        _, img = webcam_cap.read()
        contour_info, figureType = findColor(img, color, figure)
        print(contour_info, figureType)
        cv2.imshow("Video", img)


        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("hello.png", img)
            break


def detection_qr(webcam_cap):
    """
    VideoCatprue를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
    :param webcam_cap : VideoCapture
    :return: 없음
    """
    while True:
        success, img = webcam_cap.read()
        print(success)
        barcode_info, img = read_img(img)
        img = cv2.resize(img, (cam_width, cam_height))
        cv2.imshow("QR", img)

        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def read_img(img):
    """
    이미지를 받아서 qr이 있다면 contour를 그리고 그 내용을 contour 위에 출력
    :param img : 이미지
    :return : (x, y, w, h, barcode), img
    """
    # 바코드 정보 decoding
    barcodes = pyzbar.decode(img)
    print(barcodes)
    # 바코드 정보가 여러개 이기 때문에 하나씩 해석
    arr=[] # 바코드 좌표 정보
    for barcode in barcodes:
        # 바코드 rect정보
        x, y, w, h = barcode.rect
        arr.append((x, y, w, h, barcode))
        # 바코드 데이터 디코딩
        barcode_info = barcode.data.decode('utf-8')
        # print(barcode_info)
        # 인식한 바코드 사각형 표시
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 인식한 바코드 사각형 위에 글자 삽입
        cv2.putText(img, barcode_info, (x , y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
    arr.sort(key = lambda x : x[2]*x[3])
    print("arr", arr)
    if len(arr)==0: # 비어있다면
        arr.append((-1, -1, -1, -1, None))
    print(arr)
    return arr[0], img
