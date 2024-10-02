import json
import hashlib
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from MainWindow import MainWindow

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.salt = 'dashcam'
        
    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 200)
        
        layout = QtWidgets.QVBoxLayout()
        
        # Username input
        self.username_input = self.create_input_field('Username:')
        
        # Password input
        self.password_input = self.create_input_field('Password:', is_password=True)
        
        # Login button
        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        
        # Add all widgets to main layout
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        
        self.setLayout(layout)

        # Set up enter key event
        self.username_input.findChild(QtWidgets.QLineEdit).returnPressed.connect(self.focus_password)
        self.password_input.findChild(QtWidgets.QLineEdit).returnPressed.connect(self.login)
    
    def create_input_field(self, label_text, is_password=False):
        """Create a labeled input field."""
        layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(label_text)
        input_field = QtWidgets.QLineEdit()
        if is_password:
            input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(label)
        layout.addWidget(input_field)
        
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        return container

    def focus_password(self):
        """Move focus to password field when enter is pressed in username field."""
        self.password_input.findChild(QtWidgets.QLineEdit).setFocus()
        
    @pyqtSlot()
    def login(self):
        """Handle login button click or enter key press."""
        username = self.username_input.findChild(QtWidgets.QLineEdit).text()
        password = self.password_input.findChild(QtWidgets.QLineEdit).text()
        
        if not username or not password:
            self.show_error("Username and password are required.")
            return
        
        if self.check_credentials(username, password):
            QtWidgets.QMessageBox.information(self, 'Success', 'Login successful!')
            self.open_main_window(username)
        else:
            self.show_error('Invalid username or password')
    
    def check_credentials(self, username, password):
        """Verify user credentials against stored data."""
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
            
            for user in users:
                if user['username'] == username:
                    stored_password = user['password']
                    return self.verify_password(stored_password, password)
            
            return False
        except FileNotFoundError:
            self.show_error('users.json file not found')
            return False
        except json.JSONDecodeError:
            self.show_error('Invalid JSON format in users.json')
            return False
    
    def verify_password(self, stored_password, provided_password):
        """Verify the provided password against the stored hash."""
        return stored_password == self.hash_password(provided_password)
    
    def hash_password(self, password):
        """Hash the password with the salt using SHA-256."""
        return hashlib.sha256((password + self.salt).encode()).hexdigest()
    
    def show_error(self, message):
        """Display an error message."""
        QtWidgets.QMessageBox.critical(self, 'Error', message)
    
    def open_main_window(self, username):
        """Open the main application window and close the login window."""
        try:
            self.main_window = MainWindow(username)
            self.main_window.showMaximized()
            self.close()
        except Exception as e:
            self.show_error(f"Failed to open main window: {str(e)}")