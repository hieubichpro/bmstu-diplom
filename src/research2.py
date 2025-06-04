import cv2
from my_counter import *
fixed_width = 1280
fixed_height = 720
kernel_sizes = [1, 3, 5, 7, 9, 11, 13, 15, 17]
accuracy = []
def myfunc(path):
    cap = cv2.VideoCapture(path)

    counter = MyObjectCounter(
        model_path="yolov8n.pt",
        polygon1=[[544, 229], [550, 565], [677, 567], [660, 222]],
        polygon2=[[395, 229], [530, 229], [537, 563], [384, 568]],
        show=True
    )

    frame_count = 0
    skip_rate = 3

    count_so_far = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % skip_rate != 0:
            continue 

        frame = cv2.resize(frame, (fixed_width, fixed_height))
        count_so_far = counter.process_frame(frame, True)

        if cv2.waitKey(1) == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()
    return count_so_far
# for i in range(len(kernel_sizes)):
#     path = f"blur/blur_k{2*i+1}.MOV"
#     actual = myfunc(path)
#     print(actual)
#     accuracy.append(100 - abs(44 - actual)/44 * 100)
# print(accuracy)

import matplotlib.pyplot as plt
zs = [42
,41
,42
,42
,41
,40
,38
,32
,23]
accuracy = [100 - abs(44 - z)/44 * 100 for z in zs]
print(kernel_sizes)
print(accuracy)
# Dữ liệu
x = kernel_sizes
y = accuracy

# Vẽ đồ thị
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', linewidth=2)

# Gán nhãn
plt.title('Зависимость точность от качества видео')
plt.xlabel('Размер ядра фильтра Гаусса')
plt.ylabel('Точность (%)')

# Hiển thị lưới
plt.grid(True)

# Giới hạn trục tung từ 0 đến 100 để dễ đọc
plt.ylim(0, 100)

# Hiển thị đồ thị
plt.show()