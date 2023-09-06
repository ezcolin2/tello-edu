import torch
import cv2
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
class NumberModel(nn.Module):
    def __init__(self):
        super(NumberModel, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x

    def get_number_with_model(self, image):
        """
        이진화 처리 된 이미지를 받아서 해당 숫자 판단
        :param image: 이진화 된 이미지
        :return: 감지한 숫자
        """

        global model
        device = torch.device('cpu')
        image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_CONSTANT, value=0)

        image = cv2.resize(image, (28, 28))

        # 이미지를 [0, 1] 범위로 스케일링
        image = image.astype('float32') / 255.0

        # 이미지를 PyTorch 모델에 입력 가능한 형태로 변환
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])
        image = transform(image).unsqueeze(0)  # 배치 차원 추가
        with torch.no_grad():
            image = image.to(device)
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
        return predicted.item()
    # def __init__(self) -> None:
    #     super(NumberModel, self).__init__()
    #     self.relu = nn.ReLU()
    #
    #     self.fc1 = nn.Linear(1 * 28 * 28, 100)
    #     self.fc2 = nn.Linear(100, 10)
    #
    # def forward(self, x):
    #     x = x.view(x.size(0), -1)
    #     x = self.relu(self.fc1(x))
    #     x = self.fc2(x)
    #
    #     return x
    # def get_number_with_model(self, image):
    #     """
    #     이진화 처리 된 이미지를 받아서 해당 숫자 판단
    #     :param image: 이진화 된 이미지
    #     :return: 감지한 숫자
    #     """
    #
    #     """
    #     숫자인지 아닌지 판단하는 함수.
    #     Args:
    #         img (numpy.ndarray): Binary mask를 이용해 binary mask를 잘라서 얻은 이미지
    #     returns:
    #         int: 해당 부분이 어떤 숫자인지 반환한다.
    #     """
    #     global model
    #     with torch.no_grad():
    #         img = self._convert(image, keepdim=False)
    #         img = img.to(self.device)
    #
    #         label = self.model(img).max(dim=1)[1].item()
    #
    #     return label
    # def _convert(self, img, keepdim = True):
    #     """
    #     이미지를 neural network 모델의 입력값의 형식으로 바꾼다.
    #     Args:
    #         img (numpy.ndarray): 원하는 이미지의 전체 혹은 부분
    #         keep
    #     """
    #     img = torch.from_numpy(img)
    #     if keepdim:
    #         img = img / 255
    #         img = img.permute(2, 0, 1)
    #         img = self.resize(img, (28, 28))
    #
    #     else:
    #         img = img / 255
    #         img = img.unsqueeze(0)
    #         img = self.resize(img, (28, 28))
    #     img = img.unsqueeze(0)
    #     return img