import os
import sys
import cv2
import locale
import json
import io
import time
import numpy as np
import mediapipe as mp
from math import ceil
from datetime import datetime, timedelta
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QSize, QTimer, pyqtSlot, QThread
from PyQt5.QtGui import QIcon, QImage, QPixmap
from EyeTrackingMetrics import EyeTrackingMetrics
from PreprocessingWorker import PreprocessingWorker
from CSVWriter import CSVWriter

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setup_ui()
        self.initialize_media_player()
        self.initialize_variables()
        self.initialize_mediapipe()

    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("Eye Tracking Apps")
        self.resize(1920, 1080)
        self.setStyleSheet("* { font-size: 18px; }")
        
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.central_widget.setStyleSheet("#central_widget { background-color: #BDBBBE; }")
        
        self.main_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.setup_left_frame()
        self.setup_middle_frame()
        self.setup_right_frame()
        
        self.setCentralWidget(self.central_widget)

    def setup_left_frame(self):
        """Set up the left frame of the UI."""
        self.frame_left = QtWidgets.QFrame(self.central_widget)
        self.frame_left.setMaximumSize(QSize(360, 16777215))
        self.frame_left.setStyleSheet("#frame_left { background-color: #f9f9f9; border-radius: 4px; }")
        self.frame_left.setObjectName("frame_left")
        
        left_layout = QtWidgets.QVBoxLayout(self.frame_left)
        
        # Add data input fields
        self.textbox_vid = self.add_data_input_field(left_layout, "vid", "Choose Video")
        
        if self.username == 'admin':
            # Add submit button
            self.btn_submit = QtWidgets.QPushButton("Convert to CSV", self.frame_left)
            self.btn_submit.setObjectName("btn_submit")
            self.btn_submit.setStyleSheet("""
                #btn_submit {
                    padding: 12px 0px;
                    border-radius: 6px;
                    background-color: #6A676E;
                    color: #f9f9f9;
                    font-weight: 600;
                }
                #btn_submit:hover { background-color: #514E55; }
            """)
            self.btn_submit.clicked.connect(self.submit)
            left_layout.addWidget(self.btn_submit)
        
        # Add scrollable area for data display
        self.setup_scroll_area(left_layout)
        
        self.main_layout.addWidget(self.frame_left)
    
    def submit(self):
        if self.textbox_vid.toPlainText().strip() == "":
            QtWidgets.QMessageBox.warning(self, "Error", "Video cannot be empty!")
            return

        csv_writer = CSVWriter(f"{time.time_ns()}.csv")
        csv_writer.write_header()
        for metric in self.metrics:
            csv_writer.write_data([metric['timestamp'], metric['blink_duration'], metric['blink_frequency'], metric['microsleep'], metric['perclos'], metric['saccade_frequency'], metric['saccade_mean']])

    def add_data_input_field(self, layout, field_type, placeholder):
        """Add a data input field to the layout."""
        frame = QtWidgets.QFrame(self.frame_left)
        frame.setMaximumSize(QSize(16777215, 60))
        
        hlayout = QtWidgets.QHBoxLayout(frame)
        hlayout.setContentsMargins(4, 4, 4, 4)
        
        textbox = QtWidgets.QPlainTextEdit(frame)
        textbox.setReadOnly(True)
        textbox.setPlaceholderText(placeholder)
        textbox.setStyleSheet(f"""
            #textbox_{field_type} {{
                padding: 8px 10px;
                border-radius: 4px;
                background: transparent;
                border: 1px solid #BDBBBE;
            }}
        """)
        textbox.setObjectName(f"textbox_{field_type}")
        hlayout.addWidget(textbox)
        
        btn = QtWidgets.QPushButton(frame)
        btn.setMinimumSize(QSize(45, 45))
        btn.setStyleSheet(f"""
            #btn_{field_type} {{
                border-radius: 4px;
                border: 0.5px solid #BDBBBE;
            }}
            #btn_{field_type}:hover {{ background-color: #D7D5D8; }}
        """)
        btn.setObjectName(f"btn_{field_type}")
        btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DirOpenIcon))
        btn.setIconSize(QSize(24, 24))
        btn.clicked.connect(getattr(self, f"open_{field_type}"))
        hlayout.addWidget(btn)
        
        layout.addWidget(frame)
        return textbox

    def setup_scroll_area(self, layout):
        """Set up the scrollable area for data display."""
        self.scroll_area = QtWidgets.QScrollArea(self.frame_left)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("#scrollArea { border: 0px; }")
        self.scroll_area.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet("#scrollAreaWidgetContents { background-color: #f9f9f9; border: 0px; }")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.verticalLayout_data = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)
        
        layout.addWidget(self.scroll_area)

    def setup_middle_frame(self):
        """Set up the middle frame of the UI."""
        self.frame_mid = QtWidgets.QFrame(self.central_widget)
        self.frame_mid.setObjectName("frame_mid")
        
        self.mid_layout = QtWidgets.QVBoxLayout(self.frame_mid)
        self.mid_layout.setContentsMargins(0, 0, 0, 0)
        
        # Video player frame
        self.frame_vid = QtWidgets.QFrame(self.frame_mid)
        self.frame_vid.setMinimumSize(QSize(0, 750))
        self.frame_vid.setStyleSheet("#frame_vid { background-color: #f9f9f9; border-radius: 4px; }")
        self.frame_vid.setObjectName("frame_vid")
        self.mid_layout.addWidget(self.frame_vid)
        
        # Video widget (initially hidden)
        self.videoWidget = QVideoWidget(self.frame_vid)
        self.videoWidget.hide()
        
        # Video controls
        self.setup_video_controls(self.mid_layout)
        
        self.main_layout.addWidget(self.frame_mid)

    def setup_video_controls(self, layout):
        """Set up video playback controls."""
        self.frame_player = QtWidgets.QFrame(self.frame_mid)
        self.frame_player.setMaximumSize(QSize(16777215, 60))
        self.frame_player.setObjectName("frame_player")
        
        player_layout = QtWidgets.QHBoxLayout(self.frame_player)
        player_layout.setContentsMargins(12, 0, 30, 0)
        player_layout.setSpacing(18)
        
        self.btn_play = QtWidgets.QPushButton(self.frame_player)
        self.btn_play.setEnabled(False)
        self.btn_play.setMaximumSize(QSize(45, 45))
        self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.btn_play.setIconSize(QSize(40, 40))
        self.btn_play.clicked.connect(self.play)
        player_layout.addWidget(self.btn_play)
        
        self.horizontalSlider = QtWidgets.QSlider(Qt.Horizontal, self.frame_player)
        self.horizontalSlider.setMinimumSize(QSize(0, 36))
        self.horizontalSlider.sliderMoved.connect(self.slider_moved)
        self.horizontalSlider.sliderPressed.connect(self.slider_pressed)
        self.horizontalSlider.sliderReleased.connect(self.slider_released)
        self.horizontalSlider.setEnabled(False)
        player_layout.addWidget(self.horizontalSlider)
        
        self.time_label = QtWidgets.QLabel("00:00:00/00:00:00", self.frame_player)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.time_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        player_layout.addWidget(self.time_label)
        
        layout.addWidget(self.frame_player)

    def setup_right_frame(self):
        """Set up the right frame of the UI."""
        self.frame_right = QtWidgets.QFrame(self.central_widget)
        self.frame_right.setMinimumSize(QSize(480, 0))
        self.frame_right.setMaximumSize(QSize(480, 16777215))
        self.frame_right.setObjectName("frame_right")
        
        right_layout = QtWidgets.QVBoxLayout(self.frame_right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.setup_legends(right_layout)
        
        self.main_layout.addWidget(self.frame_right)

    def setup_legends(self, layout):
        """Set up the legends section in the right frame."""
        self.frame_legends = QtWidgets.QFrame(self.frame_right)
        self.frame_legends.setStyleSheet("#frame_legends { background-color: #f9f9f9; border-radius: 4px; }")
        self.frame_legends.setObjectName("frame_legends")
        
        legends_layout = QtWidgets.QVBoxLayout(self.frame_legends)
        legends_layout.setSpacing(10)
        
        self.add_legend_section(legends_layout, "collection", "Collection")
        
        layout.addWidget(self.frame_legends)

    def add_legend_section(self, layout, section_name, title):
        """Add a section to the legends frame."""
        frame = QtWidgets.QFrame(self.frame_legends)
        frame.setObjectName(f"frame_{section_name}")
        frame.setStyleSheet(f"#frame_{section_name} {{ border-top: 2px solid #BDBBBE; padding: 10px; }}")
        
        section_layout = QtWidgets.QVBoxLayout(frame)
        
        label = QtWidgets.QLabel(title, frame)
        label.setObjectName(f"label_{section_name}")
        label.setStyleSheet("font-weight: bold; font-size: 20px;")
        section_layout.addWidget(label)
        
        self.add_collection_content(section_layout)
        
        layout.addWidget(frame)

    def add_collection_content(self, layout):
        """Add content to the collection section."""
        collection_layout = QtWidgets.QGridLayout()
        
        labels = [
            ("blink_duration", "blink duration (s)"),
            ("blink_freq", "blink frequency"),
            ("microsleep", "microsleep (s)"),
            ("perclos", "PERCLOS (%)"),
            ("saccade_freq", "saccade frequency"),
            ("saccade_mean", "saccade mean (pixels/frame)"),
            ("timestamp", "timestamp")
        ]
        
        for i, (name, text) in enumerate(labels):
            label_1 = QtWidgets.QLabel(text, self.frame_legends)
            label_2 = QtWidgets.QLabel("0.0", self.frame_legends)
            label_1.setStyleSheet("font-weight: 600; font-size: 18px;")
            label_2.setStyleSheet("font-weight: 600; font-size: 18px;")
            label_1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            label_2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            collection_layout.addWidget(label_1, i, 0)
            collection_layout.addWidget(label_2, i, 1)
            setattr(self, f"label_{name}_1", label_1)
            setattr(self, f"label_{name}_2", label_2)
        
        layout.addLayout(collection_layout)

    def initialize_media_player(self):
        """Initialize the media player."""
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def initialize_variables(self):
        """Initialize variables used throughout the class."""
        self.fileName_1 = ""
        self.load_attempts = 0
        self.progress = None
        self.videoWidget = None
        self.mediaPlayer = None
        self.video_capture = None
        self.video_timer = None
        self.current_frame = 0
        self.total_frames = 0
        self.is_slider_updating = False
        self.eye_metrics = None
        self.last_processed_frame = -1

    def initialize_mediapipe(self):
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.01,
            min_tracking_confidence=0.01
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Define eye landmarks
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)

        current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
        
        # Only process if this frame hasn't been processed before
        if current_frame > self.last_processed_frame:
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    self.draw_eye_and_iris(frame, face_landmarks)

            self.last_processed_frame = current_frame

        return frame

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

        # def draw_landmark_numbers(landmarks, points):
        #     for idx, point in enumerate(points):
        #         x, y = mesh_points[point]
        #         cv2.putText(image, str(point), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)

        # draw_landmark_numbers(self.LEFT_EYE, self.LEFT_EYE)
        # draw_landmark_numbers(self.RIGHT_EYE, self.RIGHT_EYE)

    def open_vid(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if fileName:
            self.preprocess_video(fileName)

    def preprocess_video(self, fileName):
        self.progress_dialog = QtWidgets.QProgressDialog("Processing video...", "Cancel", 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setWindowTitle("Processing")
        self.progress_dialog.setLabelText("Initializing...")
        self.progress_dialog.show()

        self.preprocessor = EyeTrackingMetrics(30)  # Assume 30 fps, adjust as needed
        
        self.preprocessing_thread = QThread()
        self.preprocessing_worker = PreprocessingWorker(self.preprocessor, fileName)
        self.preprocessing_worker.moveToThread(self.preprocessing_thread)
        
        self.preprocessing_thread.started.connect(self.preprocessing_worker.run)
        self.preprocessing_worker.progress.connect(self.update_progress)
        self.preprocessing_worker.status_update.connect(self.update_status)
        self.preprocessing_worker.finished.connect(self.preprocessing_finished)

        self.preprocessing_thread.start()

    def update_status(self, status):
        self.progress_dialog.setLabelText(status)

    def preprocessing_finished(self, metrics):
        self.preprocessing_thread.quit()
        self.preprocessing_thread.wait()
        self.progress_dialog.close()
        
        self.metrics = metrics
        self.load_video(self.preprocessing_worker.fileName)
        self.last_processed_frame = -1

    def update_metrics_display(self):
        minute = int((self.current_frame / self.fps) // 60) + 1
        
        matching_data = None
        for data in self.metrics:
            if data['timestamp'] == (minute * 60):
                matching_data = data
                break
        self.label_blink_duration_2.setText(f"{data['blink_duration']:.2f}")
        self.label_blink_freq_2.setText(f"{data['blink_frequency']}")
        self.label_microsleep_2.setText(f"{data['microsleep']}")
        self.label_perclos_2.setText(f"{data['perclos']:.2f}")
        self.label_saccade_freq_2.setText(f"{data['saccade_frequency']}")
        self.label_saccade_mean_2.setText(f"{data['saccade_mean']:.2f}")
        self.label_timestamp_2.setText(f"{(data['timestamp']-60):.2f}-{data['timestamp']:.2f}")

    def load_video(self, fileName):
        """Load the video file using OpenCV."""
        # Close any existing video
        if self.video_capture is not None:
            self.video_capture.release()
        
        # Open the new video file
        self.video_capture = cv2.VideoCapture(fileName)
        if not self.video_capture.isOpened():
            QMessageBox.critical(self, "Error", "Could not open video file.")
            return

        # Get video properties
        self.total_frames = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        self.total_duration = self.total_frames / self.fps

        # Init eye tracking metrics
        self.eye_metrics = EyeTrackingMetrics(ceil(self.fps))
        
        # Update time label with total duration
        total_time = self.format_time(self.total_duration)
        self.time_label.setText(f"00:00:00/{total_time}")

        # Set up the video display
        self.setup_video_display()
        
        # Set up the slider
        self.horizontalSlider.setRange(0, self.total_frames - 1)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setEnabled(True)
        
        # Set up the play button
        self.btn_play.setEnabled(True)
        self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        
        # Start the video timer
        self.video_timer = QTimer(self)
        self.video_timer.timeout.connect(self.update_frame)
        self.video_timer.start(int(1000 / self.fps))  # Update interval based on video FPS
        
        # Update the UI
        self.textbox_vid.setPlainText(fileName)
        self.fileName_1 = fileName

    def setup_video_display(self):
        """Set up the video display area."""
        # Remove any existing layout from frame_vid
        if self.frame_vid.layout():
            QtWidgets.QWidget().setLayout(self.frame_vid.layout())
        
        # Create a new layout for frame_vid
        video_layout = QtWidgets.QVBoxLayout(self.frame_vid)
        
        # Create a QLabel to display the video frames
        self.video_label = QtWidgets.QLabel(self.frame_vid)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        video_layout.addWidget(self.video_label)
    
    def update_progress(self, progress):
        if self.progress and self.progress.isVisible():
            self.progress.setValue(progress)

    def handle_media_status(self, status):
        if status == QMediaPlayer.LoadedMedia:
            if self.progress and self.progress.isVisible():
                self.progress.close()
            self.videoWidget.show()
            self.btn_play.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.mediaPlayer.play()

    def handle_video_error(self, error):
        if self.progress and self.progress.isVisible():
            self.progress.close()
        if self.load_attempts == 1:
            print(f"First attempt failed, retrying...")
            QTimer.singleShot(100, lambda: self.load_video(self.fileName_1))
        else:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load video: {error}")
    
    def check_progress(self):
        if self.progress and self.progress.isVisible() and self.progress.value() == 0:
            self.progress.close()
            if self.load_attempts == 1:
                print(f"Progress stalled on first attempt, retrying...")
                QTimer.singleShot(100, lambda: self.load_video(self.fileName_1))
            else:
                QtWidgets.QMessageBox.warning(self, "Warning", "Video loading progress seems to be stuck. The video might still be loading in the background.")

    def use_opencv_fallback(self, fileName):
        self.cap = cv2.VideoCapture(fileName)
        if not self.cap.isOpened():
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to open video file.")
            return

        # Create a QLabel to display the video frames
        self.video_label = QtWidgets.QLabel(self.frame_vid)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.frame_vid.layout().addWidget(self.video_label)

        # Set up a timer to update video frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    @pyqtSlot()
    def update_frame(self):
        if self.video_capture is None or self.is_slider_updating:
            return

        ret, frame = self.video_capture.read()
        if ret:
            frame_with_landmarks = self.process_frame(frame)
            self.display_frame(frame_with_landmarks)
            
            # Update the slider position and time label
            self.current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            self.horizontalSlider.setValue(self.current_frame)
            self.update_time_label()
            self.update_metrics_display()
        else:
            # Video ended, stop the timer
            self.video_timer.stop()
            self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
    
    def update_time_label(self):
        current_time = self.current_frame / self.fps
        total_time = self.total_duration
        current_time_str = self.format_time(current_time)
        total_time_str = self.format_time(total_time)
        self.time_label.setText(f"{current_time_str}/{total_time_str}")
    
    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def display_frame(self, frame):
        """Display a single frame on the video label."""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(self.video_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)
    
    def set_position(self, position):
        """Set the position of the video."""
        if self.video_capture is None:
            return

        # Reset eye tracking metrics if the position change is significant
        current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
        if abs(position - current_frame) > self.fps:
            self.last_processed_frame = -1

        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = self.video_capture.read()
        if ret:
            frame_with_landmarks = self.process_frame(frame)
            self.display_frame(frame_with_landmarks)
            self.update_time_label()
            self.update_metrics_display()

    def play(self):
        """Toggle play/pause of the video."""
        if self.video_capture is None:
            return

        if self.video_timer.isActive():
            self.video_timer.stop()
            self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        else:
            self.video_timer.start()
            self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))

    def slider_pressed(self):
        """Handle slider press event."""
        self.is_slider_updating = True
        self.video_timer.stop()
        self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    def slider_released(self):
        """Handle slider release event."""
        self.is_slider_updating = False
        new_position = self.horizontalSlider.value()
        self.set_position(new_position)
        if self.btn_play.icon().cacheKey() == self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause).cacheKey():
            self.video_timer.start()
        self.current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
        self.update_time_label()
        self.update_metrics_display()

    def slider_moved(self, value):
        """Handle slider moved event."""
        if self.is_slider_updating:
            self.set_position(value)
            self.current_frame = int(self.video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            self.update_time_label()
            self.update_metrics_display()

    def position_changed(self, position):
        """Handle change in media player position."""
        self.horizontalSlider.setValue(position)

    def duration_changed(self, duration):
        """Handle change in media duration."""
        self.horizontalSlider.setRange(0, duration)
            
    def media_state_changed(self, state):
        """Handle change in media player state."""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.btn_play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
    
        # Show video widget when media is loaded and ready to play
        if state == QMediaPlayer.LoadedMedia:
            self.videoWidget.show()