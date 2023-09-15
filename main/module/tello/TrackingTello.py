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
            p_error,
            same_ratio=True
    ):

        """
        객체가 가운데에 올 수 있게끔 조절하는 함수.
        PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
        :param contour_info : (x, y, w, h)
        :param p_error : 오차
        :param same_ratio : 만약 외접 정사각형을 원하는지
        :return : 객체 중간 여부, 오차값
        """
        # pid 적용
        x, y, w, h = contour_info
        p, i, d = [0.1, 0.1, 0]
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        aspect_ratio = 0
        print(f"perror : {p_error}")
        if w != 0 and h != 0:
            aspect_ratio = w / h  # 가로세로비


        # 가로세로비가 적절하지 않다면 정면이 아닌 측면에서 보고 있다는 뜻
        # 최대한 정면에서 보게끔 이동

        if (
                same_ratio and
                aspect_ratio < 1.0 - self.range_params.aspect_ratio_percentage or
                aspect_ratio > 1.0 + self.range_params.aspect_ratio_percentage
        ):
            # contour 중심과 이미지 중심 좌표의 차이
            error = x + w // 2 - self.cam_params.width // 2
            speed = p * error + i * (error - p_error)
            speed = int(np.clip(speed, -100, 100))
            fb = 0
            ud = 0
            area = w * h
            if self.range_params.fb_range[0] <= area <= self.range_params.fb_range[1]:  # 적당하다면 멈춤
                fb = 0
                if 0.2 * cam_width <= x + w // 2 <= 0.8 * cam_width and 0.2 * cam_height <= y + h // 2 <= 0.8 * cam_height:
                    # if speed==0:
                    return True, error
            elif area > self.range_params.fb_range[1]:  # 너무 가깝다면 뒤로
                fb = -10
            elif area < self.range_params.fb_range[0] and area != 0:  # 너무 멀다면 앞으로
                fb = 10

            if self.range_params.ud_range[0] <= y + h // 2 <= self.range_params.ud_range[1]:
                ud = 0
            elif y + h // 2 > self.range_params.ud_range[1]:  # 너무 위라면 아래로
                ud = -10
            elif y + h // 2 < self.range_params.ud_range[0]:  # 너무 아래라면 위로
                ud = 10

            if x == 0:
                speed = 0
                error = 0
            # print(f'fb : {fb} ud : {ud} speed : {speed}')
            temp_speed = 20

            # 왼쪽에 존재하고 치우쳐 있다면 왼쪽 회전
            if x+w//2<0.45*cam_width:
                temp_speed=-temp_speed
            else:
                temp_speed = temp_speed

            self.tello.send_rc_control(temp_speed, fb, ud, -temp_speed)
            return False, error

        # 가로세로비가 적절하다면 정면을 보고 있다는 것
        # 정면을 보고 있다면 멈춤
        # 이후 과정은 track_figure_with_no_rotate에서 진행

        else:
            return True, 0

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
                and cam_height * (0.5 - self.range_params.center_range_percentage*2) <= y + h // 2 <= cam_height * (0.5 + self.range_params.center_range_percentage*2)
        ):
            # if speed==0:
            return True, error_lr, error_ud, error_fb
        # elif area > self.range_params.fb_range[1]:  # 너무 가깝다면 뒤로
        #     fb = -10
        # elif area < self.range_params.fb_range[0] and area != 0:  # 너무 멀다면 앞으로
        #     fb = 10

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


    def track_figure_until_not_find(
            self,
            contour_info,
            p_error,
    ):
        # pid 적용
        x, y, w, h = contour_info
        p, i, d = self.pid_params.pid_value
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        aspect_ratio = 0
        # contour 중심과 이미지 중심 좌표의 차이
        error = x + w // 2 - cam_width // 2
        speed = p * error + i * (error - p_error)
        speed = int(np.clip(speed, -100, 100))
        fb = 0
        ud = 0
        area = w * h
        if self.range_params.fb_range[0] <= area <= self.range_params.fb_range[1]:  # 적당하다면 멈춤
            fb = 0
            if (
                    x==0 and y==0 and w==0 and h==0
                    # cam_width * (0.5 - self.range_params.center_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.center_range_percentage)
                    # and cam_height * (0.5 - self.range_params.center_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.center_range_percentage)
            ):
                # if speed==0:
                return True, error

        if self.range_params.ud_range[0] <= y + h // 2 <= self.range_params.ud_range[1]:
            ud = 0
        elif y + h // 2 > self.range_params.ud_range[1]:  # 너무 아래라면 위로
            ud = -20
        elif y + h // 2 < self.range_params.ud_range[0]:  # 너무 아래라면 위로
            ud = 20

        if x == 0:
            speed = 0
            error = 0
        self.tello.send_rc_control(0, 10, ud, speed)
        return False, error
    # def is_side(self, img):


    # def track_number(tello, contour_info, pid, p_error, same_ratio=True):
    #     """
    #     객체가 가운데에 올 수 있게끔 조절하는 함수.
    #     PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
    #     :param tello : Tello 객체
    #     :param contour_info : (x, y, w, h)
    #     :param pid : [비례, 적분, 미분]
    #     :param p_error : 오차
    #     :param same_ratio : 만약 외접 정사각형을 원하는지
    #     :return : 객체 중간 여부, 오차값
    #     """
    #     # pid 적용
    #     x, y, w, h = contour_info
    #     aspect_ratio = 0
    #     if w != 0 and h != 0:
    #         aspect_ratio = w / h  # 가로세로비
    #
    #     # 가로세로비가 적절하지 않다면 정면이 아닌 측면에서 보고 있다는 뜻
    #     # 최대한 정면에서 보게끔 이동
    #
    #     if same_ratio and aspect_ratio < 1.0 - self.range_params.aspect_ratio_range or aspect_ratio > 1.0 + self.range_params.aspect_ratio_range:
    #         # contour 중심과 이미지 중심 좌표의 차이
    #         error = x + w // 2 - cam_width // 2
    #         speed = pid[0] * error + pid[1] * (error - p_error)
    #         speed = int(np.clip(speed, -100, 100))
    #         fb = 0
    #         ud = 0
    #         area = w * h
    #         if fb_range_number[0] <= area <= fb_range_number[1]:  # 적당하다면 멈춤
    #             fb = 0
    #             # if 0.2 * cam_width <= x + w // 2 <= 0.8 * cam_width and 0.2 * cam_height <= y + h // 2 <= 0.8 * cam_height:
    #             #     # if speed==0:
    #             #     return True, error
    #         elif area > fb_range_number[1]:  # 너무 가깝다면 뒤로
    #             fb = -10
    #         elif area < fb_range_number[0] and area != 0:  # 너무 멀다면 앞으로
    #             fb = 10
    #
    #         if ud_range[0] <= y + h // 2 <= ud_range[1]:
    #             ud = 0
    #         elif y + h // 2 > ud_range[1]:  # 너무 위라면 아래로
    #             ud = -20
    #         elif y + h // 2 < ud_range[0]:  # 너무 아래라면 위로
    #             ud = 20
    #
    #         if x == 0:
    #             speed = 0
    #             error = 0
    #         # print(f'fb : {fb} ud : {ud} speed : {speed}')
    #         tello.send_rc_control(speed, fb, ud, -speed)
    #         return False, error
    #
    #     # 가로세로비가 적절하다면 정면을 보고 있다는 것
    #
    #     else:
    #         # contour 중심과 이미지 중심 좌표의 차이
    #         error = x + w // 2 - cam_width // 2
    #         speed = pid[0] * error + pid[1] * (error - p_error)
    #         speed = int(np.clip(speed, -100, 100))
    #         fb = 0
    #         ud = 0
    #         area = w * h
    #         # if fb_range_number[0] <= area <= fb_range_number[1]: # 적당하다면 멈춤
    #         #     fb = 0
    #         #     if (
    #         #             cam_width * (0.5 - center_range) <= x+w//2 <= cam_width * (0.5 + center_range)
    #         #             and cam_height * (0.5 - center_range) <= y+h//2 <= cam_height * (0.5 + center_range)
    #         #     ) :
    #         #     # if speed==0:
    #         #         return True, error
    #         if area > fb_range_number[1]:  # 너무 가깝다면 뒤로
    #             fb = -10
    #         elif area < fb_range_number[0] and area != 0:  # 너무 멀다면 앞으로
    #             fb = 10
    #
    #         if ud_range[0] <= y + h // 2 <= ud_range[1]:
    #             ud = 0
    #         elif y + h // 2 > ud_range[1]:  # 너무 아래라면 위로
    #             ud = -20
    #         elif y + h // 2 < ud_range[0]:  # 너무 아래라면 위로
    #             ud = 20
    #
    #         if x == 0:
    #             speed = 0
    #             error = 0
    #         tello.send_rc_control(0, fb, ud, speed)
    #         return False, error