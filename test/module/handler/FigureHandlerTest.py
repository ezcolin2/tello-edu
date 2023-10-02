

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



contour_info ,object_type = figure_handler.find_color_with_ring(img2, Color.BLUE, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.RECTANGLE, cropped_img)
cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img2, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)

contour_info ,object_type = figure_handler.find_color_with_ring(img2, Color.RED_REC, Figure.RECTANGLE, 100)
x, y, w, h = contour_info
cropped_img = img2[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.RED_REC, Figure.RECTANGLE, cropped_img)
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
#
# img8 = cv2.imread("images/09-15.png")
#
# contour_info ,object_type = figure_handler.find_color_except_ring(img8, Color.GREEN, Figure.ANY, 100)
# x, y, w, h = contour_info
# print(contour_info)
# cropped_img = img8[y:y+h,x:x+w]
# is_ring = figure_handler.is_ring(Color.GREEN, Figure.ANY, cropped_img)
# cv2.rectangle(img8, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
# cv2.putText(img8, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
#
# contour_info ,object_type = figure_handler.find_color_except_ring(img8, Color.RED, Figure.ANY, 100)
# x, y, w, h = contour_info
# print(contour_info)
# cropped_img = img8[y:y+h,x:x+w]
# is_ring = figure_handler.is_ring(Color.RED, Figure.ANY, cropped_img)
# cv2.rectangle(img8, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
# cv2.putText(img8, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
# cv2.imshow("img 8", img8)
#
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


img13 = cv2.imread("images/home-blue.png")

contour_info ,object_type = figure_handler.find_color_with_ring(img13, Color.BLUE, Figure.ANY, 100)
x, y, w, h = contour_info
print(contour_info)
cropped_img = img13[y:y+h,x:x+w]
is_ring = figure_handler.is_ring(Color.BLUE, Figure.ANY, cropped_img)
cv2.rectangle(img13, (x, y), (x+w, y+h), (0, 255, 255), thickness=2)
cv2.putText(img13, str(is_ring), (x, y+20), cv2.FONT_ITALIC, 0.6, (0, 255, 255), 2)
cv2.imshow("img 13", img13)


cv2.waitKey()