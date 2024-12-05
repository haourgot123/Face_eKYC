import torch
import torch.nn as nn
import torch.nn.functional as F

class LivenessNet(nn.Module):
    def __init__(self, width, height, depth, classes):
        super(LivenessNet, self).__init__()

        # Initialize the model layers
        self.conv1 = nn.Conv2d(in_channels=depth, out_channels=16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1)

        self.fc1 = nn.Linear(32 * (height // 4) * (width // 4), 64)  # Assuming the input is reduced by two pool layers
        self.fc2 = nn.Linear(64, classes)

        self.batch_norm1 = nn.BatchNorm2d(16)
        self.batch_norm2 = nn.BatchNorm2d(32)
        self.batch_norm3 = nn.BatchNorm1d(64)

        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.25)
        self.dropout3 = nn.Dropout(0.5)

    def forward(self, x):
        # First Conv -> ReLU -> Conv -> ReLU -> Pooling
        x = self.conv1(x)
        x = F.relu(x)
        x = self.batch_norm1(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = self.batch_norm1(x)
        x = self.pool(x)
        x = self.dropout1(x)

        # Second Conv -> ReLU -> Conv -> ReLU -> Pooling
        x = self.conv3(x)
        x = F.relu(x)
        x = self.batch_norm2(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = self.batch_norm2(x)
        x = self.pool(x)
        x = self.dropout2(x)

        # Flatten, Fully Connected, ReLU
        x = x = x.reshape(x.size(0), -1)  # Flatten
        x = self.fc1(x)
        x = F.relu(x)
        x = self.batch_norm3(x)
        x = self.dropout3(x)

        # Output layer (softmax is applied during loss calculation)
        x = self.fc2(x)

        return F.softmax(x, dim  = 1)
