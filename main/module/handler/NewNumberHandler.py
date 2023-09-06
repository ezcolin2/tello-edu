import cv2
import numpy as np
import torch.nn as nn
import torchvision.transforms as T
import torch
import os


def save(net, optimizer, root, fileName):
    torch.save({
        'model_state_dict': net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict()
    }, root + fileName + ".pth")


def load(root, fileName):
    state_dict = torch.load(os.path.join(root, fileName + '.pth'))
    model = state_dict['model_state_dict']
    optimizer = state_dict['optimizer_state_dict']

    return model, optimizer


class Classifier(nn.Module):
    def __init__(self) -> None:
        super(Classifier, self).__init__()
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(1 * 28 * 28, 100)
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return x


class BinaryClassifier(nn.Module):
    def __init__(self) -> None:
        super(BinaryClassifier, self).__init__()
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(3 * 28 * 28, 100)
        self.fc2 = nn.Linear(100, 2)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return x


class NumberDetector:
    def __init__(self, model=None, model2=None):
        self.model = model
        self.binary = model2
        if model == None:
            raise ValueError

        self.device = torch.device('cpu')
        self.i = 0

    def to(self, device):
        self.model = self.model.to(device)
        if self.binary != None:
            self.binary = self.binary.to(device)
        self.device = device
        return self

    def find_all_numbers(self, frame, min_area):
        maskGenerator = Mask(vmin=[0, 0, 35], vmax=[179, 40, 142])

        mask = maskGenerator(frame)
        img = frame.copy()
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        returns = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(cnt)

                maskPartition = mask[y: y + h + 1, x: x + w + 1]
                figPartition = img[y: y + h + 1, x: x + w + 1, :]
                if self.binary != None:
                    toDraw = self._determine2Draw(figPartition)
                    if toDraw == 0:
                        continue
                label = self._getLabel(maskPartition)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

                cv2.putText(frame,
                            str(label),
                            (x + (w // 2) - 10, y + (h // 2) - 10),
                            cv2.FONT_HERSHEY_COMPLEX,
                            1,
                            (255, 255, 0),
                            2
                            )
                # sort 함수 생략하기 위한 과정
                if len(returns) == 0:
                    returns.append(((x, y, w, h), label))
                else:
                    if returns[0][0][0] < x:
                        returns = returns + [((x, y, w, h), label)]
                    elif returns[0][0][0] > x:
                        returns = [((x, y, w, h), label)] + returns

        return frame, returns

    def resize(self, x, size):
        """
        이미지의 가로, 세로 길이 중 짧은 부분을 0으로 채워넣어 두 길이가 같게 한 뒤에 원하는 크기로 변환한다.
        Args:
            x (torch.Tensor): 가로, 세로의 길이가 각각 W, H이고 채널 수가 C일 때 크기가 CxHxW인 이미지 텐서
            size (tuple): 메서드 실행 후의 H, W가 될 값으로 이루어진 튜플
        Returns:
            torch.Tensor: 크기가 변환된 이미지
        """
        h, w = x.shape[1], x.shape[2]

        resize = T.Resize(size, antialias=True)
        if h > w:
            pad = T.Pad((h - w, 0))
        elif h < w:
            pad = T.Pad(((0, w - h)))
        else:
            pad = T.Pad((0, 0))
        x = resize(pad(x))

        return x

    def _determine2Draw(self, img):
        """
        숫자인지 아닌지 판단하는 함수.
        Args:
            img (numpy.ndarray): Binary mask를 이용해 이미지를 잘라서 얻은 이미지
        returns:
            int: 10을 얻으면 숫자가 아니고 아니며녀 숫자라고 판단한다.
        """
        self.binary.eval()
        with torch.no_grad():
            img = self._convert(img, keepdim=True)

            img = img.to(self.device)
            todo = self.binary(img).max(dim=1)[1].item()

        return todo

    def _getLabel(self, img):
        """
        숫자인지 아닌지 판단하는 함수.
        Args:
            img (numpy.ndarray): Binary mask를 이용해 binary mask를 잘라서 얻은 이미지
        returns:
            int: 해당 부분이 어떤 숫자인지 반환한다.
        """
        self.model.eval()
        with torch.no_grad():
            img = self._convert(img, keepdim=False)
            img = img.to(self.device)

            label = self.model(img).max(dim=1)[1].item()

        return label

    def _convert(self, img, keepdim=True):
        """
        이미지를 neural network 모델의 입력값의 형식으로 바꾼다.
        Args:
            img (numpy.ndarray): 원하는 이미지의 전체 혹은 부분
            keep
        """
        img = torch.from_numpy(img)
        if keepdim:
            img = img / 255
            img = img.permute(2, 0, 1)
            img = self.resize(img, (28, 28))

        else:
            img = img / 255
            img = img.unsqueeze(0)
            img = self.resize(img, (28, 28))
        img = img.unsqueeze(0)
        return img


class Mask:
    def __init__(self, vmin=None, vmax=None) -> None:
        """
        Args:
            vmin (list): Binary mask를 생성하기 위한 하계(lower bound). 이것을 찾기 위해 openWindow 메서드를 호출했을 때 이 값이 None이 아니면 하계의 default가 된다.
            vmax (list): Binary mask를 생성하기 위한 상계(upper bound). 이것을 찾기 위해 openWindow 메서드를 호출했을 때 이 값이 None이 아니면 상계의 default가 된다.
        """
        self.name = None
        self.isOpened = False
        if vmin != None:
            self.vmin = vmin
        else:
            self.vmin = [0, 0, 0]

        if vmax != None:
            self.vmax = vmax
        else:
            self.vmax = [179, 255, 255]

    def __call__(self, img):
        """
        HSV의 범위의 상계(upper bound)와 하계(lower bound)를 알아낸 결괏값 또는 추정값을 적용하여 binary mask를 생성한다.
        Args:
            img (numpy.ndarray): 드론의 카메라로 인식한 이미지
        Returns:
            mask (numpy.ndarray): HSV의 범위를 추정하여 얻은 결괏값으로 얻은 binary mask
        """
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        if self.isOpened:
            h_min = cv2.getTrackbarPos("Hue Min", self.name)
            h_max = cv2.getTrackbarPos("Hue Max", self.name)
            s_min = cv2.getTrackbarPos("Sat Min", self.name)
            s_max = cv2.getTrackbarPos("Sat Max", self.name)
            v_min = cv2.getTrackbarPos("Val Min", self.name)
            v_max = cv2.getTrackbarPos("Val Max", self.name)

            vmin = np.array([h_min, s_min, v_min])
            vmax = np.array([h_max, s_max, v_max])
        else:
            vmin = np.array(self.vmin)
            vmax = np.array(self.vmax)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            print(vmin, vmax)

        mask = cv2.inRange(img, vmin, vmax)

        return mask

    def openWindow(self, name):
        """
        HSV 범위의 하계(lower bound)와 상계(upper bound)를 찾기 위한 작업을 하기 위해 창을 띄워주는 함수.
        이 메서드가 실행이 되지 않으면 binary mask를 생성하기 위해 파라미터로 상계와 하계를 전달해주어야 한다.

        Args:
            name (str):  창의 이름
        Returns:
            None
        """
        self.name = name
        self.isOpened = True
        cv2.namedWindow(name)
        cv2.resizeWindow(name, 640, 240)

        def empty(a):
            pass

        h_min, s_min, v_min = self.vmin
        h_max, s_max, v_max = self.vmax

        cv2.createTrackbar("Hue Min", name, h_min, 179, empty)
        cv2.createTrackbar("Hue Max", name, h_max, 179, empty)
        cv2.createTrackbar("Sat Min", name, s_min, 255, empty)
        cv2.createTrackbar("Sat Max", name, s_max, 255, empty)
        cv2.createTrackbar("Val Min", name, v_min, 255, empty)
        cv2.createTrackbar("Val Max", name, v_max, 255, empty)