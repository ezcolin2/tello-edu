from djitellopy import Tello
from main.module.enum.Color import *
from main.module.enum.Figure import *
import cv2
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.TrackingTello import TrackingTello
from main.module.handler.FigureHandler import FigureHandler
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



class FigureAndNumberDetectionTello:
    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            pid_params: PIDParams,
            range_params: RangeParams,
            number_handler: NumberHandler
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.pid_params: PIDParams = pid_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(tello, range_params, pid_params, cam_params)
        self.figure_handler: FigureHandler = FigureHandler()
        self.number_handler: NumberHandler = number_handler
    def tello_detection_with_rotate(self, color, brightness=0, save=False, console=False):
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
        p_error = 0
        p_error_lr = 0
        p_error_ud = 0
        p_error_fb = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        x, y, w, h = 0, 0, 0, 0
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            contour_info, figure_type = self.figure_handler.find_color_except_ring(img, color, Figure.ANY, 1000, draw_contour=True)
            x, y, w, h = contour_info
            # 객체 가운데로
            success, p_error_lr, p_error_ud, p_error_fb = self.tracking_tello.track_figure_with_rotate(contour_info, p_error_lr, p_error_ud, p_error_fb)

            if success:
                break

            # q를 누르면 무한 반복에서 빠져나옴
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
    def tello_detection_with_no_rotate(self, color, figure, brightness=0, save=False, console=False):
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

        # rectangle ring의 가장 바깥쪽 contour 정보
        x, y, w, h = 0, 0, 0, 0
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))

            contour_info, figure_type = self.figure_handler.find_color_except_ring(img, color, figure, 2000, draw_contour=True)
            x, y, w, h = contour_info

            # 너무 가까이 가면 contour를 감지 못 하기 때문에 뒤로 이동
            if x==0 and y==0 and w==0 and h==0:
                # self.tello.move_back(20)
                continue
            # 객체 가운데로
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
                    cv2.imwrite(f"second_result/{image_name}.png", img)

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
            # cv2.circle(img, (x+w//2, y+h//2), 3, (255, 255, 255), thickness=cv2.FILLED)
            # range = self.range_params.center_range_percentage
            # cv2.rectangle(img, (0.5-range, 0.5-range), (0.5+range, 0.5+range), (255, 255, 255), thickness=3)
            # cv2.imshow("video", img)
        cv2.destroyAllWindows()

    def move_until_find_figure(self, color, direction, brightness=0):
        """
        원하는 색상의 사각형 링을 제외한 모든 도형을 감지할 때까지 이동
        만약 사각형일 때 사각형 링이 아닌지 체크.
        :param color: Color enum 타입
        :param direction: Direction enum 타입

        :return: 없음
        """
        print('도형 탐색 시작')
        cnt = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        while cnt < 4:
            velocity = [0, 0, 0, 0]  # send_rc_control의 인자로 들어갈 값.
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame+brightness, (cam_width, cam_height))
            cv2.imshow("asdf", img)
            contour_info, figureType = self.figure_handler.find_color_except_ring(img, color, Figure.ANY, 500, draw_contour=True)
            x, y, w, h = contour_info

            try:
                print('출력')
                print(cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage))
                print(cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage))
                print(figureType)
                print(w * h > self.range_params.min_area)
                print(self.figure_handler.is_ring(color, Figure.RECTANGLE, img[y: y + h, x: x + w]))
            except:
                pass

            # 범위 안에 포함되어 있고 감지를 제대로 했으며 최소 면적을 넘고 사각형 링이 아니라는 것을 감지했다면
            if (
                    cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage)
                    and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage)
                    and figureType >= 0
                    and w * h > self.range_params.min_area
                    and not self.figure_handler.is_ring(color, Figure.RECTANGLE, img[y : y + h, x : x + w])
            ):
                cnt += 1
                self.tello.send_rc_control(0, 0, 0, 0)
                print('도형 탐색 완료')
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
    def find_number_and_contour_info_with_color(self, img, color, save=False, rectangle_contour=False):
        """
        해당 이미지의 원하는 색상의 도형을 감지한 다음 그 아래에 있는 숫자를 반환하는 함수
        :param img: 이미지 원본
        :param color: Color Enum 타입
        :param save: 숫자 이미지 저장 여부

        :return: 숫자
        """
        print('색, 숫자 매칭 시작')
        # 숫자가 짤리지 않게 패딩 추가
        padding = 0

        kernel = np.ones((5, 5))
        result = -1

        # 색 찾기
        contour_info, _ = self.figure_handler.find_color(img, color, Figure.ANY, 500)
        x, y, w, h = contour_info
        if rectangle_contour:
            coord_list = self.figure_handler.find_color_with_all_contour(img, color, Figure.ANY, 500)
            #
            # for x, y, w, h in coord_list:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 숫자 찾기
        # 정확도를 위해 색 제거
        temp = self.number_handler.delete_color(img)
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
            result = self.number_handler.get_number_with_model(bin_img)
            img_result = np.copy(img)
            # 숫자 contour 그려서 저장
            if save:
                # 외접 사각형 그리기

                cv2.rectangle(img_result, (x, y), (x + w, y + h), (255, 255, 255), 2)

                cv2.putText(img_result, str(result), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (255, 255, 255),
                            thickness=3)

                cv2.imwrite(f'{Color(color.value).name}_number.png', img_result)

        print('색, 숫자 매칭 완료')
        return result, (x, y, w, h)
