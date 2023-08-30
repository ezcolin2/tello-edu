from module.image_processing_module import *
from module.tello_tracking_module import *
def tello_detection_figure(tello, color, figure, brightness=0, save=False, print=False):
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
    while True:
        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame+brightness, (cam_width, cam_height))
        contour_info, figure_type = find_color(img, color, figure)
        cv2.imshow("Video", img)


        # 객체 가운데로
        success, p_error = track_figure(tello, contour_info,  pid, p_error)
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

            if print:
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
    tello.send_rc_control(0, 0, 0, 0)
def tello_detection_qr(tello, brightness=0):
    """
    Tello를 인자로 받아서 이미지를 얻어낸 후 qr이 있다면 감지 후 contour 그리기
    :param tello : Tello 객체
    :return: 없음
    """
    p_error = 0

    while True:
        frame_read = tello.get_fra
        me_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
        barcode_info, img = read_img(img)
        cv2.imshow("QR detection", img)
        contour_info = barcode_info[:4]
        barcode = barcode_info[4]
        if barcode==None:
            continue
        else:
            print(barcode.data.decode('utf-8'))
            break
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
def tello_detection_number(tello, brightness=0):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param tello : Tello
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    # 가장 먼저 해당 도형을 찾기 위해 회전한다.

    p_error = 0
    kernel = np.ones((5, 5), np.uint8)

    while True:
        frame_read = tello.get_frame_read()
        my_frame = frame_read.frame
        img = cv2.resize(my_frame+brightness, (cam_width, cam_height))
        cv2.imshow("origin", img)
        img = delete_color(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, kernel, iterations=1)
        contour_info, figure_type = get_contours(img, mask, Figure.NUMBER)
        cv2.imshow("Video", img)


        # 객체 가운데로
        success, p_error = track_number(tello, contour_info,  pid, p_error, False)
        if success:
            # 이미지 이름 정하기
            image_name = "num"  # 저장할 이미지 이름
            cv2.imwrite(f"images/{image_name}.png", img)

            # 터미널에 front, back 출력
            # if figure == Figure.CIRCLE:
            #     print('Front')
            # elif figure == Figure.TRI:
            #     print('Back')
            break
        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    tello.send_rc_control(0, 0, 0, 0)
def move_until_find_figure(tello, color, figure, direction, brightness=0):
    """
    원하는 색상의 도형을 찾을 때까지 회전
    :param tello: Tello 객체
    :param color: Color enum 타입
    :param figure: Figure enum 타입
    :param direction: Direction enum 타입

    :return: 없음
    """
    cnt = 0
    while cnt < 4:
        velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
        cv2.imshow("asdf", img)
        contour_info, figureType = find_color(img, color, figure)
        x, y, w, h = contour_info
        if (
                cam_width * (0.5 - find_range) <= x + w // 2 <= cam_width * (0.5 + find_range)
                and cam_height * (0.5 - find_range) <= y + h // 2 <= cam_height * (0.5 + find_range)
                and figureType >= 0
                and w * h > min_find_area
        ):
            cnt += 1
            tello.send_rc_control(0, 0, 0, 0)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        v = 20
        if direction.value%2==1: # 홀수라면 음수로 바꿈
            v=-v
        velocity[direction.value//2] = v
        tello.send_rc_control(*velocity)
    tello.send_rc_control(0, 0, 0, 0)
    cv2.destroyAllWindows()
def move_until_find_qr(tello, direction, brightness=0):
    """
    원하는 색상의 도형을 찾을 때까지 회전
    :param tello: Tello 객체
    :return: 없음
    """
    cnt = 0
    while cnt < 4:
        velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
        barcode_info, img = read_img(img)
        cv2.imshow("QR detection", img)
        contour_info = barcode_info[:4]
        barcode = barcode_info[4]
        cv2.imshow("asdf", img)
        x, y, w, h = contour_info
        if (
                cam_width * (0.5 - find_range_qr) <= x + w // 2 <= cam_width * (0.5 + find_range_qr)
                and cam_height * (0.5 - find_range_qr) <= y + h // 2 <= cam_height * (0.5 + find_range_qr)
                and barcode is not None
                and w * h > min_find_area
        ):
            cnt += 1
            tello.send_rc_control(0, 0, 0, 0)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        v = 20
        if direction.value%2==1: # 홀수라면 음수로 바꿈
            v=-v
        velocity[direction.value//2] = v
        tello.send_rc_control(*velocity)
    print("감지 ")
    tello.send_rc_control(0, 0, 0, 0)
    cv2.destroyAllWindows()

def move_until_find_number(tello, figure, direction, brightness=0):
    """
    숫자를 찾을 때까지 회전 (단순 검정 검출)
    :param tello: Tello 객체
    :param direction: Direction enum 타입
    :return: 없음
    """
    cnt = 0
    kernel = np.ones((5, 5), np.uint8)

    while cnt < 4:
        velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
        frame_read = tello.get_frame_read()
        myFrame = frame_read.frame
        img = cv2.resize(myFrame+brightness, (cam_width, cam_height))
        cv2.imshow("original", img)
        img = delete_color(img)
        cv2.imshow("delete", img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.dilate(mask, kernel, iterations=1)
        contour_info, figureType = get_contours(img, mask, Figure.NUMBER)
        cv2.imshow("asdf", img)

        x, y, w, h = contour_info
        if (
                cam_width * (0.5 - find_range) <= x + w // 2 <= cam_width * (0.5 + find_range)
                and cam_height * (0.5 - find_range) <= y + h // 2 <= cam_height * (0.5 + find_range)
                and figureType >= 0
                # and w * h > min_find_area
        ):
            cnt += 1
            tello.send_rc_control(0, 0, 0, 0)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        v = 20
        if direction.value%2==1: # 홀수라면 음수로 바꿈
            v=-v
        velocity[direction.value//2] = v
        tello.send_rc_control(*velocity)
    tello.send_rc_control(0, 0, 0, 0)
    cv2.destroyAllWindows()