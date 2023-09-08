from main.module.handler.FigureHandler import FigureHandler
from main.module.enum.Color import Color
from main.module.enum.Figure import Figure
import cv2
figure_handler = FigureHandler()
# 사각형 링 감지 테스트
img = cv2.imread("images/3_6_9.png")
contour_info ,object_type = figure_handler.find_color(img, Color.GREEN, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
print(x, y, w, h)
cropped_img = img[y:y+h,x:x+w]
cv2.imshow("cropped img", cropped_img)
approx_list = figure_handler.find_color_with_all_contour(cropped_img, Color.GREEN, Figure.RECTANGLE, 5000)
print(approx_list)
for i, approx in enumerate(approx_list):
    print(f'{i+1}번째 approx 개수 : {len(approx)}')

print(figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img))

# 사각형 감지 테스트
img_rectangle = cv2.imread("images/red-rectangle.png")
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


cv2.waitKey()