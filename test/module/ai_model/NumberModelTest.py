from main.module.handler.NumberHandler import NumberHandler
from main.module.ai_model.NumberModel import NumberModel
import torch
import cv2
# 숫자 인식 모델 생성
model = NumberModel()  # 모델 클래스 정의로 변경
model.load_state_dict(torch.load("./cnn_model.pth"))
model.eval()  # 모델을 평가 모드로 설정

# number handler 생성
number_handler = NumberHandler(model)

# 이미지 가져오기
img = cv2.imread("./red-number.png")
(x, y, w, h), predicted = number_handler.find_biggest_number(img, 1000)
print(x, y, w, h, predicted)

numbers = number_handler.find_all_numbers(img, 1000)
for (x, y, w, h), predicted in numbers:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 255),thickness=2)
    cv2.putText(img, str(predicted), (x+w, y), cv2.FONT_ITALIC, 1.5, (0, 255,255), thickness=2)
    print(x, y, w, h, predicted)

# 멀리 있는 이미지 가져오기
img2 = cv2.imread("./img.png")
numbers2 = number_handler.find_all_numbers(img2, 1000)
for (x, y, w, h), predicted in numbers2:
    cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255),thickness=2)
    cv2.putText(img2, str(predicted), (x+w, y), cv2.FONT_ITALIC, 1.5, (0, 255,255), thickness=2)
    print(x, y, w, h, predicted)

cv2.imshow("numbers", img)
cv2.imshow("numbers2", img2)
cv2.waitKey()

