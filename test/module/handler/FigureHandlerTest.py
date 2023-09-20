from main.module.handler.FigureHandler import FigureHandler
from main.module.handler.ImageHandler import ImageHandler
from main.module.enum.Color import Color
from main.module.enum.Figure import Figure
import cv2
figure_handler = FigureHandler()
image_handler = ImageHandler()
# 사각형 링 감지 테스트
img = cv2.imread("images/3_6_9.png")
contour_info ,object_type = figure_handler.find_color(img, Color.GREEN, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
print(x, y, w, h)
cropped_img = img[y:y+h,x:x+w]
cv2.imshow("cropped img", cropped_img)
print(f'초록색 링 여부 : {figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img)}, 정답 : True')
approx_list = figure_handler.find_color_with_all_contour(cropped_img, Color.GREEN, Figure.RECTANGLE, 5000)
print(approx_list)
for i, approx in enumerate(approx_list):
    print(f'{i+1}번째 approx 개수 : {len(approx)}')


# 사각형 감지 테스트
img_rectangle = cv2.imread("../../tello/detection/images/red-rectangle.png")
contour_info, object_type = figure_handler.find_color(img_rectangle, Color.RED, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
print(x, y, w, h)
cropped_img_rectangle = img_rectangle[y:y + h, x:x + w]
cv2.imshow("cropped img rectangle", cropped_img_rectangle)
approx_list_rectangle = figure_handler.find_color_with_all_contour(cropped_img_rectangle, Color.RED, Figure.RECTANGLE, 5000)
print(approx_list_rectangle)
for i, approx in enumerate(approx_list_rectangle):
    print(f'{i+1}번째 approx 개수 : {len(approx)}')

# 이미지 원본 contour 그리기 테스트
figure_handler.find_color(img, Color.BLUE, Figure.RECTANGLE, 5000, draw_contour=True)
figure_handler.find_color_with_all_contour(img, Color.GREEN, Figure.RECTANGLE, 5000, draw_contour=True)

cv2.imshow("origin image", img)

print(figure_handler.is_ring(Color.RED, Figure.RECTANGLE, cropped_img_rectangle))

img2 = cv2.imread("images/img.png")
figure_handler.find_color(img2, Color.GREEN, Figure.RECTANGLE, 100, draw_contour=True)
figure_handler.find_color_with_all_contour(img2, Color.BLUE, Figure.RECTANGLE, 0, draw_contour=True)


cv2.imshow("hello", img2)

img3 = cv2.imread("images/img_1.png")

# 잘린 사각형 링 이미지 감지 테스트
contour_info, figure_type, = figure_handler.find_color(img3, Color.BLUE, Figure.ANY, 100, draw_contour=True)
x, y, w, h = contour_info
is_blue_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, img3[y : y+h, x : x+w])
print(f'파란색 링 여부 : {is_blue_ring}, 정답 : False')

# 잘린 사각형 링 이미지 감지 테스트
contour_info, figure_type, = figure_handler.find_color(img3, Color.GREEN, Figure.ANY, 100, draw_contour=True)
x, y, w, h = contour_info
is_blue_ring = figure_handler.is_ring(Color.GREEN, Figure.ANY, img3[y : y+h, x : x+w])
print(f'초록색 링 여부 : {is_blue_ring}, 정답 : False')


figure_handler.find_color_with_all_contour(img3, Color.GREEN, Figure.RECTANGLE, 0, draw_contour=True)
cv2.imshow("hello2", img3)

img4 = cv2.imread("images/img_2.png")

# 잘린 사각형 링 이미지 감지 테스트
contour_info, figure_type, = figure_handler.find_color_except_ring(img4, Color.BLUE, Figure.ANY, 100, draw_contour=True)
x, y, w, h = contour_info
is_blue_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, img4[y : y+h, x : x+w])
print(f'파란색 링 여부 : {is_blue_ring}, 정답 : False')



contour_info, figure_type, = figure_handler.find_color(img4, Color.RED, Figure.ANY, 100, draw_contour=True)
cv2.imshow("hello3", img4)

img5 = cv2.imread("./images/ring_rectangle.png")
# 사각형, 링 구분 테스트
contour_info, figure_type, = figure_handler.find_color_except_ring(img5, Color.RED, Figure.ANY, 100, draw_contour=True)
x, y, w, h = contour_info
is_red_ring = figure_handler.is_ring(Color.RED, Figure.ANY, img5[y : y+h, x : x+w])
print(is_red_ring)
print(contour_info, figure_type)
cv2.imshow("hello4", img5)

img4 = cv2.imread("images/home-blue.png")

# 파란 링 이미지 감지 테스트
contour_info, figure_type, = figure_handler.find_color(img4, Color.BLUE, Figure.ANY, 100, draw_contour=True)
x, y, w, h = contour_info
is_blue_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, img4[y : y+h, x : x+w])
print(f'파란색 링 여부 : {is_blue_ring}, 정답 : True')
cv2.waitKey()