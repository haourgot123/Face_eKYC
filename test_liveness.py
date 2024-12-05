import os
import cv2
import cvzone
import torch
import torch.nn.functional as F
from models.livenessnet import LivenessNet
from models.yolov8_face import YOLOv8_face


def test_liveness():
    net = LivenessNet(width=32, height=32, depth=3, classes=2)
    net.load_state_dict(torch.load('weights/liveness.pth'))
    net.eval()

    yolo_net = YOLOv8_face(path = 'weights/yolov8n-face.onnx', conf_thres=0.4, iou_thres = 0.6)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Không thể mỏ Webcam !')
        return

    while True:

        sucess, frame = cap.read()
        bboxes, conf, _, landmark  =  yolo_net.detect(frame)

        x, y, w, h = bboxes[0].astype(int)

        frame = cvzone.cornerRect(
            frame,  # The image to draw on
            (x, y, w, h),  # The position and dimensions of the rectangle (x, y, width, height)
            l=30,  # Length of the corner edges
            t=5,  # Thickness of the corner edges
            rt=1,  # Thickness of the rectangle
            colorR=(255, 0, 255),  # Color of the rectangle
            colorC=(0, 255, 0)  # Color of the corner edges
        )
        img = frame[y : y + h, x : x + w]
        img = cv2.resize(img, (32, 32))
        img = img / 255.0
        img = torch.tensor(img, dtype = torch.float32).unsqueeze(0)
        img = img.permute(0, 3, 1, 2)
        output = net(img)
        output = F.softmax(output)
        _, predicted = output.max(1)
        print(output)
        conf = output[0][torch.argmax(output, dim = -1)]
        text = 'real' if predicted == 1 else 'fake' + f'{conf}'
                
        frame, bbox = cvzone.putTextRect(
            frame, text, (x + 10, y - 10),  # Image and starting position of the rectangle
            scale=3, thickness=3,  # Font scale and thickness
            colorT=(255, 255, 255), colorR=(0, 255, 0),  # Text color and Rectangle color
            font=cv2.FONT_HERSHEY_PLAIN,  # Font type
            offset=10,  # Offset of text inside the rectangle
            border=2 # Border thickness and color
        )

        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
if __name__ == "__main__":
    # net = LivenessNet(width=32, height=32, depth=3, classes=2)
    # net.load_state_dict(torch.load('weights/liveness.pth'))
    # net.eval()
    # img = cv2.imread('dataset/real-face/hao_1.jpg')
    # img = cv2.resize(img, (32, 32))
    # img = img / 255.0
    # img = torch.tensor(img, dtype = torch.float32).unsqueeze(0)
    # img = img.permute(0, 3, 1, 2)
    # output = net(img)
    # output = F.softmax(output)
    # _, predicted = output.max(1)
    # conf = output[0][torch.argmax(output, dim = -1)]
    # text = 'real' if predicted == 1 else 'fake' + f'{conf}'
    # print(output)
    # print(text)
    test_liveness()


    