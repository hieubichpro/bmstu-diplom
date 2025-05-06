import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from my_counter import MyObjectCounter  # ← đảm bảo bạn có class này sẵn

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Counter")
        self.fixed_width = 1280
        self.fixed_height = 720
        self.resize(self.fixed_width, self.fixed_height + 60)

        self.cap = None
        self.polygons = []
        self.current_points = []
        self.file_path = ""

        # QLabel hiển thị video
        self.video_label = QLabel()
        self.video_label.setFixedSize(self.fixed_width, self.fixed_height)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.mousePressEvent = self.get_point

        # Nút chọn video
        self.btn_select = QPushButton("Выбрать видео")
        self.btn_select.clicked.connect(self.open_file)

        # Nút bắt đầu đếm
        self.btn_start_counting = QPushButton("Подсчитать")
        self.btn_start_counting.clicked.connect(self.myfunc)
        self.btn_start_counting.setEnabled(False)

        # Nút xóa đa giác
        self.btn_remove_polygons = QPushButton("Удалить области")
        self.btn_remove_polygons.clicked.connect(self.remove_polygons)
        self.btn_remove_polygons.setEnabled(False)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_select)
        button_layout.addWidget(self.btn_start_counting)
        button_layout.addWidget(self.btn_remove_polygons)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Video Files (*.mp4 *.avi)")
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.polygons = []
            self.current_points = []
            self.timer.start(30)
            self.btn_start_counting.setEnabled(True)
            self.btn_remove_polygons.setEnabled(False)
            self.file_path = file_path

    def update_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            return

        # Resize frame về đúng 1280x720
        frame = cv2.resize(frame, (self.fixed_width, self.fixed_height))

        # Vẽ các đa giác đã hoàn tất
        for polygon in self.polygons:
            pts = [(p[0], p[1]) for p in polygon]
            cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Vẽ các điểm hiện tại
        for p in self.current_points:
            cv2.circle(frame, (p[0], p[1]), 4, (0, 0, 255), -1)

        # Hiển thị lên QLabel
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        qt_img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_img))

    def get_point(self, event):
        if len(self.polygons) >= 2:
            print("✅ Достаточно")
            return

        pos = event.pos()
        x, y = pos.x(), pos.y()
        self.current_points.append([x, y])
        print(f"➕ Выбранная точка: [{x}, {y}]")

        if len(self.current_points) == 4:
            self.polygons.append(self.current_points.copy())
            self.current_points.clear()
            print(f"✅ Выбранная область {len(self.polygons)}")
            self.btn_remove_polygons.setEnabled(True)

    def remove_polygons(self):
        self.polygons.clear()
        self.current_points.clear()
        self.btn_remove_polygons.setEnabled(False)
        print("🗑️ Все области удалены.")

    def myfunc(self):
        if len(self.polygons) < 2:
            print("❌ Выбрать 2 области.")
            return

        cap = cv2.VideoCapture(self.file_path)
        assert cap.isOpened()

        counter = MyObjectCounter(
            model_path="yolov8n.pt",
            polygon1=self.polygons[0],
            polygon2=self.polygons[1],
            show=True
        )

        print("▶️ Начинает обработки видео. Нажать ESC для закрытия")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (self.fixed_width, self.fixed_height))
            processed_frame = counter.process_frame(frame)

            if cv2.waitKey(1) == 27:  # ESC
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VideoWindow()
    win.show()
    sys.exit(app.exec_())
