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
