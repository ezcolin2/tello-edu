import cv2
import pyzbar.pyzbar as pyzbar

class QRHandler:
    def read_img(self, img):
        """
        이미지를 받아서 qr이 있다면 contour를 그리고 그 내용을 contour 위에 출력
        코드 참조 : https://github.com/hyunseokjoo/detecting_BarAndQR
        :param img : 이미지
        :return : (x, y, w, h, barcode), img
        """
        # 바코드 정보 decoding
        barcodes = pyzbar.decode(img)
        # 바코드 정보가 여러개 이기 때문에 하나씩 해석
        arr = []  # 바코드 좌표 정보
        for barcode in barcodes:
            # 바코드 rect정보
            x, y, w, h = barcode.rect
            arr.append((x, y, w, h, barcode))
            # 바코드 데이터 디코딩
            barcode_info = barcode.data.decode('utf-8')
            # 인식한 바코드 사각형 표시
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # 인식한 바코드 사각형 위에 글자 삽입
            cv2.putText(img, barcode_info, (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
        arr.sort(key=lambda x: x[2] * x[3])
        if len(arr) == 0:  # 비어있다면
            arr.append((-1, -1, -1, -1, None))
        return arr[0], img