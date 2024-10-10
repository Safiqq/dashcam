import PyInstaller.__main__
import os
import mediapipe

mediapipe_path = os.path.dirname(mediapipe.__file__)

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    f'--add-data={mediapipe_path}:mediapipe',
    '--hidden-import=PyQt5.QtCore',
    '--hidden-import=PyQt5.QtGui',
    '--hidden-import=PyQt5.QtWidgets',
    '--hidden-import=PyQt5.QtMultimedia',
    '--hidden-import=PyQt5.QtMultimediaWidgets',
    '--hidden-import=sys',
    '--hidden-import=signal',
    '--hidden-import=json',
    '--hidden-import=hashlib',
    '--hidden-import=os',
    '--hidden-import=csv',
    '--hidden-import=cv2',
    '--hidden-import=locale',
    '--hidden-import=io',
    '--hidden-import=time',
    '--hidden-import=numpy',
    '--hidden-import=mediapipe',
    '--hidden-import=math',
    '--hidden-import=datetime',
    '--hidden-import=LoginWindow',
    '--hidden-import=MainWindow',
    '--hidden-import=EyeTrackingMetrics',
    '--hidden-import=CSVWriter',
    '--hidden-import=PreprocessingWorker',
    '--collect-submodules=PyQt5',
    '--collect-submodules=cv2',
    '--collect-submodules=mediapipe',
    '--collect-submodules=numpy',
    '--name=EyeTrackingApp',
    '--icon=NONE',  # Replace NONE with path to your icon file if you have one
])

print("Build complete. Please check the 'dist' folder for your executable.")