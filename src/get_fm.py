import cv2
def extract_frames(video_path, fps_step=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * fps_step)
    
    frames = []
    count = 0
    frame_id = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append((frame_id, frame))
            frame_id += 1
        count += 1
    cap.release()
    return frames