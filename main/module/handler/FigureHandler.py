import cv2
import numpy as np
from main.module.enum.Color import *
from main.module.enum.Figure import *
from main.module.handler.ImageHandler import ImageHandler
class FigureHandler:
    def __init__(self):
        self.image_handler = ImageHandler()

    def find_color(self, img, color, figure, min_area, draw_contour=False):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 외접 사각형의 중심 좌표 반환
        코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
        :param img: 이미지 원본
        :param color: Color enum
        :return: contour 정보 (x, y, w, h)와 점 개수
        """

        # 이거는 BGR2HSV 사용해야 함.
        # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.

        # 빨간색이 감지가 잘 안 돼서 빨간색 감지할 때는 초록, 파랑색을 없앰
        if color == Color.RED_REC:
            img[:] = self.image_handler.delete_specific_color(img, Color.BLUE)[:]

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=3)
        cv2.imshow("maks", mask)
        contour_info, objType = self._get_biggest_contour(img, mask, figure, min_area, draw_contour=draw_contour, show=True)

        return contour_info, objType

    def find_color_except_ring(self, img, color, figure, min_area, draw_contour=False, show=False):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 (링 제외) 외접 사각형의 중심 좌표 반환
        코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
        :param img: 이미지 원본
        :param color: Color enum
        :return: contour 정보 (x, y, w, h)와 점 개수
        """

        # 이거는 BGR2HSV 사용해야 함.
        # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.

        # 빨간색이 감지가 잘 안 돼서 빨간색 감지할 때는 초록, 파랑색을 없앰
        if color == Color.RED_REC:
            img[:] = self.image_handler.delete_specific_color(img, Color.BLUE)

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)


        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgResult = img.copy()
        x, y, w, h = 0, 0, 0, 0
        figureTypeList = []  # 모든 contour
        figureTypeArea = []  # contour 주위 직사각형의 넓이. 가장 큰 하나의 contour를 구하기 위함.
        figureCntList = []

        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # 이미지 원본에 contour 그리기
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                if count[figure.value][0] <= objType <= count[figure.value][1]:

                    # print("ok")
                    x_t, y_t, w_t, h_t = cv2.boundingRect(approx)

                    # ring이 아니고 가로세로 비율이 일정 비율 이상일 때만 추가
                    if not self.is_ring(color, figure, img[y_t: y_t + h_t, x_t: x_t + w_t]) and w_t!=0 and h_t!=0 and min(w_t, h_t)/max(w_t, h_t)>=0.2:
                        # if draw_contour:
                        #     cv2.drawContours(img, cnt, -1, (0, 255, 255), 3)
                        figureTypeList.append(objType)
                        figureTypeArea.append((x_t, y_t, w_t, h_t))
                        figureCntList.append(cnt)
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
            x, y, w, h = temp[-1]

            # 가장 큰 면적의 인덱스를 통해서 가장 큰 하나의 contour의 objType 알아내기
            max_idx = figureTypeArea.index((x, y, w, h))
        if max_idx != -1:
            figure_type = figureTypeList[max_idx]
        if draw_contour and figure_type!=-1:
            # cv2.rectangle(imgResult, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            # cv2.putText(imgResult, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            cv2.putText(img, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            cv2.drawContours(img, figureCntList[max_idx], -1, (0, 255, 255), 3)
            stacked_image = self.image_handler.stackImages(0.6, [img, mask])
            if show:
                cv2.imshow("image adn mask", stacked_image)

        return (x, y, w, h), figure_type
    def find_color_with_ring(self, img, color, figure, min_area, draw_contour=False, show=False):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 (링 제외) 외접 사각형의 중심 좌표 반환
        코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
        :param img: 이미지 원본
        :param color: Color enum
        :return: contour 정보 (x, y, w, h)와 점 개수
        """

        # 이거는 BGR2HSV 사용해야 함.
        # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.

        # 빨간색이 감지가 잘 안 돼서 빨간색 감지할 때는 초록, 파랑색을 없앰
        if color == Color.RED_REC:
            img[:] = self.image_handler.delete_specific_color(img, Color.BLUE)

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)


        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgResult = img.copy()
        x, y, w, h = 0, 0, 0, 0
        figureTypeList = []  # 모든 contour
        figureTypeArea = []  # contour 주위 직사각형의 넓이. 가장 큰 하나의 contour를 구하기 위함.
        figureCntList = []

        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # 이미지 원본에 contour 그리기
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                if count[figure.value][0] <= objType <= count[figure.value][1]:

                    # print("ok")
                    x_t, y_t, w_t, h_t = cv2.boundingRect(approx)

                    # ring이rh 가로세로 비율이 일정 비율 이상일 때만 추가
                    if self.is_ring(color, figure, img[y_t: y_t + h_t, x_t: x_t + w_t]) and w_t!=0 and h_t!=0 and min(w_t, h_t)/max(w_t, h_t)>=0.2:
                        # if draw_contour:
                        #     cv2.drawContours(img, cnt, -1, (0, 255, 255), 3)
                        figureTypeList.append(objType)
                        figureTypeArea.append((x_t, y_t, w_t, h_t))
                        figureCntList.append(cnt)
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
            x, y, w, h = temp[-1]

            # 가장 큰 면적의 인덱스를 통해서 가장 큰 하나의 contour의 objType 알아내기
            max_idx = figureTypeArea.index((x, y, w, h))
        if max_idx != -1:
            figure_type = figureTypeList[max_idx]
        if draw_contour and figure_type!=-1:
            # cv2.rectangle(imgResult, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            # cv2.putText(imgResult, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            # cv2.putText(img, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            cv2.drawContours(img, figureCntList[max_idx], -1, (0, 255, 255), 3)
            stacked_image = self.image_handler.stackImages(0.6, [img, mask])
            if show:
                cv2.imshow("Video", stacked_image)

        return (x, y, w, h), figure_type

    def find_color_with_all_contour(self, img, color, figure, min_area, draw_contour=False, show=False):
        """
        인자로 들어온 Color에 해당하는 도형이 있으면 approx의 리스트 반환
        코드 참조 : https://github.com/murtazahassan/Learn-OpenCV-in-3-hours
        :param img: 이미지 원본
        :param color: Color enum
        :return: approx 리스트
        """

        # 이거는 BGR2HSV 사용해야 함.
        # HSV로 변환하면 grayscale로 바꿔주고 채널이 하나.

        # 빨간색이 감지가 잘 안 돼서 빨간색 감지할 때는 초록, 파랑색을 없앰
        if color == Color.RED_REC:
            img = self.image_handler.delete_specific_color(img, Color.BLUE)

        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        return self._get_all_contours(img, mask, figure, min_area, draw_contours=draw_contour, show=show)

    def _get_biggest_contour(self, img, mask, figure, min_area, draw_contour=True, show=True):
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
        figureCntList = []
        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # 이미지 원본에 contour 그리기
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                if count[figure.value][0] <= objType <= count[figure.value][1]:
                    # print("ok")
                    x, y, w, h = cv2.boundingRect(approx)

                    # 삼각형이 짤리면 꼭짓점이 4개가 나와서 사각형을 방지할 수 있음
                    # 이를 방지하기 위해서 x와 y가 0이 아닐 때만 추가
                    if x!=0 and y!=0:
                        figureTypeList.append(objType)
                        figureTypeArea.append((x, y, w, h))
                        figureCntList.append(cnt)
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
            x, y, w, h = temp[-1]

            # 가장 큰 면적의 인덱스를 통해서 가장 큰 하나의 contour의 objType 알아내기
            max_idx = figureTypeArea.index(temp[-1])
        if max_idx != -1:
            figure_type = figureTypeList[max_idx]
        if draw_contour and figure_type!=-1:
            cv2.rectangle(imgResult, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            cv2.putText(imgResult, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
            cv2.putText(img, f'area : {w * h}', (x, y - 10), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
            cv2.drawContours(img, figureCntList[max_idx], -1, (0, 255, 255), 3)

            stacked_image = self.image_handler.stackImages(0.6, [img, mask])
            if show:
                cv2.imshow("image adn mask", img)

        return (x, y, w, h), figure_type

    def _get_biggest_contour_area(self, img, mask, figure, min_area, draw_contour=False):
        """
        mask로부터 contour를 얻어내서 가장 큰 contour의 넓이 반환
        하나의 도형만 감지
        :param img: 이미지 원본 (웹캠)
        :param mask: 원하는 색만 추출해낸 이미지
        :return: 도형 중심 좌표 (x, y)와 얻은 모든 contour의 점 개수
        """
        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgResult = img.copy()
        x, y, w, h = 0, 0, 0, 0
        area_list = []

        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            area_list.append(area)
        area_list.sort()
        if not area_list:
            area_list.append(0)
        return area_list[-1]


    def _get_all_contours(self, img, mask, figure, min_area, draw_contours=False, show=False):
        """
        원하는 도형의 특정 넓이 이상의 모든 contour를 외접 사각형(원본 x) 그려서 (x, y, w, h) 리스트 반환
        draw_contours가 True라면 이미지 원본에다 contour 그림
        :param img: 이미지 원본 (웹캠)
        :param mask: 원하는 색만 추출해낸 이미지
        :return: approx 리스트
        """
        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # (x, y, w h) 리스트
        approx_list = []
        cnt_list = []

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
                    cnt_list.append(cnt)

        imgResult = np.copy(img)
        if cnt_list and draw_contours:
            cv2.drawContours(img, cnt_list, -1, (255, 255, 255), thickness=2)

        if approx_list:
            for app in approx_list:
                x, y, w, h = cv2.boundingRect(app)
                print('hello')
                # 외접, 내접 사각형 그리기
                # cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 255), thickness=2)
                # cv2.putText(imgResult, f'area : {w*h}', (x, y-10,), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), thickness=2)
                cv2.putText(img, f'area : {w*h}', (x, y-10,), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)

                # contour 그리기
                stacked_image = self.image_handler.stackImages(0.6, [img, mask])
                if show:
                    cv2.imshow("image adn mask", img)
        return approx_list

    def is_ring(self, color, figure, cropped_img):
        if self.check_ring_by_area(color, figure, cropped_img):
            print("area : True")
            return True
        elif self.check_ring_by_cnt(color, figure, cropped_img):
            print("cnt : True")
            return True
        print("is_ring : false")
        return False

    def check_ring_by_cnt(self, color, figure, cropped_img, draw_contours=False):
        """
        가장 바깥쪽 contour 정보를 받아서 이 도형이 가운데가 비어있는 링 형태인지 반환.
        get_biggest_contour와 함께 쓰는 것을 추천.
        :param color: Color Enum 타입
        :param figure: Figure Enum 타입
        :param cropped_img: contour를 기준으로 자른 이미지
        :return: boolean 타입
        """

        # mask 구하기
        imgHSV = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask = cv2.inRange(imgHSV, lower, upper)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)

        # 자른 이미지에서 모든 contour를 구함.
        cropped_area = cropped_img.shape[0]*cropped_img.shape[1] #
        approx_list = self._get_all_contours(cropped_img, mask, figure, cropped_area*0.3, draw_contours = draw_contours)
        print(f'개수 : {len(approx_list)}')
        # 가운데가 비어있다면 우선 바깥 contour와 안쪽 contour 두 개가 감지되어야 함
        if len(approx_list)==2:
            for approx in approx_list:
                # 바깥 contour, 안쪽 contour 모두 같은 도형이어야 함
                if not count[figure.value][0]<=len(approx)<=count[figure.value][1]:
                    return False
            return True
        return False

    def check_ring_by_area(self, color, figure, cropped_img):
        """
        가장 바깥쪽 contour 정보를 받아서 이 도형이 가운데가 비어있는 링 형태인지 반환.
        area를 계산해서 외접 사각형과의 넓이 비율을 계산.
        :param color: Color Enum 타입
        :param figure: Figure Enum 타입
        :param cropped_img: contour를 기준으로 자른 이미지
        :return: boolean 타입
        """

        # mask 구하기
        imgHSV = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
        lower = np.array([myColors[color.value][0:3]])
        upper = np.array([myColors[color.value][3:6]])
        mask1 = cv2.inRange(imgHSV, lower, upper)
        cv2.imshow("maks1", mask1)

        # mask의 넓이
        big_area = cv2.countNonZero(mask1)



        # 가운데 작은 사각형으로 변경
        height = cropped_img.shape[0]
        width = cropped_img.shape[1]
        img_height = int(height * 0.5)
        img_width = int(width * 0.5)
        cropped_img = cropped_img[(height - img_height) // 2:height - (height - img_height) // 2,
                      (width - img_width) // 2:width - (width - img_width) // 2]
        imgHSV = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)

        mask2 = cv2.inRange(imgHSV, lower, upper)
        cv2.imshow("maks2", mask2)
        small_area = cv2.countNonZero(mask2)
        # kernel = np.ones((5, 5), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=2)

        # # 자른 이미지에서 모든 contour를 구함.
        # cropped_area = cropped_img.shape[0] * cropped_img.shape[1]
        #
        # # 가장 큰 contour의 좌표 정보 구함
        # contour_info, figure_type = self._get_biggest_contour(cropped_img, mask, figure, 100, draw_contour=False)
        # x, y, w, h = contour_info
        #
        # # 가장 큰 contour의 면적 구함
        # area = self._get_biggest_contour_area(cropped_img, mask, figure, 100, draw_contour=False)
        print(f'area : {big_area}, small : {small_area}')
        # # 반절 미만을 차지하면 링이라고 판단
        # if cv2.countNonZero(mask) < w*h*0.5:
        #     return True
        # else:
        #     return False
        if small_area<big_area*0.2:
            return True
        return False
