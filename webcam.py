import os
import cv2
import argparse
import config
import config.config
from models.yolov8_face import YOLOv8_face

CONFIG_APP = config.config.load_config()
YOLO_CONFIG = CONFIG_APP['yolo_face']


detection_model = YOLOv8_face(path = YOLO_CONFIG['weight_path'], conf_thres = YOLO_CONFIG['conf_thres'], iou_thres = YOLO_CONFIG['iou_thres'])


def webcam(interval = 3, person_name = '', saved_file = 'dataset/real-face'):
    '''
    Chụp ảnh từ webcam và lưu vào thư mục ảnh để tạo dataset
    '''
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print('Không thể mở webcam !')
        return 
    try:
        while True:
            for countdown in range(interval, 0, -1):
                ret, frame = cap.read()
                if not ret:
                    print('Không thể đọc khung hình từ webcam !')
                    break
                
                # Hiển thị thời gian lên màn hình
                text = f'Chup sau: {countdown}'
                cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 255), 2,  cv2.LINE_AA)
                
                # Hiển thị webcam
                cv2.imshow('Webcam', frame)

                # Đợi 1s
                if cv2.waitKey(1000) & 0xFF == ord('q'):
                    return
            
            # Chụp ảnh
            idx = len(os.listdir(saved_file))
            ret, image = cap.read()
            bboxes, conf, _, _ = detection_model.detect(image)
            x, y, w, h = bboxes[0].astype(int)
            image = image[y : y + h, x : x + w]
            file_name = os.path.join(saved_file, f'{person_name}_{idx}.jpg')
            cv2.imwrite(file_name, image)
            print(f'Lưu thành công file: {file_name}')            
            if cv2.waitKey(500) & 0xFF == ord('q'):
                break
    finally:
        # Giải phóng tài nguyên
        cap.release()
        cv2.destroyAllWindows()


def run():
    parser = argparse.ArgumentParser(description="Chụp ảnh từ Webcam !")
    parser.add_argument('--saved_path', '-p', type = str, required=True, help= 'Đường dẫn lưu ảnh')
    parser.add_argument('--interval', '-i', type = int, required = True, help = 'Thời gian đếm ngược')
    parser.add_argument('--person_name', '-n', type = str, required=True, help='Tên người chụp ảnh')   

    args = parser.parse_args()
    webcam(args.interval, args.person_name, args.saved_path)


if __name__  == '__main__':
    run()
