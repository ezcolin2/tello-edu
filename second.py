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
    # 숫자가 짤리지 않게 패딩 추가
    padding = 20

    kernel = np.ones((3, 3))
    result = -1
    contour_info, _ = find_color(img, color, Figure.RECTANGLE)
    x, y, w, h = contour_info
    if rectangle_contour:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    temp = delete_color(img)
    temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)

    thr, mask = cv2.threshold(temp, 95, 255, cv2.THRESH_BINARY_INV)
    mask = cv2.dilate(mask, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
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

                num_img = img[y:y+h, x:x+w]
                result_image = cv2.cvtColor(num_img, cv2.COLOR_BGR2GRAY)

                thr, bin_img = cv2.threshold(result_image, 80, 255, cv2.THRESH_BINARY_INV)
                bin_img = cv2.dilate(bin_img, kernel, iterations=1)

                # 이진화 된 이미지로 숫자 판단
                result = get_number_with_model(bin_img)

                # 숫자 contour 그려서 저장
                if save:
                    # 외접 사각형 그리기
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

                    cv2.putText(img, str(result), (x+w//2, y-20), cv2.FONT_ITALIC, 1, (255, 255, 255), thickness=3)

                    cv2.imwrite(f'second_result/{Color(color.value).name}_number.png', img)

    return result
img = cv2.imread("tri9.png")
img+=30
n = find_number_with_color_rectangle(img, Color.BLUE, save=True, rectangle_contour=True)
print(n)

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
    my_frame += brightness
    img = cv2.resize(my_frame, (cam_width, cam_height))

    # 색깔과 매칭되는 값을 -1로 초기화
    red = -1
    green = -1
    blue = -1

    # 색깔별로 매칭되는 값 구하기
    temp_r = find_number_with_color_rectangle(img)
    temp_g = find_number_with_color_rectangle(img)
    temp_b = find_number_with_color_rectangle(img)

    # 아직 값이 정해지지 않는 색에 매칭
    if red!=-1:
        red = temp_r
    if green!=-1:
        green = temp_g
    if blue!=-1:
        blue = temp_b

    # 옆으로 이동
    tello.move_left(50)

    # 색깔별로 매칭되는 값 구하기
    temp_r = find_number_with_color_rectangle(img)
    temp_g = find_number_with_color_rectangle(img)
    temp_b = find_number_with_color_rectangle(img)

    # 아직 값이 정해지지 않는 색에 매칭
    if red != -1:
        red = temp_r
    if green != -1:
        green = temp_g
    if blue != -1:
        blue = temp_b

    # 옆으로 이동
    tello.move_right(100)

    # 색깔별로 매칭되는 값 구하기
    temp_r = find_number_with_color_rectangle(img)
    temp_g = find_number_with_color_rectangle(img)
    temp_b = find_number_with_color_rectangle(img)

    # 아직 값이 정해지지 않는 색에 매칭
    if red != -1:
        red = temp_r
    if green != -1:
        green = temp_g
    if blue != -1:
        blue = temp_b

    # 원위치로

    tello.move_left(50)

    # 만약 전부 찾지 못했다면 다시 반복
    if red==-1 or green==-1 or blue==-1:
        return match_color_and_number(tello, brightness)

    # RGB 순서로 값 반환
    result = [(red, Color.RED), (green, Color.GREEN), (blue, Color.BLUE)]
    result.sort()

    return result



logging.getLogger('djitellopy').setLevel(logging.WARNING)

tello = Tello()
decoder = cv2.QRCodeDetector()
# 연결
tello.connect()
# 초기 세팅
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0
# 배터리 출력
print(tello.get_battery())

# stream 끔
tello.streamoff()
# detection_qr(tello)
tello.send_rc_control(0, 0, 0, 0)
# stream 킴
tello.streamon()
tello.send_rc_control(0, 0, 0, 0)
# 이륙
tello.takeoff()
time.sleep(2)
# 도형들이 위치한 높이까지 올라간다.
tello.move_up(30)

# 오름차순 정렬
result = match_color_and_number(tello, brightness=30)

# 순서대로 미션 진행
for i in range(3):

    # 숫자1에 매치되는 색상을 찾음
    move_until_find_figure(tello, result[i][1], Figure.ANY, Direction.CLOCKWISE, brightness=30)

    # 해당 색상이 가운데로 오게 함
    tello_detection_figure(tello, result[i][1], Figure.ANY, brightness=30)

    # 숫자 contour 그려서 저장
    frame_read = tello.get_frame_read()
    my_frame = frame_read.frame
    my_frame += 30
    img = cv2.resize(my_frame, (cam_width, cam_height))
    find_number_with_color_rectangle(img, result[i][1], save=True)

    # 통과
    tello.move_forward(150)

    # RGB 순서대로 통과
    move_until_find_figure(tello, Color.value(i), Figure.ANY, Direction.CLOCKWISE, brightness=30)
    tello_detection_figure(tello, Color.value(i), Figure.ANY, brightness=30)
    tello.move_forward(150)

    # 다시 숫자 쪽을 바라보도록 회전
    tello.rotate_clockwise(180)





