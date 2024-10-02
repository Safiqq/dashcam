import cv2
import mediapipe as mp
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QImage, QPixmap

class EyeTrackingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initializeMediaPipe()
        self.initializeVariables()

    def setupUi(self):
        self.setWindowTitle("Eye and Iris Tracking")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        self.video_label = QtWidgets.QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        self.btn_start = QtWidgets.QPushButton("Start")
        self.btn_start.clicked.connect(self.toggleVideo)
        layout.addWidget(self.btn_start)

    def initializeMediaPipe(self):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def initializeVariables(self):
        self.video_capture = None
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_frame)
        self.is_running = False
        
        # Define eye landmarks
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

    def toggleVideo(self):
        if not self.is_running:
            self.startVideo()
        else:
            self.stopVideo()

    def startVideo(self):
        if self.video_capture is None:
            self.video_capture = cv2.VideoCapture(0)  # Use default camera
        
        if not self.video_capture.isOpened():
            QtWidgets.QMessageBox.critical(self, "Error", "Could not open camera.")
            return

        self.video_timer.start(33)  # ~30 fps
        self.is_running = True
        self.btn_start.setText("Stop")

    def stopVideo(self):
        self.video_timer.stop()
        if self.video_capture:
            self.video_capture.release()
        self.video_capture = None
        self.is_running = False
        self.btn_start.setText("Start")
        self.video_label.clear()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(frame_rgb)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.draw_eye_and_iris(frame_rgb, face_landmarks)

            self.display_frame(frame_rgb)

    def draw_eye_and_iris(self, image, face_landmarks):
        img_h, img_w = image.shape[:2]
        mesh_points = np.array([
            np.multiply([p.x, p.y], [img_w, img_h]).astype(int)
            for p in face_landmarks.landmark
        ])

        # Draw eyes
        cv2.polylines(image, [mesh_points[self.LEFT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.polylines(image, [mesh_points[self.RIGHT_EYE]], True, (0, 255, 0), 1, cv2.LINE_AA)

        # Draw irises
        (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[self.LEFT_IRIS])
        (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[self.RIGHT_IRIS])
        center_left = np.array([l_cx, l_cy], dtype=np.int32)
        center_right = np.array([r_cx, r_cy], dtype=np.int32)
        cv2.circle(image, center_left, int(l_radius), (255, 0, 255), 1, cv2.LINE_AA)
        cv2.circle(image, center_right, int(r_radius), (255, 0, 255), 1, cv2.LINE_AA)

    def display_frame(self, frame):
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)

    def closeEvent(self, event):
        self.stopVideo()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = EyeTrackingWindow()
    window.show()
    sys.exit(app.exec_())