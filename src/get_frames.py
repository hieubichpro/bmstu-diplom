# import cv2
# import os

# video_path = './vid/vid.mp4'   # путь к твоему видео
# output_dir = 'frames'      # папка для сохранения

# os.makedirs(output_dir, exist_ok=True)

# cap = cv2.VideoCapture(video_path)
# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_interval = int(fps)  # 1 кадр в секунду

# frame_id = 0
# saved_id = 0

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     if frame_id % frame_interval == 0:
#         # показываем кадр
#         cv2.imshow('Frame', frame)
#         cv2.imwrite(f'{output_dir}/frame_{saved_id:01}.jpg', frame)
#         print(f'Сохраняю кадр {saved_id}')
#         saved_id += 1

#         key = cv2.waitKey(0)  # ждём нажатия клавиши
#         if key == 27:  # ESC — выход
#             break

#     frame_id += 1

# cap.release()
# cv2.destroyAllWindows()