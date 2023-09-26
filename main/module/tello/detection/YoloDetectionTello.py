from djitellopy import Tello
from main.module.enum.Color import *
from main.module.enum.Figure import *
import cv2
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.TrackingTello import TrackingTello
from main.module.handler.FigureHandler import FigureHandler
from main.module.handler.NumberHandler import NumberHandler
import numpy as np


class YoloDetectionTello:
    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            pid_params: PIDParams,
            range_params: RangeParams,
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.pid_params: PIDParams = pid_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(tello, range_params, pid_params, cam_params)


    def tello_detection_with_rotate_v3(self, color, figure, brightness=0, save=False, console=False):
        """
        도형을 가운데로 맞춤
        :param color : 색상
        :param figure : 도형
        :param brightness : 드론으로 찍은 사진 밝기 조절 값
        :param save : 사진 저장 여부
        :param console : front, back 출력 여부
        :return: 없음
        """
        print('도형 감지 시작')

        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        min_area = self.range_params.min_area
        aspect_ratio_percentage = self.range_params.aspect_ratio_percentage

        frame_read = self.tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
        contour_info= self.get_xyxy(img, [0, 1])
        x, y, w, h = contour_info

        # 가로 세로 비율 구함
        p_aspect_ratio = w/h

        # 범위 안에 있으면 끝냄
        if 1.0 - aspect_ratio_percentage <= p_aspect_ratio <= 1.0 + aspect_ratio_percentage:
            print('도형 감지 성공')
            return

        # 범위 안에 있으면 어디로 회전할지 판단하기
        self.tello.move_right(40)
        self.tello.rotate_counter_clockwise(20)

        # 우선 회전 해보고 aspect ratio 계산
        frame_read = self.tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
        contour_info= self.get_xyxy(img, [0, 1])
        x, y, w, h = contour_info

        # 링을 감지 못했거나 aspect_ratio가 더 작아졌다면 방향 변경
        is_left = h==0 or w==0 or w/h < p_aspect_ratio
        # if is_left:
        #     print(f'회전 방향 변경 : {p_aspect_ratio} -> {w/h}')
        # else:
        #     print(f'회전 그대로: {p_aspect_ratio} - > {w/h}')
        speed = -20 if is_left else 20

        # 맞출 때까지 회전
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            contour_info = self.get_xyxy(img, [0, 1])
            cv2.imshow("Video", img)
            x, y, w, h = contour_info
            # aspect ratio가 범위 안에 들어오면 멈춤
            if h != 0 and w != 0 and 1.0 - aspect_ratio_percentage <= w/h <= 1.0 + aspect_ratio_percentage:
                if save:
                    # 이미지 이름 정하기

                    image_name = ""  # 저장할 이미지 이름
                    if color == Color.RED:
                        image_name += "Red"
                    elif color == Color.GREEN:
                        image_name += "Green"
                    elif color == Color.BLUE:
                        image_name += "Blue"

                    if save:
                        cv2.imwrite(f"{image_name}.png", img)
                break
            # q를 누르면 무한 반복에서 빠져나옴
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.tello.send_rc_control(speed*2, 0, 0, -speed)







    def tello_detection_rectangle_ring_with_no_rotate(self, color, figure, brightness=0, save=False, console=False):
        """
        도형을 가운데로 맞춤
        감지한 링의 내접, 외접 contour를 모두 그림
        :param color : 색상
        :param figure : 도형
        :param brightness : 드론으로 찍은 사진 밝기 조절 값
        :param save : 사진 저장 여부
        :param console : front, back 출력 여부
        :return: 없음
        """
        print('도형 감지 시작')
        p_error_lr = 0
        p_error_ud = 0
        p_error_fb = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        min_area = self.range_params.min_area

        # rectangle ring의 가장 바깥쪽 contour 정보
        x, y, w, h = 0, 0, 0, 0
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            # 모든 contour를 찾고나면 이 중에서 rectangle ring을 걸러내야하기 때문에 contour를 그리지는 않는다.
            approx_list = self.figure_handler.find_color_with_all_contour(img, color, figure, min_area, draw_contour=True, show=True)
            if approx_list:
                for approx in approx_list:
                    x_temp, y_temp, w_temp, h_temp = cv2.boundingRect(approx)

                    # 감지한 contour 중 ring이 있다면 그 값을 저장
                    if self.figure_handler.is_ring(color, figure, img[y_temp:y_temp + h_temp + 1, x_temp:x_temp + w_temp + 1]):
                        x, y, w, h = x_temp, y_temp, w_temp, h_temp

                        # rectangle ring에만 contour를 그림
                        approx_list_ring = self.figure_handler.find_color_with_all_contour(img[y_temp:y_temp+h_temp+1, x_temp:x_temp+w_temp+1], color, figure, min_area, draw_contour=True, show=False)

                        # 외접, 내접 contour도 그리기

            # contour_info, figure_type = self.figure_handler.find_color(img, color, figure, 500)
            # x, y, w, h = contour_info

            # 너무 가까이 가면 contour를 감지 못 하기 때문에 뒤로 이동
            if x==0 and y==0 and w==0 and h==0:
                # self.tello.move_back(30)
                continue
            # 객체 가운데로
            contour_info = (x, y, w, h)
            success, p_error_lr, p_error_ud, p_error_fb = self.tracking_tello.track_figure_with_no_rotate(contour_info, p_error_lr, p_error_ud, p_error_fb)

            # 가운데로 왔고 저장을 하고 싶다면 이미지 저장
            if success and save:
                # 이미지 이름 정하기

                image_name = ""  # 저장할 이미지 이름
                if color == Color.RED:
                    image_name += "Red"
                elif color == Color.GREEN:
                    image_name += "Green"
                elif color == Color.BLUE:
                    image_name += "Blue"

                if save:
                    cv2.imwrite(f"{image_name}.png", img)

                if console:
                    # 터미널에 front, back 출력
                    if figure == Figure.CIRCLE:
                        print('Front')
                    elif figure == Figure.TRI:
                        print('Back')
                    break

                print(f'도형 감지 성공 : {image_name}')

                break
            # q를 누르면 무한 반복에서 빠져나옴
            elif success:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


    def move_until_find(self, color, figure, direction, brightness=0):
        """
        원하는 색상의 사각형 링을 찾을 때까지 회전
        :param color: Color enum 타입
        :param figure: Figure enum 타입
        :param direction: Direction enum 타입

        :return: 없음
        """
        print('도형 탐색 시작')
        cnt = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        min_area = self.range_params.min_area

        while cnt < 4:
            velocity = [0, 0, 0, 0]  # send_rc_control의 인자로 들어갈 값.
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            cv2.imshow("asdf", img)
            contour_info, figureType = self.figure_handler.find_color(img, color, figure, min_area)
            x, y, w, h = contour_info
            print(x, y, w, h)
            print(img[y:y+h, x:x+w])
            print(img[x:x+w][y:y+h])
            # 만약 가운데가 비어있는 링이 아닌 사각형이라면
            if x != 0 and y != 0 and w != 0 and h != 0 and not self.figure_handler.is_ring(color, figure,
                                                                                           img[y: y + h,x: x + w]):
                continue

            if (
                    cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (
                    0.5)
                    and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (
                    0.5 + self.range_params.find_range_percentage)
                    and figureType >= 0
                    and w * h > self.range_params.min_area
            ):
                cnt += 1
                self.tello.send_rc_control(0, 0, 0, 0)
                print('도형 탐색 완료')
                return w/h
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            v = 35
            if direction.value % 2 == 1:  # 홀수라면 음수로 바꿈
                v = -v
            velocity[direction.value // 2] = v
            self.tello.send_rc_control(*velocity)
        self.tello.send_rc_control(0, 0, 0, 0)
        cv2.destroyAllWindows()

    def get_xyxy(img, idx_list):
        """
        이미지에서 원하는 클래스의 인덱스를 찾았다면 bounding rectangle 좌표 정보 반환
        :param img: 이미지 원본
        :param idx: 찾고자하는 클래스의 인덱스
        :return: (x, y, w, h)
        """
        # 이미지를 모델에 적용
        results = yolo_model(img)

        # 마스크와 마스크로 표시된 객체의 종류를 순서대로 알려줌
        for r in results:
            for i, c in enumerate(r.boxes):
                if int(c.cls) in idx_list:
                    x1, y1, x2, y2 = r.boxes[i].xyxy.squeeze(0).tolist()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    return x1, y1, x2, y2

