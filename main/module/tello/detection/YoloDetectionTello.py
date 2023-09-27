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
from main.module.handler.YoloHandler import YoloHandler
import numpy as np


class YoloDetectionTello:
    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            pid_params: PIDParams,
            range_params: RangeParams,
            yolo_handler: YoloHandler
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.pid_params: PIDParams = pid_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(tello, range_params, pid_params, cam_params)
        self.yolo_handler: YoloHandler = yolo_handler
        self.figure_handler = FigureHandler()



    def tello_detection_yolo_with_no_rotate(self, brightness=0, save=False):
        """
        도형을 가운데로 맞춤
        :param brightness : 드론으로 찍은 사진 밝기 조절 값
        :param save : 사진 저장 여부
        :return: 없음
        """
        print('기체 감지 시작')
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
            contour_info = self.yolo_handler.get_object_xyxy(img, draw_rectangle=True)

            x, y, w, h = contour_info

            # 너무 가까이 가면 contour를 감지 못 하기 때문에 뒤로 이동
            if x==0 and y==0 and w==0 and h==0:
                # self.tello.move_back(30)
                continue
            # 객체 가운데로
            success, p_error_lr, p_error_ud, p_error_fb = self.tracking_tello.track_figure_with_no_rotate(contour_info, p_error_lr, p_error_ud, p_error_fb)

            # 가운데로 왔고 저장을 하고 싶다면 이미지 저장
            if success and save:
                cv2.imwrite(f"plane.png", img)
                break
            # q를 누르면 무한 반복에서 빠져나옴
            elif success:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()


    def move_until_find(self, direction, brightness=0, save=False):
        """
        원하는 기체를 찾을 때까지 이동
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
            contour_info = self.yolo_handler.get_object_xyxy(img, draw_rectangle=True)
            cv2.imshow("asdf", img)
            x, y, w, h = contour_info

            if (
                    cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (
                    0.5)
                    and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (
                    0.5 + self.range_params.find_range_percentage)
                    and w * h > self.range_params.min_area
            ):
                cnt += 1
                self.tello.send_rc_control(0, 0, 0, 0)
                print('도형 탐색 완료')
                if save:
                    cv2.imwrite("images/yolo.png", img)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            v = 35
            if direction.value % 2 == 1:  # 홀수라면 음수로 바꿈
                v = -v
            velocity[direction.value // 2] = v
            self.tello.send_rc_control(*velocity)
        self.tello.send_rc_control(0, 0, 0, 0)
        cv2.destroyAllWindows()

