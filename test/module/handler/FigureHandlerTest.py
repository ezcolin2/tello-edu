# from main.module.handler.FigureHandler import FigureHandler
# from main.module.handler.ImageHandler import ImageHandler
# from main.module.enum.Color import Color
# from main.module.enum.Figure import Figure
# import cv2
# figure_handler = FigureHandler()
# image_handler = ImageHandler()
# # 사각형 링 감지 테스트
# img = cv2.imread("images/3_6_9.png")
# contour_info ,object_type = figure_handler.find_color(img, Color.GREEN, Figure.RECTANGLE, 100)
# x, y, w, h = contour_info
# print(x, y, w, h)
# cropped_img = img[y:y+h,x:x+w]
# cv2.imshow("cropped img", cropped_img)
# print(f'초록색 링 여부 : {figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img)}, 정답 : True')
# approx_list = figure_handler.find_color_with_all_contour(cropped_img, Color.GREEN, Figure.RECTANGLE, 5000)
# print(approx_list)
# for i, approx in enumerate(approx_list):
#     print(f'{i+1}번째 approx 개수 : {len(approx)}')
#
#
# # 사각형 감지 테스트
# img_rectangle = cv2.imread("../../tello/detection/images/red-rectangle.png")
# contour_info, object_type = figure_handler.find_color(img_rectangle, Color.RED, Figure.RECTANGLE, 100)
# x, y, w, h = contour_info
# print(x, y, w, h)
# cropped_img_rectangle = img_rectangle[y:y + h, x:x + w]
# cv2.imshow("cropped img rectangle", cropped_img_rectangle)
# approx_list_rectangle = figure_handler.find_color_with_all_contour(cropped_img_rectangle, Color.RED, Figure.RECTANGLE, 5000)
# print(approx_list_rectangle)
# for i, approx in enumerate(approx_list_rectangle):
#     print(f'{i+1}번째 approx 개수 : {len(approx)}')
#
# # 이미지 원본 contour 그리기 테스트
# figure_handler.find_color(img, Color.BLUE, Figure.RECTANGLE, 5000, draw_contour=True)
# figure_handler.find_color_with_all_contour(img, Color.GREEN, Figure.RECTANGLE, 5000, draw_contour=True)
#
# cv2.imshow("origin image", img)
#
# print(figure_handler.is_ring(Color.RED, Figure.RECTANGLE, cropped_img_rectangle))
#
# img2 = cv2.imread("images/img.png")
# figure_handler.find_color(img2, Color.GREEN, Figure.RECTANGLE, 100, draw_contour=True)
# figure_handler.find_color_with_all_contour(img2, Color.BLUE, Figure.RECTANGLE, 0, draw_contour=True)
#
#
# cv2.imshow("hello", img2)
#
# img3 = cv2.imread("images/img_1.png")
#
# # 잘린 사각형 링 이미지 감지 테스트
# contour_info, figure_type, = figure_handler.find_color(img3, Color.BLUE, Figure.ANY, 100, draw_contour=True)
# x, y, w, h = contour_info
# cv2.rectangle(img3, (x, y), (x+w, y+h), (0, 255, 255))
# is_blue_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, img3[y : y+h, x : x+w])
# print(f'파란색 링 여부 : {is_blue_ring}, 정답 : True')
#
# # 잘린 사각형 링 이미지 감지 테스트
# contour_info, figure_type, = figure_handler.find_color(img3, Color.GREEN, Figure.ANY, 100, draw_contour=True)
# x, y, w, h = contour_info
# is_blue_ring = figure_handler.is_ring(Color.GREEN, Figure.ANY, img3[y : y+h, x : x+w])
# print(f'초록색 링 여부 : {is_blue_ring}, 정답 : False')
#
#
# figure_handler.find_color_with_all_contour(img3, Color.GREEN, Figure.RECTANGLE, 0, draw_contour=True)
# cv2.imshow("hello2", img3)
#
# img4 = cv2.imread("images/img_2.png")
#
# # 잘린 사각형 링 이미지 감지 테스트
# contour_info, figure_type, = figure_handler.find_color_except_ring(img4, Color.BLUE, Figure.ANY, 100, draw_contour=True)
# x, y, w, h = contour_info
# is_blue_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, img4[y : y+h, x : x+w])
# print(f'파란색 링 여부 : {is_blue_ring}, 정답 : False')
#
#
#
# contour_info, figure_type, = figure_handler.find_color(img4, Color.RED, Figure.ANY, 100, draw_contour=True)
# cv2.imshow("hello3", img4)
#
# img5 = cv2.imread("./images/ring_rectangle.png")
# # 사각형, 링 구분 테스트
# contour_info, figure_type, = figure_handler.find_color_except_ring(img5, Color.RED, Figure.ANY, 100, draw_contour=True)
# x, y, w, h = contour_info
# cv2.rectangle(img5, (x, y), (x+w, y+h), (0, 255, 255))
#
# is_red_ring = figure_handler.is_ring(Color.RED, Figure.ANY, img5[y : y+h, x : x+w])
# print(contour_info, figure_type)
# cv2.imshow("hello4", img5)
#
#
#
# cv2.waitKey()

from main.module.handler.FigureHandler import FigureHandler
from main.module.handler.ImageHandler import ImageHandler
from main.module.enum.Color import Color
from main.module.enum.Figure import Figure
import cv2
figure_handler = FigureHandler()
image_handler = ImageHandler()
# 사각형 링 감지 테스트
img = cv2.imread("images/3_6_9.png")
contour_info ,object_type = figure_handler.find_color_with_ring(img, Color.GREEN, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness=2)
cv2.putText(img, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

#
contour_info ,object_type = figure_handler.find_color_with_ring(img, Color.BLUE, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness=2)
cv2.putText(img, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img, Color.RED_REC, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), thickness=2)
cv2.putText(img, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 1", img)

# 2번째
img2 = cv2.imread("images/img.png")
contour_info ,object_type = figure_handler.find_color_except_ring(img2, Color.GREEN, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_except_ring(img2, Color.BLUE, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_except_ring(img2, Color.RED, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img2, Color.RED, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img2, Color.BLUE, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 2", img2)

# 3번째
img3 = cv2.imread("images/img_1.png")
contour_info ,object_type = figure_handler.find_color_except_ring(img3, Color.GREEN, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img3[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.GREEN, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img3, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img3, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img3, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img3[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img3, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img3, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 3", img3)

# 4번째
img4 = cv2.imread("images/img_2.png")
contour_info ,object_type = figure_handler.find_color_except_ring(img4, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img4[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img4, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img4, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img4, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img4[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img4, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img4, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 4", img4)

# 5번째

img5 = cv2.imread("images/img_2.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img5, Color.RED_REC, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img5[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.ANY, cropped_img)
cv2.rectangle(img5, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img5, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img5, Color.RED_REC, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img5[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.ANY, cropped_img)
cv2.rectangle(img5, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img5, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 5", img5)

# 6번째

img6 = cv2.imread("images/ring_rectangle.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img6, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img6[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img6, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img6, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img6, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img6[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img6, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img6, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 6", img6)

# 7번째

img7 = cv2.imread("images/ring_rectangle.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img7, Color.RED_REC, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img7[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.ANY, cropped_img)
cv2.rectangle(img7, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img7, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img7, Color.RED_REC, Figure.ANY, 100)
x, y, w, h = contour_info
cropped_img = img7[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.ANY, cropped_img)
cv2.rectangle(img7, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img7, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

cv2.imshow("img 7", img7)

# 8번째

img8 = cv2.imread("images/09-15.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img8, Color.GREEN, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img8[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.GREEN, Figure.ANY, cropped_img)
cv2.rectangle(img8, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img8, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_except_ring(img8, Color.RED, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img8[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED, Figure.ANY, cropped_img)
cv2.rectangle(img8, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img8, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 8", img8)

# 9번째
# 가려진 링
img9 = cv2.imread("images/hidden_red_2.png")

contour_info ,object_type = figure_handler.find_color_with_ring(img9, Color.RED_REC, Figure.EVERY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img9[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.EVERY, cropped_img)
cv2.rectangle(img9, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img9, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 9", img9)

# 10번째
# 가려진 링 앞 플래그 감지
img10 = cv2.imread("images/hidden_red_2.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img10, Color.RED_REC, Figure.EVERY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img10[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.EVERY, cropped_img)
cv2.rectangle(img10, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img10, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 10", img10)

# 11번째
# 가려진 링
img11 = cv2.imread("images/hidden_blue_2.png")

contour_info ,object_type = figure_handler.find_color_with_ring(img11, Color.BLUE, Figure.EVERY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img11[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.EVERY, cropped_img)
cv2.rectangle(img11, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img11, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 11", img11)

# 12번째
# 가려진 링 앞 플래그 감지
img12 = cv2.imread("images/hidden_blue.png")

contour_info ,object_type = figure_handler.find_color_except_ring(img12, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img12[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img12, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img12, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 12", img12)



cv2.waitKey()