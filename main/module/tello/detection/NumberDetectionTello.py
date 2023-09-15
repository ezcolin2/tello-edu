from djitellopy import Tello
import cv2
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.TrackingTello import TrackingTello
from main.module.handler.NumberHandler import NumberHandler
from main.module.handler.ImageHandler import ImageHandler
class NumberDetectionTello:

    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            pid_params: PIDParams,
            range_params: RangeParams,
            model
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.pid_params: PIDParams = pid_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(tello, range_params, pid_params, cam_params)
        self.number_handler: NumberHandler = NumberHandler(model)
        self.image_handler : ImageHandler = ImageHandler()
        self.model = model

    def move_until_find_number(self, direction, brightness=0, save=True):
        """
        숫자를 찾을 때까지 이동  (단순 검정 검출)
        :param direction: Direction enum 타입
        :return: 예측 숫자
        """
        cnt = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        img = None
        predicted = -1
        x, y, w, h = 0, 0, 0, 0
        while cnt < 4:
            velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
            frame_read = self.tello.get_frame_read()
            myFrame = frame_read.frame
            img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
            # cv2.imshow("original", img)
            # img = self.image_handler.delete_color(img)
            # cv2.imshow("delete", img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
            # mask = cv2.dilate(mask, kernel, iterations=1)Vk
            img = self.image_handler.delete_color(img)
            contour_info, predicted = self.number_handler.find_biggest_number(img, 500)
            x, y, w, h = contour_info
            if (
                    x!= 0 and y!=0 and w!=0 and h!=0
                    and cam_width * (0.5 - self.range_params.find_range_percentage//2) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage//2)
                    and cam_height * (0.5 - self.range_params.find_range_percentage//2) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage//2)
            ):
                cnt += 1
                self.tello.send_rc_control(0, 0, 0, 0)
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            v = 20
            if direction.value%2==1: # 홀수라면 음수로 바꿈
                v=-v
            velocity[direction.value//2] = v
            self.tello.send_rc_control(*velocity)
        self.tello.send_rc_control(0, 0, 0, 0)
        cv2.imshow("asdf", img)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
        cv2.imwrite("number.png", img)
        cv2.destroyAllWindows()
        return predicted
    # def move_until_find_specific_number(self, direction, number, brightness=0):
    #     """
    #     원하는 숫자를 찾을 때까지 이동하는 함수
    #     :param direction: 이동 방향
    #     :param number: 찾을 숫자
    #     :param brightness: 밝기
    #     :return:
    #     """
    #     cnt = 0
    #     kernel = np.ones((5, 5), np.uint8)
    #     cam_width = self.cam_params.width
    #     cam_height = self.cam_params.height
    #
    #     while cnt < 4:
    #         velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
    #         frame_read = self.tello.get_frame_read()
    #         myFrame = frame_read.frame
    #         img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
    #         cv2.imshow("original", img)
    #         img = self.number_handler.delete_color(img)
    #         cv2.imshow("delete", img)
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
    #         mask = cv2.dilate(mask, kernel, iterations=1)
    #         contour_info, figureType = self.figure_handler._get_biggest_contour(img, mask, Figure.NUMBER)
    #         cv2.imshow("asdf", img)
    #
    #         x, y, w, h = contour_info
    #         if (
    #                 cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage)
    #                 and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage)
    #                 and figureType >= 0
    #                 # and w * h > min_find_area
    #         ):
    #             cnt += 1
    #             self.tello.send_rc_control(0, 0, 0, 0)
    #             break
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #         v = 20
    #         if direction.value%2==1: # 홀수라면 음수로 바꿈
    #             v=-v
    #         velocity[direction.value//2] = v
    #         self.tello.send_rc_control(*velocity)
    #     self.tello.send_rc_control(0, 0, 0, 0)
    #     cv2.destroyAllWindows()
    # def tello_detection_number(self, brightness=0):
    #     """
    #     인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    #     :param tello : Tello
    #     :param color : 색상
    #     :param figure : 도형
    #     :return: 도형 감지 여부 반환
    #     """
    #
    #     cam_width = self.cam_params.width
    #     cam_height = self.cam_params.height
    #     pid = self.pid_params.pid_value
    #
    #
    #     p_error = 0
    #     kernel = np.ones((5, 5), np.uint8)
    #
    #     while True:
    #         frame_read = self.tello.get_frame_read()
    #         my_frame = frame_read.frame
    #         img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
    #         cv2.imshow("origin", img)
    #         img = self.image_handler.delete_color(img)
    #         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #         thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
    #         mask = cv2.dilate(mask, kernel, iterations=1)
    #         contour_info, figure_type = self.figure_handler._get_biggest_contour(img, mask, Figure.NUMBER)
    #         cv2.imshow("Video", img)
    #
    #         # 객체 가운데로
    #         success, p_error = self.tracking_tello.track_number(self.tello, contour_info, pid, p_error, False)
    #         if success:
    #             # 이미지 이름 정하기
    #             image_name = "num"  # 저장할 이미지 이름
    #             cv2.imwrite(f"images/{image_name}.png", img)
    #
    #             # 터미널에 front, back 출력
    #             # if figure == Figure.CIRCLE:
    #             #     print('Front')
    #             # elif figure == Figure.TRI:
    #             #     print('Back')
    #             break
    #         # q를 누르면 무한 반복에서 빠져나옴
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     cv2.destroyAllWindows()
    #     self.tello.send_rc_control(0, 0, 0, 0)