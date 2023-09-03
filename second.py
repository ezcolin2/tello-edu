from module.ai_model.NumberModel import *
from module.handler.NumberHandler import NumberHandler
import time
from module.enum.Color import *

# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# img+=30
# n=number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=True)
# print(n)
#
number_handler = NumberHandler(model)
cam_width = 640
cam_height = 480
def match_color_and_number(tello, brightness=0):
    """
    R, G, B에 대해서 아래에 있는 숫자를 매치하고 오름차순으로 정렬해서 반환
    :param tello: Tello 객체
    :param brightness: 이미지 밝기
    :return: [(숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상)]
    """
    global number_handler
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    # 색깔과 매칭되는 값을 -1로 초기화
    red = -1
    green = -1
    blue = -1

    # 색깔별로 매칭되는 값 구하기
    temp_r = number_handler.find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
    temp_g = number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=False)
    temp_b = number_handler.find_number_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=False)

    # 아직 값이 정해지지 않는 색에 매칭
    if red==-1:
        red = temp_r
    if green==-1:
        green = temp_g
    if blue==-1:
        blue = temp_b

    print(f'첫 번째 숫자 인식 : {[(temp_r, Color.RED), (temp_g, Color.GREEN), (temp_b, Color.BLUE)]}')


    time.sleep(2)
    # 옆으로 이동
    tello.move_left(70)

    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    # 색깔별로 매칭되는 값 구하기
    temp_r = number_handler.find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
    temp_g = number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=False)
    temp_b = number_handler.find_number_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=False)

    # 아직 값이 정해지지 않는 색에 매칭
    if red == -1:
        red = temp_r
    if green == -1:
        green = temp_g
    if blue == -1:
        blue = temp_b

    print(f'두 번째 숫자 인식 : {[(temp_r, Color.RED), (temp_g, Color.GREEN), (temp_b, Color.BLUE)]}')
    # 옆으로 이동
    time.sleep(2)
    tello.move_right(160)

    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    # 색깔별로 매칭되는 값 구하기
    temp_r = number_handler.find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
    temp_g = number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=False)
    temp_b = number_handler.find_number_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=False)

    # 아직 값이 정해지지 않는 색에 매칭
    if red == -1:
        red = temp_r
    if green == -1:
        green = temp_g
    if blue == -1:
        blue = temp_b
    print(f'세 번째 숫자 인식 : {[(temp_r, Color.RED), (temp_g, Color.GREEN), (temp_b, Color.BLUE)]}')

    # 원위치로
    time.sleep(2)
    tello.move_left(70)

    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    # 색깔별로 매칭되는 값 구하기
    temp_r = number_handler.find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=False)
    temp_g = number_handler.find_number_with_color_rectangle(img, Color.GREEN, save=True, rectangle_contour=False)
    temp_b = number_handler.find_number_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=False)

    # 아직 값이 정해지지 않는 색에 매칭
    if red == -1:
        red = temp_r
    if green == -1:
        green = temp_g
    if blue == -1:
        blue = temp_b
    print(f'네 번째 숫자 인식 : {[(temp_r, Color.RED), (temp_g, Color.GREEN), (temp_b, Color.BLUE)]}')

    print([(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)])

    # 만약 전부 찾지 못했다면 다시 반복
    if red==-1 or green==-1 or blue==-1:
        # return match_color_and_number(tello, brightness)
        return "don't find"

    # RGB 순서로 값 반환
    result = [(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)]
    result.sort()
    print(f'최종 숫자 : {[(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)]}')

    return result

# def move_until_find_number(tello, figure, direction, brightness=30, number):
#     """
#     숫자를 찾을 때까지 회전 (단순 검정 검출)
#     :param tello: Tello 객체
#     :param direction: Direction enum 타입
#     :return: 없음
#     """
#     cnt = 0
#     kernel = np.ones((5, 5), np.uint8)
#
#     while cnt < 4:
#         velocity = [0, 0, 0, 0] # send_rc_control의 인자로 들어갈 값.
#         frame_read = tello.get_frame_read()
#         myFrame = frame_read.frame
#         myFrame += brightness
#         img = cv2.resize(myFrame, (cam_width, cam_height))
#         cv2.imshow("original", img)
#         img = delete_color(img)
#         cv2.imshow("delete", img)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         thr, mask = cv2.threshold(img, 95, 255, cv2.THRESH_BINARY_INV)
#         mask = cv2.dilate(mask, kernel, iterations=1)
#         contour_info, figureType = get_contours(img, mask, Figure.NUMBER)
#         cv2.imshow("asdf", img)
#
#         x, y, w, h = contour_info
#         if (
#                 cam_width * (0.5 - find_range) <= x + w // 2 <= cam_width * (0.5 + find_range)
#                 and cam_height * (0.5 - find_range) <= y + h // 2 <= cam_height * (0.5 + find_range)
#                 and figureType >= 0
#                 and get_number_with_model()
#                 # and w * h > min_find_area
#         ):
#             cnt += 1
#             tello.send_rc_control(0, 0, 0, 0)
#             break
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#         v = 20
#         if direction.value%2==1: # 홀수라면 음수로 바꿈
#             v=-v
#         velocity[direction.value//2] = v
#         tello.send_rc_control(*velocity)
#     tello.send_rc_control(0, 0, 0, 0)
#     cv2.destroyAllWindows()
#
# logging.getLogger('djitellopy').setLevel(logging.WARNING)
#
# tello = Tello()
# # 연결
# tello.connect()
# print("연결 완료")
# # 초기 세팅
# tello.for_back_velocity = 0
# tello.left_right_velocity = 0
# tello.up_down_velocity = 0
# tello.yaw_velocity = 0
# tello.speed = 0
# # 배터리 출력
# print(f'남은 배터리 : {tello.get_battery()}')
#
# # stream 끔
# tello.streamoff()
# # tello.send_rc_control(0, 0, 0, 0)
# # stream 킴
# tello.streamon()
# # tello.send_rc_control(0, 0, 0, 0)
# # 이륙
# tello.takeoff()
# print('이륙')
# time.sleep(2)
# # 도형들이 위치한 높이까지 올라간다.
# tello.move_up(30)
# print('위로 이동')
# time.sleep(2)
#
# # 오름차순 정렬
# result = match_color_and_number(tello, brightness=30)
# move_until_find_figure(tello, result[2][1], Figure.ANY, Direction.CLOCKWISE, brightness=30)
# tello_detection_figure(tello, result[2][1], Figure.ANY, brightness=30, save=True)
# tello.land()
# print(result)

#
# # 순서대로 미션 진행
# for i, color in enumerate(Color):
#
#     # 숫자1에 매치되는 색상을 찾음
#     move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.CLOCKWISE, brightness=30)
#
#     # 해당 색상이 가운데로 오게 함
#     tello_detection_figure(tello, result[i][1], Figure.ANY, brightness=30)
#
#     # 숫자 contour 그려서 저장
#     frame_read = tello.get_frame_read()
#     my_frame = frame_read.frame
#     my_frame += 30
#     img = cv2.resize(my_frame, (cam_width, cam_height))
#     find_number_with_color_rectangle(img, result[i][1], save=True)
#
#     # 통과
#     tello.move_forward(150)
#     # RGB 순서대로 통과
#     move_until_find_figure(tello, color, Figure.ANY, Direction.CLOCKWISE, brightness=30)
#     tello_detection_figure(tello, color, Figure.ANY, brightness=30, save=True)
#     tello.move_forward(150)
#
#     # 다시 숫자 쪽을 바라보도록 회전
#     tello.rotate_clockwise(180)
#


