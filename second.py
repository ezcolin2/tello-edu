import cv2

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
img = cv2.imread("tri7.png")
img+=30
n = find_number_with_color_rectangle(img, Color.RED, save=True, rectangle_contour=True)
print(n)

# TODO : 1. 원하는 색상 사각형이 가운데로 오게하는 코드 작성

# TODO : 2. find_number_with_color를 통해 색상과 숫자 매칭

# TODO : 3. 1, 2번을 반복하여 모든 색상에 대해서 숫자 매칭

# TODO : 4. 숫자를 기준으로 정렬

# TODO : 5. 순서에 맞게 진행

