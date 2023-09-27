import cv2
class YoloHandler:
    def __init__(self, model):
        self.model = model

    def get_object_xyxy(self, img, draw_rectangle=False):
        results = self.model(img)
        res = results[0].boxes.xyxy.tolist()
        print(res)

        # 감지를 못했다면 0, 0, 0, 0 반환
        if not res:
            return [0, 0, 0, 0]
        res = list(map(int, res[0]))
        x1, y1, x2, y2 = res
        if draw_rectangle:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return res