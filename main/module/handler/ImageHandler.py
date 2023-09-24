import cv2
import numpy as np
from main.module.enum.Color import *
class ImageHandler:
    def stackImages(self, scale, imgArray):
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]
        if rowsAvailable:
            for x in range(0, rows):
                for y in range(0, cols):
                    if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                    else:
                        imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                    None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank] * rows
            hor_con = [imageBlank] * rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
            ver = np.vstack(hor)
        else:
            for x in range(0, rows):
                if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                    imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
                else:
                    imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                             scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack(imgArray)
            ver = hor
        return ver
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
        lower_color = np.array([0, 100, 0])
        upper_color = np.array([180, 255, 255])

        # 마스크 생성
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # 노이즈 제거
        dilated_mask = cv2.dilate(mask, kernel, iterations=2)

        temp_img = np.copy(img)

        # 해당 범위의 색상 전부 흰색으로 변경
        temp_img[dilated_mask > 0] = [255, 255, 255]
        return temp_img
    def delete_specific_color(self, img, color):
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
        kernel = np.ones((3, 3), np.uint8)

        # HSV 범위
        lower_color = np.array(myColors[color.value][:3])
        upper_color = np.array(myColors[color.value][3:])

        # 마스크 생성
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # 노이즈 제거
        dilated_mask = cv2.dilate(mask, kernel, iterations=2)

        temp_img = np.copy(img)

        # 해당 범위의 색상 전부 흰색으로 변경
        temp_img[dilated_mask > 0] = [255, 255, 255]
        return temp_img


    def save_contours_by_color(self, img, color):
        """
        원하는 색의 contour를 그려서 저장하는 함수
        :param img: 이미지 원본
        :param color: Color Enum 타입
        :return:
        """
        cv2.imshow("asdsdgsgdf", img)
        # 이미지를 HSV로 변환
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # lower, upper 구하기
        hsv_lower = np.array(myColors[color.value][:3])
        hsv_upper = np.array(myColors[color.value][3:])

        mask = cv2.inRange(hsv_image, hsv_lower, hsv_upper)
        mask = cv2.dilate(mask, np.ones((5, 5)), 5)

        # contour 찾기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        result_image = np.copy(img)
        cv2.drawContours(result_image, contours, -1, (0, 255, 0), 1)
        cv2.imwrite("./hello.png", result_image)
        cv2.imshow("asdf", result_image)
        cv2.imshow("mask", mask)
        cv2.waitKey()