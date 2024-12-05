import os
import argparse
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, Dataset
from models.livenessnet import LivenessNet


class MyDataset(Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        return self.data[idx], self.label[idx]


def create_dataloader(dataset_path = './dataset', batch_size = 32):
    real_path = os.path.join(dataset_path, 'real-face')
    fake_path = os.path.join(dataset_path, 'fake-face')
    datas, labels = [], []
    for filename in os.listdir(real_path):
        img = cv2.imread(os.path.join(real_path, filename))
        img = cv2.resize(img, (32, 32))
        datas.append(img)
        labels.append(1)
    for filename in os.listdir(fake_path):
        img = cv2.imread(os.path.join(fake_path, filename))
        img = cv2.resize(img, (32, 32))
        datas.append(img)
        labels.append(0)
    
    
    datas = np.array(datas, dtype = 'float32') / 255.0

    X_train, X_test, Y_train, Y_test = train_test_split(datas, labels, test_size = 0.2, random_state = 42)
    X_val, X_test, Y_val, Y_test = train_test_split(X_test, Y_test, test_size = 0.5, random_state = 42)

    train_dataset = MyDataset(X_train, Y_train)
    val_dataset = MyDataset(X_val, Y_val)
    test_dataset = MyDataset(X_test, Y_test)

    train_loader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True)
    val_loader = DataLoader(val_dataset, batch_size = batch_size, shuffle = True)
    test_loader = DataLoader(test_dataset, batch_size = batch_size, shuffle = True)

    return train_loader, val_loader, test_loader



    



def train(model, dataset_path = './dataset', lr = 0.001, epochs = 50, num_classes = 2, batch_size = 32,  device = 'cpu'):
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []

    train_loader, val_loader, test_loader = create_dataloader(dataset_path, batch_size)

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr = lr)

    best_val_loss = float('inf')  # Giá trị loss tốt nhất ban đầu (vô cực)
    save_path = "weights/liveness.pth"  # Đường dẫn lưu mô hình

    for epoch in range(epochs):
        
        model.train()
        train_loss = 0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.float().to(device), labels.long().to(device)
            inputs = inputs.permute(0, 3, 1, 2) 
            optimizer.zero_grad()

            # Foward
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            # Caculate metrics
            train_loss += loss.item()
            total += labels.size(0)
            _, predicted = outputs.max(1)
            correct += (predicted == labels).sum().item()
        train_loss /= total
        train_accuracy = 100 * correct / total
        train_losses.append(train_loss)
        train_accuracies.append(train_accuracy)

        # Validation
        model.eval()
        val_loss = 0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.float().to(device), labels.long().to(device)
                inputs = inputs.permute(0, 3, 1, 2)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                val_loss += loss.item()
                total += labels.size(0)
                _, predicted = outputs.max(1)
                correct += (predicted == labels).sum().item()
        
        val_loss /= total
        val_accuracy = 100 * correct / total
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        
        print(f"Epoch {epoch+1}/{epochs}, "
          f"Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.2f}%, "
          f"Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.2f}%")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved at epoch {epoch+1} with Validation Loss: {val_loss:.4f}") 

    history_train = {
        'epochs': epochs,
        'train_losses': train_losses,
        'val_losses': val_losses,
        'train_accuracy': train_accuracies,
        'val_accuracy': val_accuracies
    }          

    return history_train

def plot_history(history):
    train_losses = history['train_losses']
    val_losses = history['val_losses']
    train_accuracies = history['train_accuracy']
    val_accuracies = history['val_accuracy']

    # Giả sử đã lưu các giá trị loss và accuracy trong các danh sách
    plt.figure(figsize=(12, 6))

    # Vẽ Loss
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss')
    plt.legend()
    plt.grid()

    # Vẽ Accuracy
    plt.subplot(1, 2, 2)
    plt.plot(train_accuracies, label='Train Accuracy')
    plt.plot(val_accuracies, label='Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy')
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig("history.png", dpi=300, bbox_inches='tight')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Training LivenessNet')
    parser.add_argument('--dataset', '-d', type = str, required= True, help = 'Đường dẫn đến file dataset')
    parser.add_argument('--learning_rate', '-lr', type = float, default = 0.001, help = 'Tốc độ học')
    parser.add_argument('--epochs', '-ep', type = int, required = True, help = 'Số lượng epochs')
    parser.add_argument('--batch_size', '-bz', type = int, required = True, help = 'Batch size')
    parser.add_argument('--device', '-dv', type = str, default = 'cpu', help = 'Device')

    args = parser.parse_args()

    model = LivenessNet(width =32, height = 32, depth = 3, classes = 2)
    history_train = train(model, args.dataset, args.learning_rate, args.epochs, 2, args.batch_size, args.device)
    plot_history(history_train)