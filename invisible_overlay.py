import sys
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap, QKeyEvent
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QMainWindow, QDesktopWidget
from PyQt5.QtCore import Qt
from pynput import keyboard
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QEvent, QCoreApplication

class InvisibleOverlay(QMainWindow):
    def __init__(self, rotation_names):
        super().__init__()
        fontPath = './res/Google_Sans-500-100_0-0_0.ttf'
        QFontDatabase.addApplicationFont(fontPath)

        self.setWindowTitle("Overlay Window")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.current_rotation_index = 0
        self.rotation_names = rotation_names
        
        layout = QVBoxLayout()
        
        self.label = QLabel('This is a centered label')
        self.label.setAlignment(Qt.AlignCenter)  # Align the label text to center
        
        layout.addWidget(self.label)
        self.setWindowOpacity(0)


        with open('./res/invis_style.qss', 'r') as f:
            style = f.read()
            self.label.setStyleSheet(style)

        central_widget.setLayout(layout)
        
        self.setGeometry(100, 100, 600, 400)  # x, y, width, height
        self.centerWindow()

    def onKeyPressEvent(self):
        self.current_rotation_index += 1
        self.setWindowOpacity(1)
        self.label.setText(self.rotation_names[self.current_rotation_index % len(self.rotation_names)])

        if self.windowOpacity() == 1:
            threading.Thread(target=self.decrease_opacity).start()
                    
    def decrease_opacity(self):
        while self.windowOpacity() > 0:
            self.setWindowOpacity(self.windowOpacity() - 0.05)
            time.sleep(0.05)

    def centerWindow(self):
        # Get the rectangle specifying the geometry of the main window.
        qr = self.frameGeometry()
        # Get the screen resolution of your monitor (screen) and find the center point.
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_center = screen_geometry.center()

        # Adjust window position: keep the x coordinate centered, adjust the y coordinate to be near the top of the screen
        qr.moveTop(screen_geometry.top())
        qr.setX(int(1080 / 2) - 250)
        # qr.moveLeft(int(screen_geometry.width()))

        # Move the top-left point of the window to the calculated position, thus centering the window at the top of the screen.
        self.move(qr.topLeft())