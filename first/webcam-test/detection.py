from color_detection_module import *
import time
def detection_figure(webcam_cap, color, figure):
    """
    인자로 들어온 색과 모양으로 해당 도형을 감지 여부 반환
    :param webcam_cap : cam
    :param color : 색상
    :param figure : 도형
    :return: 도형 감지 여부 반환
    """

    # 가장 먼저 해당 도형을 찾기 위해 회전한다.

    p_error = 0
    while True:
        # success는 성공 여부, img는 이미지
        _, img = webcam_cap.read()
        contour_info, figureType = findColor(img, color, figure)
        print(contour_info, figureType)
        cv2.imshow("Video", img)


        # q를 누르면 무한 반복에서 빠져나옴
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("hello.png", img)
            break