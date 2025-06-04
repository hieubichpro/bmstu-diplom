import cv2

# input_path = 'test2.mp4'
# output_path = 'darker_video.mp4'
# brightness_factor = 0.5  # hệ số < 1 để giảm sáng

# # Mở video
# cap = cv2.VideoCapture(input_path)

# # Thông tin về kích thước và fps
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = cap.get(cv2.CAP_PROP_FPS)
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec

# # Ghi video mới
# out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Giảm độ sáng
#     darker = cv2.convertScaleAbs(frame, alpha=brightness_factor, beta=0)

#     out.write(darker)  # Ghi khung hình

# cap.release()
# out.release()
# print("Video đã được lưu:", output_path)
# from my_counter import *
# import cv2

# fixed_width = 1280
# fixed_height = 720
brightness_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
# accuracy = []
# def myfunc(path):
#     cap = cv2.VideoCapture(path)

#     counter = MyObjectCounter(
#         model_path="yolov8n.pt",
#         polygon1=[[544, 229], [550, 565], [677, 567], [660, 222]],
#         polygon2=[[395, 229], [530, 229], [537, 563], [384, 568]],
#         show=True
#     )

#     frame_count = 0
#     skip_rate = 3

#     count_so_far = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame_count += 1
#         if frame_count % skip_rate != 0:
#             continue 

#         frame = cv2.resize(frame, (fixed_width, fixed_height))
#         count_so_far = counter.process_frame(frame, True)

#         if cv2.waitKey(1) == 27: 
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return count_so_far
# for i in range(len(brightness_factors)):
#     path = f"dark/dark_{i}.MOV"
#     actual = myfunc(path)
#     print(actual)
#     accuracy.append(100 - abs(44 - actual)/44 * 100)
# print(accuracy)

import matplotlib.pyplot as plt


zs = [33, 36,40,41,41,42,41,42,41,42]
accuracy = [100 - abs(44 - z)/44 * 100 for z in zs]
print(brightness_factors)
print(accuracy)
# Dữ liệu
x = brightness_factors
y = accuracy

# Vẽ đồ thị
plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', linewidth=2)

# Gán nhãn
plt.title('Зависимость точность от освещенности')
plt.xlabel('Значение параметра α')
plt.ylabel('Точность (%)')

# Hiển thị lưới
plt.grid(True)

# Giới hạn trục tung từ 0 đến 100 để dễ đọc
plt.ylim(0, 100)

# Hiển thị đồ thị
plt.show()