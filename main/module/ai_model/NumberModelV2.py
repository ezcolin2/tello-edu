import torch
import cv2
import torch.nn as nn

class NumberModelV2(nn.Module):
    def __init__(self) -> None:
        super(NumberModelV2, self).__init__()
        self.relu = nn.ReLU()

        self.fc1 = nn.Linear(1 * 28 * 28, 100)
        self.fc2 = nn.Linear(100, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)

        return x