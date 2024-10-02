import sys
import signal
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from LoginWindow import LoginWindow

def sigint_handler(signum, frame):
    """Handler for SIGINT signal (Ctrl+C)."""
    print("\nCtrl+C detected. Closing the application...")
    QtWidgets.QApplication.quit()


def main():
    """Main function to run the application with SIGINT handling."""
    # Set up SIGINT handler
    signal.signal(signal.SIGINT, sigint_handler)

    app = QtWidgets.QApplication(sys.argv)

    # Create a timer to handle SIGINT in the Qt event loop
    timer = QTimer()
    timer.start(500)  # Fire every 500ms
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms

    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

