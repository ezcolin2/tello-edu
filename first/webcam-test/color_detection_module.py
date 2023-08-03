import time

import cv2
import numpy as np
from config import *
def findColor(img, color, figure):
    """
    인자로 들어온 Color에 해당하는 도형이 있으면 도형을 포함하는 최소 사각형의 중심 좌표 반환
    :param img: 이미지 원본 (웹캠)
    :param color: Color enum
    :return: 도형 중심 좌표 (x, y)와 점 개수
    """

    # 이거는 BGR2HSV 사용해야 함.
    # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([myColors[color.value][0:3]])
    upper = np.array([myColors[color.value][3:6]])
    # print(lower, upper)
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("sdf", mask)
    contour_info, objType = getContours(img, mask, figure)
    # print(is_center(x, y))
    # print(x, y)
    return contour_info, objType



def getContours(img, mask, figure):
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
        if area > 100: # area가 500보다 클 때만 contour 그리기
            cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
            # curve 길이 구하기
            peri = cv2.arcLength(cnt, True)

            # 점 위치
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            objType = len(approx)
            if objType == count[figure.value]:
                print("ok")
                x, y, w, h = cv2.boundingRect(approx)
                figureTypeList.append(objType)
                figureTypeArea.append((x, y, w, h))
            if figure.value == Figure.TRI.value and objType==3:
                print('tri')
            # if figure.value==Figure.TRI.value:
            #     print('tri')
            elif figure.value == Figure.CIRCLE.value and objType>=4:
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

