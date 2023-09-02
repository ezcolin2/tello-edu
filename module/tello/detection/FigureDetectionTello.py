from djitellopy import Tello
from module.enum.Color import *
from module.enum.Direction import *
from module.enum.Figure import *
import cv2
from module.params.PIDParams import PIDParams
from module.params.RangeParams import RangeParams
from module.params.CamParams import CamParams
from module.tello.TrackingTello import TrackingTello
from module.handler.FigureHandler import FigureHandler
class FigureDetectionTello:

    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            pid_params: PIDParams,
            range_params: RangeParams
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.pid_params: PIDParams = pid_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(tello, range_params, pid_params, cam_params)
        self.figure_handler: FigureHandler = FigureHandler()

    def tello_detection_figure(self, color, figure, brightness=0, save=False, console=False):
        """
        인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
        :param tello : Tello
        :param color : 색상
        :param figure : 도형
        :param brightness : 드론으로 찍은 사진 밝기 조절 값
        :param save : 사진 저장 여부
        :param print : front, back 출력 여부
        :return: 도형 감지 여부 반환
        """

        p_error = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        pid = self.pid_params.pid_value
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            contour_info, figure_type = self.figure_handler.find_color(img, color, figure)
            cv2.imshow("Video", img)

            # 객체 가운데로
            success, p_error = self.tracking_tello.track_figure(self.tello, contour_info, pid, p_error)
            if success:
                # 이미지 이름 정하기
                image_name = ""  # 저장할 이미지 이름
                if color == Color.RED:
                    image_name += "red"
                elif color == Color.GREEN:
                    image_name += "green"
                elif color == Color.BLUE:
                    image_name += "blue"
                if figure == Figure.TRI:
                    image_name += " triangle"
                elif figure == Figure.CIRCLE:
                    image_name += " circle"

                if save:
                    cv2.imwrite(f"images/{image_name}.png", img)

                if console:
                    # 터미널에 front, back 출력
                    if figure == Figure.CIRCLE:
                        print('Front')
                    elif figure == Figure.TRI:
                        print('Back')
                    break
            # q를 누르면 무한 반복에서 빠져나옴
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.tello.send_rc_control(0, 0, 0, 0)





    def move_until_find_figure(self, color, figure, direction, brightness=0):
        """
        원하는 색상의 도형을 찾을 때까지 회전
        :param tello: Tello 객체
        :param color: Color enum 타입
        :param figure: Figure enum 타입
        :param direction: Direction enum 타입

        :return: 없음
        """
        cnt = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        while cnt < 4:
            velocity = [0, 0, 0, 0]  # send_rc_control의 인자로 들어갈 값.
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame+brightness, (cam_width, cam_height))
            img += 30
            cv2.imshow("asdf", img)
            contour_info, figureType = self.figure_handler.find_color(img, color, figure)
            x, y, w, h = contour_info
            if (
                    cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage)
                    and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage)
                    and figureType >= 0
                    and w * h > self.range_params.min_area
            ):
                cnt += 1
                self.tello.send_rc_control(0, 0, 0, 0)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            v = 20
            if direction.value % 2 == 1:  # 홀수라면 음수로 바꿈
                v = -v
            velocity[direction.value // 2] = v
            self.tello.send_rc_control(*velocity)
        self.tello.send_rc_control(0, 0, 0, 0)
        cv2.destroyAllWindows()