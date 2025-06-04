import cv2

input_path = 'test/test3.MOV'
output_path = 'test3double.MOV'

# Mở video gốc
cap = cv2.VideoCapture(input_path)

# Lấy thông tin video gốc
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec

# Tạo đối tượng ghi video mới
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Đọc toàn bộ khung hình gốc và lưu vào danh sách
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

# Ghi toàn bộ khung hình 2 lần để tăng gấp đôi thời lượng
for _ in range(3):
    for frame in frames:
        out.write(frame)

out.release()
print("Video đã được lưu:", output_path)
