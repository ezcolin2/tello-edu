import cv2
import torch
import numpy as np
import torchvision.transforms as transforms
from module.enum.Color import *

from module.enum.Figure import *
from module.handler.FigureHandler import FigureHandler

class NumberHandler:
    def __init__(self, model):
        self.model = model
        self.figure_handler = FigureHandler()
    def get_number_with_model(self, image):
        """
        이진화 처리 된 이미지를 받아서 해당 숫자 판단
        :param image: 이진화 된 이미지
        :return: 감지한 숫자
        """

        device = torch.device('cpu')

        # square_img = self.make_img_square(image)


        image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=0)

        image = cv2.resize(image, (28, 28))
        cv2.imshow("border", image)
        # cv2.imshow("border", image)

        # 이미지를 [0, 1] 범위로 스케일링
        image = image.astype('float32') / 255.0

        # 이미지를 PyTorch 모델에 입력 가능한 형태로 변환
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        image = transform(image).unsqueeze(0)  # 배치 차원 추가
        with torch.no_grad():
            image = image.to(device)
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
        return predicted.item()
    def make_img_square(self, img):
        """
        이진화된 이미지를 받아서 검은색 padding을 넣어서 정사각형으로 만들어서 반환
        :param img: 이진화된 정사각형이 아닌 이미지
        :return:
        """
        h, w = img.shape

        # 높이와 너비 중 큰 값을 찾아 정사각형의 한 변의 길이로 설정
        max_dim = max(h, w)

        # 패딩 값 계산
        top_pad = (max_dim - h) // 2
        bottom_pad = max_dim - h - top_pad
        left_pad = (max_dim - w) // 2
        right_pad = max_dim - w - left_pad

        # 검은색으로 패딩 추가
        square_img = cv2.copyMakeBorder(img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT,
                                        value=[0, 0, 0])
        return square_img

    def find_number_with_color_rectangle(self, img, color, save=False, rectangle_contour=False):
        """
        해당 이미지의 원하는 색상의 사각형을 감지한 다음 그 아래에 있는 숫자를 반환하는 함수
        :param img: 이미지 원본
        :param color: Color Enum 타입
        :param save: 숫자 이미지 저장 여부

        :return: 숫자
        """
        print('색, 숫자 매칭 시작')
        # 숫자가 짤리지 않게 패딩 추가
        padding = 20

        kernel = np.ones((3, 3))
        result = -1
        contour_info, _ = self.figure_handler.find_color(img, color, Figure.RECTANGLE)
        x, y, w, h = contour_info
        if rectangle_contour:
            coord_list = self.figure_handler.find_color_with_all_contour(img, color, Figure.RECTANGLE, 500)
            #
            # for x, y, w, h in coord_list:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        temp = self.delete_color(img)
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

        thr, mask = cv2.threshold(temp, 95, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, kernel, iterations=1)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # 감지한 contour 외접 사각형 좌표
        coord_list = []
        for cnt in contours:
            area = cv2.contourArea(cnt)

            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > 500:  # area가 500보다 클 때만 contour 그리기

                x, y, w, h = cv2.boundingRect(cnt)
                x -= padding
                y -= padding
                w += padding * 2
                h += padding * 2
                if contour_info[0] < x + w // 2 < contour_info[0] + contour_info[2] and y + h // 2 > \
                        contour_info[1] + contour_info[3]:
                    coord_list.append([area, x, y, w, h])

        # 감지한 사각형이 있을 때만
        if coord_list:
            # 정렬
            coord_list.sort()
            # 가장 면적이 큰 외접 사각형
            x, y, w, h = coord_list[-1][1:]
            num_img = img[y:y + h, x:x + w]
            result_image = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY)

            thr, bin_img = cv2.threshold(result_image, 80, 255, cv2.THRESH_BINARY_INV)
            bin_img = cv2.dilate(bin_img, kernel, iterations=1)

            # 이진화 된 이미지로 숫자 판단
            result = self.get_number_with_model(bin_img)
            img_result = np.copy(img)
            # 숫자 contour 그려서 저장
            if save:
                # 외접 사각형 그리기

                cv2.rectangle(img_result, (x, y), (x + w, y + h), (255, 255, 255), 2)

                cv2.putText(img_result, str(result), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (255, 255, 255),
                            thickness=3)

                cv2.imwrite(f'second_result/{Color(color.value).name}_number.png', img_result)

        print('색, 숫자 매칭 완료')
        return result

    def find_biggest_number(self, img, min_area):
        """
        이미지 원본에서 mask 추출 및 이진화 진행 후 감지한 bounding rectangle 중 가장 면적이 큰 값의 (x, y, w, h) 반환
        :param img: 이미지 원본
        :param min_area: 감지할 숫자의 가장 작은 면적
        :return: 숫자 bounding rectangle (x, y, w, h) 좌표와 그 숫자의 예측 값 반환 ex) (x, y, w, h),
        """
        kernel = np.ones((5, 5), np.uint8)
        padding = 20 # 정확도를 위해 숫자 이미지에 패딩 추가
        img = self.delete_color(img)
        cv2.imshow("delete", img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, kernel, iterations=1)

        x, y, w, h = self._get_biggest_number_contour(img, mask, min_area)
        x -= padding
        y -= padding
        w += padding * 2
        h += padding * 2

        num_img = mask[y:y + h, x:x + w]

        # 정사각형을 만듦
        h, w = num_img.shape

        # 높이와 너비 중 큰 값을 찾아 정사각형의 한 변의 길이로 설정
        max_dim = max(h, w)

        # 패딩 값 계산
        top_pad = (max_dim - h) // 2
        bottom_pad = max_dim - h - top_pad
        left_pad = (max_dim - w) // 2
        right_pad = max_dim - w - left_pad

        # 검은색으로 패딩 추가
        square_img = cv2.copyMakeBorder(num_img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT,
                                        value=[0, 0, 0])

        # 예측 값
        predicted = self.get_number_with_model(square_img)

        return (x, y, w, h), predicted

    def find_all_numbers(self, img, min_area):
        """
        이미지 원본에서 mask 추출 및 이진화 진행 후 감지한 모든 bounding rectangle의 (x, y, w, h) 반환
        :param img: 이미지 원본 (웹캠)
        :param mask: 원하는 숫자만 추출해낸 이미지
        :param min_area: 감지할 숫자의 가장 작은 면적
        :return: (x, y, w, h) 리스트
        """

        kernel = np.ones((5, 5), np.uint8)
        padding = 20 # 정확도를 위해 숫자 이미지에 패딩 추가



        img = self.delete_color(img)
        cv2.imshow("delete", img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, kernel, iterations=1)
        bounding_list = self._get_all_number_contours(img, mask, min_area)

        list = []
        for x, y, w, h in bounding_list:
            x -= padding
            y -= padding
            w += padding * 2
            h += padding * 2

            num_img = mask[y:y + h, x:x + w]

            h, w = num_img.shape

            # 높이와 너비 중 큰 값을 찾아 정사각형의 한 변의 길이로 설정
            max_dim = max(h, w)

            # 패딩 값 계산
            top_pad = (max_dim - h) // 2
            bottom_pad = max_dim - h - top_pad
            left_pad = (max_dim - w) // 2
            right_pad = max_dim - w - left_pad

            # 검은색으로 패딩 추가
            square_img = cv2.copyMakeBorder(num_img, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT,
                                            value=[0, 0, 0])

            # 예측 값
            predicted = self.get_number_with_model(square_img)
            list.append(((x, y, w, h), predicted))

        return list

    def _get_biggest_number_contour(self, img, mask, min_area):
        """
        mask로부터 contour를 얻어내서 숫자의 중심 좌표 반환
        하나의 숫자만 감지
        정확도를 위해서 여러 개의 contour를 찾는다면 가장 면적이 큰 것만 가져옴
        :param img: 이미지 원본 (웹캠)
        :param mask: 숫자만 추출해낸 이미지
        :param min_area: 감지할 숫자의 가장 작은 면적
        :return: 숫자 bounding rectangle (x, y, w, h) 좌표 반환
        """
        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        imgResult = img.copy()
        x, y, w, h = 0, 0, 0, 0
        figureTypeArea = []  # contour 주위 직사각형의 넓이. 가장 큰 하나의 contour를 구하기 위함.

        max_idx = -1
        figure_type = -1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # cv2.drawContours(img, cnt, -1, (255, 0, 0), 3)
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                objType = len(approx)
                x, y, w, h = cv2.boundingRect(approx)
                figureTypeArea.append((x, y, w, h))

        if figureTypeArea:
            # 면적 큰 순으로 정렬
            temp = sorted(figureTypeArea, key=lambda x: x[2] * x[3])
            # 가장 큰 하나의 contour의 x, y, w, h 가져옴
            x, y, w, h = temp[0]

        return x, y, w, h

    # noinspection PyMethodMayBeStatic
    def _get_all_number_contours(self, img, mask, min_area):
        """
        원하는 도형의 특정 넓이 이상의 모든 contour를 외접 사각형의 (x, y, w, h) 리스트 반환
        :param img: 이미지 원본 (웹캠)
        :param mask: 원하는 숫자만 추출해낸 이미지
        :param min_area: 감지할 숫자의 가장 작은 면적
        :return: (x, y, w, h) 리스트
        """
        # (이미지, retrieval method) RETR_EXTERNAL은 outer detail을 찾거나 outer corner를 찾을 때 유용함.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # (x, y, w h) 리스트
        coord_list = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            # minimum threshold를 정하면 noise를 줄일 수 있음
            if area > min_area:  # area가 500보다 클 때만 contour 그리기
                # curve 길이 구하기
                peri = cv2.arcLength(cnt, True)

                # 점 위치
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                coord_list.append((x, y, w, h))
        return coord_list

    # noinspection PyMethodMayBeStatic
    def delete_color(self, img):
        """
        모든 색깔을 흰색으로 칠해서 반환
        :param img: 원본 이미지
        :return: 색깔을 흰색으로 칠한 이미지
        """
        # # 색깔 밝게
        # img+=30

        # HSV 색 공간으로 변경
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 커널
        kernel = np.ones((5, 5), np.uint8)

        # HSV 범위
        lower_color = np.array([0, 110, 0])
        upper_color = np.array([180, 255, 255])

        # 마스크 생성
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # 노이즈 제거
        dilated_mask = cv2.dilate(mask, kernel, iterations=2)

        temp_img = np.copy(img)

        # 해당 범위의 색상 전부 흰색으로 변경
        temp_img[dilated_mask > 0] = [255, 255, 255]
        return temp_img