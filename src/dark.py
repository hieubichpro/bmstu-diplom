import cv2

input_path = 'test/test3double.MOV'
brightness_factors = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
for i in range(len(brightness_factors)):
    cap = cv2.VideoCapture(input_path)

    # Thông tin về kích thước và fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # codec

    # Ghi video mới
    out = cv2.VideoWriter(f"dark/dark_{i}.MOV", fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Giảm độ sáng
        darker = cv2.convertScaleAbs(frame, alpha=brightness_factors[i], beta=0)

        out.write(darker)  # Ghi khung hình

    cap.release()
    out.release()
    print("Video đã được lưu")