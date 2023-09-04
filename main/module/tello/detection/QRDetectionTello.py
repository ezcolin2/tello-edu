from djitellopy import Tello
import cv2
from main.module.params.PIDParams import PIDParams
from main.module.params.RangeParams import RangeParams
from main.module.params.CamParams import CamParams
from main.module.tello.TrackingTello import TrackingTello
from main.module.handler.FigureHandler import FigureHandler
from main.module.handler.QRHandler import QRHandler
class QRDetectionTello:

    def __init__(
            self,
            tello: Tello,
            cam_params: CamParams,
            range_params: RangeParams,
            pid_params: PIDParams
    ):
        self.tello: Tello = tello
        self.cam_params: CamParams = cam_params
        self.range_params: RangeParams = range_params
        self.tracking_tello: TrackingTello = TrackingTello(self.tello, range_params, pid_params, cam_params)
        self.figure_handler: FigureHandler = FigureHandler()
        self.qr_handler: QRHandler = QRHandler()



    def tello_detection_qr(self, brightness=0):
        """
        Tello를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
        (qr 코드를 중앙에 맞추는 코드를 구현했으나 필요성을 못 느껴 코드 전에 break 넣음)
        :return: 없음
        """
        p_error = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        while True:
            frame_read = self.tello.get_frame_read()
            my_frame = frame_read.frame
            img = cv2.resize(my_frame + brightness, (cam_width, cam_height))
            barcode_info, img = self.qr_handler.read_img(img)
            cv2.imshow("QR detection", img)
            contour_info = barcode_info[:4]
            barcode = barcode_info[4]
            if barcode is None:
                continue
            else:
                print(barcode.data.decode('utf-8'))
                break
            # 객체 가운데로
            success, p_error = self.tracking_tello.track_figure_with_rotate(self.tello, contour_info, pid, p_error)
            if success:
                barcode_info = barcode.data.decode('utf-8')
                print(barcode_info)
                break
            # q를 누르면 무한 반복에서 빠져나옴
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self.tello.send_rc_control(0, 0, 0, 0)

    def move_until_find_qr(self, direction, brightness=0):
        """
        원하는 색상의 도형을 찾을 때까지 회전
        :return: 없음
        """
        cnt = 0
        cam_width = self.cam_params.width
        cam_height = self.cam_params.height
        while cnt < 4:
            velocity = [0, 0, 0, 0]  # send_rc_control의 인자로 들어갈 값.
            frame_read = self.tello.get_frame_read()
            myFrame = frame_read.frame
            img = cv2.resize(myFrame + brightness, (cam_width, cam_height))
            barcode_info, img = self.qr_handler.read_img(img)
            cv2.imshow("QR detection", img)
            contour_info = barcode_info[:4]
            barcode = barcode_info[4]
            cv2.imshow("asdf", img)
            x, y, w, h = contour_info
            if (
                    cam_width * (0.5 - self.range_params.find_range_percentage) <= x + w // 2 <= cam_width * (0.5 + self.range_params.find_range_percentage)
                    and cam_height * (0.5 - self.range_params.find_range_percentage) <= y + h // 2 <= cam_height * (0.5 + self.range_params.find_range_percentage)
                    and barcode is not None
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
        print("감지 ")
        self.tello.send_rc_control(0, 0, 0, 0)
        cv2.destroyAllWindows()