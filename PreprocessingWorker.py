from PyQt5.QtCore import QObject, pyqtSignal

class PreprocessingWorker(QObject):
    finished = pyqtSignal(list)
    progress = pyqtSignal(int)

    def __init__(self, preprocessor, fileName):
        super().__init__()
        self.preprocessor = preprocessor
        self.fileName = fileName

    def run(self):
        metrics = self.preprocessor.preprocess_video(self.fileName, self.progress.emit)
        self.finished.emit(metrics)