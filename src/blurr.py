import cv2
import matplotlib.pyplot as plt

input_path = 'test/test3double.MOV'
kernel_sizes = [1, 3, 5, 7, 9, 11, 13, 15, 17]


for k in kernel_sizes:
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out_path = f'blur/blur_k{k}.MOV'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Làm mờ nếu kernel size lẻ (yêu cầu của GaussianBlur)
        if k % 2 == 1:
            blurred = cv2.GaussianBlur(frame, (k, k), 0)
        else:
            blurred = frame
        out.write(blurred)

    cap.release()
    out.release()