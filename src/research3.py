import cv2
from my_counter import *
import time
import matplotlib.pyplot as plt

fixed_width = 1280
fixed_height = 720
kernel_sizes = [1, 3, 5, 7, 9, 11, 13, 15, 17]
times = []
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
#     start_time = time.time()  # Bắt đầu đo thời gian
#     actual = myfunc(path)
#     end_time = time.time()    # Kết thúc đo thời gian
#     elapsed_time = end_time - start_time  # Thời gian thực thi tính bằng giây

#     print(elapsed_time)
#     times.append(elapsed_time)
# print(times)

times = [63.76174211502075
,59.31864380836487
,56.752888441085815
,55.04888558387756
,55.51057839393616
,52.89027404785156
,50.443230628967285
,51.66649627685547
,50.59608311653137]

print(kernel_sizes)
print(times)
# Dữ liệu
x = kernel_sizes
y = times

# Vẽ đồ thị
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', linewidth=2)

# Gán nhãn
plt.title('Зависимость времени обработки видео от качества видео')
plt.xlabel('Размер ядра фильтра Гаусса')
plt.ylabel('Время (в секундах)')
plt.xticks(kernel_sizes)
# Hiển thị lưới
plt.grid(True)
plt.ylim(bottom=0, top=80)        # Bắt đầu trục Y từ 0

# Hiển thị đồ thị
plt.show()