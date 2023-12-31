from main.module.handler.NumberHandler import NumberHandler
from main.module.handler.NumberHandlerV2 import NumberHandlerV2
from main.module.ai_model.NumberModel import NumberModel
from main.module.ai_model.NumberModelV2 import NumberModelV2
import torch
import cv2
import numpy as np
from main.module.enum.Color import Color
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
def load(root, fileName):
    import os

    state_dict = torch.load(os.path.abspath(os.path.join(root, fileName + '.pth')))
    model = state_dict['model_state_dict']
    optimizer = state_dict['optimizer_state_dict']

    return model, optimizer

# model = NumberModelV2()  # 모델 클래스 정의로 변경
#
# msd, _ = load('../../../main/module/ai_model/', 'classifier')
# model.load_state_dict(msd)
# model.eval()
# number_handler = NumberHandlerV2(model)

model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("../../../main/module/ai_model/cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# NumberHandler 인스턴스 생성
number_handler = NumberHandler(model)

# 숫자 이미지 파일
one_img = cv2.imread("images/1.png")
one_img[240:, :] = (255, 255, 255)
(x, y, w, h), predicted = number_handler.find_biggest_number(one_img, 500)
cv2.rectangle(one_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
cv2.putText(one_img, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

# 더 큰 숫자 이미지
one_img_big = cv2.imread("images/1_big.png")
(x, y, w, h), predicted = number_handler.find_biggest_number(one_img_big, 500)
cv2.rectangle(one_img_big, (x, y), (x+w, y+h), (255, 0, 0), 2)
cv2.putText(one_img_big, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

# 1, 7, 9 멀리서
one_seven_nine = cv2.imread("images/1_and_7_and_9.png")
one_seven_nine[240:, :] = (255, 255, 255)
result = number_handler.find_all_numbers(one_seven_nine, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(one_seven_nine, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(one_seven_nine, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

# 7, 9 가까이
seven_nine = cv2.imread("images/7_and_9.png")
seven_nine[300:, :] = (255, 255, 255)
result = number_handler.find_all_numbers(seven_nine, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(seven_nine, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(seven_nine, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

numbers = cv2.imread("images/numbers.png")
result = number_handler.find_all_numbers(numbers, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(numbers, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(numbers, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

three_six_nine = cv2.imread("images/3_6_9.png")
result = number_handler.find_all_numbers(three_six_nine, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(three_six_nine, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(three_six_nine, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

three_six_nine_only_red = cv2.imread("images/3_6_9.png")

three_six_nine_only_red = number_handler.delete_specific_color(three_six_nine_only_red, Color.BLUE)
three_six_nine_only_red = number_handler.delete_specific_color(three_six_nine_only_red, Color.GREEN)
result = number_handler.find_all_numbers(three_six_nine_only_red, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(three_six_nine_only_red, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(three_six_nine_only_red, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)
# 작은 숫자 이미지
hihi = cv2.imread("images/09-15.png")
result = number_handler.find_all_numbers(hihi, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

# 여러 숫자 이미지
stacked_img = stackImages(0.6, ([[one_img, one_img_big, numbers], [one_seven_nine, seven_nine, three_six_nine_only_red]]))
cv2.imshow("stack", stacked_img)
cv2.imshow("small", hihi)

# 작은 숫자 이미지
hihi2 = cv2.imread("images/09-27-number-7.png")
result = number_handler.find_all_numbers(hihi2, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi2, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi2, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

cv2.imshow("small2", hihi2)

# 작은 숫자 이미지
hihi3 = cv2.imread("images/09-27-2.png")
result = number_handler.find_all_numbers(hihi3, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi3, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi3, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

cv2.imshow("small3", hihi3)

# 작은 숫자 이미지
hihi4 = cv2.imread("images/blue-2.png")
result = number_handler.find_all_numbers(hihi4, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi4, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi4, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

cv2.imshow("small4", hihi4)

# 작은 숫자 이미지
hihi5 = cv2.imread("images/red-8.png")
result = number_handler.find_all_numbers(hihi5, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi5, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi5, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

cv2.imshow("small5", hihi5)

# 작은 숫자 이미지
hihi6 = cv2.imread("images/green-52.png")
result = number_handler.find_all_numbers(hihi6, 500)
for (x, y, w, h), predicted in result:
    cv2.rectangle(hihi6, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.putText(hihi6, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)

cv2.imshow("small6", hihi6)

# # 숫자 이미지 파일
# hihi4= cv2.imread("images/09-27-number-7.png")
# (x, y, w, h), predicted = number_handler.find_biggest_number(hihi4, 500)
# cv2.rectangle(hihi4, (x, y), (x+w, y+h), (255, 0, 0), 2)
# cv2.putText(hihi4, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)
# cv2.imshow("small4", hihi4)
# # 숫자 이미지 파일
# hihi5= cv2.imread("images/09-27-2.png")
# (x, y, w, h), predicted = number_handler.find_biggest_number(hihi5, 500)
# cv2.rectangle(hihi5, (x, y), (x+w, y+h), (255, 0, 0), 2)
# cv2.putText(hihi5, str(predicted), (x + w // 2, y - 20), cv2.FONT_ITALIC, 1, (0, 0, 0),thickness=3)
# cv2.imshow("small5", hihi5)
cv2.waitKey()