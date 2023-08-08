from config import *
import numpy as np
def track_figure(tello, contour_info, pid, p_error):
    """
    객체가 가운데에 올 수 있게끔 조절하는 함수.
    PID를 통해 오차를 계산해서 객체가 중간에 있는지를 알려주는 boolean 값과 오차값 반환.
    :param tello : Tello 객체
    :param contour_info : (x, y, w, h)
    :param pid : [비례, 적분, 미분]
    :param p_error : 오차
    :return : 객체 중간 여부, 오차값
    """
    # pid 적용
    x, y, w, h = contour_info
    aspect_ratio = 0
    if w!=0 and h!=0:
        aspect_ratio = w/h # 가로세로비

    # 가로세로비가 적절하지 않다면 정면이 아닌 측면에서 보고 있다는 뜻
    # 최대한 정면에서 보게끔 이동

    if aspect_ratio<0.95 or aspect_ratio>1.05:
        # contour 중심과 이미지 중심 좌표의 차이
        error = x + w // 2 - cam_width // 2
        speed = pid[0] * error + pid[1] * (error - p_error)
        speed = int(np.clip(speed, -100, 100))
        fb = 0
        ud = 0
        area = w * h
        if fb_range[0] <= area <= fb_range[1]:  # 적당하다면 멈춤
            fb = 0
            if 0.2 * cam_width <= x + w // 2 <= 0.8 * cam_width and 0.2 * cam_height <= y + h // 2 <= 0.8 * cam_height:
                # if speed==0:
                return True, error
        elif area > fb_range[1]:  # 너무 가깝다면 뒤로
            fb = -10
        elif area < fb_range[0] and area != 0:  # 너무 멀다면 앞으로
            fb = 10
        if x == 0:
            speed = 0
            error = 0
        # print(f'fb : {fb} ud : {ud} speed : {speed}')
        tello.send_rc_control(speed, fb, ud, -speed)
        return False, error

    # 가로세로비가 적절하다면 정면을 보고 있다는 것

    else:
        # contour 중심과 이미지 중심 좌표의 차이
        error = x+w//2 - cam_width//2
        speed = pid[0]*error + pid[1]*(error-p_error)
        speed = int(np.clip(speed, -100, 100))
        fb = 0
        ud = 0
        area = w*h
        if fb_range[0] <= area <= fb_range[1]: # 적당하다면 멈춤
            fb = 0
            if 0.2*cam_width <= x+w//2 <= 0.8*cam_width and 0.2*cam_height <= y+h//2 <= 0.8*cam_height :
            # if speed==0:
                return True, error
        elif area > fb_range[1]: # 너무 가깝다면 뒤로
            fb = -10
        elif area < fb_range[0] and area != 0: # 너무 멀다면 앞으로
            fb = 10

        if ud_range[0] <= y+h//2 <=ud_range[1]:
            ud = 0
        elif y+h//2 > ud_range[1]: # 너무 아래라면 위로
            ud = -10
        elif y+h//2 < ud_range[0]: # 너무 아래라면 위로
            ud = 10

        if x==0:
            speed = 0
            error = 0
        # print(f'fb : {fb} ud : {ud} speed : {speed}')
        tello.send_rc_control(0, fb, ud, speed)
        return False, error