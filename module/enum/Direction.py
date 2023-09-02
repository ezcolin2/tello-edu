from enum import Enum


class Direction(Enum):
    """
    Tello 객체의 send_rc_control 메소드의 인자로 들어갈 값.
    홀수라면 음수이고 짝수라면 양수임.
    """
    RIGHT = 0
    LEFT = 1
    FORWARD = 2
    BACKWARD = 3
    UP = 4
    DOWN = 5
    CLOCKWISE = 6
    COUNTERCLOCKWISE = 7