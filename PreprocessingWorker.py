from PyQt5.QtCore import QObject, pyqtSignal
import cv2
from EyeTrackingMetrics import EyeTrackingMetrics

class PreprocessingWorker(QObject):
    finished = pyqtSignal(list)
    progress = pyqtSignal(int)
    status_update = pyqtSignal(str)

    def __init__(self, preprocessor, fileName):
        super().__init__()
        self.preprocessor = preprocessor
        self.fileName = fileName

    def run(self):
        self.status_update.emit("Initializing eye tracking metrics...")
        cap = cv2.VideoCapture(self.fileName)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        self.status_update.emit("Processing video frames...")
        metrics = self.preprocessor.preprocess_video(self.fileName, self.progress.emit)
        
        self.progress.emit(100)
        self.status_update.emit("Processing complete!")
        self.finished.emit(metrics)