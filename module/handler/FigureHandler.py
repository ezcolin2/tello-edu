import cv2
import numpy as np
from module.enum.Color import *
from module.enum.Direction import *
from module.enum.Figure import *
from module.handler.ImageHandler import ImageHandler

class FigureHandler:
    def __init__(self):
        self.image_handler = ImageHandler()

    def find_color(self, img, color, figure, draw_contour=True):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 외접 사각형의 중심 좌표 반환
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
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)


        contour_info, objType = self._get_biggest_contour(img, mask, figure)

        stacked_img = self.image_handler.stackImages(0.6, [img, mask])
        return contour_info, objType

    def find_color_with_all_contour(self, img, color, figure, min_area):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 approx의 리스트 반환
        코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
        :param img: 이미지 원본
        :param color: Color enum
        :return: approx 리스트
        """

        # 이거는 BGR2HSV 사용해야 함.
        # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        cv2.imshow("mask", mask)
        return self._get_all_contours(img, mask, figure, min_area)

    def _get_biggest_contour(self, img, mask, figure, draw_contour=True):
        """
        mask로부터 contour를 얻어내서 도형의 중심 좌표 반환
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
        figureTypeList = []  # 모든 contour
        figureTypeArea = []  # contour 주위 직사각형의 넓이. 가장 큰 하나의 contour를 구하기 위함.

        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > 500:  # area가 500보다 클 때만 contour 그리기
                # cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                if count[figure.value][0] <= objType <= count[figure.value][1]:
                    # print("ok")
                    x, y, w, h = cv2.boundingRect(approx)
                    figureTypeList.append(objType)
                    figureTypeArea.append((x, y, w, h))
                # if figure.value == Figure.TRI.value and objType == 3:
                #     print('tri')
                # elif count[figure.value][0]<=objType <= count[figure.value][1]:
                #     print(f'circle : {objType}')
                #     print('circle')

                # # 도형 주변에 표시하고 contour 정보 리스트에 추가
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(figureTypeArea) != 0 and len(figureTypeList) != 0:
            # 면적 큰 순으로 정렬
            temp = sorted(figureTypeArea, key=lambda x: x[2] * x[3])
            # 가장 큰 하나의 contour의 x, y, w, h 가져옴
            x, y, w, h = temp[0]

            # 가장 큰 면적의 인덱스를 통해서 가장 큰 하나의 contour의 objType 알아내기
            max_idx = figureTypeArea.index(temp[0])
        if max_idx != -1:
            figure_type = figureTypeList[max_idx]
        if draw_contour and figure_type!=-1:
            cv2.rectangle(imgResult, (x, y), (x+w, y+h), (255, 0, 0), thickness=2)
            stacked_image = self.image_handler.stackImages(0.6, [imgResult, mask])
            cv2.imshow("image adn mask", stacked_image)

        return (x, y, w, h), figure_type

    def _get_all_contours(self, img, mask, figure, min_area):
        """
        원하는 도형의 특정 넓이 이상의 모든 contour를 외접 사각형 그려서 (x, y, w, h) 리스트 반환
        :param img: 이미지 원본 (웹캠)
        :param mask: 원하는 색만 추출해낸 이미지
        :return: approx 리스트
        """
        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(img, contours, -1, (255, 0, 0), thickness=2)
        # (x, y, w h) 리스트
        approx_list = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                if count[figure.value][0] <= objType <= count[figure.value][1]:
                    approx_list.append(approx)
        return approx_list
