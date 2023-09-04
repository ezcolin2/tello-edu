from typing import List
class RangeParams():
    def __init__(
            self,
            fb_range: List[int],
            ud_range: List[int],
            min_area: int,
            center_range_percentage: float,
            aspect_ratio_percentage: float,
            find_range_percentage: float
    ):
        """
        드론 움직임 관련 범위
        만약 center_range_percentage가 0.2라면 가로 세로 기준으로 0.3 ~ 0.7 안에 있다면 가운데로 판단
        :param fb_range:[최소 넓이, 최대 넓이] 최소 넓이 보다 작다면 앞으로, 크다면 뒤로
        :param ud_range:[최소 높이, 최대 높이] 최소 높이 보다 작다면 위로, 크다면 아래로
        :param min_area:객체를 탐지 할 가장 작은 넓이
        :param center_range_percentage:[최소 퍼센테이지, 최대 퍼센테이지] 가운데 있다고 판단할 범위
        """
        self.fb_range = fb_range #
        self.ud_range = ud_range #
        self.min_area = min_area #
        self.center_range_percentage = center_range_percentage #
        self.aspect_ratio_percentage = aspect_ratio_percentage  # 정면에 있다고 판단할 가로세로 비율
        self.find_range_percentage = find_range_percentage # 객체를 찾았다고 판단할 가로세로 비율
