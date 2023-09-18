from enum import Enum
class Figure(Enum):
    TRI = 0
    CIRCLE = 1
    RECTANGLE = 2
    NUMBER = 3
    ANY = 4
# 도형 점의 개수
count = [
    [3, 4], # 삼각형
    [7, 9], # 원
    [3, 5],  # 사각형
    [1, 255], # 숫자
    [3, 9] # 아무거나
]

