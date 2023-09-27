from djitellopy import Tello
import numpy as np
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams

class TrackingTello:

    def __init__(
            self,
            tello: Tello,
            range_params: RangeParams,
            pid_params:  PIDParams,
            cam_params: CamParams
    ):
        self.tello = tello
        self.range_params = range_params
        self.pid_params = pid_params
        self.cam_params = cam_params

    def __getattr__(self, name):
        # range_params에서 변수를 찾고 반환
        if hasattr(self.range_params, name):
            return getattr(self.range_params, name)
        else:
            raise AttributeError(f"'FigureHandler' object has no attribute '{name}'")


    def track_figure_with_rotate(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error : 오차
        :param same_ratio : 만약 외접 정사각형을 원하는지
        :return : 객체 중간 여부, error_lr, error_ud, error_fb
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height

        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        speed_lr = int(np.clip(speed_lr, -100, 100))

        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        error_fb = w * h - (self.range_params.fb_range[0] + self.range_params.fb_range[1]) // 2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        area = w * h

        # 가로세로비
        aspect_ratio = 0
        if w != 0 and h != 0:
            aspect_ratio = w / h  # 가로세로비



        # fb = 0
        # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
            1.0 - self.range_params.aspect_ratio_percentage <= aspect_ratio <= 1.0 + self.range_params.aspect_ratio_percentage
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb

        # yaw 스피드
        # 이 코드가 실행된다는 것은 치우쳐 있다는 뜻
        speed_yaw = 20
        speed_lr = -20

        # 벗어나면 멈춤
        if x == 0 and y == 0 and w == 0 and h == 0:
            speed_lr = 0
            error_lr = 0
            speed_ud = 0
            error_ud = 0
            speed_fb = 0
            error_fb = 0
        self.tello.send_rc_control(speed_lr, -speed_fb, -speed_ud, speed_yaw)
        return False, error_lr, error_ud, error_fb

    def track_figure_with_rotate_v2(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb,
            p_aspect_ratio,
            p_is_aspect
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error : 오차
        :param same_ratio : 만약 외접 정사각형을 원하는지
        :return : 객체 중간 여부, error_lr, error_ud, error_fb
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        fb_min_area = self.range_params.fb_range[0]
        fb_max_area = self.range_params.fb_range[1]
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height

        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        # speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        # speed_lr = int(np.clip(speed_lr, -100, 100))
        speed_lr = -20
        # if speed_lr < 0:
        #     speed_lr = -20
        # else:
        #     speed_lr = 20
        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        error_fb = w * h - (self.range_params.fb_range[0] + self.range_params.fb_range[1]) // 2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        area = w * h

        # 가로세로비
        aspect_ratio = 0
        if w != 0 and h != 0:
            aspect_ratio = (int((min(w, h)/max(w, h))*100))/100.0  # 가로 세로 비율을 소수점 첫 번째 자리까지만 표기


        # fb = 0
        # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
            1.0 - self.range_params.aspect_ratio_percentage <= aspect_ratio <= 1.0 + self.range_params.aspect_ratio_percentage
            # and
            # fb_min_area <= area <= fb_max_area
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb, aspect_ratio, p_is_aspect

        # yaw 스피드
        # 이 코드가 실행된다는 것은 치우쳐 있다는 뜻


        # is_aspect가 True면 회전 방향 유지
        is_aspect = p_is_aspect

        # is_aspect가 False면 회전 방향 변경
        if not is_aspect:
            print('놓침')
            speed_lr = -speed_lr
        elif x==0 and y==0 and w==0 and h==0:
            speed_lr = -speed_lr
            speed_fb = 0
            speed_ud = 0

        # 현재 가로세로 비율이 더 적다는 뜻은 지금 방향이 잘못되었다는 뜻
        # 다른 방향으로 간다면 is_aspect 변경해서 반환
        if aspect_ratio < p_aspect_ratio:
            print('방향 변경')
            is_aspect = not is_aspect
        else:
            is_aspect = is_aspect
        self.tello.send_rc_control(-speed_lr*2, -speed_fb, -speed_ud, speed_lr)
        return False, error_lr, error_ud, error_fb, aspect_ratio, is_aspect

    def track_figure_with_rotate_v3(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb,
            move_left
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error : 오차
        :param same_ratio : 만약 외접 정사각형을 원하는지
        :return : 객체 중간 여부, error_lr, error_ud, error_fb,
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        fb_min_area = self.range_params.fb_range[0]
        fb_max_area = self.range_params.fb_range[1]
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height

        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        # speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        # speed_lr = int(np.clip(speed_lr, -100, 100))
        speed_lr = -20
        # if speed_lr < 0:
        #     speed_lr = -20
        # else:
        #     speed_lr = 20
        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        error_fb = w * h - (self.range_params.fb_range[0] + self.range_params.fb_range[1]) // 2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        area = w * h

        # 가로세로비
        aspect_ratio = 0
        if w != 0 and h != 0:
            aspect_ratio = (int((min(w, h)/max(w, h))*100))/100.0  # 가로 세로 비율을 소수점 첫 번째 자리까지만 표기


        # fb = 0
        # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
            1.0 - self.range_params.aspect_ratio_percentage <= aspect_ratio <= 1.0 + self.range_params.aspect_ratio_percentage
            # and
            # fb_min_area <= area <= fb_max_area
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb, aspect_ratio, p_is_aspect

        # yaw 스피드
        # 이 코드가 실행된다는 것은 치우쳐 있다는 뜻


        # is_aspect가 True면 회전 방향 유지
        is_aspect = p_is_aspect

        # is_aspect가 False면 회전 방향 변경
        if not is_aspect:
            print('놓침')
            speed_lr = -speed_lr
        elif x==0 and y==0 and w==0 and h==0:
            speed_lr = -speed_lr
            speed_fb = 0
            speed_ud = 0

        # 현재 가로세로 비율이 더 적다는 뜻은 지금 방향이 잘못되었다는 뜻
        # 다른 방향으로 간다면 is_aspect 변경해서 반환
        if aspect_ratio < p_aspect_ratio:
            print('방향 변경')
            is_aspect = not is_aspect
        else:
            is_aspect = is_aspect
        # speed_yaw = 0
        # # 왼쪽에 존재하고 치우쳐 있다면 왼쪽 회전과 오른쪽 이동
        # if x+w//2<0.45*cam_width:
        #     speed_yaw = -20
        # # 오른쪽에 존재하고 치우쳐 있다면 오른쪽 회전과 왼쪽 이동
        # else:
        #     speed_yaw = 20
        #     speed_lr = -abs(speed_lr)
        #
        # 벗어나면 멈춤
        # if x == 0 and y == 0 and w == 0 and h == 0:
        #     speed_lr = 0
        #     error_lr = 0
        #     speed_ud = 0
        #     error_ud = 0
        #     speed_fb = 0
        #     error_fb = 0
        self.tello.send_rc_control(-speed_lr*2, -speed_fb, -speed_ud, speed_lr)
        return False, error_lr, error_ud, error_fb, aspect_ratio

    def track_figure_with_no_rotate(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error_lr : 좌우 이전 오차 값
        :param p_error_ud : 위아래 이전 오차 값
        :return : 객체 중간 여부, lr 오차값, ud 오차값
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height


        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        speed_lr = int(np.clip(speed_lr, -100, 100))


        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        error_fb = w * h - (self.range_params.fb_range[0] + self.range_params.fb_range[1])//2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        area = w * h



            # fb = 0
            # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
                self.range_params.fb_range[0] <= w * h <= self.range_params.fb_range[1]
                and cam_width * (0.5 - self.range_params.center_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.center_range_percentage)
                and cam_height * (0.5 - self.range_params.center_range_percentage*1.5) <= y + h // 2 <= cam_height * (0.5 + self.range_params.center_range_percentage*1.5)
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb

        # 벗어나면 멈춤
        if x == 0 and y == 0 and w == 0 and h == 0:
            speed_lr = 0
            error_lr = 0
            speed_ud = 0
            error_ud = 0
            speed_fb = 0
            error_fb = 0
        self.tello.send_rc_control(speed_lr, -speed_fb, -speed_ud, 0)
        return False, error_lr, error_ud, error_fb

    def track_figure_with_no_rotate(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error_lr : 좌우 이전 오차 값
        :param p_error_ud : 위아래 이전 오차 값
        :return : 객체 중간 여부, lr 오차값, ud 오차값
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height


        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        speed_lr = int(np.clip(speed_lr, -100, 100))


        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        error_fb = w * h - (self.range_params.fb_range[0] + self.range_params.fb_range[1])//2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        area = w * h



            # fb = 0
            # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
                self.range_params.fb_range[0] <= w * h <= self.range_params.fb_range[1]
                and cam_width * (0.5 - self.range_params.center_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.center_range_percentage)
                and cam_height * (0.5 - self.range_params.center_range_percentage*3) <= y + h // 2 <= cam_height * (0.5 + self.range_params.center_range_percentage*3)
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb

        # 벗어나면 멈춤
        if x == 0 and y == 0 and w == 0 and h == 0:
            speed_lr = 0
            error_lr = 0
            speed_ud = 0
            error_ud = 0
            speed_fb = 0
            error_fb = 0
        self.tello.send_rc_control(speed_lr, -speed_fb, -speed_ud, 0)
        return False, error_lr, error_ud, error_fb
    def track_figure_with_long(
            self,
            contour_info,
            p_error_lr,
            p_error_ud,
            p_error_fb
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        외접 사각형 좌표가 들어오면 가장 긴 변을 기준으로 정사각형 넓이를 구함.
        track_figure_with_no_rotate에서 area를 구하는 방법만 다름.
        :param contour_info : (x, y, w, h)
        :param p_error_lr : 좌우 이전 오차 값
        :param p_error_ud : 위아래 이전 오차 값
        :return : 객체 중간 여부, lr 오차값, ud 오차값
        """
        # pid 적용
        x, y, w, h = contour_info

        p_lr, i_lr, d_lr = self.pid_params.pid_value_lr
        p_ud, i_ud, d_ud = self.pid_params.pid_value_ud
        p_fb, i_fb, d_fb = self.pid_params.pid_value_fb
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height


        # contour 중심과 이미지 중심 좌표의 차이
        error_lr = x + w // 2 - cam_width // 2
        speed_lr = p_lr * error_lr + i_lr * (error_lr - p_error_lr)
        speed_lr = int(np.clip(speed_lr, -100, 100))


        # contour 중심과 이미지 중심 좌표의 차이
        error_ud = y + h // 2 - cam_height // 2
        speed_ud = p_ud * error_ud + i_ud * (error_ud - p_error_ud)
        speed_ud = int(np.clip(speed_ud, -100, 100))

        # contour 넓이와 원하는 넓이의 차이
        area = max(w, h)**2
        error_fb = area - (self.range_params.fb_range[0] + self.range_params.fb_range[1])//2
        speed_fb = p_fb * error_fb + i_fb * (error_fb - p_error_fb)
        speed_fb = int(np.clip(speed_fb, -100, 100))

        # fb = 0
            # 이미지의 width, height가 다르기 때문에 center_range_percentage를 조정함
        if (
                self.range_params.fb_range[0] <= area <= self.range_params.fb_range[1]
                and cam_width * (0.5 - self.range_params.center_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.center_range_percentage)
                and cam_height * (0.5 - self.range_params.center_range_percentage*3) <= y + h // 2 <= cam_height * (0.5 + self.range_params.center_range_percentage*3)
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb

        # 벗어나면 멈춤
        if x == 0 and y == 0 and w == 0 and h == 0:
            speed_lr = 0
            error_lr = 0
            speed_ud = 0
            error_ud = 0
            speed_fb = 0
            error_fb = 0
        self.tello.send_rc_control(speed_lr, -speed_fb, -speed_ud, 0)
        return False, error_lr, error_ud, error_fb