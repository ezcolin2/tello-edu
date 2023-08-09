import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from module.config import *

def find_color(img, color, figure):
    """
    인자로 들어온 Color에 해당하는 도형이 있으면 도형을 포함하는 최소 사각형의 중심 좌표 반환
    코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
    :param img: 이미지 원본
    :param color: Color enum
    :return: contour 정보 (x, y, w, h)와 점 개수
    """

    # 이거는 BGR2HSV 사용해야 함.
    # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([myColors[color.value][0:3]])
    upper = np.array([myColors[color.value][3:6]])
    # print(lower, upper)
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("mask", mask)
    contour_info, objType = get_contours(img, mask, figure)
    # print(is_center(x, y))
    # print(x, y)
    return contour_info, objType

def find_qr(img, decoder):
    """
    이미지에서 qr 코드를 발견해서 읽음
    :param img : 이미지 원본 (웹캠)
    :param decoder : QRCodeDetector 객체
    :return : qr 코드 감지 여부 반환
    """
    data, points, _ = decoder.detectAndDecode(img)

    if len(data) !=0 and points is not None:
        # print('Decoded data: ' + data)
        # print(f'point : {points}')
        return True

        points = points[0]
        for i in range(len(points)):
            pt1 = [int(val) for val in points[i]]
            pt2 = [int(val) for val in points[(i + 1) % 4]]
            cv2.line(img, pt1, pt2, color=(255, 0, 0), thickness=3)

        cv2.imshow('Detected QR code', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    return False

def get_contours(img, mask, figure):
    """
    mask로부터 contour를 얻어내서 img에 그린 후 도형의 중심 좌표 반환
    하나의 도형만 감지
    정확도를 위해서 여러 개의 contour를 찾는다면 가장 면적이 큰 것만 가져옴
    :param img: 이미지 원본 (웹캠)
    :param mask: 원하는 색만 추출해낸 이미지
    :return: 도형 중심 좌표 (x, y)와 얻은 모든 contour의 점 개수
    """
    # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    imgResult = img.copy()
    x, y, w, h = 0, 0, 0, 0
    figureTypeList = [] # 모든 contour
    figureTypeArea = [] # contour 주위 직사각형의 넓이. 가장 큰 하나의 contour를 구하기 위함.

    max_idx = -1
    figure_type = -1
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # minimum threshold를 정하면 noise를 줄일 수 있음
        if area > 300: # area가 500보다 클 때만 contour 그리기
            cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
            # curve 길이 구하기
            peri = cv2.arcLength(cnt, True)

            # 점 위치
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objType = len(approx)
            if count[figure.value][0] <= objType <= count[figure.value][1]:
                print("ok")
                x, y, w, h = cv2.boundingRect(approx)
                figureTypeList.append(objType)
                figureTypeArea.append((x, y, w, h))
            if figure.value == Figure.TRI.value and objType == 3:
                print('tri')
            # if figure.value==Figure.TRI.value:
            #     print('tri')
            elif count[figure.value][0]<=objType <= count[figure.value][1]:
            # elif figure.value == Figure.CIRCLE.value and objType>=4:
                print(f'circle : {objType}')
                print('circle')

            # # 도형 주변에 표시하고 contour 정보 리스트에 추가

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if len(figureTypeArea)!=0 and len(figureTypeList)!=0:
        # 면적 큰 순으로 정렬
        temp = sorted(figureTypeArea, key = lambda x : x[2]*x[3])
        # 가장 큰 하나의 contour의 x, y, w, h 가져옴
        x, y, w, h = temp[0]

        # 가장 큰 면적의 인덱스를 통해서 가장 큰 하나의 contour의 objType 알아내기
        max_idx = figureTypeArea.index(temp[0])
    print(max_idx)
    if max_idx != -1:
        print(max_idx)
        figure_type = figureTypeList[max_idx]
    return (x, y, w, h), figure_type

def read_img(img):
    """
    이미지를 받아서 qr이 있다면 contour를 그리고 그 내용을 contour 위에 출력
    코드 참조 : https://github.com/hyunseokjoo/detecting_BarAndQR
    :param img : 이미지
    :return : (x, y, w, h, barcode), img
    """
    # 바코드 정보 decoding
    barcodes = pyzbar.decode(img)
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
    if len(arr)==0: # 비어있다면
        arr.append((-1, -1, -1, -1, None))
    return arr[0], img
