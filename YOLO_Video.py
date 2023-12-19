import torch
import cv2
import os

video_capture = None
model = None

def video_detection(path_x):
    global video_capture, model

    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    lebar_frame = int(cap.get(3))
    tinggi_frame = int(cap.get(4))

    # Memuat model YOLOv5
    absolute_path = os.path.abspath('YOLO-Weights/terabik150.pt')

    # Memuat model YOLOv5
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=absolute_path, force_reload=True)

    classNames = ['kosong', 'terisi']

    while True:
        berhasil, img = cap.read()
        if not berhasil:
            break

        # Mengatur ulang hitungan untuk setiap frame
        terisi_count = 0
        kosong_count = 0

        results = model(img)

        for _, det in enumerate(results.pred[0]):
            x1, y1, x2, y2, conf, cls = det.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            class_name = classNames[int(cls)]
            label = f'{class_name}{conf:.2f}'

            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3

            if class_name == 'kosong':
                warna = (0, 204, 255)
                kosong_count += 1
            elif class_name == "terisi":
                warna = (222, 82, 175)
                if conf > 0.5:
                    terisi_count += 1
            else:
                warna = (85, 45, 255)

            if conf > 0.5:
                cv2.rectangle(img, (x1, y1), (x2, y2), warna, 3)
                cv2.rectangle(img, (x1, y1), c2, warna, -1, cv2.LINE_AA)
                cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        cv2.putText(img, f'Terisi: {terisi_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, f'Kosong: {kosong_count}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        yield img

cv2.destroyAllWindows()
