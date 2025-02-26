from datetime import datetime
import cv2
import numpy as np
import pandas as pd
import pytesseract
from ultralytics import YOLO

# Đường dẫn tới tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load model YOLO
model = YOLO('best.pt')


# Hàm lấy tọa độ con trỏ chuột
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)


# Đặt callback để lấy tọa độ chuột
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# Mở video
cap = cv2.VideoCapture('mycarplate.mp4')

# Đọc danh sách class từ file coco1.txt
with open("coco1.txt", "r") as my_file:
    data = my_file.read()
class_list = data.split("\n")

# Định nghĩa vùng quan tâm
area = [(27, 417), (16, 456), (1015, 451), (992, 417)]

count = 0
list1 = []
processed_numbers = set()

# Mở file để ghi dữ liệu biển số xe
with open("car_plate_data.txt", "a") as file:
    file.write("NumberPlate\tDate\tTime\n")  # Viết tiêu đề cột

while True:
    ret, frame = cap.read()
    count += 1
    if count % 3 != 0:  # Để giảm tốc độ xử lý các khung hình
        continue
    if not ret:
        break

    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])

        d = int(row[5])  # Lấy class ID
        c = class_list[d]  # Lấy tên class dựa vào ID
        cx = (x1 + x2) // 2  # Tọa độ trung tâm vùng phát hiện
        cy = (y1 + y2) // 2

        # Kiểm tra xem điểm trung tâm có nằm trong vùng quan tâm không
        result = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
        if result >= 0:
            # Crop vùng chứa biển số
            crop = frame[y1:y2, x1:x2]
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 10, 20, 20)

            # Nhận diện biển số
            text = pytesseract.image_to_string(gray).strip()
            text = text.replace('(', '').replace(')', '').replace(',', '').replace(']', '')
            if text not in processed_numbers:
                processed_numbers.add(text)
                list1.append(text)

                # Lấy thời gian hiện tại
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Ghi biển số và thời gian vào file
                with open("car_plate_data.txt", "a") as file:
                    file.write(f"{text}\t{current_datetime}\n")

                # Vẽ hình chữ nhật quanh biển số
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                cv2.imshow('crop', crop)

    # Vẽ vùng quan tâm lên khung hình
    cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 0), 2)
    cv2.imshow("RGB", frame)

    # Nhấn phím ESC để thoát
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
