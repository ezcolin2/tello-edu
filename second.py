import colorama.ansi
import cv2
from module.tello_detection_module import *
from module.config import *
import time
from djitellopy import Tello
import logging

from module.tello_detection_module import *
from module.config import *
from module.ai_module import *

model = CNN()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("module/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정


def get_number_with_model(image):
    """
    이진화 처리 된 이미지를 받아서 해당 숫자 판단
    :param image: 이진화 된 이미지
    :return: 감지한 숫자
    """

    global model
    device = torch.device('cpu')
    image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=0)

    image = cv2.resize(image, (28, 28))

    # 이미지를 [0, 1] 범위로 스케일링
    image = image.astype('float32') / 255.0

    # 이미지를 PyTorch 모델에 입력 가능한 형태로 변환
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    image = transform(image).unsqueeze(0)  # 배치 차원 추가
    with torch.no_grad():
        image = image.to(device)
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
    return predicted.item()


def find_number_with_color_rectangle(img, color, save=False, rectangle_contour=False):
    """
    해당 이미지의 원하는 색상의 사각형을 감지한 다음 그 아래에 있는 숫자를 반환하는 함수
    :param img: 이미지 원본
    :param color: Color Enum 타입
    :param save: 숫자 이미지 저장 여부

    :return: 숫자
    """
    print('색, 숫자 매칭 시작')
    # 숫자가 짤리지 않게 패딩 추가
    padding = 20

    kernel = np.ones((3, 3))
    result = -1
    contour_info, _ = find_color(img, color, Figure.RECTANGLE)
    x, y, w, h = contour_info
    if rectangle_contour:
        coord_list = find_color_with_all_contour(img, color, Figure.RECTANGLE, 500)
        #
        # for x, y, w, h in coord_list:
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    temp = delete_color(img)
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    thr, mask = cv2.threshold(temp, 95, 255, cv2.THRESH_BINARY_INV)
    mask = cv2.dilate(mask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 감지한 contour 외접 사각형 좌표
    coord_list =[]
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
        result = get_number_with_model(bin_img)
        img_result = np.copy(img)
        # 숫자 contour 그려서 저장
        if save:
            # 외접 사각형 그리기

            cv2.rectangle(img_result, (x, y), (x + w, y + h), (255, 255, 255), 2)

            cv2.putText(img_result, str(result), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (255, 255, 255), thickness=3)

            cv2.imwrite(f'second_result/{Color(color.value).name}_number.png', img_result)



    print('색, 숫자 매칭 완료')
    return result

# # img+=30
# # n = find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=True)
# print(n)

# TODO : 1. 원하는 색상 사각형이 가운데로 오게하는 코드 작성

# TODO : 2. find_number_with_color를 통해 색상과 숫자 매칭

# TODO : 3. 1, 2번을 반복하여 모든 색상에 대해서 숫자 매칭

# TODO : 4. 숫자를 기준으로 정렬

# TODO : 5. 순서에 맞게 진행



def match_color_and_number(tello, brightness=0):
    """
    R, G, B에 대해서 아래에 있는 숫자를 매치하고 오름차순으로 정렬해서 반환
    :param tello: Tello 객체
    :param brightness: 이미지 밝기
    :return: [(숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상), (숫자1, 숫자 1에 매치되는 색상)]
    """
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    img = cv2.resize(my_frame+brightness, (cam_width, cam_height))

    # 색깔과 매칭되는 값을 -1로 초기화
    red = -1
    green = -1
    blue = -1

    # 색깔별로 매칭되는 값 구하기
    temp_r = find_number_with_color_rectangle(img, Color.RED, save=True)
    temp_g = find_number_with_color_rectangle(img, Color.GREEN, save=True)
    temp_b = find_number_with_color_rectangle(img, Color.BLUE, save=True)

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
    temp_r = find_number_with_color_rectangle(img, Color.RED, save=True)
    temp_g = find_number_with_color_rectangle(img, Color.GREEN, save=True)
    temp_b = find_number_with_color_rectangle(img, Color.BLUE, save=True)

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
    temp_r = find_number_with_color_rectangle(img, Color.RED, save=True)
    temp_g = find_number_with_color_rectangle(img, Color.GREEN, save=True)
    temp_b = find_number_with_color_rectangle(img, Color.BLUE, save=True)

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

logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()
# 연결
tello.connect()
print("연결 완료")
# 초기 세팅
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0
# 배터리 출력
print(f'남은 배터리 : {tello.get_battery()}')

# stream 끔
tello.streamoff()
# tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
# tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
print('이륙')
time.sleep(2)
# 도형들이 위치한 높이까지 올라간다.
tello.move_up(30)
print('위로 이동')
time.sleep(2)

# 오름차순 정렬
result = match_color_and_number(tello, brightness=30)
move_until_find_figure(tello, result[2][1], Figure.ANY, Direction.CLOCKWISE, brightness=30)
tello_detection_figure(tello, result[2][1], Figure.ANY, brightness=30, save=True)
tello.land()
print(result)

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




