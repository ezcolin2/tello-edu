from module.image_processing_module import *
from module.tello_tracking_module import *
def tello_detection_figure(tello, color, figure):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param tello : Tello
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    # 가장 먼저 해당 도형을 찾기 위해 회전한다.

    p_error = 0
    while True:
        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame, (cam_width, cam_height))
        contour_info, figure_type = find_color(img, color, figure)
        print(contour_info, figure_type)
        cv2.imshow("Video", img)

        # 이미지 이름 정하기
        image_name="" # 저장할 이미지 이름
        if color==Color.RED:
            image_name+="red"
        elif color==Color.GREEN:
            image_name+="green"
        elif color==Color.BLUE:
            image_name+="blue"
        if figure==Figure.TRI:
            image_name+=" triangle"
        elif figure==Figure.CIRCLE:
            image_name+=" circle"

        # 객체 가운데로
        success, p_error = track_figure(tello, contour_info,  pid, p_error)
        # print(success, p_error)
        if success:
            cv2.imwrite(f"images/{image_name}.png", img)
            break
        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    tello.send_rc_control(0, 0, 0, 0)
def tello_detection_qr(tello):
    """
    Tello를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
    :param tello : Tello 객체
    :return: 없음
    """
    p_error = 0

    while True:
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (cam_width, cam_height))
        barcode_info, img = read_img(img)
        cv2.imshow("QR detection", img)
        contour_info = barcode_info[:4]
        barcode = barcode_info[4]
        if barcode==None:
            continue
        # 객체 가운데로
        success, p_error = track_figure(tello, contour_info, pid, p_error)
        if success:
            barcode_info = barcode.data.decode('utf-8')
            print(barcode_info)
            break
        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    tello.send_rc_control(0, 0, 0, 0)
def rotate_until_find(tello, color, figure):
    """
    원하는 색상의 도형을 찾을 때까지 회전
    :param tello: Tello 객체
    :return: 없음
    """
    cnt = 0
    while cnt < 4:
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame, (cam_width, cam_height))
        cv2.imshow("asdf", img)
        contour_info, figureType = find_color(img, color, figure)
        print(contour_info, figureType)
        x, y, w, h = contour_info
        if cam_width * 0.2 <= x + w // 2 <= cam_width * 0.8 and cam_height * 0.2 <= y + h // 2 <= cam_height * 0.8 and figureType >= 0 and w * h > 5000:
            cnt += 1
            tello.send_rc_control(0, 0, 0, 0)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        tello.send_rc_control(0, 0, 0, 20)
    print("감지 ")
    tello.send_rc_control(0, 0, 0, 0)
    cv2.destroyAllWindows()